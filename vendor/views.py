from django.views.generic import TemplateView
from django.http import HttpResponse
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
import json
from dashboards.models import Category, Product


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
        # KTTheme.addJavascriptFile('js/custom/apps/ecommerce/catalog/save-category.js')
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
        # KTTheme.addJavascriptFile('js/custom/apps/ecommerce/catalog/save-category.js')

        category_id = kwargs['id']
        category = get_object_or_404(Category, id=category_id)
        
        user = self.request.user.vendor
        
        # Фильтруем продукты по категории и пользователю
        products = Product.objects.filter(category=category, user=user)
        
        context['category'] = category
        context['products'] = products

        context.update({
            'layout': KTTheme.setLayout('default.html', context),
        })

        return context
