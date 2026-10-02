from rest_framework.routers import DefaultRouter
from .views import TableViewSet, TableSessionViewSet

router = DefaultRouter()

router.register("tables", TableViewSet)
router.register("table-sessions", TableSessionViewSet)

urlpatterns = router.urls