from django.contrib import admin
from .models import Company, Deal, Purchase, InvoiceLine


class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'chief', 'phone']
    ordering = ['name']
    fieldsets = [
        (None, {'fields': [('name', 'fullname'),
                           ('address'),
                           ('requisites'),
                           ('bank_requisites'),
                           ('chief', 'phone'),
                           ('tax_system')
                          ]})
        ]


class DealAdmin(admin.ModelAdmin):
    list_display = ['number', 'customer', 'company', 'expire_date']
    ordering = ['number']
    fieldsets = [
        (None, {'fields': [('number', 'date'),
                           ('customer', 'company'),
                           ('expire_date'),
                           ('upload'),
                           ('comment'),
                          ]})
        ]


class InvoiceLineInline(admin.TabularInline):

    model = InvoiceLine
    fields = ['product', 'unit_price', 'quantity', 'units']
    extra = 0
    show_change_link = True
    can_delete = False


class PurchaseAdmin(admin.ModelAdmin):

    list_display = ['deal', 'invoice_number', 'value_wc',
                    'in_stock', 'creator']
    list_per_page = 50
    fieldsets = [
        (None, {'fields': [('deal'),
                   ('invoice_number', 'invoice_date'),
                   ('value', 'currency'),
                   ('in_stock', 'upload')]}),
        ]
    inlines = [InvoiceLineInline]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Deal, DealAdmin)
admin.site.register(Purchase, PurchaseAdmin)
