from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    vendor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Shop
        fields = ('id', 'name', 'owner', 'business_type', 'latitude', 'longitude', 
                  'created_at', 'updated_at', 'vendor', 'vendor_name')
        read_only_fields = ('vendor', 'created_at', 'updated_at', 'vendor_name')
    
    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None
    
    def create(self, validated_data):
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)

class NearbyShopSerializer(serializers.ModelSerializer):
    distance = serializers.FloatField()
    vendor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Shop
        fields = ('id', 'name', 'owner', 'business_type', 'latitude', 'longitude', 'distance', 'vendor_name')
    
    def get_vendor_name(self, obj):
        return obj.vendor.name if obj.vendor else None