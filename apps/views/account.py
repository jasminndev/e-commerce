from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

from apps.models import Category
from apps.models.product import Product


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account/dashboard.html'
    login_url = reverse_lazy('login')

    def get_login_url(self):
        return super().get_login_url()


class MarketListView(ListView):
    queryset = Product.objects.all()
    template_name = 'account/market.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.kwargs.get('category')
        if category:
            queryset = queryset.filter(category__name__iexact=category.strip())
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        data['current_category'] = self.kwargs.get('category', '')
        data['no_products'] = not data['products'].exists()
        return data
