from django.contrib import admin
from .models import Category, Product
from django.urls import reverse
from django.utils.safestring import mark_safe

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


def product_detail(obj):
    url = reverse('shop:product_detail', args=[obj.id, obj.slug])
    return mark_safe(f'<a href="{url}">View</a>')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price',
                    'available', 'created', 'updated', product_detail]
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}