from django.urls import path

from apps.views import OrderView

urlpatterns = [
    path('order', OrderView.as_view(), name='order'),

]
