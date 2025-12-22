from apps.users.permissions import IsAdmin
from apps.cart.models import CartItem
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import Order, OrderItem
from apps.products.models import Product

from apps.products.models import Category, Product

from .serializers import OrderSerializer


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        idem_key = request.headers.get("Idempotency-Key")

        if not idem_key:
            return Response({"detail": "Idempotency-Key header required"}, status=400)

        # Return existing order if this key was used before
        existing = Order.objects.filter(idempotency_key=idem_key, user=user).first()
        if existing:
            return Response(OrderSerializer(existing).data, status=200)

        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({"detail": "Cart is empty"}, status=400)

        with transaction.atomic():
            order = Order.objects.create(user=user, idempotency_key=idem_key)
            total = 0

            for item in cart_items:
                if item.product.stock < item.quantity:
                    raise ValueError(f"Not enough stock for {item.product.name}")

                # Decrement stock
                item.product.stock -= item.quantity
                item.product.save()

                # Create order item
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                )

                total += item.product.price * item.quantity

            order.total_amount = total
            order.save()

            # Clear cart
            cart_items.delete()

        return Response(OrderSerializer(order).data, status=201)

from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # user sees only their own orders
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_staff:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Not allowed")
        return obj
