from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Table, TableSession
from .serializers import TableSerializer, TableSessionSerializer


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TableSessionViewSet(ModelViewSet):
    queryset = TableSession.objects.all()
    serializer_class = TableSessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["table", "staff"]