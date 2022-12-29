from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection
from .serializers import ProductSeriliarizer, CollectionSerializer

# Create your views here.
@api_view(["GET", "POST"])
def product_list(request):
    if request.method == "GET":
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSeriliarizer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ProductSeriliarizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_detail(request, pk):
    queryset = get_object_or_404(Product, pk=pk)
    if request.method == "GET":
        serializer = ProductSeriliarizer(queryset, many=False)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = ProductSeriliarizer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        if queryset.orderitems.count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because It is associated with order items."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def collection_list(request):
    if request.method == "GET":
        queryset = Collection.objects.all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail(request, pk):
    queryset = get_object_or_404(Collection, pk=pk)
    if request.method == "GET":
        serializer = CollectionSerializer(queryset, many=False)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CollectionSerializer(queryset, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        if queryset.product_set.count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because It is associated with Product."
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
