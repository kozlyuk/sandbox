from django.db import models


class Requisites(models.Model):
    TAXATION_CHOICES = (
        ('wvat', 'З ПДВ'),
        ('wovat', 'Без ПДВ'),
    )
    fullname = models.CharField('Повна назва', max_length=50)
    address = models.CharField('Юридична адреса', blank=True)
    requisites = models.CharField('Реквізити', blank=True)
    bank_requisites = models.CharField('Банківські реквізити', blank=True)
    chief = models.CharField('Керівник', max_length=50, blank=True)
    contact_person = models.CharField('Контактна особа', max_length=50, blank=True)
    phone = models.CharField('Телефон', max_length=13, blank=True)
    taxation = models.CharField('Система оподаткування', max_length=5, choices=TAXATION_CHOICES, default='wvat')

    class Meta:
        verbose_name = 'Реквізити'
        verbose_name_plural = 'Реквізити'

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField('Назва', max_length=50)
    requisites = models.OneToOneField(Requisites, on_delete=models.CASCADE())

    class Meta:
        verbose_name = 'Компанія'
        verbose_name_plural = 'Компанії'

    def __str__(self):
        return self.name