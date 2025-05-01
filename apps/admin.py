from django.contrib import admin
from django.contrib.auth.models import User, Group
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


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     icon = html.format_html('<img width="64" height="64" src="https://img.icons8.com/external-icongeek26-linear-colour-icongeek26/64/external-Headphones-academy-icongeek26-linear-colour-icongeek26.png" alt="external-Headphones-academy-icongeek26-linear-colour-icongeek26"/>')

# def is_quantity(self, obj):
#     if obj.quantity > 0:
#         return html.format_html('<img width="30" height="30" src="https://img.icons8.com/color/30/checked--v1.png" alt="checked--v1"/>')
#     else:
#         return html.format_html('<img width="30" height="30" src="https://img.icons8.com/emoji/30/cross-mark-button-emoji.png" alt="cross-mark-button-emoji"/>')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'description', 'category', 'reviews', 'main_image')


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


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    pass


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Stream)
class StreamAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_established', 'product', 'link')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('balance', 'review', 'status', 'created_at', 'payment_id')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('username',)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('description', 'stream', 'created_at')
