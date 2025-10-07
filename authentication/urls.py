from django.urls import path
from django.views.generic import TemplateView

from apps.views import LogoutView, ChangePasswordFormView, ProfileUpdateView, UpdateProfilePhotoView, LoginFormView, \
    VerifyCodeFormView, LoginWithPasswordFormView, ChangeMailFormView, ChangeMailCodeFormView

urlpatterns = [
    path('login', LoginFormView.as_view(), name='login'),
    path('login/verify-code', VerifyCodeFormView.as_view(), name='verify_code'),
    path('login/login_w_passwd', LoginWithPasswordFormView.as_view(), name="login_w_passwd"),
    path('account/logout', LogoutView.as_view(), name='logout'),
    path('account/profile/<int:pk>', ProfileUpdateView.as_view(), name='profile'),
    path('account/profile/profile-photo/<int:pk>', UpdateProfilePhotoView.as_view(), name='profile_image'),
    path('account/profile/change-passwd/<int:pk>', ChangePasswordFormView.as_view(), name='change_passwd'),
    path('account/profile/change_email', ChangeMailFormView.as_view(), name='change_email'),
    path('account/profile/change_email/change_email_verify_code', ChangeMailCodeFormView.as_view(), name='get_code'),
    path('account/propfile/contact-w-tg', TemplateView.as_view(template_name="profile/contact_w_tg.html"), name='contact_w_tg'),

]
