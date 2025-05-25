from django.urls import path
from django.views.generic import TemplateView

from apps.views import SendMailFormView, LogoutView, ChangePasswordFormView, ProfileUpdateView, LoginCreateView, \
    AuthFormView, UpdateProfilePhotoView, SendEmailFormView, ChangeEmailFormView

urlpatterns = [
    path('login', SendMailFormView.as_view(), name='login'),
    path('check-email', LoginCreateView.as_view(), name='check_email'),
    path('login_w_passwd', AuthFormView.as_view(), name="login_w_passwd"),
    path('account/logout', LogoutView.as_view(), name='logout'),
    path('account/profile/<int:pk>', ProfileUpdateView.as_view(), name='profile'),
    path('account/profile-photo/<int:pk>', UpdateProfilePhotoView.as_view(), name='profile_image'),
    path('contact-w-tg', TemplateView.as_view(template_name="profile/contact_w_tg.html"), name='contact_w_tg'),
    path('account/profile/change-passwd/<int:pk>', ChangePasswordFormView.as_view(), name='change_passwd'),
    path('account/profile/change_email', SendEmailFormView.as_view(), name='change_email'),
    path('account/profile/change_email/change_email_wcode', ChangeEmailFormView.as_view(), name='get_code'),

]
