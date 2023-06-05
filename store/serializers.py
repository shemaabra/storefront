from rest_framework import serializers
from decimal import Decimal
from .models import Product, Collection, Review, Cart, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "product_count"]

    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "description",
            "price",
            "slug",
            "inventory",
            "price_with_tax",
            "collection",
        ]

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.price * Decimal(1.1)


class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerialzer(serializers.ModelSerializer):
    """
    this is form minimizing object list from product class
    so that to display product with minimal field on cartitem
    """

    class Meta:
        model = Product
        fields = ["id", "title", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    """
    simpleproductserializer and productserializer deliver same result but
    productserializer return with many properties
    """

    # product = ProductSerializer() # if you need all properties|objects from product
    product = SimpleProductSerialzer()  # if you need some properties | objects
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item: CartItem):
        """
        cart_item: CartItem => for allow intelsense but with or without it works
        """
        return cart_item.quantity * cart_item.product.price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(
        read_only=True
    )  # make the object empty so that we can send empty object and not id with null field
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
