from django.contrib import admin

from .models import Product, ProductAccess


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "name",
    )
    list_filter = (
        "owner",
    )


@admin.register(ProductAccess)
class ProductAccessAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "product",
    )