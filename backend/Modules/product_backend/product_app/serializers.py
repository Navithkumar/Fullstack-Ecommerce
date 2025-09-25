import json
from rest_framework import serializers
from .models import Products, ProductSpecification, ProductInventory

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ['product_colour', 'product_size', 'product_model_name']


class ProductsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ['product_stock_count']


class ProductsSerializer(serializers.ModelSerializer):
    specifications = ProductSpecificationSerializer(many=True, required=False)
    inventory = ProductsInventorySerializer(many=True, required=False)

    class Meta:
        model = Products
        fields = [
            'id', 'product_name', 'product_price', 'product_description',
            'product_image', 'category_id', 'specifications', 'inventory',
            'created_at', 'updated_at'
        ]

    def to_internal_value(self, data):
        """Convert form-data JSON strings into Python objects"""
        data = data.copy()

        if 'specifications' in data and isinstance(data.get('specifications'), str):
            try:
                data['specifications'] = json.loads(data['specifications'])
            except json.JSONDecodeError:
                raise serializers.ValidationError({"specifications": "Invalid JSON"})

        if 'inventory' in data and isinstance(data.get('inventory'), str):
            try:
                data['inventory'] = json.loads(data['inventory'])
            except json.JSONDecodeError:
                raise serializers.ValidationError({"inventory": "Invalid JSON"})

        return super().to_internal_value(data)

    def create(self, validated_data):
        

        specs_data = validated_data.pop('specifications', [])
        inventory_data = validated_data.pop('inventory', [])
        product = Products.objects.create(**validated_data)

      

        for spec in specs_data:
            ProductSpecification.objects.create(product=product, **spec)

        for inv in inventory_data:
            ProductInventory.objects.create(product=product, **inv)

        return product
