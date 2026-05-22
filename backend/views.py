import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Stock, Company, Plan, FAQ, ChatHistory
from .services.gemini import ask_gemini


def market_data(request):
    stocks = Stock.objects.select_related('company').all()
    companies = Company.objects.all()
    plans = Plan.objects.all()
    faqs = FAQ.objects.all()

    stocks_data = []
    for s in stocks:
        history_qs = s.history.order_by('date').values('date', 'open', 'high', 'low', 'close', 'volume')
        stocks_data.append({
            'key': s.company.key,
            'name': s.company.name,
            'ticker': s.ticker,
            'sector': s.sector,
            'price': float(s.price),
            'change': float(s.change),
            'changePercent': float(s.change_percent),
            'changeYear': float(s.change_year) if s.change_year else 0,
            'changeYearPercent': float(s.change_year_percent) if s.change_year_percent else 0,
            'high': float(s.high),
            'low': float(s.low),
            'volume': s.volume,
            'avgVolume': s.avg_volume or 0,
            'open': float(s.open_price),
            'prevClose': float(s.prev_close),
            'history': [
                {
                    'time': h['date'].strftime('%Y-%m-%d'),
                    'open': float(h['open']),
                    'high': float(h['high']),
                    'low': float(h['low']),
                    'close': float(h['close']),
                    'volume': h['volume'],
                }
                for h in history_qs
            ],
        })

    companies_data = [{'key': c.key, 'name': c.name, 'sector': c.sector} for c in companies]

    plans_data = [{'name': p.name, 'commissions': p.commissions} for p in plans]

    faq_data = []
    cats = {}
    for f in faqs:
        if f.category not in cats:
            cats[f.category] = []
        cats[f.category].append({'q': f.question, 'a': f.answer})
    for cat_name, questions in cats.items():
        faq_data.append({'category': cat_name, 'questions': questions})

    data = {
        'lastUpdated': '2026-05-22',
        'site': {
            'name': 'Bozor',
            'description': "O'zbekiston fond bozori ma'lumotlari",
            'company': 'MULTIBROKER MChJ',
        },
        'companies': companies_data,
        'stocks': stocks_data,
        'plans': plans_data,
        'faq': faq_data,
    }
    return JsonResponse(data)


def stocks_list(request):
    stocks = Stock.objects.select_related('company').all()
    data = []
    for s in stocks:
        data.append({
            'key': s.company.key,
            'name': s.company.name,
            'ticker': s.ticker,
            'sector': s.sector,
            'price': float(s.price),
            'change': float(s.change),
            'changePercent': float(s.change_percent),
            'high': float(s.high),
            'low': float(s.low),
            'volume': s.volume,
            'open': float(s.open_price),
            'prevClose': float(s.prev_close),
        })
    return JsonResponse(data, safe=False)


def companies_list(request):
    companies = Company.objects.all()
    data = [{'key': c.key, 'name': c.name, 'sector': c.sector} for c in companies]
    return JsonResponse(data, safe=False)


def plans_list(request):
    plans = Plan.objects.all()
    data = [{'name': p.name, 'commissions': p.commissions} for p in plans]
    return JsonResponse(data, safe=False)


def faq_list(request):
    faqs = FAQ.objects.all()
    cats = {}
    for f in faqs:
        if f.category not in cats:
            cats[f.category] = []
        cats[f.category].append({'q': f.question, 'a': f.answer})
    data = [{'category': cat, 'questions': qs} for cat, qs in cats.items()]
    return JsonResponse(data, safe=False)


@csrf_exempt
def chat(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    message = body.get('message')
    context = body.get('context')
    if not message or not context:
        return JsonResponse({'error': 'message and context required'}, status=400)

    try:
        reply = ask_gemini(context, message)
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    if request.user.is_authenticated:
        ChatHistory.objects.create(
            user=request.user,
            message=message,
            reply=reply,
            context=context,
        )

    return JsonResponse({'reply': reply})


@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    username = body.get('username')
    password = body.get('password')
    if not username or not password:
        return JsonResponse({'error': 'username and password required'}, status=400)

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'ok': True, 'username': user.username})
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@login_required
def logout_view(request):
    logout(request)
    return JsonResponse({'ok': True})


def me_view(request):
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'username': request.user.username,
        })
    return JsonResponse({'authenticated': False})
