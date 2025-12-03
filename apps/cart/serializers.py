from rest_framework import serializers
from .models import CartItem
from apps.products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity", "created_at"]

    def create(self, validated_data):
        user = self.context["request"].user
        product_id = validated_data.pop("product_id")

        item, created = CartItem.objects.get_or_create(
            user=user,
            product_id=product_id,
            defaults={"quantity": validated_data.get("quantity", 1)}
        )

        if not created:
            item.quantity += validated_data.get("quantity", 1)
            item.save()

        return item
