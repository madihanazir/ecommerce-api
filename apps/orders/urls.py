from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView

urlpatterns = [
    path("orders/", OrderListView.as_view()),
    path("orders/create/", OrderCreateView.as_view()),
    path("orders/<uuid:pk>/", OrderDetailView.as_view()),
]
