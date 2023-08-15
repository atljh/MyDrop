from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse

import json
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthVendorSigninView(TemplateView):
    template_name = 'pages/auth/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/vendor/main/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context
    
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode('utf-8'))

        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            response_data = {'success': True, 'message': 'Login successful'}
            return JsonResponse(response_data)
        else:
            response_data = {'success': False, 'message': 'Invalid credentials'}
            return JsonResponse(response_data, status=401)
        

class AuthDropSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')

        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context


