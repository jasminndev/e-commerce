from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField

from apps.models import User, Product, Stream, Order


class EmailForm(Form):
    email = EmailField()


class LoginModelForm(Form):
    email = EmailField(label='Email')
    sms = CharField(label='SMS Code')

    class Meta:
        model = User
        fields = 'email', 'sms',

    def validate_user(self):
        user = self.cleaned_data['email']
        return user

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class AuthForm(Form):
    email = EmailField()
    password = CharField(max_length=30)

    def clean_password(self):
        password = self.cleaned_data.get("password")
        return make_password(str(password))

    def is_exists(self):
        email = self.cleaned_data.get("email")
        password = self.data.get("password")
        query = User.objects.filter(email=email)
        if not query.exists():
            user = User.objects.create_user(email)
            user.set_password(password)
            user.save()
        else:
            user = query.first()
            if check_password(password, user.password):
                return user

    def save(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        return User.objects.create_user(email=email, password=password)


class ProfileModelForm(ModelForm):
    class Meta:
        model = User
        fields = "first_name", "last_name", "phone_number", "email",


class UpdateProfilePhoto(ModelForm):
    class Meta:
        model = User
        fields = "image",


class PasswordForm(Form):
    new_password = CharField(max_length=30)
    confirm_password = CharField(max_length=30)

    def clean_confirm_password(self):
        new_password = self.cleaned_data.get("new_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if new_password != confirm_password:
            raise ValidationError("Parollar mos kelmadi.")
        return confirm_password


class StreamCreateModelForm(ModelForm):
    class Meta:
        model = Stream
        fields = 'name', 'product', 'owner',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

    def clean_product(self):
        product_id = self.data.get('product')
        return Product.objects.filter(id=product_id).first()

class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = 'first_name', 'phone_number', 'owner', 'product', 'stream',


class OldEmailForm(Form):
    email = EmailField(label="Hozirgi email")


class NewEmailForm(Form):
    old_email = EmailField(label="Yangi email")
    sms = CharField(label="Tasdiqlash kodi")