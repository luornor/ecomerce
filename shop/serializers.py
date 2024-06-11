from rest_framework import serializers
from .models import Category, Region, Product, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'product', 'product_name', 'quantity']

    def get_product_name(self, obj):
        return obj.product.name


class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['stock_quantity']
