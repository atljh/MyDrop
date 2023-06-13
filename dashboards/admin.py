from django.contrib import admin
from .models import User, Vendor, Dropshipper, Order, DropOrder
# Register your models here.

admin.site.register(User)
admin.site.register(Vendor)
admin.site.register(Dropshipper)
admin.site.register(Order)
admin.site.register(DropOrder)
