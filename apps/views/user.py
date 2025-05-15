import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView, CreateView
from redis import Redis

from apps.forms import EmailForm, RegisterModelForm
from apps.models import Category, Product, User
from root.settings import EMAIL_HOST_USER


class HomeListView(ListView):
    queryset = Category.objects.all()
    context_object_name = 'categories'
    template_name = 'block/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        return data


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
            return redirect('check_email')

        user, created = User.objects.get_or_create(email=email)

        if created:
            user.set_unusable_password()
            user.save()
            messages.success(self.request, "Foydalanuvchi muvaffaqiyatli yaratildi va tizimga kirdingiz.")
        else:
            messages.success(self.request, "Tizimga muvaffaqiyatli kirdingiz.")

        login(self.request, user)
        return redirect('dashboard')


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
