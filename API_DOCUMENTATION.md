# Noticeboard API Documentation

## 🚀 Quick Start Guide

Welcome to the **Noticeboard API** - a comprehensive business directory and marketplace platform! This guide will help you get started quickly, whether you're a frontend developer, mobile app developer, or building integrations.

### 📋 What This API Does

The Noticeboard API is a complete platform that combines:
- **🏢 Business Directory**: Companies can list their businesses with detailed profiles
- **🛍️ Marketplace**: Users can buy/sell products with price negotiation
- **💬 Real-time Messaging**: Chat system for user communication  
- **🎫 Event Ticketing**: Businesses can create and sell event tickets
- **📱 Notifications**: Push/pull notification system
- **👤 User Management**: Multi-role user system with authentication

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Basic knowledge of REST APIs
- A tool for API testing (Postman, cURL, or similar)

### 1. Clone and Setup (For Development)
```bash
# Clone the repository
git clone <repository-url>
cd noticeboard-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (admin account)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### 2. Access Points
- **API Base URL**: `http://127.0.0.1:8000/api/`
- **Token Generator**: `http://127.0.0.1:8000/generate-api`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`

---

## 🔐 Authentication Guide

### Overview
The API supports **two authentication methods**:
1. **JWT Tokens** (Recommended for web/mobile apps)
2. **Permanent API Tokens** (For integrations and scripts)

### Method 1: JWT Authentication (Recommended)

#### Step 1: Register a New User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "customer"
  }'
```

**Response:**
```json
{
  "id": 2,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "customer"
}
```

#### Step 2: Login to Get JWT Tokens
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john@example.com",
    "password": "securepassword123"
  }'
```

**⚠️ Important**: Use `username` field with your email address, not `email` field.

**Response:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Step 3: Use JWT Token in Requests
```bash
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/products/
```

#### Token Refresh (When Access Token Expires)
```bash
curl -X POST http://127.0.0.1:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### Method 2: Permanent API Tokens

#### Option A: Use the Web Interface
1. Visit: `http://127.0.0.1:8000/generate-api`
2. Enter your username (email) and password
3. Copy the generated tokens

#### Option B: Generate via API (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/api/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@example.com",
    "password": "adminpassword"
  }'
```

**Use Permanent Token:**
```bash
curl -H "Authorization: Token YOUR_PERMANENT_TOKEN" \
  http://127.0.0.1:8000/api/products/
```

---

## 📚 API Endpoints Reference

### 👤 User Management

#### Register New User
- **Endpoint**: `POST /api/register/`
- **Authentication**: None required
- **Request Body**:
```json
{
  "name": "Full Name",
  "email": "user@example.com",
  "password": "securepassword123",
  "role": "customer"
}
```
- **Available Roles**: `customer`, `business`, `staff`
- **Response**: User object with ID

#### Login (Get JWT Tokens)
- **Endpoint**: `POST /api/login/`
- **Authentication**: None required
- **Request Body**:
```json
{
  "username": "user@example.com",
  "password": "securepassword123"
}
```
- **Response**: JWT access and refresh tokens

#### User CRUD Operations
- `GET /api/users/` - List all users
- `POST /api/users/` - Create user (admin only)
- `GET /api/users/{id}/` - Get specific user
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

**User Model Fields:**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "user_type": "customer",
  "phone_number": "+1234567890",
  "profile_picture": "profile_pics/user.jpg",
  "email_verified": false,
  "kyc_verified": false,
  "wallet_balance": "0.00",
  "training_points": 0,
  "region": "North America",
  "location": "New York, NY",
  "notification_preferences": {},
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### 🏢 Business Management

#### Business Endpoints
- `GET /api/businesses/` - List businesses
- `POST /api/businesses/` - Create business
- `GET /api/businesses/{id}/` - Get business details
- `PUT /api/businesses/{id}/` - Update business
- `DELETE /api/businesses/{id}/` - Delete business

**Business Model Fields:**
```json
{
  "id": 1,
  "owner": 2,
  "name": "Tech Solutions Inc",
  "slug": "tech-solutions-inc",
  "description": "We provide innovative tech solutions",
  "logo": "business_logos/logo.jpg",
  "cover_image": "business_covers/cover.jpg",
  "categories": [1, 2],
  "tags": [1, 3, 5],
  "established_date": "2020-01-01",
  "website": "https://techsolutions.com",
  "phone": "+1234567890",
  "email": "info@techsolutions.com",
  "views": 150,
  "likes": 25,
  "is_verified": true,
  "status": "active",
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Categories & Tags
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category
- `GET /api/tags/` - List tags
- `POST /api/tags/` - Create tag

### 🛍️ Product & Marketplace

#### Product Management
- `GET /api/products/` - List products
- `POST /api/products/` - Create product
- `GET /api/products/{id}/` - Get product details
- `PUT /api/products/{id}/` - Update product
- `DELETE /api/products/{id}/` - Delete product

**Create Product Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": 1,
    "name": "Fresh Organic Apples",
    "description": "Premium quality organic apples from local farm",
    "price": "5.99",
    "quantity": 100,
    "unit": "kg",
    "harvest_date": "2024-01-10",
    "is_organic": true,
    "location": "California, USA",
    "type": "fruit"
  }'
