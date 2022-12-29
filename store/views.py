from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .serializers import ProductSeriliarizer

# Create your views here.
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSeriliarizer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSeriliarizer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 


@api_view()
def product_detail(request, id):
    queryset = get_object_or_404(Product, pk=id)
    serializer = ProductSeriliarizer(queryset, many=False)
    return Response(serializer.data)