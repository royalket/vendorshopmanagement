from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Shop
from .serializers import ShopSerializer

class IsVendorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the vendor who owns the shop
        return obj.vendor == request.user

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOrReadOnly]

    def get_queryset(self):
        return Shop.objects.filter(vendor=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(vendor=self.request.user)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.vendor != request.user:
            raise PermissionDenied("You do not have permission to update this shop.")
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.vendor != request.user:
            raise PermissionDenied("You do not have permission to delete this shop.")
        return super().destroy(request, *args, **kwargs)