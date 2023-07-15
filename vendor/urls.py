from django.urls import path
from django.conf import settings
from vendor.views import VendorView, AddCategoryView, CategoryDetailView, OrdersView, AddOrderView

app_name = 'vendor'

urlpatterns = [
    path('', VendorView.as_view(template_name = 'pages/dashboards/vendor.html'), name='vendor'),
    path('main/', VendorView.as_view(template_name = 'pages/vendor/main.html'), name='vendor-main'),
    path('profile/', VendorView.as_view(template_name = 'pages/dashboards/profile.html'), name='vendor-profile'),
    path('settings/', VendorView.as_view(template_name = 'pages/dashboards/settings.html'), name='settings'),

    path('orders/', OrdersView.as_view(template_name = 'pages/catalog/orders.html'), name='vendor-orders'),
    path('add_order/', AddOrderView.as_view(template_name = 'pages/catalog/add-order.html'), name='vendor-add-orders'),

    path('categories/', VendorView.as_view(template_name = 'pages/catalog/categories.html'), name='vendor-categories'),
    path('categories/new', VendorView.as_view(template_name = 'pages/catalog/categories-new.html'), name='vendor-categories-new'),
    path('categories/<int:id>', CategoryDetailView.as_view(), name='category_detail'),

    path('categories/add_category', AddCategoryView.as_view(), name='add_category'),
]