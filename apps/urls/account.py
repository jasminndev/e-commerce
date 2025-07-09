from django.urls import path
from django.views.generic import TemplateView

from apps.views import AccountView, MarketListView, StreamCreateView, StreamListView, StreamProductDetail, \
    StatisticsListView

urlpatterns = [
    path('dashboard/', AccountView.as_view(), name='dashboard'),
    path('market/', MarketListView.as_view(), name='market'),
    path('market/<str:category>', MarketListView.as_view(), name='category_filter'),
    path('stream-create', StreamCreateView.as_view(), name='create_stream'),
    path('stream/<int:pk>', StreamProductDetail.as_view(), name='stream-detail'),
    path('stream/', StreamListView.as_view(), name='stream'),
    path('statistics/', StatisticsListView.as_view(), name='statistics'),
    # path('statistics/dates', TemplateView.as_view(template_name='account/statistics_dates.html'), name='statistics_dates'),
    path('payment', TemplateView.as_view(template_name='account/payment.html'), name='payment'),
]
