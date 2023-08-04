from django.contrib import admin
from .models import CustomUser, Vendor, Dropshipper, Order, Product, Category, OrderProduct, SubCategory, Employee, Storage, Sector, Shelf, StorageContact

admin.site.register(CustomUser)
admin.site.register(Vendor)
admin.site.register(Dropshipper)
# admin.site.register(DropOrder)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(OrderProduct)

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductInline]

class StorageContactInline(admin.TabularInline):
    model = StorageContact
    extra = 0

class EmployeeInline(admin.TabularInline):
    model = Employee
    extra = 0

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    inlines = [StorageContactInline, EmployeeInline]

admin.site.register(Employee)
admin.site.register(Sector)
admin.site.register(Shelf)
