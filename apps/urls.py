from django.urls import path

from apps.views import HomeListView, CategoriesView, ProductDetail, AccountView, OrderView, SendMailFormView, \
    RegisterCreateView

urlpatterns = [
    path('home', HomeListView.as_view(), name='home'),
    path('electronics', CategoriesView.as_view(), name='electronics'),
    path('product-detail', ProductDetail.as_view(), name='product_detail'),
    path('signin', AccountView.as_view(), name='signin'),
    path('order', OrderView.as_view(), name='order'),
    path('send-email', SendMailFormView.as_view(), name='send_email'),
    path('check-email', RegisterCreateView.as_view(), name='check_email'),
]