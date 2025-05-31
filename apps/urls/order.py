from django.urls import path

from apps.views import OrderCreateView

urlpatterns = [
    path('order', OrderCreateView.as_view(), name='create-order'),
]
