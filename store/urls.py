from django.urls import path
from rest_framework.routers import SimpleRouter, DefaultRouter
from . import views

# from pprint import pprint  for printing / display data

router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)
# pprint(router.urls)


urlpatterns = router.urls
