import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, FormView, UpdateView
from redis import Redis

from apps.forms import EmailForm, LoginModelForm, PasswordForm, ProfileModelForm, AuthForm
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


class LoginCreateView(FormView):
    form_class = LoginModelForm
    template_name = 'auth/check-message.html'
    success_url = reverse_lazy('home')

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

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


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


class AuthFormView(FormView):
    form_class = AuthForm
    template_name = 'auth/login_with_passwd.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            user = form.is_exists()
            if user == None:
                messages.error(self.request, "Parol xato!")
                return redirect('login_w_passwd')
            login(self.request, user)

        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    form_class = ProfileModelForm
    template_name = 'profile/profile.html'
    login_url = reverse_lazy('login')
    pk_url_kwarg = "pk"
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={"pk": self.request.user.pk})


class ChangePasswordFormView(FormView):
    form_class = PasswordForm
    template_name = "profile/change_passwd.html"

    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data.get("new_password")
        user.set_password(new_password)
        user.save()
        login(self.request, user)
        messages.success(self.request, "Parol muvaffaqqiyatli yangilandi!")
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('change_passwd', kwargs={"pk": self.request.user.pk})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
