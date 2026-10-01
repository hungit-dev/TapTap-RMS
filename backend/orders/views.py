from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import PromoCode, Order , OrderItem
from .serializers import PromoCodeSerializer, OrderSerializer, OrderItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from accounts.permissions import IsManager,IsServer,IsKitchen,IsCustomer


from rest_framework.permissions import AllowAny

class PromoCodeViewSet(ModelViewSet):
    permission_classes=[IsManager]

    queryset = PromoCode.objects.all()
    serializer_class = PromoCodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['discount_type']
    search_fields = ["code"]

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ["order_type", "status"]
    search_fields =["order_number"]

    # customer can view their orders. Manager, Server, Kitchen can view all orders
    def get_queryset(self):
        user = self.request.user
        if user.role == "CUSTOMER":
            return Order.objects.filter(customer=user)
        return Order.objects.all()

    def get_permissions(self):
        if self.action == "destroy":
            return [IsManager()]
        if self.action == "create":
            return [(IsManager | IsServer | IsCustomer)()]
        if self.action in ["update", "partial_update"]:
            return [(IsManager | IsServer)()]
        return [(IsManager | IsServer | IsKitchen | IsCustomer)()]
    
    def perform_create(self, serializer):
        # if user orders online, store customer = their user id
        user = self.request.user
        if user.role == "CUSTOMER":
            serializer.save(
                customer=user,
                created_by=user
            )
        # if dine-in orders, we dont need to store the customer 
        else:
            serializer.save(
                created_by=user
            )

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.select_related(
        "order",
        "menu_item"
    )
    serializer_class = OrderItemSerializer

    def get_permissions(self):
        if self.action == "create":
            return [(IsManager | IsServer | IsCustomer)()]
        if self.action in ["update", "partial_update", "destroy"]:
            return [(IsManager | IsServer)()]
        return [(IsManager | IsServer | IsKitchen | IsCustomer)()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "CUSTOMER":
            return OrderItem.objects.filter(
                order__customer=user
            )
        return OrderItem.objects.all()

    # get the order id from url
    def perform_create(self, serializer):
        order_id = self.kwargs["order_pk"]
        order = Order.objects.get(pk=order_id)
        serializer.save(order=order)
    