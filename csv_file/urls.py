from django.urls import path

from . import views

app_name = 'csv_file'

urlpatterns = [
    path('user/csv', views.CSVHandleView.as_view(), name='csv_handle'),
]