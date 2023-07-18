from django import forms
from dashboards.models import Order, OrderProduct, Product, Category, SubCategory


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
    image = forms.ImageField(required=False)  # Make the image field optional

    class Meta:
        model = Category
        fields = ['name', 'description', 'hidden_from_drop', 'image']

    

class SubCategoryForm(forms.ModelForm):
    image = forms.ImageField(required=False)

    class Meta:
        model = SubCategory
        fields = ['name', 'description', 'hidden_from_drop', 'image']