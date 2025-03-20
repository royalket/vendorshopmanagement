from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('shops/', include('shops.urls')),
    path('nearby-shops/', include('api.views')),
]