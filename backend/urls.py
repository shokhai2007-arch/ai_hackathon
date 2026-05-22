from django.urls import path
from . import views

urlpatterns = [
    path('market/', views.market_data, name='market-data'),
    path('stocks/', views.stocks_list, name='stocks-list'),
    path('companies/', views.companies_list, name='companies-list'),
    path('plans/', views.plans_list, name='plans-list'),
    path('faq/', views.faq_list, name='faq-list'),
    path('chat/', views.chat, name='chat'),
    path('auth/login/', views.login_view, name='auth-login'),
    path('auth/logout/', views.logout_view, name='auth-logout'),
    path('auth/me/', views.me_view, name='auth-me'),
]
