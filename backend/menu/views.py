from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from .models import MenuCategory, MenuItem
from .serializers import MenuCategorySerializer, MenuItemSerializer
from .pagination import MenuItemsResultsPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

class MenuCategoryViewSet(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]

    queryset = MenuCategory.objects.all()
    serializer_class = MenuCategorySerializer
    filter_backends=[SearchFilter]
    search_fields = ['name']

class MenuItemViewSet(ModelViewSet):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    pagination_class = MenuItemsResultsPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['category']
    search_fields = ['name', 'description']