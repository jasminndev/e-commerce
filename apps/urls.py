from django.urls import path
from django.views.generic import TemplateView

from apps.views import HomeListView, CategoriesView, ProductDetail, AccountView, OrderView, SendMailFormView, \
    RegisterCreateView

urlpatterns = [
    path('home', HomeListView.as_view(), name='home'),
    path('products', CategoriesView.as_view(), name='category_products'),
    path('product-detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('signin', AccountView.as_view(), name='signin'),
    path('order', OrderView.as_view(), name='order'),
    path('send-email', SendMailFormView.as_view(), name='send_email'),
    path('check-email', RegisterCreateView.as_view(), name='check_email'),
    path('account', TemplateView.as_view(template_name='account/account.html'), name='account'),
    path('login', TemplateView.as_view(template_name='auth/login-register/login.html'), name='login'),
    path('login_w_passwd', TemplateView.as_view(template_name='auth/login-register/login_with_passwd.html'),
         name="login_w_passwd"),

]
