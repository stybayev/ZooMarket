from django.contrib import admin

from pet.models import Pet
from . import models


class PetInline(admin.StackedInline):
    model = Pet
    extra = 1


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
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

    def get_deleted_objects(self, objs, request):
        deleted_objects, model_count, perms_needed, protected = \
            super().get_deleted_objects(objs, request)
        return deleted_objects, model_count, set(), protected
