from django.contrib import admin
from .models import CustomUser, Vendor, Dropshipper, Order, DropOrder, Product, Category, OrderProduct

admin.site.register(CustomUser)
admin.site.register(Vendor)
admin.site.register(Dropshipper)
admin.site.register(DropOrder)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderProduct)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

