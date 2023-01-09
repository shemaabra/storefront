from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Count
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("collection").all()
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related("collection").all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset =  Product.objects.all()
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        if queryset.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because It is associated with order items."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(product_count=Count("product"))
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}



class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        if queryset.product_set.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because It is associated with Product."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
