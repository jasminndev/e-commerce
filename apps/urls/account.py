from django.urls import path
from django.views.generic import TemplateView

from apps.views import AccountView, MarketListView

urlpatterns = [
    path('dashboard', AccountView.as_view(), name='dashboard'),
    path('market', MarketListView.as_view(), name='market'),
    path('stream/', TemplateView.as_view(template_name='account/stream.html'), name='stream'),
    path('statistics', TemplateView.as_view(template_name='account/statistics.html'), name='statistics'),
    path('payment', TemplateView.as_view(template_name='account/payment.html'), name='payment'),
]
