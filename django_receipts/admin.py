from django.contrib import admin
from django_receipts.models import Receipt

class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('created', 'checked', 'valid', 'allow')
    list_filter = ('valid', 'allow')

admin.site.register(Receipt, ReceiptAdmin)
