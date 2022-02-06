from django.urls import path
from .views import (
    home_view,
    SaleDetailView,
    SaleListView
)


app_name = 'sales'

urlpatterns = [
    path('', home_view, name='home view'),
    path('sales/', SaleListView.as_view(), name= 'list' ), #this name help in url maping 
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail')
]
