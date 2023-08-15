from django import forms
from dashboards.models import Order, OrderProduct, Product, Category, SubCategory, Employee, Storage, Sector, Shelf, StorageContact, ContactType
import json

class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity', 'cost_price', 'drop_price', 'sell_price']
        widgets = {
            'drop_price': forms.NumberInput(attrs={'step': '0.01'}),
            'sell_price': forms.NumberInput(attrs={'step': '0.01'}),
        }
        labels = {
            'drop_price': 'Drop Price',
            'cost_price': 'Sell Price',
        }

    drop_price = forms.DecimalField(required=False)
    cost_price = forms.DecimalField(required=False)



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone_number', 'city']


class CategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Category
        fields = ['name', 'description', 'hidden_from_drop', 'image']

    

class SubCategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = SubCategory
        fields = ['name', 'description', 'hidden_from_drop', 'image']

    

class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = ['name', 'description', 'hidden_from_drop', 'image', 'category', 'sell_price', 'subcategory']


class EmployeeForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = Employee
        fields = ['name', 'phone_number', 'description', 'image', 'storage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['storage'].required = False


class StorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['name', 'address', 'schedule']

    contact_options = forms.CharField(widget=forms.HiddenInput(), required=False)

    def save_contact_options(self, storage):
        contact_options_data = self.cleaned_data.get('contact_options', '')
        if not contact_options_data:
            return
        data = json.loads(contact_options_data)
        if contact_options_data:
            for option_data in data:
                StorageContact.objects.create(storage=storage, **option_data)
    
    def save_employees(self, employees, storage):
        for employee_id in employees:
            employee = Employee.objects.get(id=employee_id)
            employee.storage = storage
            employee.save()

    def save(self, commit=True):
        instance = super().save(commit=False)  
        if commit:
            instance.save() 
            self.save_contact_options(instance)
        return instance


class StorageContactForm(forms.ModelForm):
    class Meta:
        model = StorageContact
        fields = ['type', 'value', 'description']


class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ['name']


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ['name']


class ContactTypeForm(forms.ModelForm):
    class Meta:
        model = ContactType
        fields = ['type', 'value']
    
    def __init__(self, user=None, *args, **kwargs):
        super(ContactTypeForm, self).__init__(*args, **kwargs)
        self.fields['type'].widget.attrs['class'] = 'form-select'
        self.fields['value'].widget.attrs['class'] = 'form-control'
        
        if user:
            self.instance.user = user