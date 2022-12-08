from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'phone_number',
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',)
    list_filter = ['phone_number', 'email']
    ordering = ('email',)
