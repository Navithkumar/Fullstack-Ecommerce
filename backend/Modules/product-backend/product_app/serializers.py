import json
from rest_framework import serializers
from .models import Products, ProductSpecification, ProductInventory


class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ["product_colour", "product_size", "product_model_name"]


class ProductsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = ["product_stock_count"]


class ProductsSerializer(serializers.ModelSerializer):
    specifications = serializers.CharField(write_only=True, required=False)
    inventory = serializers.CharField(write_only=True, required=False)

    specifications_data = serializers.SerializerMethodField()
    inventory_data = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = [
            "id",
            "product_name",
            "product_price",
            "product_description",
            "product_image",
            "category_id",
            "specifications",
            "inventory",
            "specifications_data",
            "inventory_data",
            "created_at",
            "updated_at",
        ]

    def get_specifications_data(self, obj):
        return ProductSpecificationSerializer(obj.specifications.all(), many=True).data

    def get_inventory_data(self, obj):
        return ProductsInventorySerializer(obj.inventory.all(), many=True).data

    def create(self, validated_data):
        specs_raw = validated_data.pop("specifications", "[]")
        inventory_raw = validated_data.pop("inventory", "[]")

        try:
            specs_data = json.loads(specs_raw) if specs_raw else []
        except Exception:
            raise serializers.ValidationError({"specifications": "Invalid JSON"})

        try:
            inventory_data = json.loads(inventory_raw) if inventory_raw else []
        except Exception:
            raise serializers.ValidationError({"inventory": "Invalid JSON"})

        product = Products.objects.create(**validated_data)

        for spec in specs_data:
            ProductSpecification.objects.create(product=product, **spec)

        for inv in inventory_data:
            ProductInventory.objects.create(product=product, **inv)

        return product

    def update(self, instance, validated_data):
        specs_raw = validated_data.pop("specifications", None)
        inventory_raw = validated_data.pop("inventory", None)

        # Update basic product fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update specifications if provided
        if specs_raw is not None:
            try:
                specs_data = json.loads(specs_raw) if specs_raw else []
            except Exception:
                raise serializers.ValidationError({"specifications": "Invalid JSON"})

            instance.specifications.all().delete()  # clear old
            for spec in specs_data:
                ProductSpecification.objects.create(product=instance, **spec)

        # Update inventory if provided
        if inventory_raw is not None:
            try:
                inventory_data = json.loads(inventory_raw) if inventory_raw else []
            except Exception:
                raise serializers.ValidationError({"inventory": "Invalid JSON"})

            instance.inventory.all().delete()  # clear old
            for inv in inventory_data:
                ProductInventory.objects.create(product=instance, **inv)

        return instance
