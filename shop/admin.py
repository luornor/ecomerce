from django.contrib import admin
from .models import Category, Region, Product, Cart

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'stock_quantity', 'get_category', 'get_region','image_url')
    search_fields = ('name', 'description')
    list_filter = ('category', 'region', 'price')
    ordering = ('-id',)
    fields = ('name', 'description', 'price', 'stock_quantity', 'category', 'region','image_url')

    def get_category(self, obj):
        return obj.category.name
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'

    def get_region(self, obj):
        return obj.region.name
    get_region.short_description = 'Region'
    get_region.admin_order_field = 'region__name'

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product', 'quantity')
    search_fields = ('product__name',)
    list_filter = ('product',)
    ordering = ('-id',)
    fields = ('product', 'quantity')

    def get_product(self, obj):
        return obj.product.name
    get_product.short_description = 'Product'
    get_product.admin_order_field = 'product__name'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
