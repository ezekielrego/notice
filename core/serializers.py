from rest_framework import serializers
from .models import (
    User, Category, Tag, Business, BusinessLocation, BusinessHours, Staff, BusinessMedia, BusinessRating, StaffRating, TicketType, Ticket, MessageThread, Message, FavoriteBusiness, Notification, Subscription, Ad, Product, ProductNegotiation, ChatRoom, ChatMessage
)
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    name = serializers.CharField(source='first_name', required=True)
    role = serializers.CharField(source='user_type', required=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'password', 'role')

    def create(self, validated_data):
        validated_data['first_name'] = validated_data.pop('first_name', '')
        validated_data['user_type'] = validated_data.pop('user_type', 'customer')
        user = User(
            email=validated_data['email'],
            username=validated_data['email'],
            first_name=validated_data['first_name'],
            user_type=validated_data['user_type']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'

class BusinessLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessLocation
        fields = '__all__'

class BusinessHoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessHours
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class BusinessMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessMedia
        fields = '__all__'

class BusinessRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessRating
        fields = '__all__'

class StaffRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffRating
        fields = '__all__'

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class MessageThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageThread
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class FavoriteBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteBusiness
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Notification
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductNegotiationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductNegotiation
        fields = '__all__'

class ChatRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatRoom
        fields = '__all__'

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__' 