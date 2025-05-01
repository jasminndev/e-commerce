import code
import random
from datetime import timedelta

from django.contrib import messages
from django.core.mail import send_mail
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, FormView, CreateView
from redis import Redis

from apps.forms import EmailForm, RegisterModelForm
from apps.models import Category, Product
from root.settings import EMAIL_HOST_USER


class HomeListView(ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'auth/block/base.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] =Product.objects.all()
        return data


class CategoriesView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    template_name = 'auth/categories/electronics.html'

class ProductDetail(TemplateView):
    template_name = 'auth/categories/detail/product_detail.html'


class AccountView(TemplateView):
    template_name = 'account/account.html'


class OrderView(TemplateView):
    template_name = 'auth/categories/detail/ready_for_order.html'


class SendMailFormView(FormView):
    form_class =EmailForm
    template_name = 'auth/login-register/register.html'
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        verify_code = random.randrange(10**5 , 10**6)
        send_mail(
            subject="Verification Code !!!",
            message=f"{verify_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        redis = Redis()
        redis.set(email , verify_code)
        redis.expire(email , time=timedelta(minutes=5))



        return render(self.request , 'auth/login-register/check-message.html' , {"email":email})


    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request , error)
        return super().form_invalid(form)


class RegisterCreateView(CreateView):
    form_class = RegisterModelForm
    template_name = 'auth/login-register/check-message.html'
    success_url = reverse_lazy('signin')
    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request , error)
        return super().form_invalid(form)
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        sms_code = str(form.cleaned_data.get('sms'))
        redis = Redis()
        redis_code = redis.get(email)
        if not redis_code:
            messages.error(self.request, "Kod muddati tugagan.")
            return redirect('signin')

        if str(redis_code) != sms_code:
            messages.error(self.request, "Kod noto‘g‘ri.")
            return redirect('send_email')

        form.save()
        return redirect(self.success_url)
