from django.db import models


class SingletonModel(models.Model):
    """
    Модель нужна для того чтобы у нас в настройках была
    всегда одна запись.
    """

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Удаляем все другие записи перед сохранением новой
        self.__class__.objects.exclude(id=self.pk).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class SiteSettings(SingletonModel):
    """Непосредственно сама модель с настройками"""

    logotype = models.FileField(
        upload_to="files/logo", verbose_name="Логотип", blank=True, null=True
    )
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True)
    email = models.EmailField(max_length=50, verbose_name="Email", blank=True)
    skype = models.CharField(max_length=50, verbose_name="Skype", blank=True)
    address = models.CharField(max_length=200, verbose_name="Адрес", blank=True)
    price_delivery_express = models.DecimalField(
        verbose_name="Стоимость экспресс доставки",
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    price = models.DecimalField(
        verbose_name="Стоимость обычной доставки",
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    min_sum = models.DecimalField(
        verbose_name="Минимальная сумма для бесплатной доставки",
        max_digits=8,
        decimal_places=2,
        default=0,
    )

    def __str__(self):
        return "Configuration"

    class Meta:
        verbose_name = "настройки сайта"
        verbose_name_plural = "настройки сайта"
