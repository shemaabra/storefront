from django.urls import path
from rest_framework_nested import routers
from . import views

# from pprint import pprint  for printing / display data

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

# pprint(router.urls)


urlpatterns = router.urls + product_router.urls
