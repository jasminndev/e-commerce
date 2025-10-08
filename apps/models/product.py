from django.db import models
from django.db.models import Model, ImageField, CharField, DecimalField, ForeignKey, \
    DateTimeField, CASCADE, FileField, PositiveIntegerField, SlugField
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class SlugBasedModel(Model):
    name = CharField(max_length=255)
    slug = SlugField(max_length=255, unique=True, editable=False)

    class Meta:
        abstract = True

    def save(self, **kwargs):
        slug = slugify(self.name)
        i = 1
        while self.__class__.objects.filter(slug=slug).exists():
            slug += f"-{i}"
            i += 1
        self.slug = slug
        super().save()

    def __str__(self):
        return self.name


class Category(SlugBasedModel):
    class Meta:
        verbose_name_plural = 'categories'

    icon = CharField(max_length=500, null=True, blank=True)

    def __repr__(self):
        return self.name


class Product(Model):
    name = CharField(max_length=255)
    price = DecimalField(max_digits=10, decimal_places=0)
    discount = PositiveIntegerField()
    main_image = ImageField(upload_to='product/%Y/%m/%d/')
    quantity = PositiveIntegerField()
    description = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    manual = CKEditor5Field('Text', config_name='extends', null=True, blank=True)
    created_at = DateTimeField(auto_now=True)
    bonus_price = DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    attribute = ForeignKey('apps.Attribute', on_delete=CASCADE, related_name='products', null=True, blank=True)
    seller = ForeignKey('apps.Seller', on_delete=CASCADE, related_name='products', null=True, blank=True)
    category = ForeignKey('apps.Category', on_delete=models.CASCADE, related_name='products', )

    @property
    def discount_price(self):
        price = int(self.price)
        return price - price * (self.discount / 100)


class ProductImage(Model):
    image = ImageField(upload_to='product/%Y/%m/%d/', null=True, blank=True)
    video = FileField(upload_to='products', null=True, blank=True)
    product = ForeignKey('apps.Product', on_delete=CASCADE, related_name='images')


class Stream(Model):
    class Meta:
        default_related_name = "streams"

    name = CharField(max_length=255)
    product = ForeignKey('apps.Product', on_delete=CASCADE)
    owner = ForeignKey('authentication.User', on_delete=CASCADE)
    created_at = DateTimeField(auto_now=True)
    visit_count = PositiveIntegerField(default=0)


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
