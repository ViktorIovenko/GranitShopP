
from django.contrib import admin
from .models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'model', 'mount_type')
    list_filter = ('model', 'mount_type')
    search_fields = ('name', 'model')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]

    # Переопределение атрибута verbose_name_plural
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.verbose_name_plural = 'Добавление товара'


admin.site.register(Product, ProductAdmin)

# Register your models here.
