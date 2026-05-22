import json
from datetime import datetime
from django.core.management.base import BaseCommand
from backend.models import Company, Stock, StockHistory, Plan, FAQ


class Command(BaseCommand):
    help = 'Import data from bozor_data.json into the database'

    def add_arguments(self, parser):
        parser.add_argument('json_path', nargs='?', default='backend/frontend/parser/data/bozor_data.json')

    def handle(self, *args, **options):
        path = options['json_path']
        self.stdout.write(f"Loading data from {path}...")

        with open(path, encoding='utf-8') as f:
            data = json.load(f)

        companies = {}
        for item in data.get('companies', []):
            company, _ = Company.objects.get_or_create(
                key=item['key'],
                defaults={'name': item['name'], 'sector': item['sector']},
            )
            companies[item['key']] = company
        self.stdout.write(f"  Companies: {len(companies)}")

        for item in data.get('stocks', []):
            company = companies.get(item['key'])
            if not company:
                continue

            stock, created = Stock.objects.update_or_create(
                company=company,
                ticker=item.get('ticker', item['key'].upper()),
                defaults={
                    'sector': item.get('sector', company.sector),
                    'price': item['price'],
                    'change': item.get('change', 0),
                    'change_percent': item.get('changePercent', 0),
                    'change_year': item.get('changeYear'),
                    'change_year_percent': item.get('changeYearPercent'),
                    'high': item.get('high', item['price']),
                    'low': item.get('low', item['price']),
                    'volume': item.get('volume', 0),
                    'avg_volume': item.get('avgVolume'),
                    'open_price': item.get('open', item['price']),
                    'prev_close': item.get('prevClose', item['price']),
                    'market_cap': item.get('marketCap'),
                    'shares_outstanding': item.get('sharesOutstanding'),
                    'pe_ratio': item.get('peRatio'),
                    'dividend_yield': item.get('dividendYield'),
                    'beta': item.get('beta'),
                    'eps': item.get('eps'),
                    'day_range': item.get('dayRange'),
                    'week52_range': item.get('week52Range'),
                    'volatility': item.get('volatility'),
                    'order_book': item.get('orderBook'),
                    'spread': item.get('spread'),
                    'recent_trades': item.get('recentTrades'),
                },
            )

            StockHistory.objects.filter(stock=stock).delete()
            hist_entries = []
            for h in item.get('history', []):
                hist_entries.append(StockHistory(
                    stock=stock,
                    date=datetime.strptime(h['time'], '%Y-%m-%d').date(),
                    open=h['open'],
                    high=h['high'],
                    low=h['low'],
                    close=h['close'],
                    volume=h.get('volume', 0),
                ))
            StockHistory.objects.bulk_create(hist_entries)

        self.stdout.write(f"  Stocks: {len(data.get('stocks', []))}")

        Plan.objects.all().delete()
        for item in data.get('plans', []):
            Plan.objects.create(
                name=item['name'],
                commissions=item.get('commissions', {}),
            )
        self.stdout.write(f"  Plans: {len(data.get('plans', []))}")

        FAQ.objects.all().delete()
        for cat in data.get('faq', []):
            for q in cat.get('questions', []):
                FAQ.objects.create(
                    category=cat['category'],
                    question=q['q'],
                    answer=q['a'],
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
