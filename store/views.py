from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from rest_framework.views import APIView
from .models import Product, Collection
from .serializers import ProductSerializer, CollectionSerializer


class ProductList(APIView):
    def get(self, request):
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductDetail(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(queryset, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        queryset = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(queryset, data=request.data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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


class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(product_count=Count("product"))
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CollectionDetail(APIView):
    def get(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(queryset, many=False)
        return Response(serializer.data)
    
    def put(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        serializer = CollectionSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        queryset = get_object_or_404(Collection, pk=pk)
        if queryset.product_set.count() > 0:
            return Response({"error": "Collection cannot be deleted because It is associated with Product."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(["GET", "PUT", "DELETE"])
# def collection_detail(request, pk):
#     queryset = get_object_or_404(Collection, pk=pk)
#     if request.method == "GET":
#         serializer = CollectionSerializer(queryset, many=False)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = CollectionSerializer(queryset, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     elif request.method == "DELETE":
#         if queryset.product_set.count() > 0:
#             return Response(
#                 {
#                     "error": "Collection cannot be deleted because It is associated with Product."
#                 },
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
