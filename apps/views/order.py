from django.views.generic import TemplateView


class OrderView(TemplateView):
    template_name = 'category/product/ready_for_order.html'

