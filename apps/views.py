import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, FormView, CreateView, DetailView
from redis import Redis

from apps.forms import EmailForm, RegisterModelForm
from apps.models import Category, Product, Region, User, Delivery
from root.settings import EMAIL_HOST_USER


class HomeListView(ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'block/base.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        return data


def category_products(request):
    category_name = request.GET.get('category')
    products = []
    category = None

    if category_name:
        try:
            category = Category.objects.get(name=category_name)
            products = Product.objects.filter(category=category)
        except Category.DoesNotExist:
            products = []

    categories = Category.objects.all()

    return render(request, 'category/category_products.html', {
        'products': products,
        'category': category,
        'categories': categories,
        'active_category_id': category.pk if category else None
    })


class ProductDetail(DetailView):
    queryset = Product.objects.all()
    context_object_name = 'product'
    template_name = 'category/product/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['regions'] = Region.objects.all()
        return context


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'account/account.html'
    login_url = reverse_lazy('login')

    def get_login_url(self):
        return super().get_login_url()


class OrderView(TemplateView):
    template_name = 'category/product/ready_for_order.html'


class SendMailFormView(FormView):
    form_class = EmailForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        verify_code = random.randrange(10 ** 5, 10 ** 6)
        send_mail(
            subject="Verification Code!",
            message=f"{verify_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        redis = Redis()
        redis.set(email, verify_code)
        redis.expire(email, time=timedelta(minutes=5))

        return render(self.request, 'auth/check-message.html', {"email": email})

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class RegisterCreateView(CreateView):
    form_class = RegisterModelForm
    template_name = 'auth/check-message.html'
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        sms_code = str(form.cleaned_data.get('sms'))
        redis = Redis()
        redis_code = redis.get(email)

        if not redis_code:
            messages.error(self.request, "Kod muddati tugagan.")
            return redirect('login')

        if int(redis_code) != int(sms_code):  # noqa
            messages.error(self.request, "Kod noto‘g‘ri.")
            return redirect('send_email')

        user, created = User.objects.get_or_create(email=email)

        if created:
            user.set_unusable_password()
            user.save()
            messages.success(self.request, "Foydalanuvchi muvaffaqiyatli yaratildi va tizimga kirdingiz.")
        else:
            messages.success(self.request, "Tizimga muvaffaqiyatli kirdingiz.")

        login(self.request, user)

        return redirect('account')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


def checkout_view(request, product_id, delivery_id):
    product = get_object_or_404(Product, id=product_id)
    delivery = get_object_or_404(Delivery, id=delivery_id)

    total = product.price + delivery.price

    return render(request, 'category/product/ready_for_order.html', {
        'product': product,
        'delivery': delivery,
        'total': total,
        'products': Product.objects.all(),
    })


def explore_category(request, pk):
    categories = Category.objects.all()
    return render(request, 'category/category_products.html', {
        'categories': categories,
        'active_category_id': pk
    })
