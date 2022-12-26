from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import (
    Collection,
    Product,
    Order,
    OrderItem,
    Promotion,
    Customer,
)


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request, model_admin):
        return [("<10", "Low")]

    def queryset(self, request, queryset):
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "product_count"]

    # overide method of queryset
    @admin.display(ordering="product_count")
    def product_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html('<a href="{}">{}</a>', url, collection.product_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(product_count=Count("product"))


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "price", "inventory_status", "collection"]
    list_editable = ["price"]
    ordering = ["title"]
    list_per_page = 10
    list_select_related = ["collection"]
    search_fields = ["title", "price", "inventory_status"]
    list_filter = ["collection", "last_update", InventoryFilter]

    @admin.display(ordering="inventory")
    # This decorator Function Allow Sorting Mechanism in This automated column
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return "Low"
        return "Ok"


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "address",
        "phone",
        "dob",
        "membership",
        "order_count",
    ]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    search_fields = ["first_name__istartswith", "last_name__istartswith"]
    list_per_page = 10

    @admin.display(ordering="order_count")
    def order_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html('<a href="{}">{}</a>', url, customer.order_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_count=Count("order"))


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "placed_at", "payment_status", "customer"]
    list_per_page = 10
    list_select_related = ["customer"]
    ordering = ["placed_at"]
    list_editable = ["payment_status"]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass