"""
URL configuration for the Herkey project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from core.views import (
    EventViewSet,
    EventParticipantViewSet,
    EventAttachmentViewSet,
    UserViewSet,
    get_pre_signed_url,
    create_agora_token,
    health_check,
    CustomTokenObtainPairView
)

router = routers.DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'event-participants', EventParticipantViewSet, basename='event-participant')
router.register(r'event-attachments', EventAttachmentViewSet, basename='event-attachment')
router.register(r'users', UserViewSet, basename='user')

# Assign the router URLs to urlpatterns
urlpatterns = router.urls

# Define additional URL patterns
urlpatterns = [
    path('admin/', admin.site.urls), # Admin site
    path('api/', include(router.urls)), # API routes from the router
    path('api/event-attachments/get_pre_signed_url/', get_pre_signed_url, name='get_pre_signed_url'), # Pre-signed URL for event attachments
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # JWT token obtain pair
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# JWT token refresh
    path('api/agora-token/', create_agora_token, name='agora_token'), # Agora token creation
    path('health/', health_check, name='health_check'),# Health check endpoint
]
