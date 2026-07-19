from django.contrib import admin

from .models import Product

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'description', 'price', 'original_price', 'unit', 'stock', 'is_organic', 'rating', 'review_count', 'discount', 'created_at', )
    list_filter = ('category', 'created_at',)
    search_fields = ('name','description','category',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Product Info',{
            'fields':('category', 'name', 'description', 'is_organic',)
        }),
        ('Product Costing Info',{
            'fields':('price', 'original_price', 'discount',)
        }),
        ('Storage Info',{
            'fields':('unit', 'stock', )
        }),
        ('Review and Rating Info',{
            'fields':('rating', 'review_count')
        }),
        ("Timestamps", {
            "fields": ("created_at", )
        }),
    )