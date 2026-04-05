from django.urls import path
from . import views

app_name = 'returns'

urlpatterns = [
    path('request/<uuid:order_id>/', views.request_return, name='request_return'),
    path('history/', views.return_list, name='return_list'),
]
