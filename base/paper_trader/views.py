from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
import yfinance as yf
import json
from .models import PortfolioStock, Transaction
from .forms import TradeForm
from decimal import Decimal


def home(request):
    mycasha = Transaction.objects.last().cash
        
    mystocks = PortfolioStock.objects.all()  
   
    form = TradeForm()
    context = {
        'mystocks': mystocks, 
        'mycasha': mycasha,
        'form': form
    }
    return render(request, 'paper_trader/home.html', context)

def update(request, pk):
    if request.method == 'POST':
        form = TradeForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            action = form.cleaned_data['action']
            pstock = PortfolioStock.objects.get(id=pk)
            mycasha = pstock.cash 
            stock = yf.Ticker(pstock.symbol)
            price = stock.info['previousClose']
            total = price * quantity
            if action == 'buy':
                
                if total > pstock.cash:
                    alert = 'You do not have enough cash to buy this stock'
                    return redirect('update', pk=pk)
               
                pstock.quantity += quantity
                pstock.total = pstock.quantity * price
                pstock.cash -= Decimal(total)
                pstock.save()
                transaction = Transaction(
                    name=pstock.name, 
                    symbol=pstock.symbol, 
                    quantity=quantity, 
                    price=price, 
                    total=total, 
                    type='buy',)
                transaction.cash -= Decimal(total)
                transaction.save()
                
                
            elif action == 'sell':
                if quantity > pstock.quantity:
                    return redirect('update')
              
                pstock.quantity -= quantity
                pstock.total = pstock.quantity * price
                pstock.cash += Decimal(total)
                pstock.save()
                transaction = Transaction(
                    name=pstock.name, 
                    symbol=pstock.symbol, 
                    quantity=quantity, 
                    price=price, 
                    total=total, 
                    type='sell')
                transaction.cash += Decimal(total)
                transaction.save()
                
            mycasha = transaction.cash       
            return redirect('update', pk=pk)
       
    form = TradeForm()
    mystocks = PortfolioStock.objects.all()
    pstock = PortfolioStock.objects.get(id=pk)
    mycasha = Transaction.objects.last().cash
    
    
    stock = yf.Ticker(pstock.symbol)
    hist = stock.history(period="5d")  # Fetching last 5 days of stock data
    

    context = {
    'mystocks': mystocks, 'pstock': pstock, 
    'price': stock.info['previousClose'],
    'name': stock.info['shortName'], 
    'data': hist['Close'].tolist(),
    'dates': hist.index.strftime('%Y-%m-%d').tolist(),
    'mycasha': mycasha, 'form': form, 
    
    }

    return render(request, 'paper_trader/home.html', context)

def buy(request):
     if request.method == 'GET':
        symbol = request.GET.get('symbol', '').upper()  # Fetch the symbol from query parameters
        if symbol:
            stock = yf.Ticker(symbol)
            stock_info = stock.info
            
            # You can add logic to check if the stock already exists in the portfolio
            if not PortfolioStock.objects.filter(symbol=symbol).exists():
                pstock = PortfolioStock(
                    name=stock_info.get('shortName', 'Unknown Stock'),
                    symbol=symbol,
                    quantity=0,  # Initially set to 0, to be updated with a buy transaction
                    value=Decimal(stock_info['previousClose']),
                    total=0  # Initially 0
                )
                pstock.save()
                return redirect(reverse('update', kwargs={'pk': pstock.pk}))
            else:
                return JsonResponse({'error': 'Stock already exists in your portfolio.'})

     return JsonResponse({'error': 'Invalid request'})
  








def fetch_stock_data(request):
    # this is called in the home.html file to fetch the stock
    # a function at the bottom of the main.html file is called to display the stock data in the graph
    if request.method == 'GET':
        symbol = request.GET.get('symbol', '').upper()
        if symbol:
            stock = yf.Ticker(symbol)
            hist = stock.history(period="5d")  # Fetching last 5 days of stock data
            
            data = {
                'price': stock.info['previousClose'],
                'symbol': symbol,
                'name': stock.info['shortName'],
                'data': hist['Close'].tolist(),
                'dates': hist.index.strftime('%Y-%m-%d').tolist(),
            }
            
            return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'})
