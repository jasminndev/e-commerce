from django.urls import path

from apps.views import HomeListView, ProductDetail, ProductListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('products', ProductListView.as_view(), name='category_products'),
    path('product-detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    # path('search', SearchListView.as_view(), name='search'),
]
