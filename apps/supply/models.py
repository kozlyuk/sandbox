from django.db import models
from oscar.apps.partner.models import Partner, StockRecord
from oscar.apps.catalogue.models import Product
from sandbox.apps.company.models import Company
from django.contrib.auth.models import User
from .formatChecker import ContentTypeRestrictedFileField
from datetime import datetime
from django.utils.timezone import now
from crum import get_current_user


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/projects/user_<id>/Year/Month/<filename>
    return 'invoice/user_{0}/{1}/{2}/{3}'\
        .format(get_current_user().id, datetime.now().year, datetime.now().month, filename)


class Purchase(models.Model):
    NotPaid = 'NP'
    AdvancePaid = 'AP'
    PaidUp = 'PU'
    PAYMENT_STATUS_CHOICES = (
        (NotPaid, 'Не оплачений'),
        (AdvancePaid, 'Оплачений аванс'),
        (PaidUp, 'Оплачений')
        )
    customer = models.ForeignKey(Partner, verbose_name='Партнер', on_delete=models.PROTECT)
    company = models.ForeignKey(Company, verbose_name='Компанія', on_delete=models.PROTECT)
    invoice_number = models.CharField('Номер договору', max_length=30)
    invoice_date = models.DateField('Дата договору', default=now)
    products = models.ManyToManyField(Product, through='InvoiceLine', related_name='products',
                                   verbose_name='Товари', blank=True)
    value = models.DecimalField('Вартість робіт, грн.', max_digits=8, decimal_places=2, default=0)
    currency = models.CharField('Валюта', max_length=12, default='грн')
    creator = models.ForeignKey(User, verbose_name='Створив', related_name='purchase_creators', on_delete=models.PROTECT)
    creation_date = models.DateField(auto_now_add=True)
    pdf_copy = ContentTypeRestrictedFileField('Електронний примірник', upload_to=user_directory_path,
                                              content_types=['application/pdf',
                                                             'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                                             'application/vnd.openxmlformats-officedocument.wordprocessingml.document'],
                                              max_upload_size=26214400,
                                              blank=True, null=True)

    class Meta:
        unique_together = ('number', 'customer')
        verbose_name = 'Договір'
        verbose_name_plural = 'Договори'
        ordering = ['-creation_date', 'customer', '-number']

    def __str__(self):
        return self.number + ' ' + self.customer.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creator = get_current_user()


class Payment(models.Model):
    purchase = models.ForeignKey(Partner, verbose_name='Партнер', on_delete=models.PROTECT)
    pay_date = models.DateField('Дата оплати', blank=True, null=True)
    pay_value = models.DecimalField('Вартість робіт, грн.', max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплати'

    def __str__(self):
        return self.name


class InvoiceLine(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.PROTECT)
    purchase = models.ForeignKey(Purchase, verbose_name='Закупівля', on_delete=models.PROTECT)
    stockrecord = models.OneToOneField(StockRecord, blank=True, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField('Кількість', default=1)
    units = models.CharField('Одиниці', max_length=12, default='шт.')
    unit_price = models.DecimalField('Ціна одиниці, грн.', max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.name
