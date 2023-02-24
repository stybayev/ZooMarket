# from django.contrib import admin
# from . import models
# from .models import Product
#
#
# @admin.register(models.Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = (
#         'vendor_code',
#         'title',
#         'brand',
#         'created_at')
#     list_filter = ['brand', 'title', 'vendor_code']
#     search_fields = (
#         'vendor_code',
#         'title',
#         'brand',
#     )
#     ordering = ('created_at',)
#     exclude = ('product_list',)
#
#
# @admin.register(models.ProductList)
# class ProductListAdmin(admin.ModelAdmin):
#     list_display = ('created_at', 'product')
#     list_filter = ('created_at',)
#     ordering = ('created_at',)
