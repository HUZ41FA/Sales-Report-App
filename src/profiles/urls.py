from django.urls import path
from .views import profile_view

app_name = 'profiles'


urlpatterns =[
    path('my_profile/', profile_view, name='my_profile'),
    
]
