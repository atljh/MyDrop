from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    phone_number = models.IntegerField(default=False)

    is_dropshipper = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    # Add related_name arguments to resolve clashes
    groups = models.ManyToManyField(
        'auth.Group',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser'
    )


    def __str__(self):
        return self.email

class Dropshipper(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vendor')


    def get_orders(self):
        return self.user.vendor.orders.all()

    def __str__(self) -> str:
        return f'{self.user}'

class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Order(models.Model):
    STATUS_CHOICES = (
        ("NEW", 'Новый'),
        ("OLD", "Старый")
    )

    user = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')

    date = models.DateTimeField(auto_now_add=True, null=True)
    full_name = models.CharField(max_length=100)
    dropshipper = models.ForeignKey('Dropshipper', null=True, blank=True, on_delete=models.SET_NULL)
    product = models.ForeignKey('Product', null=True, blank=True, on_delete=models.CASCADE)
    city = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=20,  decimal_places=10)    
    status = models.CharField(max_length=9,
                  choices=STATUS_CHOICES,
                  default="NEW")
    
    # # Информация о товарах
    # # Предполагается наличие модели "Товар" с соответствующими полями
    # # Применяем ForeignKey для связи с моделью "Товар"
    # products = models.ManyToManyField('Product', through='OrderProduct')

    # # Информация о доставке
    # delivery_service = models.ForeignKey('DeliveryService', null=True, on_delete=models.SET_NULL)
    # nova_poshta_counterparty = models.ForeignKey('NovaPoshtaCounterparty', null=True, blank=True, on_delete=models.SET_NULL)
    # weight = models.DecimalField(max_digits=5, decimal_places=2)
    # package_count = models.PositiveIntegerField()
    # package_description = models.TextField()
    # recipient_city = models.CharField(max_length=100)
    # recipient_post_office = models.CharField(max_length=100)
    # delivery_cost_by_sender = models.BooleanField(default=False)
    # self_pickup = models.BooleanField(default=False)
    # courier_delivery = models.BooleanField(default=False)
    # ttn_number = models.CharField(max_length=50, blank=True)
    
    # # Информация о предоплате
    # full_prepayment = models.BooleanField(default=False)
    # cash_on_delivery = models.BooleanField(default=False)
    
    # # Прочая информация
    # note = models.TextField(blank=True)
    # photo = models.ImageField(upload_to='order_photos/', blank=True)
    # send_sms_after_ttn_added = models.BooleanField(default=False)
    # send_sms_after_dispatch = models.BooleanField(default=False)
    # send_sms_on_arrival = models.BooleanField(default=False)
    # send_sms_reminder = models.BooleanField(default=False)
    # sms_token = models.CharField(max_length=100, blank=True)
    
    # # Источник заказа
    # order_source = models.ForeignKey('OrderSource', null=True, on_delete=models.SET_NULL)
    
    # # Источник трафика
    # traffic_source = models.ForeignKey('TrafficSource', null=True, on_delete=models.SET_NULL)
    
    # # Статусы заказа
    # payment_status = models.ForeignKey('PaymentStatus', null=True, on_delete=models.SET_NULL)
    # order_status = models.ForeignKey('OrderStatus', null=True, on_delete=models.SET_NULL)
    # manual_order_status = models.BooleanField(default=False)
    
    # # Дополнительные поля
    # manual_profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # manual_advertising_costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # manual_date = models.DateField(null=True, blank=True)
    
    # # Автоматическое присвоение ID
    # order_id = models.AutoField(primary_key=True)
    
    def __str__(self):
        return f"Order {self.id}"


class DropOrder(models.Model):
    user = models.ForeignKey(Dropshipper, on_delete=models.CASCADE, related_name='orders')

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.SET_NULL)
    
