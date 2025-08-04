from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('business', 'Business Owner'),
        ('staff', 'Business Staff'),
        ('customer', 'Customer'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer', db_index=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True, null=True)
    notification_preferences = models.JSONField(default=dict)
    last_seen = models.DateTimeField(blank=True, null=True, help_text="Last time the user was active.")
    last_login_ip = models.CharField(max_length=45, blank=True, null=True, help_text="Last login IP address.")
    
    region = models.CharField(max_length=100, blank=True, null=True)
    wallet_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    kyc_verified = models.BooleanField(default=False)
    kyc_verified_at = models.DateTimeField(blank=True, null=True)
    training_points = models.IntegerField(default=0)
    
    def __str__(self):
        return getattr(self, 'username', super().__str__())

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='children')
    color = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color for UI.")
    featured = models.BooleanField(help_text="Is this a featured category?", blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, blank=True, null=True, help_text="Hex color for UI.")
    featured = models.BooleanField(help_text="Is this a featured tag?", blank=True, null=True)
    
    def __str__(self):
        return self.name

class Business(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('pending', 'Pending Verification'),
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_businesses')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True, help_text="SEO-friendly URL.")
    description = models.TextField()
    logo = models.ImageField(upload_to='business_logos/')
    cover_image = models.ImageField(upload_to='business_covers/', blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name='businesses')
    tags = models.ManyToManyField(Tag, blank=True, related_name='businesses')
    established_date = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(db_index=True)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', db_index=True)
    # location = models.PointField(blank=True, null=True)  # Uncomment if using GeoDjango
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Businesses"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class BusinessLocation(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='locations')
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{getattr(self.business, 'name', str(self.business))} - {getattr(self, 'city', '')}, {getattr(self, 'country', '')}"

class BusinessHours(models.Model):
    DAY_CHOICES = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='business_hours')
    day = models.IntegerField(choices=DAY_CHOICES)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    is_closed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('business', 'day')
        ordering = ['day']
    
    def __str__(self):
        return f"{getattr(self.business, 'name', str(self.business))} - {self.get_day_display()}"  # type: ignore

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='staff_members')
    position = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(default=timezone.now)
    permissions = models.JSONField(default=dict)  # Store staff permissions
    
    class Meta:
        verbose_name_plural = "Staff"
        ordering = ['-joined_date']
    
    def __str__(self):
        return f"{getattr(self.user, 'get_full_name', lambda: str(self.user))()} - {getattr(self.business, 'name', str(self.business))}"  # type: ignore

class BusinessMedia(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=5, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='business_media/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-created_at']
    
    def __str__(self):
        return f"{getattr(self.business, 'name', str(self.business))} - {getattr(self, 'media_type', '')}"

class BusinessRating(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True, null=True)
    reply = models.TextField(blank=True, null=True, help_text="Business owner's reply to the review.")
    helpful_count = models.PositiveIntegerField(help_text="Number of users who found this review helpful.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('business', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{getattr(self.user, 'username', str(self.user))} rated {getattr(self.business, 'name', str(self.business))} {getattr(self, 'rating', '')} stars"

class StaffRating(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='given_staff_ratings')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('staff', 'user')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{getattr(self.user, 'username', str(self.user))} rated {getattr(getattr(self.staff, 'user', None), 'username', str(self.staff))} {getattr(self, 'rating', '')} stars"

class TicketType(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity_available = models.PositiveIntegerField()
    start_sale_date = models.DateTimeField()
    end_sale_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{getattr(self, 'name', '')} - {getattr(self.business, 'name', str(self.business))}"

class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='tickets')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_tickets')
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, blank=True, null=True, related_name='assigned_tickets')
    purchase_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='valid', choices=(
        ('valid', 'Valid'),
        ('used', 'Used'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ))
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='ticket_qrcodes/', blank=True, null=True)
    used_at = models.DateTimeField(blank=True, null=True, help_text="When the ticket was used.")
    barcode = models.CharField(max_length=100, blank=True, null=True, help_text="Barcode for physical scanning.")
    
    def __str__(self):
        return f"Ticket #{getattr(self, 'id', '')} - {getattr(getattr(self, 'ticket_type', None), 'name', str(getattr(self, 'ticket_type', '')))}"

class MessageThread(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.subject or f"Thread {getattr(self, 'id', '')}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='messages', blank=True, null=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='message_attachments/', blank=True, null=True)
    thread = models.ForeignKey(MessageThread, on_delete=models.SET_NULL, blank=True, null=True, related_name='messages')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Message from {getattr(self.sender, 'username', str(self.sender))} to {getattr(self.recipient, 'username', str(self.recipient))}"

class FavoriteBusiness(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_businesses')
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'business')
    
    def __str__(self):
        return f"{getattr(self.user, 'username', str(self.user))} likes {getattr(self.business, 'name', str(self.business))}"

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('new_listing', 'New Listing'),
        ('message', 'Message'),
        ('rating', 'Rating'),
        ('ticket', 'Ticket Update'),
        ('system', 'System Notification'),
    )
    
    users = models.ManyToManyField(User, related_name='notifications')
    is_active = models.BooleanField(default=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_id = models.PositiveIntegerField(blank=True, null=True)  # ID of related object
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(auto_now_add=True, help_text="When the notification was sent.")
    read_at = models.DateTimeField(blank=True, null=True, help_text="When the notification was read.")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{getattr(self.notification_type, '__str__', lambda: str(self.notification_type))()} notification for {getattr(self.user, 'username', str(self.user))}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscribers', blank=True, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='subscribers', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'category', 'business')
    
    def __str__(self):
        if self.category:
            return f"{getattr(self.user, 'username', str(self.user))} subscribed to {getattr(self.category, 'name', str(self.category))}"
        elif self.business:
            return f"{getattr(self.user, 'username', str(self.user))} subscribed to {getattr(self.business, 'name', str(self.business))}"
        else:
            return f"{getattr(self.user, 'username', str(self.user))} subscription"

class Ad(models.Model):
    AD_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    button = models.CharField(max_length=100, blank=True, null=True)
    media = models.URLField()
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()
    unit = models.CharField(max_length=50)
    harvest_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50, blank=True, null=True)
    is_organic = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    type = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    video = models.FileField(upload_to='product_videos/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    is_opportunity = models.BooleanField(default=False)
    sold_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProductNegotiation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='negotiations')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='negotiations')
    proposed_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Negotiation for {self.product.name} by {self.buyer.email}"

class ChatRoom(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message in {self.room.name} by {self.sender.email}"

# Signals
@receiver(post_save, sender=Business)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:
        # Get all users subscribed to the business's categories
        subscriptions = Subscription.objects.filter(category__in=instance.categories.all())
        
        for subscription in subscriptions:
            # Create notification
            Notification.objects.create(
                user=subscription.user,
                notification_type='new_listing',
                title=f"New Business Listing: {instance.name}",
                message=f"A new business {instance.name} has been listed in {(subscription.category.name if subscription.category else 'a category')} category.",
                related_id=instance.id
            )
            
            # Send email if user has email notifications enabled
            if subscription.user.notification_preferences.get('email', False):
                category_name = subscription.category.name if subscription.category else "a category"
                subject = f"New Business Listing in {category_name}"
                html_message = render_to_string('emails/new_listing.html', {
                    'business': instance,
                    'category': subscription.category,
                    'user': subscription.user
                })
                plain_message = strip_tags(html_message)
                send_mail(
                    subject,
                    plain_message,
                    settings.DEFAULT_FROM_EMAIL,
                    [subscription.user.email],
                    html_message=html_message,
                    fail_silently=True
                )