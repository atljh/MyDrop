from django.urls import path
from django.conf import settings
from dashboards.views import DashboardsView, DropshipperView

app_name = 'dashboards'

urlpatterns = [
    path('', DashboardsView.as_view(template_name = 'pages/dashboards/landing.html'), name='index'),
    path('dropshipper/', DropshipperView.as_view(template_name = 'pages/dashboards/dropshipper.html'), name='dropshipper'),
    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]