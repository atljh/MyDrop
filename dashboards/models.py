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
    email = models.EmailField('Почта', unique=True)
    first_name = models.CharField("Имя", max_length=150)
    last_name = models.CharField("Фамилия", max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    phone_number = models.IntegerField("Номер телефона", default=False)

    is_vendor = models.BooleanField("Поставщик", default=False)
    is_dropshipper = models.BooleanField("Дропшиппер", default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

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

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи'


class Dropshipper(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.user)

    class Meta:
        verbose_name = 'Дропшиппер',
        verbose_name_plural = 'Дропшипперы'

class Vendor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name="Пользователь", on_delete=models.CASCADE, related_name='vendor')
    dropshippers = models.ManyToManyField(Dropshipper, verbose_name="Дропшипперы", blank=True, related_name='dropshippers')

    def get_orders(self):
        return self.user.vendor.orders.all()

    def get_categories(self):
        return self.user.vendor.categories.all()

    def __str__(self) -> str:
        return f'{self.user}'

    class Meta:
        verbose_name = 'Поставщик',
        verbose_name_plural = 'Поставщики'

class Order(models.Model):
    STATUS_CHOICES = (
        ("NEW", 'Новый'),
        ("OLD", "Старый")
    )

    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='orders')

    phone_number = models.CharField(verbose_name="Номер телефона", max_length=30, default='')
    date = models.DateTimeField(verbose_name="Дата", auto_now_add=True, null=True)
    full_name = models.CharField(verbose_name="Полное имя", max_length=100)
    dropshipper = models.ForeignKey('Dropshipper', verbose_name="Дропшиппер", null=True, blank=True, on_delete=models.SET_NULL)
    city = models.CharField(verbose_name="Город", max_length=255, blank=True)
    amount = models.DecimalField(verbose_name="Сумма", blank=True, null=True, max_digits=20,  decimal_places=10)    
    status = models.CharField(max_length=9, verbose_name="Статус",  
                  choices=STATUS_CHOICES,
                  default="NEW")
    
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
    
    def __str__(self):
        return f"Order {self.id}"

    class Meta:
        verbose_name = 'Заказ',
        verbose_name_plural = 'Заказы'


class DropOrder(models.Model):
    user = models.ForeignKey(Dropshipper, on_delete=models.CASCADE, related_name='orders')

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    vendor = models.ForeignKey('Vendor', null=True, blank=True, on_delete=models.SET_NULL)


class Category(models.Model):
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Название", blank=True)
    hidden_from_drop = models.BooleanField(verbose_name="Скрыт от поставщика", default=False)
    image = models.ImageField(verbose_name="Изображение", upload_to ='assets/uploads')

    def get_products(self):
        return Product.objects.filter(category=self)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'



class SubCategory(models.Model):
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, related_name='subcategories')
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(verbose_name="Название", max_length=100)
    description = models.TextField(verbose_name="Название", blank=True)
    hidden_from_drop = models.BooleanField(verbose_name="Скрыт от дропшиппера", default=False)
    image = models.ImageField(verbose_name="Изображение", upload_to='assets/uploads', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Подкатегория',
        verbose_name_plural = 'Подкатегории'



class Product(models.Model):
    name = models.CharField(verbose_name="Название", max_length=255)
    cost_price = models.DecimalField(verbose_name="Себестоимость", max_digits=10, decimal_places=2, default=0)
    drop_price = models.DecimalField("Дроп цена", max_digits=10, decimal_places=2, default=0)
    sell_price = models.DecimalField("Цена продажи", max_digits=10, decimal_places=2, default=0)
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='products')
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE, null=True)
    subcategory = models.ForeignKey(SubCategory, verbose_name="Подкатегория", on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField("Описание", blank=True)
    hidden_from_drop = models.BooleanField("Скрыт от дропшиппера", default=False)
    preorder = models.BooleanField("Предзаказ", default=False)

    image = models.ImageField("Изображение", upload_to='assets/uploads/', null=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Товар',
        verbose_name_plural = 'Товары'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    drop_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = 'Товар заказа',
        verbose_name_plural = 'Товары заказа'



class Storage(models.Model):
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='storages')
    name = models.CharField(verbose_name='Название', max_length=100)
    address = models.CharField('Адрес', max_length=200, blank=True)
    schedule = models.TextField('График работы', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

class StorageContact(models.Model):
    storage = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(verbose_name="Тип", max_length=100)
    value = models.CharField(verbose_name='Значение', max_length=100)
    description = models.CharField(verbose_name='Примечание', max_length=255, blank=True)

    def __str__(self):
        return f'{self.storage} - {self.type} {self.value}'

    class Meta:
        verbose_name = 'Контакт склада'
        verbose_name_plural = 'Контакты склада'


class Sector(models.Model):
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    storage = models.ForeignKey(Storage, verbose_name="Склад", on_delete=models.CASCADE, related_name='sectors')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Сектор"
        verbose_name_plural = "Сектора"


class Shelf(models.Model):
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    sector = models.ForeignKey(Sector, verbose_name="Сектор", on_delete=models.CASCADE, related_name='shelves')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Отделение'
        verbose_name_plural = 'Отделения'
        

class Employee(models.Model):
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='employees')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    description = models.TextField(blank=True)
    phone_number = models.CharField(max_length=200)
    storage = models.ForeignKey(Storage, on_delete=models.SET_NULL, related_name='employees', null=True)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural= "Сотрудники"


class ContactType(models.Model):
    user = models.ForeignKey(Vendor, verbose_name="Поставщик", on_delete=models.CASCADE, related_name='contacts')
    type = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.type