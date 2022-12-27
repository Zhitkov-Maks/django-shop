from django.db import models


class SingletonModel(models.Model):
    """Модель для нужна для того чтобы у нас в настройках была всгда одна запись"""
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
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
    logotype = models.FileField(upload_to='files/logo', verbose_name='Логотип', default=0)
    phone = models.CharField(max_length=15, verbose_name='Телефон', default=0)
    email = models.EmailField(max_length=50, verbose_name='Email', default=0)
    skype = models.CharField(max_length=50, verbose_name='Skype', default=0)
    address = models.CharField(max_length=200, verbose_name='Адрес', default=0)
    price_delivery_express = models.DecimalField(verbose_name='Стоимость экспресс доставки',
                                                 max_digits=8, decimal_places=2, default=0)
    price = models.DecimalField(verbose_name='Стоимость обычной доставки', max_digits=8, decimal_places=2, default=0)
    min_sum = models.DecimalField(verbose_name='Минимальная сумма для бесплатной доставки',
                                  max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return 'Configuration'

    class Meta:
        verbose_name = 'настройки сайта'
        verbose_name_plural = 'настройки сайта'
