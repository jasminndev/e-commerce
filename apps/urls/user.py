from django.urls import path
from django.views.generic import TemplateView

from apps.views import SendMailFormView, RegisterCreateView

urlpatterns = [
    path('login', SendMailFormView.as_view(), name='login'),
    path('check-email', RegisterCreateView.as_view(), name='check_email'),
    path('login_w_passwd', TemplateView.as_view(template_name='auth/login_with_passwd.html'),
         name="login_w_passwd"),
]
