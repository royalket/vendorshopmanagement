from rest_framework import viewsets
from .models import Shop
from .serializers import ShopSerializer
from rest_framework.permissions import IsAuthenticated

class ShopViewSet(viewsets.ModelViewSet):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if this is a Swagger schema generation request
        if getattr(self, 'swagger_fake_view', False):
            # Return an empty queryset during schema generation to avoid errors
            return Shop.objects.none()

        # Ensure the user is authenticated before filtering by vendor
        if self.request.user.is_authenticated:
            return Shop.objects.filter(vendor=self.request.user)
        else:
            # Return an empty queryset for unauthenticated users
            return Shop.objects.none()