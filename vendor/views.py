from django.views.generic import TemplateView
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.forms import formset_factory

import json
from dashboards.models import Category, Product, Order, Dropshipper, OrderProduct
from .serializers import CategorySerializer, OrderSerializer, ProductSerializer, DropshipperSerializer
from .forms import OrderForm, OrderProductForm

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics



class VendorView(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['user-profile', 'catalog', 'formrepeater'])
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context


class OrdersView(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['orders', 'datatables'])
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context


class AddOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'pages/catalog/add-order.html'
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['edit-order'])
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })
        user = self.request.user.vendor
        products = Product.objects.filter(user=user)
        
        context.update({
            'success': True,
            'products': products,
            'dropshippers': self.request.user.vendor.dropshippers,
        })
        return context
    
    def post(self, request):
        data = json.loads(request.body)
        order_form = OrderForm(data)
        print(data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            order.user = request.user.vendor
            order.save()
            order_products_data = json.loads(data['order_products'])
            for product_data in order_products_data:
                product_form = OrderProductForm(product_data)
                if product_form.is_valid():
                    product = product_form.save(commit=False)
                    product.order = order
                    product.save()
                else:
                    return JsonResponse({'success': False, 'errors': product_form.errors})
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': order_form.errors})


class AddCategoryView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            data = request.POST 
            name = data.get('category_name')
            
            description = data.get('description', '')
            image = request.FILES.get('avatar')

            if not name:
                return JsonResponse({'error': 'Name is required'}, status=400)

            category = Category(user=request.user.vendor, name=name, description=description, image=image)
            category.save()

            return JsonResponse({'success': True})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

class CategoryDetailView(TemplateView):
    template_name = 'pages/catalog/category.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['user-profile', 'catalog', 'formrepeater'])

        category_id = kwargs['id']
        category = get_object_or_404(Category, id=category_id)
        
        user = self.request.user.vendor
        
        products = Product.objects.filter(category=category, user=user)
        
        context['category'] = category
        context['products'] = products

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context
