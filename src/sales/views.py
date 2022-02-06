from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from pandas import DataFrame
from .utils import get_customer_from_id, get_salesman_from_id, get_chart
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def home_view(request):                                 #Home page view
    search_form = SalesSearchForm(request.POST or None) #without "or none" the fields will execute automatically
    report_form = ReportForm()
    sales_df = None
    positions_df = None
    merged_df = None
    grouped_by_price_df = None
    chart = None
    no_data = None

    if request.method == 'POST': #This line shows how to extract data from post req
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        result_by = request.POST.get('result_by')
        qs = Sale.objects.filter(created__date__lte=date_to, created__date__gte=date_from)
        if search_form.is_valid(): #This line show how to extract data from a form
            print(search_form.cleaned_data)
            print(search_form.cleaned_data['date_from'])
            print(search_form.cleaned_data['date_to'])
            print(search_form.cleaned_data['chart_type'])
            print(search_form.cleaned_data['result_by'])
        if len(qs) > 0:
            df = DataFrame(qs.values())
            df["customer_id"] = df["customer_id"].apply(get_customer_from_id)
            df["salesman_id"] = df["salesman_id"].apply(get_salesman_from_id)
            df["created"] = df["created"].apply(lambda x: x.strftime('%d-%m-%Y'))
            df["updated"] = df["updated"].apply(lambda x: x.strftime('%d-%m-%Y'))
            df.rename({'salesman_id': "salesman", "customer_id": "customer", "id": "sales_id"}, axis=1, inplace=True)
            sales_df = df.to_html(index=False)
            position_data = []
            for sale in qs:
                sale_id  = sale.id
                for pos in sale.get_positions():
                    obj = {
                        "sales_id": sale_id,
                        "position_id" : pos.id,
                        "position_quantity" : pos.quantity,
                        "product": pos.product,
                        "price": pos.price
                    }
                    position_data.append(obj)
            df2 = DataFrame(position_data)
            positions_df = df2.to_html(index=False)
            df3 = pd.merge(df, df2, on="sales_id")
            merged_df = df3.to_html(index=False)
            df4 = df3.groupby('transaction_id', as_index=False)["price"].agg('sum')
            grouped_by_price_df = df4.to_html(index = False)
            chart = get_chart(chart_type, df, result_by)
        
        else:
            no_data = 'No data availble in this data range'
    context = {
        'search_form':search_form,
        'report_form':report_form,
        'sales_df':sales_df, 
        'positions_df':positions_df,
        'merged_df':merged_df, 
        'grouped_by_price_df':grouped_by_price_df,
        'chart':chart,
        'no_data': no_data,
        }
    return render(request, 'sales/home.html', context)

class SaleListView(LoginRequiredMixin, ListView):           #Class based view for List of sales
    model = Sale
    template_name = 'sales/main.html'

class SaleDetailView(LoginRequiredMixin, DetailView):       #Class based view for individual sale
    model = Sale
    template_name = 'sales/detail.html'

