from django.urls import path

from apps.views import HomeListView, ProductDetail, ProductListView, StreamCreateView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('products', ProductListView.as_view(), name='category_products'),
    path('product-detail/<int:pk>', ProductDetail.as_view(), name='product_detail'),
    path('steam-create', StreamCreateView.as_view(), name='stream_create'),

    # path('create-stream/', create_stream, name='create_stream'),
    # path('delete-stream/', delete_stream, name='delete_stream'),
    # path('stream/<int:stream_id>/', stream_detail, name='stream_detail'),
    # path('search', SearchListView.as_view(), name='search'),
]
