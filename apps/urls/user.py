from django.urls import path
from django.views.generic import TemplateView

from apps.views import SendMailFormView, RegisterCreateView, LogoutView

urlpatterns = [
    path('login', SendMailFormView.as_view(), name='login'),
    path('check-email', RegisterCreateView.as_view(), name='check_email'),
    path('login_w_passwd', TemplateView.as_view(template_name='auth/login_with_passwd.html'),
         name="login_w_passwd"),
    path('logout', LogoutView.as_view(), name='logout'),
    path('change_num', TemplateView.as_view(template_name="profile/changing_number.html"), name='changing_num'),
    path('contact-w-tg', TemplateView.as_view(template_name="profile/contact_w_tg.html"), name='contact_w_tg'),
    path('change-passwd', TemplateView.as_view(template_name="profile/change_passwd.html"), name='change_passwd'),
]
