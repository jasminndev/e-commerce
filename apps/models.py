from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager, AbstractUser
from django.db import models
from django.db.models import Model, ImageField, CharField, DecimalField, SmallIntegerField, TextField, ForeignKey, \
    DateTimeField, CASCADE, BooleanField, EmailField, TextChoices, FileField


class Category(Model):
    class Meta:
        verbose_name_plural = 'categories'

    icon = CharField(max_length=500, null=True, blank=True)
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(Model):
    main_image = ImageField(upload_to='products', null=False, blank=False)
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = SmallIntegerField(default=1)
    description = TextField()
    reviews = TextField(null=True, blank=True)
    video = FileField(upload_to='products', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    attribute_id = ForeignKey('apps.Attribute', on_delete=CASCADE, related_name='products',null=True, blank=True)
    seller_id = ForeignKey('apps.Seller', on_delete=CASCADE, related_name='products',null=True, blank=True)
    category = ForeignKey('apps.Category', on_delete=models.CASCADE, related_name='products',)


class Attribute(Model):
    name = CharField(max_length=255)

    def __str__(self):
        return self.name


class Seller(Model):
    name = CharField(max_length=255)
    username_telegram = CharField(max_length=255)


class Tag(Model):
    name = CharField(max_length=255)


class ProductTag(Model):
    tag = ForeignKey('apps.Tag', on_delete=CASCADE, related_name='product_tgs')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='product_tags')


class Option(Model):
    name = CharField(max_length=255)
    attribute = ForeignKey('apps.Attribute', on_delete=CASCADE, related_name='options')


class ProductImage(Model):
    image_file = ImageField(upload_to='product_images', null=True, blank=True)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='product_images')


class Region(Model):
    name = CharField(max_length=255)


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='districts')


class CustomerUser(UserManager):
    def _create_user_object(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        user = self._create_user_object(email, password, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = EmailField(max_length=255, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomerUser()


class Stream(Model):
    name = CharField(max_length=255)
    link = CharField(max_length=255)
    is_established = BooleanField(default=False)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='streams')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='streams')


class Transaction(Model):
    class StatusType(TextChoices):
        PENDING = 'pending', 'Pending',
        COMPLETED = 'completed', 'Completed'
        FAILED = 'failed', 'Failed'

    balance = DecimalField(max_digits=10, decimal_places=2)
    review = TextField()
    status = CharField(max_length=255, choices=StatusType, default=StatusType.PENDING)
    created_at = DateTimeField(auto_now_add=True)
    payment_id = ForeignKey('apps.Payment', on_delete=CASCADE, related_name='transactions')


class Account(Model):
    image = ImageField(upload_to='accounts', null=True, blank=True)
    username = CharField(max_length=255)
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='accounts')
    district = ForeignKey('apps.District', on_delete=CASCADE, related_name='accounts')


class Query(Model):
    class StatusType(TextChoices):
        POSITIVE = 'positive', 'Positive',
        NEGATIVE = 'negative', 'Negative',

    description = TextField()
    status = CharField(max_length=255, choices=StatusType, default=StatusType.POSITIVE)
    created_at = DateTimeField(auto_now_add=True)
    stream = ForeignKey('apps.Stream', on_delete=CASCADE, related_name='queries')
    order_address = ForeignKey('apps.OrderAddress', on_delete=CASCADE, related_name='queries')


class OrderAddress(Model):
    address = CharField(max_length=255)
    district = CharField(max_length=255)


class Order(Model):
    class StatusType(TextChoices):
        PENDING = 'pending', 'Pending'
        SHIPPED = 'shipped', 'Shipped'
        IN_TRANSIT = 'in_transit', 'In Transit'
        DELIVERED = 'delivered', 'Delivered'
        FAILED = 'failed', 'Failed'

    name = CharField(max_length=255)
    phone_number = CharField(max_length=255)
    status = CharField(max_length=255, choices=StatusType, default=StatusType.PENDING)
    created_at = DateTimeField(auto_now_add=True)
    stream_ordering = CharField(max_length=255)
    payment = ForeignKey('apps.Payment', on_delete=CASCADE, related_name='orders')
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='orders')
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='orders')
    region = ForeignKey('apps.Region', on_delete=CASCADE, related_name='orders')
    order_address = ForeignKey('apps.OrderAddress', on_delete=CASCADE, related_name='orders')


class Payment(Model):
    card_number = CharField(max_length=255)
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='payments')
    amount = DecimalField(max_digits=10, decimal_places=2)


class Charity(Model):
    description = TextField()
    seller = ForeignKey('apps.Seller', on_delete=CASCADE, related_name='charities')
    amount = DecimalField(max_digits=10, decimal_places=2)


class Delivery(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=2)
    description = TextField()
    delivery_time = DateTimeField()
    phone_number = CharField(max_length=255)


class Post(Model):
    name = CharField(max_length=255)
    description = TextField()
    image = ImageField(upload_to='posts', null=True, blank=True)
    created_at = DateTimeField(auto_now_add=True)


class Settings(Model):
    phone_number = CharField(max_length=255)
    telegram_link = CharField(max_length=255)


class Penalty(Model):
    name = CharField(max_length=255)
    amount = DecimalField(max_digits=10, decimal_places=2)
    description = TextField()
    response = TextField()
    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='penalties')