```

#### Price Negotiations
- `GET /api/negotiations/` - List negotiations
- `POST /api/negotiations/` - Propose price
- `GET /api/negotiations/{id}/` - Get negotiation details
- `POST /api/negotiations/{id}/accept/` - Accept offer
- `POST /api/negotiations/{id}/decline/` - Decline offer

**Negotiate Price Example:**
```bash
curl -X POST http://127.0.0.1:8000/api/negotiations/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "buyer": 2,
    "proposed_price": "4.50"
  }'
```

### 💬 Chat & Messaging

#### Chat Rooms
- `GET /api/chatrooms/` - List chat rooms
- `POST /api/chatrooms/` - Create chat room
- `GET /api/chatrooms/{id}/` - Get chat room details

**Create Chat Room:**
```bash
curl -X POST http://127.0.0.1:8000/api/chatrooms/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Discussion",
    "users": [1, 2, 3]
  }'
```

#### Messages
- `GET /api/messages/` - List messages
- `POST /api/messages/` - Send message
- `GET /api/messages/{id}/` - Get message details

**Send Message:**
```bash
curl -X POST http://127.0.0.1:8000/api/messages/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "room": 1,
    "sender": 2,
    "content": "Hi! I'm interested in your organic apples. Can we negotiate the price?"
  }'
```

### 📱 Notifications

#### Pull Notifications (Get Your Notifications)
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://127.0.0.1:8000/notifications/pull/
```

#### Push Notification (Admin Only)
```bash
curl -X POST http://127.0.0.1:8000/notifications/push/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"notification_id": 1}'
```

#### Notification Management (Admin)
- `GET /api/notifications/` - List all notifications
- `POST /api/notifications/` - Create notification

### 🎫 Ticketing System

#### Ticket Types
- `GET /api/ticket-types/` - List ticket types
- `POST /api/ticket-types/` - Create ticket type

#### Tickets
- `GET /api/tickets/` - List tickets
- `POST /api/tickets/` - Purchase ticket
- `GET /api/tickets/{id}/` - Get ticket details

### 📢 Advertisements

#### Get Active Ads (No Authentication Required)
```bash
curl http://127.0.0.1:8000/api/ads/
```

---

## 🔧 Advanced Usage Examples

### Complete Workflow: User Registration to Product Purchase

#### 1. Register as a Customer
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "password": "alicepassword123",
    "role": "customer"
  }'
```

#### 2. Register as a Business Owner
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "bob@farmfresh.com",
    "password": "bobpassword123",
    "role": "business"
  }'
```

#### 3. Business Owner Login and Create Business
```bash
# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "bob@farmfresh.com", "password": "bobpassword123"}' \
  | jq -r '.access')

# Create Business
curl -X POST http://127.0.0.1:8000/api/businesses/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Farm Fresh Produce",
    "description": "Organic fruits and vegetables direct from farm",
    "phone": "+1555123456",
    "email": "info@farmfresh.com",
    "website": "https://farmfresh.com"
  }'
```

#### 4. Add Products
```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": 1,
    "name": "Organic Tomatoes",
    "description": "Fresh organic tomatoes, perfect for salads",
    "price": "3.99",
    "quantity": 50,
    "unit": "kg",
    "is_organic": true,
    "location": "California Farm"
  }'
```

#### 5. Customer Browse and Negotiate
```bash
# Customer login
CUSTOMER_TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice@example.com", "password": "alicepassword123"}' \
  | jq -r '.access')

# Browse products
curl -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  http://127.0.0.1:8000/api/products/

# Negotiate price
curl -X POST http://127.0.0.1:8000/api/negotiations/ \
  -H "Authorization: Bearer $CUSTOMER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "buyer": 1,
    "proposed_price": "3.50"
  }'
```

### File Upload Example

For endpoints that accept file uploads (profile pictures, business logos, product images):

```bash
curl -X POST http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "name=Premium Coffee Beans" \
  -F "description=Freshly roasted coffee beans" \
  -F "price=15.99" \
  -F "quantity=20" \
  -F "unit=bags" \
  -F "category=1" \
  -F "image=@/path/to/coffee-image.jpg"
```

---

## ⚠️ Error Handling

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required or invalid
- **403 Forbidden**: Permission denied
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

### Error Response Format

```json
{
  "detail": "Authentication credentials were not provided."
}
```

