from django.urls import path
from django.conf import settings
from vendor.views import  VendorView

app_name = 'vendor'

urlpatterns = [
    path('', VendorView.as_view(template_name = 'pages/dashboards/vendor.html'), name='vendor'),
    path('active_orders/', VendorView.as_view(template_name = 'pages/dashboards/vendor.html'), name='vendor-main')
]