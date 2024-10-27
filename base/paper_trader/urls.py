from django.urls import path
from .views import home, fetch_stock_data, update, buy

urlpatterns = [
    path('', home, name='home'),
    path('fetch_stock_data/', fetch_stock_data, name='fetch_stock_data'),
    path('update/<str:pk>', update, name='update'),
    path('buy/', buy, name='buy')
   
]
