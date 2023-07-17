from rest_framework import serializers
from dashboards.models import Category, Order, Product, Dropshipper

class CategorySerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()

    def get_products(self, obj):
        products = obj.get_products()
        # Assuming you have a ProductSerializer defined, you can serialize the related products
        serializer = ProductSerializer(products, many=True)
        return serializer.data

    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'description', 'image', 'products']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['full_name', 'dropshipper', 'product', 'city', 'amount', 'status']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'user', 'category', 'subcategory']


class DropshipperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dropshipper
        fields = ['id', 'user']