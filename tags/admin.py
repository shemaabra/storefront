from django.contrib import admin
from .models import TaggedItem, Tag

# Register your models here.


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ["label"]
