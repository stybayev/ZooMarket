from django.contrib.auth import get_user_model
from django.db import models


class Pet(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя')

    age = models.PositiveIntegerField(verbose_name='Возраст', )

    pet_type = models.ForeignKey('pet.PetType',
                                 on_delete=models.PROTECT,
                                 verbose_name='Вид питомца',
                                 related_name='pet')

    user = models.ForeignKey(get_user_model(),
                             null=True, blank=True,
                             verbose_name='Владелец питомца',
                             on_delete=models.PROTECT,
                             related_name='pet')

    def __str__(self):
        return f"{self.name} - {self.age}"

    class Meta:
        verbose_name = "Питомец"
        verbose_name_plural = "01 Питомец"


class PetType(models.Model):
    title = models.CharField(max_length=255, verbose_name='Вид питомца')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Вид питомца"
        verbose_name_plural = "02 Вид питомца"
