from django.db import models


class BaseModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Criado em'
    )
    last_change = models.DateTimeField(
        auto_now=True, verbose_name='Atualizado em'
    )
