from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from apps.forms import OrderModelForm
from apps.models import Order, Delivery, Product


class OrderCreateView(CreateView):
    queryset = Order.objects.all()
    template_name = 'category/product/product_detail.html'
    success_url = reverse_lazy('home')
    form_class = OrderModelForm

    def form_valid(self, form):
        super().form_valid(form)
        delivery = Delivery.objects.first()

        context = {
            'order': self.object,
            'delivery_price': delivery.price,
            'products': Product.objects.all()
        }

        return render(self.request, 'category/product/ready_for_order.html', context)

    def form_invalid(self, form):
        return super().form_invalid(form)



