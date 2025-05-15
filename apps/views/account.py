from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView

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

    # def get_context_data(self, **kwargs):
    #     data = super().get_context_data(**kwargs)
