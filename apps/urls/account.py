from django.urls import path
from django.views.generic import TemplateView

from apps.views import AccountView, MarketListView, StreamCreateView, StreamListView, StreamProductDetail

urlpatterns = [
    path('dashboard/', AccountView.as_view(), name='dashboard'),
    path('market/', MarketListView.as_view(), name='market'),
    path('market/<str:category>', MarketListView.as_view(), name='category_filter'),
    path('market/stream', StreamCreateView.as_view(), name='create_stream'),
    path('market/stream_/<int:pk>', StreamProductDetail.as_view(), name='stream-list'),
    path('stream/', StreamListView.as_view(), name='stream'),
    path('statistics', TemplateView.as_view(template_name='account/statistics.html'), name='statistics'),
    path('payment', TemplateView.as_view(template_name='account/payment.html'), name='payment'),
]
