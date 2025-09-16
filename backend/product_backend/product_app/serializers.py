from rest_framework import serializers
from .models import Products, ProductSpecification, ProductsInventory


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['id', 'product_colour', 'product_size', 'product_model_name']


class ProductsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInventory
        fields = ['id', 'stock_count']


class ProductsSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True, read_only=True)
    inventory = ProductsInventorySerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = [
            'id',
            'product_name',
            'product_price',
            'product_description',
            'product_image',
            'specifications',
            'inventory',
            'created_at',
            'updated_at',
        ]
