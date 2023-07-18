from django.urls import path
from django.conf import settings
from vendor.views import (VendorView, AddCategoryView, CategoryDetailView,
                          OrdersView, AddOrderView, CategoryView, AddCategory,
                          SubCategoryDetailView, AddSubCategory, AddProductView, ProductView, StatsView)

app_name = 'vendor'

urlpatterns = [
    path('', VendorView.as_view(template_name = 'pages/dashboards/vendor.html'), name='vendor'),
    path('main/', VendorView.as_view(template_name = 'pages/vendor/main.html'), name='vendor-main'),
    path('profile/', VendorView.as_view(template_name = 'pages/dashboards/profile.html'), name='vendor-profile'),
    path('settings/', VendorView.as_view(template_name = 'pages/dashboards/settings.html'), name='settings'),

    path('orders/', OrdersView.as_view(template_name = 'pages/catalog/orders.html'), name='vendor-orders'),
    path('orders/<id>', OrdersView.as_view(template_name = 'pages/catalog/orders.html'), name='vendor-orders'),
    path('add_order/', AddOrderView.as_view(), name='vendor-add-orders'),

    path('categories/', CategoryView.as_view(template_name = 'pages/catalog/categories.html'), name='vendor-categories'),
    path('categories/new', AddCategory.as_view(template_name = 'pages/catalog/categories-new.html'), name='vendor-categories-new'),
    path('categories/<int:id>', CategoryDetailView.as_view(), name='category_detail'),

    path('categories/<int:id>/add_product', AddProductView.as_view(template_name = 'pages/catalog/add-product.html'), name='add-subcategory'),
    path('categories/<int:id>/<int:sub>/add_product', AddProductView.as_view(template_name = 'pages/catalog/add-product.html'), name='add-product'),

    path('categories/<int:id>/add_subcategory', AddSubCategory.as_view(template_name = 'pages/catalog/subcategory-new.html'), name='add-subcategory'),
    path('categories/<int:sub>/<int:id>', SubCategoryDetailView.as_view(), name='subcategory_detail'),
    path('categories/add_category', AddCategoryView.as_view(), name='add_category'),

    path('products/<int:id>', ProductView.as_view(template_name = 'pages/catalog/product.html'), name='product'),

    path('stats/', StatsView.as_view(template_name = 'pages/catalog/stats.html'), name='stats'),
]   