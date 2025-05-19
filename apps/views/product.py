from django.views.generic import DetailView, ListView, CreateView

from apps.forms import StreamModelForm
from apps.models import Category, Product, Region, Stream


class ProductDetail(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'category/product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        return context


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'category/category_products.html'
    context_object_name = "products"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        slug = self.request.GET.get("category")
        data['slug'] = slug
        if not slug == "all":
            data['products'] = data.get('products').filter(category__slug=slug)
        data['categories'] = Category.objects.all()
        return data

class StreamCreateView(CreateView):
    queryset = Stream.objects.all()
    form_class = StreamModelForm
    template_name = 'account/market.html'

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)





