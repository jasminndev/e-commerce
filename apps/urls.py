from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('stream/', TemplateView.as_view(template_name='stream.html'), name='stream'),
    path('', TemplateView.as_view(template_name='ert.html'), name='stream1'),
]
