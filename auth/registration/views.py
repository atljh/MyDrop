from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render
from dashboards.models import User
from django.contrib.auth import get_user_model

import json
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthRegisterVendorView(TemplateView):
    template_name = 'pages/auth/registration.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context

    def post(self, request, *args, **kwargs):
        # Получение данных регистрации из запроса
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        password = data.get('password')
        CustomUser = get_user_model()

        if CustomUser.objects.filter(email=email).exists():
            response_data = {'success': False, 'message': 'User with this email already exists'}
            return JsonResponse(response_data, status=400)

        user = CustomUser(email=email, password=password)
        user.set_password(password)
        user.save()

        response_data = {'success': True, 'message': 'Registration successful'}
        return JsonResponse(response_data)

class AuthRegisterDropView(TemplateView):
    template_name = 'pages/auth/signup.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        return context
