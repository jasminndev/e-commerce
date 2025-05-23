from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from apps.forms import  StreamCreateModelForm
from apps.models import Category
from apps.models.product import Product, Stream


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


class StreamCreateView(CreateView):
    queryset = Stream.objects.all()
    form_class = StreamCreateModelForm
    template_name = 'account/market.html'
    success_url = reverse_lazy('stream')

    def form_valid(self, form):
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        self.object = object
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class StreamListView(ListView):
    queryset = Stream.objects.all()
    template_name = 'account/stream.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class StreamProductDetail(DetailView):
    queryset = Stream.objects.all()
    template_name = 'category/product/product_detail.html'
    context_object_name = 'stream'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        stream = self.get_object(self.get_queryset())
        stream.visit_count += 1
        stream.save()
        product = self.get_object(self.get_queryset())
        data['product'] = product
        data['discount_price'] = float(product.discount_price) - float(data.get('stream').discount_price)
        return data
