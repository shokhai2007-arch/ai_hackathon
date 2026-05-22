from django.contrib import admin
from .models import Company, Stock, StockHistory, Plan, FAQ, ChatHistory


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['key', 'name', 'sector']
    search_fields = ['name', 'key']
    list_filter = ['sector']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['ticker', 'company', 'price', 'change_percent', 'volume']
    search_fields = ['ticker', 'company__name']
    list_filter = ['sector']


@admin.register(StockHistory)
class StockHistoryAdmin(admin.ModelAdmin):
    list_display = ['stock', 'date', 'close', 'volume']
    list_filter = ['date']
    date_hierarchy = 'date'


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['category', 'question', 'order']
    list_filter = ['category']


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'created_at']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
