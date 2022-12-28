from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from .models import Product
from .serializers import ProductSeriliarizer

# Create your views here.
@api_view()
def product_list(request):
    queryset = Product.objects.select_related("collection").all()
    serializer = ProductSeriliarizer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def product_detail(request, id):
    queryset = get_object_or_404(Product, pk=id)
    serializer = ProductSeriliarizer(queryset, many=False)
    return Response(serializer.data)