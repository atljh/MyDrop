from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.http import HttpResponseRedirect



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


