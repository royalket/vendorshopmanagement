from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.apps import apps

class NearbyShopsAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        # Import inside the method to avoid loading models at module level
        from shops.models import Shop
        from shops.serializers import NearbyShopSerializer
        from haversine import haversine
        
        # Get parameters from request
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
        except (TypeError, ValueError):
            return Response(
                {"error": "Latitude and longitude must be provided as valid numbers"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get radius parameter with default value
        try:
            radius = float(request.query_params.get('radius', 5))
        except ValueError:
            radius = 5
        
        # User's location
        user_location = (latitude, longitude)
        
        # Get all shops and calculate distances
        shops = Shop.objects.all()
        nearby_shops = []
        
        for shop in shops:
            shop_location = (shop.latitude, shop.longitude)
            distance = haversine(user_location, shop_location)
            
            if distance <= radius:
                shop.distance = distance
                nearby_shops.append(shop)
        
        # Sort shops by distance
        nearby_shops.sort(key=lambda x: x.distance)
        
        # Serialize and return
        serializer = NearbyShopSerializer(nearby_shops, many=True)
        return Response(serializer.data)

# Define URL patterns separately to avoid model imports at module level
def get_urlpatterns():
    return [
        path('', NearbyShopsAPIView.as_view(), name='nearby-shops'),
    ]

urlpatterns = get_urlpatterns()