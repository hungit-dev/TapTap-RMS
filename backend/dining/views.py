from rest_framework import serializers
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .models import Table, TableSession
from .serializers import TableSerializer, TableSessionSerializer
from accounts.permissions import IsManager,IsServer


class TableViewSet(ModelViewSet):
    permission_classes = [IsManager | IsServer ]
    
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    # custom view to set the table status to "OCCUPIED" or "AVAILABLE"
    @action(detail=True, methods=["post"], url_path="set-occupied")
    def set_occupied(self, request, pk=None):
        table = self.get_object()
        if table.status == "OCCUPIED":
            return Response(
                {"detail": "Table is already occupied."},
                status=status.HTTP_400_BAD_REQUEST
            )
        table.status = "OCCUPIED"
        table.save()
        return Response(TableSerializer(table).data)

    @action(detail=True, methods=["post"], url_path="set-available")
    def set_available(self, request, pk=None):
        table = self.get_object()
        if table.status == "AVAILABLE":
            return Response(
                {"detail": "Table is already available."},
                status=status.HTTP_400_BAD_REQUEST
            )
        table.status = "AVAILABLE"
        table.save()
        return Response(TableSerializer(table).data)


class TableSessionViewSet(ModelViewSet):
    queryset = TableSession.objects.all()
    serializer_class = TableSessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["table", "staff"]

    def get_permissions(self):
        if self.action in ["destroy"]:
            return [IsManager()]
        return [(IsManager | IsServer)()]
    
    def perform_create(self, serializer):
        serializer.save(staff=self.request.user)

    # custom view to close the table session and set the closed_at field to the current time
    @action(detail=True, methods=["post"], url_path="close")
    def close(self, request, pk=None):
        session = self.get_object()
        if session.closed_at is not None:
            return Response(
                {"detail": "This table session is already closed."},
                status=status.HTTP_400_BAD_REQUEST
            )
        session.closed_at = timezone.now()
        session.save()
        return Response(
            TableSessionSerializer(session).data,
            status=status.HTTP_200_OK
        )