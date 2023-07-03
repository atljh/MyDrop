from django.contrib import admin
from .models import CustomUser, Vendor, Dropshipper, Order, DropOrder, Product, Category

admin.site.register(CustomUser)
admin.site.register(Vendor)
admin.site.register(Dropshipper)
admin.site.register(Order)
admin.site.register(DropOrder)
admin.site.register(Product)
admin.site.register(Category)

