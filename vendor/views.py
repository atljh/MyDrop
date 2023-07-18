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
from dashboards.models import Category, Product, Order, Dropshipper, OrderProduct, SubCategory
from .forms import OrderForm, OrderProductForm, CategoryForm, SubCategoryForm, ProductForm

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
                    return JsonResponse({'success': False, 'errors': product_form.errors}, status=400)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': order_form.errors}, status=400)



class CategoryView(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['categories'])
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context

class AddCategory(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('/js/custom/pages/catalog/save-category.js')
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context


class AddCategoryView(LoginRequiredMixin, View):
    def post(self, request):
        form = CategoryForm(request.POST, request.FILES)

        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user.vendor
            category.save()

            return JsonResponse({'success': True})

        return JsonResponse({'errors': form.errors}, status=400)


class CategoryDetailView(TemplateView):
    template_name = 'pages/catalog/category.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['categories'])

        user = self.request.user.vendor

        category_id = kwargs['id']
        category = get_object_or_404(Category, id=category_id, user=user)        
        
        subcategories = SubCategory.objects.filter(category=category, user=user)
        products = Product.objects.filter(category=category, user=user
                                          )
        context['category'] = category
        context['subcategories'] = subcategories
        context['products'] = products

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context
    

class SubCategoryDetailView(TemplateView):
    template_name = 'pages/catalog/subcategory.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['categories'])

        user = self.request.user.vendor

        category_id = kwargs['sub']
        category = get_object_or_404(Category, id=category_id, user=user)
        

        subcategory_id = kwargs['id']
        subcategory = get_object_or_404(SubCategory, id=subcategory_id, user=user)
        
        
        products = Product.objects.filter(subcategory=subcategory, user=user)
        
        context['category'] = category
        context['subcategory'] = subcategory
        context['products'] = products

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context


class AddSubCategory(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addJavascriptFile('/js/custom/pages/catalog/save-subcategory.js')
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        user = self.request.user.vendor

        category_id = kwargs['id']
        category = get_object_or_404(Category, id=category_id, user=user)
                
        context['category'] = category

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context

    def post(self, request, id):
        form = SubCategoryForm(request.POST, request.FILE)
        category = get_object_or_404(Category, id=id, user=request.user.vendor)

        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.user = request.user.vendor
            subcategory.category = category
            subcategory.save()

            return JsonResponse({'success': True})

        return JsonResponse({'errors': form.errors}, status=400)



class AddProductView(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['add-product', 'formrepeater'])

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        user = self.request.user.vendor
        
        category_id = kwargs['id']
        category = get_object_or_404(Category, id=category_id, user=user)
        subcategory_id = kwargs.get('sub')
        subcategory = SubCategory.objects.filter(id=subcategory_id, user=user).first()
        
        
        context['category'] = category
        context['subcategory'] = subcategory

        return context
    
    def post(self, request, id = None, sub = None):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user.vendor
            product.save()


            return JsonResponse({'success': True})

        return JsonResponse({'errors': form.errors}, status=400)



class ProductView(TemplateView):
    template_name = 'pages/dashboards/profile.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/vendor/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendors(['add-product', 'formrepeater'])

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        user = self.request.user.vendor
        
        product_id = kwargs['id']
        product = get_object_or_404(Product, id=product_id, user=user) 

        print(product, '_'*100, product.description)
        
        context['product'] = product

        return context