from rest_framework.routers import DefaultRouter
from .views import PromoCodeViewSet, OrderViewSet, OrderItemViewSet
from rest_framework_nested import routers


router = DefaultRouter()
# /api/orders/promo-codes/
router.register("promo-codes", PromoCodeViewSet)
# /api/orders/
router.register("", OrderViewSet)
# /api/orders/<order_id>/
orders_router = routers.NestedDefaultRouter(
    router,
    "",
    lookup="order"
)
# /api/orders/<order_id>/items/
orders_router.register(
    "items",
    OrderItemViewSet,
    basename="order-items"
)
# /api/orders/<order_id>/items/<item_id>/
urlpatterns = [
    *router.urls,
    *orders_router.urls,
]

