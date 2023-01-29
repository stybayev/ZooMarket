# from django.contrib import admin
# from . import models
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
# 
# 
# @admin.register(models.ProductList)
# class ProductListAdmin(admin.ModelAdmin):
#     list_display = (
#         'user',
#         'created_at')
#     list_filter = ['user', 'created_at']
#     ordering = ('created_at',)
# 
# 
# @admin.register(models.PriceProduct)
# class PriceProductAdmin(admin.ModelAdmin):
#     list_display = (
#         'product',
#         'price',
#         'price_date')
#     list_filter = ['product', 'price_date']
#     ordering = ('price_date',)
# 
# 
# @admin.register(models.QuantityProduct)
# class QuantityProductAdmin(admin.ModelAdmin):
#     list_display = (
#         'product_list',
#         'product',
#         'quantity_product',
#         'created_at')
#     list_filter = ['product', ]
#     ordering = ('created_at',)
