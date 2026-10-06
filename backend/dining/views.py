from rest_framework import serializers
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction
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



class TableSessionViewSet(ModelViewSet):
    permission_classes = [IsManager | IsServer]

    queryset = TableSession.objects.all()
    serializer_class = TableSessionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["table", "staff"]

    # client should not be able to delete table sessions, as this would cause data integrity issues. Instead, they should use the close action to close the session and set the closed_at field to the current time.
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "Table sessions cannot be deleted."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def perform_create(self, serializer):
        table = serializer.validated_data["table"]
        if table.status == "OCCUPIED":
            raise serializers.ValidationError(
                {"table": "This table is already occupied."}
            )
        
        with transaction.atomic():
            session = serializer.save(
                staff=self.request.user
            )
            table = session.table
            table.status = "OCCUPIED"
            table.save()

    # custom view to close the table session and set the closed_at field to the current time -> set status of table to available
    @action(detail=True, methods=["post"], url_path="close")
    def close(self, request, pk=None):
        with transaction.atomic():
            session = self.get_object()
            if session.closed_at is not None:
                return Response(
                    {"detail": "This table session is already closed."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            session.closed_at = timezone.now()
            session.save()
            table = session.table
            table.status = "AVAILABLE"
            table.save()

        return Response(
            TableSessionSerializer(session).data,
            status=status.HTTP_200_OK
        )