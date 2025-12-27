from rest_framework import viewsets, permissions, filters
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from apps.users.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from apps.users.permissions import IsAdmin

class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Categories
    - Anyone can view categories
    - Only admin can create/update/delete
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.AllowAny()]

class ProductViewSet(viewsets.ModelViewSet):
    """
    same logic
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsAdmin()]
        return [permissions.AllowAny()]