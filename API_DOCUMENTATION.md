# Noticeboard API Documentation

## Getting Started

### 1. Authentication
- **Users can register and log in via the API using email and password.**
- Log in at `/api/login/` to obtain your JWT access and refresh tokens.
- Use the token in the `Authorization` header for all API requests:
  ```
  Authorization: Bearer <your_jwt_token>
  ```

### 2. API Base URL
- Local: `http://127.0.0.1:8000/api/`

---

## Endpoints Overview
All endpoints require authentication via JWT unless otherwise noted.

### Registration
- `POST /api/register/` — Register a new user
  - **Request Body:**
    ```json
    {
      "name": "Test User",
      "email": "testuser@example.com",
      "password": "testpassword123",
      "role": "customer"
    }
    ```
  - **Response:**
    ```json
    {
      "id": 2,
      "name": "Test User",
      "email": "testuser@example.com",
      "role": "customer"
    }
    ```

### Login (JWT)
- `POST /api/login/` — Obtain JWT access and refresh tokens
  - **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "yourpassword"
    }
    ```
  - **Response:**
    ```json
    {
      "refresh": "<refresh_token>",
      "access": "<access_token>"
    }
    ```

### Users
- `GET /api/users/` — List users
- `POST /api/users/` — Create user (admin only)
- `GET /api/users/{id}/` — Retrieve user
- `PUT/PATCH /api/users/{id}/` — Update user
- `DELETE /api/users/{id}/` — Delete user

**User Fields:**
- `id`, `name`, `email`, `profile_picture`, `email_verified`, `kyc_verified`, `password`, `role`, `region`, `phone_number`, `location`, `created_at`, `updated_at`, `wallet_balance`, `kyc_verified_at`, `training_points`, `notification_preferences`

---

### Products
- `GET /api/products/` — List products
- `POST /api/products/` — Create product
- `GET /api/products/{id}/` — Retrieve product
- `PUT/PATCH /api/products/{id}/` — Update product
- `DELETE /api/products/{id}/` — Delete product

**Product Fields:**
- `id`, `category`, `user`, `name`, `description`, `price`, `quantity`, `unit`, `harvest_date`, `status`, `is_organic`, `is_featured`, `type`, `image`, `video`, `location`, `is_opportunity`, `sold_count`, `created_at`, `updated_at`

---

### Product Negotiations
- `GET /api/negotiations/` — List negotiations
- `POST /api/negotiations/` — Propose a price for a product
- `GET /api/negotiations/{id}/` — Retrieve negotiation details
- `POST /api/negotiations/{id}/accept/` — Accept a price offer
- `POST /api/negotiations/{id}/decline/` — Decline a price offer

**ProductNegotiation Fields:**
- `id`, `product`, `buyer`, `proposed_price`, `status` (pending, accepted, declined), `created_at`, `updated_at`

---

### Chat & Messaging
- `GET /api/chatrooms/` — List chat rooms
- `POST /api/chatrooms/` — Create a chat room
- `GET /api/chatrooms/{id}/` — Retrieve a chat room
- `GET /api/messages/` — List messages
- `POST /api/messages/` — Send a message
- `GET /api/messages/{id}/` — Retrieve a message

**ChatRoom Fields:**
- `id`, `name`, `users`, `created_at`, `updated_at`

**ChatMessage Fields:**
- `id`, `room`, `sender`, `content`, `created_at`, `is_read`

---

### Notifications
- `GET /api/notifications/` — List all notifications (admin only)
- `POST /api/notifications/` — Create a notification (admin only)
- `GET /notifications/pull/` — Pull (fetch) active notifications for the authenticated user
- `POST /notifications/push/` — Push a notification to the authenticated user

**Notification Fields:**
- `id`, `users`, `notification_type`, `title`, `message`, `is_read`, `related_id`, `created_at`, `sent_at`, `read_at`, `is_active`

---

### Ads
- `GET /api/ads/` — List active ads (no authentication required)

**Ad Fields:**
- `id`, `type`, `title`, `subtitle`, `description`, `button`, `media`, `link`, `is_active`, `created_at`, `updated_at`

---

## Example Usage

### 1. Register a New User
```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "testuser@example.com",
    "password": "testpassword123",
    "role": "customer"
  }'
```

### 2. Obtain JWT Token (Login)
```bash
curl -X POST http://127.0.0.1:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "yourpassword"
  }'
```

### 3. Make an Authenticated Request
```bash
curl -H "Authorization: Bearer <your_jwt_token>" http://127.0.0.1:8000/api/products/
```

### 4. Pull Notifications
```bash
curl -H "Authorization: Bearer <your_jwt_token>" http://127.0.0.1:8000/notifications/pull/
```

### 5. Push Notification to User
```bash
curl -X POST http://127.0.0.1:8000/notifications/push/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{ "notification_id": 1 }'
```

### 6. Create a Chat Room
```bash
curl -X POST http://127.0.0.1:8000/api/chatrooms/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Negotiation Room",
    "users": [2, 3]
  }'
```

### 7. Send a Message
```bash
curl -X POST http://127.0.0.1:8000/api/messages/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "room": 1,
    "sender": 2,
    "content": "Hello, I'm interested in your product."
  }'
```

### 8. Propose a Negotiation
```bash
curl -X POST http://127.0.0.1:8000/api/negotiations/ \
  -H "Authorization: Bearer <your_jwt_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "product": 1,
    "buyer": 2,
    "proposed_price": "8.50"
  }'
```

### 9. Accept a Negotiation
```bash
curl -X POST http://127.0.0.1:8000/api/negotiations/1/accept/ \
  -H "Authorization: Bearer <your_jwt_token>"
```

### 10. Decline a Negotiation
```bash
curl -X POST http://127.0.0.1:8000/api/negotiations/1/decline/ \
  -H "Authorization: Bearer <your_jwt_token>"
```

---

## Notes
- All endpoints require a valid JWT unless otherwise noted.
- All endpoints support standard HTTP methods (GET, POST, PUT, PATCH, DELETE).
- For file uploads, use `multipart/form-data`.
- Pagination, filtering, and search can be added as needed.
- **Foreign Key fields**: When providing a foreign key field, use the referenced object's ID.
- **Notifications**: Only users with `is_active=true` will receive notifications.
- **Error Handling**: All endpoints return clear error messages for invalid input, duplicate emails, and authentication issues.

---

## Download
- This documentation is available as `API_DOCUMENTATION.md` in your project folder. 