from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, CategoryViewSet, TagViewSet, BusinessViewSet, BusinessLocationViewSet, BusinessHoursViewSet, StaffViewSet, BusinessMediaViewSet, BusinessRatingViewSet, StaffRatingViewSet, TicketTypeViewSet, TicketViewSet, MessageThreadViewSet, MessageViewSet, FavoriteBusinessViewSet, NotificationViewSet, SubscriptionViewSet, NotificationPullView, NotificationPushView, AdViewSet,
    UserRegistrationView, SuperuserOnlyTokenObtainPairView, SuperuserOnlyObtainAuthToken, GenerateAPITokenView,
    ProductViewSet, ProductNegotiationViewSet, ChatRoomViewSet, ChatMessageViewSet, HomeTokenView
)
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)
router.register(r'businesses', BusinessViewSet)
router.register(r'locations', BusinessLocationViewSet)
router.register(r'business-hours', BusinessHoursViewSet)
router.register(r'staff', StaffViewSet)
router.register(r'media', BusinessMediaViewSet)
router.register(r'business-ratings', BusinessRatingViewSet)
router.register(r'staff-ratings', StaffRatingViewSet)
router.register(r'ticket-types', TicketTypeViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'message-threads', MessageThreadViewSet)
router.register(r'messages', MessageViewSet)
router.register(r'favorites', FavoriteBusinessViewSet)
router.register(r'notifications', NotificationViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'ads', AdViewSet, basename='ad')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'negotiations', ProductNegotiationViewSet, basename='negotiation')
router.register(r'chatrooms', ChatRoomViewSet, basename='chatroom')
router.register(r'messages', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', UserRegistrationView.as_view(), name='register'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('api/token/', SuperuserOnlyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/api-token-auth/', SuperuserOnlyObtainAuthToken.as_view(), name='api_token_auth'),
]

urlpatterns += [
    path('generate-api', GenerateAPITokenView.as_view(), name='generate_api'),
    path('notifications/pull/', NotificationPullView.as_view(), name='notifications-pull'),
    path('notifications/push/', NotificationPushView.as_view(), name='notifications-push'),
    path('home/', HomeTokenView.as_view(), name='home-token'),
    path('', HomeTokenView.as_view(), name='home-token'),

] 