from django.db import models

# Create your models here.
class Transaction(models.Model):
    name = models.CharField(max_length=20, default="Apple Inc")
    symbol = models.CharField(max_length=5, default="AAPL")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type = models.CharField(max_length=4, default='buy')
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    
    def __str__(self):
        return self.name

class PortfolioStock(models.Model):
    name = models.CharField(max_length=20, default="Apple Inc")
    symbol = models.CharField(max_length=5, default="AAPL")
    quantity = models.IntegerField(default=0)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    
    def __str__(self):
        return self.name