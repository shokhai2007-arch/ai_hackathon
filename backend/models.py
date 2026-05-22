from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    sector = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'companies'
        ordering = ['name']

    def __str__(self):
        return self.name


class Stock(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='stocks')
    ticker = models.CharField(max_length=20)
    sector = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    change = models.DecimalField(max_digits=15, decimal_places=2)
    change_percent = models.DecimalField(max_digits=8, decimal_places=2)
    change_year = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    change_year_percent = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.BigIntegerField()
    avg_volume = models.BigIntegerField(null=True, blank=True)
    open_price = models.DecimalField(max_digits=15, decimal_places=2)
    prev_close = models.DecimalField(max_digits=15, decimal_places=2)
    market_cap = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    shares_outstanding = models.BigIntegerField(null=True, blank=True)
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dividend_yield = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    beta = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    eps = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    day_range = models.CharField(max_length=50, null=True, blank=True)
    week52_range = models.CharField(max_length=50, null=True, blank=True)
    volatility = models.DecimalField(max_digits=8, decimal_places=4, null=True, blank=True)
    order_book = models.JSONField(null=True, blank=True)
    spread = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    recent_trades = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-volume']

    def __str__(self):
        return f"{self.ticker} - {self.price}"


class StockHistory(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='history')
    date = models.DateField()
    open = models.DecimalField(max_digits=15, decimal_places=2)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.BigIntegerField()

    class Meta:
        verbose_name_plural = 'stock histories'
        ordering = ['date']
        unique_together = ['stock', 'date']

    def __str__(self):
        return f"{self.stock.ticker} - {self.date}"


class Plan(models.Model):
    name = models.CharField(max_length=100)
    commissions = models.JSONField()

    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return self.question[:50]


class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    reply = models.TextField()
    context = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'chat histories'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.message[:30]}"
