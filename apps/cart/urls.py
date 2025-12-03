from django.urls import path
from .views import (
    CartListView,
    CartItemCreateView,
    CartItemUpdateDeleteView,
)

urlpatterns = [
    path("cart/items/", CartListView.as_view(), name="cart-list"),         # GET
    path("cart/items/add/", CartItemCreateView.as_view(), name="cart-add"), # POST
    path("cart/items/<uuid:pk>/", CartItemUpdateDeleteView.as_view(), name="cart-update-delete"),  # GET/PUT/DELETE
]
