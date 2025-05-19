from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, EmailField

from apps.models import User, Stream, Product


class EmailForm(Form):
    email = CharField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        query = User.objects.filter(email=email)
        if query.exists():
            raise ValidationError(f'{email} exists')
        return email


class RegisterModelForm(ModelForm):
    # password = CharField(widget=PasswordInput())
    # password_confirm = CharField(widget=PasswordInput())
    sms = CharField(label='SMS Code')
    email = EmailField()

    class Meta:
        model = User
        fields = 'email', 'sms',

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class StreamModelForm(ModelForm):
    class Meta:
        model = Stream
        fields = 'name', 'product', 'owner', 'visit_count',

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()

    def clean_discount_price(self):
        product_id = self.data.get('product')
        product = Product.objects.filter(id=product_id).first()
        return product
