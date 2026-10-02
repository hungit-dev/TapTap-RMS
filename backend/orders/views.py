from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import PromoCode, Order , OrderItem
from .serializers import PromoCodeSerializer, OrderSerializer, OrderItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from accounts.permissions import IsManager,IsServer,IsKitchen,IsCustomer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import status
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
        if self.action in ["start_preparing","mark_ready","serve","complete","cancel"]:
            return [(IsManager | IsKitchen | IsServer)()]
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

    # Custom actions for order status transitions
    @action(detail=True, methods=["post"],url_path="start-preparing")
    def start_preparing(self, request, pk=None):
        order = self.get_object()
        if order.status != "PLACED":
            return Response(
                {"detail": "Order must be PLACED before starting preparation."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "PREPARING"
        order.preparing_started_at = timezone.now()
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"],url_path="mark-ready")
    def mark_ready(self, request, pk=None):
        order = self.get_object()

        if order.status != "PREPARING":
            return Response(
                {"detail": "Order must be PREPARING before marking it ready."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "READY"
        order.ready_at = timezone.now()
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"],url_path="serve")
    def serve(self, request, pk=None):
        order = self.get_object()
        if order.status != "READY":
            return Response(
                {"detail": "Order must be READY before serving it."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "FOOD_SERVED"
        order.food_served_at = timezone.now()
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"],url_path="complete")
    def complete(self, request, pk=None):
        order = self.get_object()
        if order.status != "FOOD_SERVED":
            return Response(
                {"detail": "Order must be FOOD_SERVED before completing it."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "COMPLETED"
        order.completed_at = timezone.now()
        order.save()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"],url_path="cancel")
    def cancel(self, request, pk=None):
        order = self.get_object()
        if order.status in ["COMPLETED", "CANCELLED"]:
            return Response(
                {"detail": "This order cannot be cancelled."},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = "CANCELLED"
        order.cancelled_at = timezone.now()
        order.save()

        return Response(OrderSerializer(order).data)


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
    