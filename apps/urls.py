from django.urls import path
from django.views.generic import TemplateView

from apps.views import HomeListView, ProductDetail, AccountView, OrderView, SendMailFormView, \
    RegisterCreateView, category_products

urlpatterns = [
    path('home', HomeListView.as_view(), name='home'),
    path('products', category_products, name='category_products'),
    path('product-detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('account', AccountView.as_view(), name='account'),
    path('order', OrderView.as_view(), name='order'),
    path('send-email', SendMailFormView.as_view(), name='send_email'),
    path('check-email', RegisterCreateView.as_view(), name='check_email'),
    path('login', TemplateView.as_view(template_name='auth/login.html'), name='login'),
    path('login_w_passwd', TemplateView.as_view(template_name='auth/login_with_passwd.html'),
         name="login_w_passwd"),

]
