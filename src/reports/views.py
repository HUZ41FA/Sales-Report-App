from re import T
from django.shortcuts import get_object_or_404, render
from profiles.models import Profile
from django.http import JsonResponse
from .utils import get_report_image, link_callback
from .models import Report
from .forms import ReportForm
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from sales.models import Sale, Position, CSV
import csv
from django.utils.dateparse import parse_date
from products.models import Product
from customers.models import Customer
from profiles.models import Profile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def create_report_view(request):
    form  = ReportForm(request.POST or None)
    if request.method == 'POST': #This should be a request.is_ajax() but its depreciated will improve this feature in future
        image = request.POST.get('image')
        img = get_report_image(image)
        author = Profile.objects.get(id=request.user.id)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.image = img
            instance.author = author
            instance.save()
            print(instance.image.url)
            return JsonResponse({ 'msg': 'send'})
    return JsonResponse({})

class UploadTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'reports/from_file.html'

@login_required
def csv_upload_view(request):
    if request.method == 'POST':
        csv_file_name = request.FILES.get('file').name
        csv_file = request.FILES.get('file')
        obj, created = CSV.objects.get_or_create(file_name = csv_file_name)
        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, "r") as f:
                reader = csv.reader(f)
                reader.__next__()  #Skips the first row (which is just the name of the coulumns)
                for row in reader:
                    transaction_id = row[1]
                    product = row[2]
                    quantity = int(row[3])
                    customer = row[4]
                    date = parse_date(row[5])

                    try:
                        product_obj = Product.objects.get(name__iexact = product)
                    except Product.DoesNotExist:
                        product_obj = None
                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name = customer)
                        salesman_obj = Profile.objects.get(user = request.user)
                        position_obj = Position.objects.create(product = product_obj, quantity
                        =quantity, created = date)
                        print(position_obj)
                        sale_obj, _ = Sale.objects.get_or_create(transaction_id = transaction_id, customer = customer_obj, salesman = salesman_obj, created = date)
                        sale_obj.positions.add(position_obj) #just another method to add a manyToMany Field
                        sale_obj.save()
                return JsonResponse({"ex": False})
        else:
            return JsonResponse({"ex": True})
    return HttpResponse()

class ReportList(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'reports/reportList.html'

class ReportDetail(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'reports/details.html'

@login_required
def render_pdf_view(request, pk):
    object = get_object_or_404(Report, pk=pk)
    template_path = 'reports/pdf.html'
    context = {'object': object}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #if download
    #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    #if display 
    response['Content-Disposition'] = 'filename="report.pdf"' #JUST remove the atachment part
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback )
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response