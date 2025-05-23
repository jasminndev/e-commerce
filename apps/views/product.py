from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView, ListView

from apps.models import Category, Product, Region


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


class SearchListView(View):
    def post(self, request):
        search = request.POST.get("search")
        products = Product.objects.filter(Q(name__icontains=search) | Q(description_icontains=search))
        context = {"products" : products}
        return render(request, '' , context)


