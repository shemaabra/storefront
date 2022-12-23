from django.contrib import admin
from .models import Collection, Product, Promotion, Customer


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "price", "inventory_status", "collection"]
    list_editable = ["price"]
    ordering = ["title"]
    list_per_page = 10

    @admin.display(ordering="inventory")
    # This decorator Function Allow Sorting Mechanism in This automated column
    def inventory_status(self, Product):
        if Product.inventory < 10:
            return "Low"
        return "Ok"


# admin.site.register(Promotion)
@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "address", "phone", "dob", "membership"]
    list_editable = ["membership"]
    ordering = ["first_name", "last_name"]
    list_per_page = 10
