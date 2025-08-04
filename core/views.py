from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Category, Tag, Business, BusinessLocation, BusinessHours, Staff, BusinessMedia, BusinessRating, StaffRating, TicketType, Ticket, MessageThread, Message, FavoriteBusiness, Notification, Subscription, Ad
)
from .serializers import (
    UserSerializer, CategorySerializer, TagSerializer, BusinessSerializer, BusinessLocationSerializer, BusinessHoursSerializer, StaffSerializer, BusinessMediaSerializer, BusinessRatingSerializer, StaffRatingSerializer, TicketTypeSerializer, TicketSerializer, MessageThreadSerializer, MessageSerializer, FavoriteBusinessSerializer, NotificationSerializer, SubscriptionSerializer, AdSerializer
)
from django.views.generic import TemplateView
from rest_framework import generics
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import mixins
from .serializers import ProductSerializer, ProductNegotiationSerializer, ChatRoomSerializer, ChatMessageSerializer
from .models import Product, ProductNegotiation, ChatRoom, ChatMessage
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.shortcuts import redirect

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

class BusinessLocationViewSet(viewsets.ModelViewSet):
    queryset = BusinessLocation.objects.all()
    serializer_class = BusinessLocationSerializer

class BusinessHoursViewSet(viewsets.ModelViewSet):
    queryset = BusinessHours.objects.all()
    serializer_class = BusinessHoursSerializer

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

class BusinessMediaViewSet(viewsets.ModelViewSet):
    queryset = BusinessMedia.objects.all()
    serializer_class = BusinessMediaSerializer

class BusinessRatingViewSet(viewsets.ModelViewSet):
    queryset = BusinessRating.objects.all()
    serializer_class = BusinessRatingSerializer

class StaffRatingViewSet(viewsets.ModelViewSet):
    queryset = StaffRating.objects.all()
    serializer_class = StaffRatingSerializer

class TicketTypeViewSet(viewsets.ModelViewSet):
    queryset = TicketType.objects.all()
    serializer_class = TicketTypeSerializer

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class MessageThreadViewSet(viewsets.ModelViewSet):
    queryset = MessageThread.objects.all()
    serializer_class = MessageThreadSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class FavoriteBusinessViewSet(viewsets.ModelViewSet):
    queryset = FavoriteBusiness.objects.all()
    serializer_class = FavoriteBusinessSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

class NotificationPullView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notifications = Notification.objects.filter(users=request.user, is_active=True)
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

class NotificationPushView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        notification_id = request.data.get('notification_id')
        notification = get_object_or_404(Notification, id=notification_id)
        notification.users.add(request.user)
        return Response({'status': 'Notification pushed to user'})

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

class GenerateAPITokenView(TemplateView):
    template_name = 'generate_api.html'

SUPERUSER_ERROR_MESSAGE = {
    'detail': 'Token generation is restricted. Only admin (superuser) accounts can generate API tokens. Please contact your administrator if you need access.'
}

class SuperuserOnlyObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_superuser:
            return Response(SUPERUSER_ERROR_MESSAGE, status=status.HTTP_403_FORBIDDEN)
        return super().post(request, *args, **kwargs)

class SuperuserOnlyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.user
        except Exception:
            user = None
        if response.status_code == 200 and user and not user.is_superuser:
            return Response(SUPERUSER_ERROR_MESSAGE, status=status.HTTP_403_FORBIDDEN)
        return response

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class AdViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Ad.objects.filter(is_active=True)
    serializer_class = AdSerializer
    permission_classes = []

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductNegotiationViewSet(viewsets.ModelViewSet):
    queryset = ProductNegotiation.objects.all()
    serializer_class = ProductNegotiationSerializer

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        negotiation = self.get_object()
        negotiation.status = 'accepted'
        negotiation.save()
        return Response({'status': 'Negotiation accepted'})

    @action(detail=True, methods=['post'])
    def decline(self, request, pk=None):
        negotiation = self.get_object()
        negotiation.status = 'declined'
        negotiation.save()
        return Response({'status': 'Negotiation declined'})

class ChatRoomViewSet(viewsets.ModelViewSet):
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomSerializer

class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class HomeTokenView(TemplateView):
    template_name = 'home_token.html'

    def get(self, request, *args, **kwargs):
        token, created = Token.objects.get_or_create(user=request.user)
        return render(request, self.template_name, {'token': token.key, 'user': request.user})
