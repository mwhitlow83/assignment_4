from django.contrib import admin
from .models import PortfolioStock, Transaction

admin.site.register(PortfolioStock)
admin.site.register(Transaction)    