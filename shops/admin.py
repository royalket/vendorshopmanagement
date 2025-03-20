from django.contrib import admin
from .models import Shop

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'business_type', 'vendor', 'latitude', 'longitude', 'created_at')
    list_filter = ('business_type', 'created_at')
    search_fields = ('name', 'owner', 'business_type')
    readonly_fields = ('created_at', 'updated_at')