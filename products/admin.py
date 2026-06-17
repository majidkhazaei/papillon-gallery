from django.contrib import admin
from .models import Category, Product, ProductVariant

admin.site.register(Category)

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'price', 'available', 'stock')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    raw_id_fields = ('category',)
    inlines = [ProductVariantInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'price', 'available', 'stock')
    list_filter = ('product', 'available')
