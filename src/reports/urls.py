from django.urls import path
from .views import (UploadTemplateView, 
                    create_report_view, 
                    ReportList, ReportDetail, 
                    csv_upload_view, 
                    render_pdf_view,
                    )

app_name = 'reports'

urlpatterns = [
    path('upload/', csv_upload_view, name='upload'),
    path('save/', create_report_view, name = 'create-report'),
    path('from_file/', UploadTemplateView.as_view(), name = 'from_file'),
    path('list/', ReportList.as_view(), name='list'),
    path('<pk>/', ReportDetail.as_view(), name='detail' ),
    path('pdf/<pk>', render_pdf_view, name='pdf'),
    

    ]