from django.contrib import admin
from . import models


class PetInline(admin.StackedInline):
    model = models.Pet
    extra = 1


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'phone_verified',
        'phone_number',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'blocked')
    list_filter = ['phone_number', 'email']
    ordering = ('email',)
    inlines = [PetInline]
    save_as = True
    save_on_top = True


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
