from django.contrib import admin
from .models import CustomUser, Vendor, Dropshipper, Order, DropOrder

admin.site.register(CustomUser)
admin.site.register(Vendor)
admin.site.register(Dropshipper)
admin.site.register(Order)
admin.site.register(DropOrder)
