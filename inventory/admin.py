from django.contrib import admin

from .models import Item, ItemCategory, SaleInvoice, SaleLine, StockEntry, Supplier

admin.site.register(ItemCategory)
admin.site.register(Supplier)
admin.site.register(Item)
admin.site.register(StockEntry)
admin.site.register(SaleInvoice)
admin.site.register(SaleLine)
