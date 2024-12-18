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


urlpatterns = router.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/event-attachments/get_pre_signed_url/', get_pre_signed_url, name='get_pre_signed_url'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/agora-token/', create_agora_token, name='agora_token'),
    path('health/', health_check, name='health_check'),
]
