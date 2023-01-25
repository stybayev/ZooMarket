from django.contrib import admin
from . import models


@admin.register(models.Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'age',
        'pet_type',)
    list_filter = ['pet_type', 'age']
    ordering = ('name',)


@admin.register(models.PetType)
class PetTypeAdmin(admin.ModelAdmin):
    list_display = (
        'title',)
    list_filter = ['title']
    ordering = ('title',)
