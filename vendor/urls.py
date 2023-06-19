from django.urls import path
from django.conf import settings
from vendor.views import  VendorView

app_name = 'vendor'

urlpatterns = [
    path('', VendorView.as_view(template_name = 'pages/dashboards/vendor.html'), name='1-vendor'),
    path('main/', VendorView.as_view(template_name = 'pages/vendor/main.html'), name='vendor-main'),
    path('profile/', VendorView.as_view(template_name = 'pages/dashboards/profile.html'), name='vendor-profile'),
    path('settings/', VendorView.as_view(template_name = 'pages/dashboards/settings.html'), name='settings'),
    path('orders/', VendorView.as_view(template_name = 'pages/catalog/orders.html'), name='vendor-orders'),
    path('add_order/', VendorView.as_view(template_name = 'pages/catalog/add-order.html'), name='vendor-add-orders'),
    path('products/', VendorView.as_view(template_name = 'pages/catalog/products.html'), name='vendor-products'),

]