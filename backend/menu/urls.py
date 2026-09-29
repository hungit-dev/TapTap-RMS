from rest_framework.routers import DefaultRouter
from .views import MenuCategoryViewSet, MenuItemViewSet

router = DefaultRouter()

router.register(r'menu-categories', MenuCategoryViewSet)
router.register(r'menu-items', MenuItemViewSet)

urlpatterns = router.urls