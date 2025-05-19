from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.timezone import localtime
from unfold.admin import TabularInline

from apps.models import *

admin.site.unregister(Group)

from django.contrib import admin
from .models import Category

from django.utils.html import format_html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon_tag')

    def icon_tag(self, obj):
        if obj.icon:
            return format_html(
                '<img src="{}" style="width:60px !important; height:60px !important; object-fit:contain;" />',
                obj.icon
            )
        return "-"

    icon_tag.short_description = 'Icon'


class ProductImageAdmin(TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'description', 'category', 'discount')
    inlines = ProductImageAdmin,


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('name', 'username_telegram')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'product')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('balance', 'review', 'status', 'created_at', 'payment_id')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('description', 'stream', 'created_at')


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    def formatted_delivery_time(self, obj):
        return localtime(obj.delivery_time).strftime('%Y-%m-%d %H:%M')

    formatted_delivery_time.short_description = 'Delivery time'
    list_display = ('id', 'formatted_delivery_time')
