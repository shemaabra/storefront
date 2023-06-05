from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from .filters import ProductFilter
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework import status
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import (
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializers,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer
)
from rest_framework.filters import SearchFilter, OrderingFilter

# from rest_framework.pagination import PageNumberPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["collection_id"]
    filterset_class = ProductFilter
    # pagination_class = PageNumberPagination # if you decide to use pagenation class
    search_fields = ["title", "description"]
    ordering_fields = ["price", "last_update"]

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product__id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because It is associated with order items."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(product_count=Count("product"))
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection__id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because It is associated with Product."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializers

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):  # Here We use Custome View Set
    queryset = Cart.objects.prefetch_related("items__product").all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_pk"]).select_related(
            "product"
        )