Or for validation errors:
```json
{
  "email": ["This field is required."],
  "password": ["This password is too short."]
}
```

### Authentication Errors

#### Invalid Credentials
```json
{
  "detail": "No active account found with the given credentials"
}
```

#### Expired Token
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "Authentication credentials were not provided"
**Problem**: Forgot to include Authorization header
**Solution**: Add header: `Authorization: Bearer YOUR_TOKEN`

#### 2. "This field is required" on login
**Problem**: Using `email` instead of `username` in login request
**Solution**: Use `username` field with your email address

#### 3. "Token is invalid or expired"
**Problem**: JWT access token expired (default: 5 minutes)
**Solution**: Use refresh token to get new access token

#### 4. "Permission denied"
**Problem**: Trying to access admin-only endpoints
**Solution**: Use superuser account or check endpoint permissions

#### 5. Server not responding
**Problem**: Development server not running
**Solution**: Run `python manage.py runserver`

### Testing Your Setup

Run this quick test to verify everything works:

```bash
# 1. Test server is running
curl http://127.0.0.1:8000/api/ads/

# 2. Test registration
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test User", "email": "test@example.com", "password": "testpass123", "role": "customer"}'

# 3. Test login
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "test@example.com", "password": "testpass123"}'

# 4. Test authenticated endpoint (use token from step 3)
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  http://127.0.0.1:8000/api/users/
```

---

## 📱 Frontend Integration Examples

### JavaScript/React Example

```javascript
// API client setup
const API_BASE_URL = 'http://127.0.0.1:8000/api';

class NoticeboardAPI {
  constructor() {
    this.token = localStorage.getItem('access_token');
  }

  async login(username, password) {
    const response = await fetch(`${API_BASE_URL}/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });
    
    const data = await response.json();
    
    if (response.ok) {
      this.token = data.access;
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
    }
    
    return data;
  }

  async getProducts() {
    const response = await fetch(`${API_BASE_URL}/products/`, {
      headers: {
        'Authorization': `Bearer ${this.token}`,
      },
    });
    
    return response.json();
  }

  async createProduct(productData) {
    const response = await fetch(`${API_BASE_URL}/products/`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(productData),
    });
    
    return response.json();
  }
}

// Usage
const api = new NoticeboardAPI();

// Login
api.login('user@example.com', 'password123')
  .then(data => console.log('Logged in:', data));

// Get products
api.getProducts()
  .then(products => console.log('Products:', products));
```

### Python Requests Example

```python
import requests
import json

class NoticeboardAPI:
    def __init__(self, base_url='http://127.0.0.1:8000/api'):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        response = requests.post(
            f'{self.base_url}/login/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data['access']
            return data
        else:
            raise Exception(f'Login failed: {response.text}')
    
    def get_headers(self):
        if not self.token:
            raise Exception('Not authenticated. Please login first.')
        return {'Authorization': f'Bearer {self.token}'}
    
    def get_products(self):
        response = requests.get(
            f'{self.base_url}/products/',
            headers=self.get_headers()
        )
        return response.json()
    
    def create_product(self, product_data):
        response = requests.post(
            f'{self.base_url}/products/',
            headers=self.get_headers(),
            json=product_data
        )
        return response.json()

# Usage
api = NoticeboardAPI()

# Login
api.login('user@example.com', 'password123')

# Get products
products = api.get_products()
print(f'Found {len(products)} products')

# Create product
new_product = {
    'category': 1,
    'name': 'Fresh Bananas',
    'price': '2.99',
    'quantity': 30,
    'unit': 'kg'
}
result = api.create_product(new_product)
print('Product created:', result)
```

---

## 🚀 Production Deployment Notes

### Environment Variables
Create a `.env` file for production:

```env
DEBUG=False
SECRET_KEY=your-super-secret-production-key
DATABASE_URL=postgresql://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### Database Migration
```bash
# Switch to PostgreSQL
pip install psycopg2-binary

# Update settings.py database configuration
# Run migrations
python manage.py migrate
```

### Security Checklist
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up proper CORS origins
- [ ] Use HTTPS in production
- [ ] Set up rate limiting
- [ ] Configure logging
- [ ] Set up monitoring

---

## 📞 Support & Resources

### Quick Links
- **Token Generator**: `http://127.0.0.1:8000/generate-api`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **API Root**: `http://127.0.0.1:8000/api/`

### Need Help?
1. Check the troubleshooting section above
2. Test with the provided examples
3. Use the web token generator for easy testing
4. Verify your authentication headers

### API Testing Tools
- **Postman**: Import the cURL examples above
- **Insomnia**: Great for REST API testing
- **Thunder Client**: VS Code extension
- **Browser**: Use the web token generator

---

**🎉 You're ready to build amazing applications with the Noticeboard API!**

This documentation covers everything you need to get started. The API is production-ready and feature-complete. Happy coding! 🚀 