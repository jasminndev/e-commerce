from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Count
from django.db.models.aggregates import Sum
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView, DetailView

from apps.forms import StreamModelForm
from apps.models import Category, Order, Region
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
    form_class = StreamModelForm
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
    template_name = 'category/stream/stream_detail.html'
    context_object_name = 'stream'
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        stream = self.get_object(self.get_queryset())
        stream.visit_count += 1
        stream.save()
        product = self.get_object(self.get_queryset()).product
        data['product'] = product
        data['regions'] = Region.objects.all()
        # data['discount_price'] = float(product.discount) - float(data.get('stream').discount_price)
        return data


class StatisticsListView(ListView):
    queryset = Stream.objects.all()
    template_name = 'account/statistics.html'
    context_object_name = 'streams'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        dict_data = self.get_queryset().aggregate(
            visit_count=Sum('visit_count'),
            new_total=Sum('new_count'),
            ready_to_deliver=Sum('ready_to_delivery_count'),
            delivering=Sum('delivering_count'),
            delivered=Sum('delivered_count'),
            missed_call=Sum('missed_call_count'),
            canceled=Sum('canceled_count'),
            archived=Sum('archived_count'),
            completed=Sum('completed_count')
        )
        data.update(dict_data)
        return data

    def get_queryset(self):
        # dates = self.request
        # print(dates)
        # if dates:
        #     return super().get_queryset().filter(owner=self.request.user)

        # else:
        qs = super().get_queryset().filter(owner=self.request.user)
        qs = qs.annotate(
            new_count=Count('orders', filter=Q(orders__status=Order.StatusType.NEW)),
            ready_to_delivery_count=Count('orders', filter=Q(orders__status=Order.StatusType.READY_TO_DELIVER)),
            delivering_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERING)),
            delivered_count=Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED)),
            missed_call_count=Count('orders', filter=Q(orders__status=Order.StatusType.COMPLETED)),
            missed_call=Count('orders', filter=Q(orders__status=Order.StatusType.MISSED_CALL)),
            canceled_count=Count('orders', filter=Q(orders__status=Order.StatusType.CANCELED)),
            archived_count=Count('orders', filter=Q(orders__status=Order.StatusType.ARCHIVED)),
            completed_count=Count('orders', filter=Q(orders__status=Order.StatusType.COMPLETED)), )
        return qs
        # qs.stream = qs.aggregate(
        #     total_visit_count=Sum('visit_count'),
        #     total_new_count=Sum(Order.StatusType.NEW),
        #     total_ready_count=Sum(Order.StatusType.READY_TO_DELIVER),
        #     total_deliver_count=Sum(Order.StatusType.DELIVERING),
        #     total_delivered_count=Sum(Order.StatusType.DELIVERED),
        #     total_completed_count=Sum(Order.StatusType.COMPLETED),
        #     total_missed_call_count=Sum(Order.StatusType.MISSED_CALL),
        #     total_canceled_count=Sum(Order.StatusType.CANCELED),
        #     total_archived_count=Sum(Order.StatusType.ARCHIVED),
        # )
