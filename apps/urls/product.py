from django.urls import path

from apps.views import HomeListView, ProductDetailView, ProductListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('products', ProductListView.as_view(), name='category_products'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]