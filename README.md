# Vendor and Shop Management System

A Django-based web application that enables vendors to register on a platform and manage their shops using CRUD operations. It also provides a public API for users to search for nearby shops based on their latitude and longitude.

## Features

- **Vendor Registration and Authentication**
  - Register with name, email, and password
  - JWT-based authentication for secure operations

- **Shop Management (CRUD Operations)**
  - Create: Add new shops with details (name, owner, type, location)
  - Read: Retrieve shop information
  - Update: Modify shop information
  - Delete: Remove shops from profile

- **Public API for Nearby Shop Search**
  - Search shops within a specified radius based on user's location

## Technology Stack

- Python
- Django
- Django REST Framework
- SQLite (Database)
- JWT Authentication

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vendor-shop-system.git
   cd vendor-shop-system
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at: `http://127.0.0.1:8000/`

## API Documentation

### Authentication Endpoints

- **Register**: `POST /api/accounts/register/`
  - Request body: `{"name": "Vendor Name", "email": "vendor@email.com", "password": "strong_password"}`
  - Response: `{"id": 1, "name": "Vendor Name", "email": "vendor@email.com"}`

- **Login**: `POST /api/accounts/login/`
  - Request body: `{"email": "vendor@email.com", "password": "strong_password"}`
  - Response: `{"refresh": "refresh_token", "access": "access_token"}`

- **Refresh Token**: `POST /api/accounts/token/refresh/`
  - Request body: `{"refresh": "refresh_token"}`
  - Response: `{"access": "new_access_token"}`

### Shop Management Endpoints

- **Create Shop**: `POST /api/shops/`
  - Authentication: Bearer Token
  - Request body: `{"name": "Shop Name", "owner": "Owner Name", "business_type": "Retail", "latitude": 28.7041, "longitude": 77.1025}`
  - Response: Created shop object

- **List Shops**: `GET /api/shops/`
  - Authentication: Bearer Token
  - Response: List of all shops owned by the authenticated vendor

- **Retrieve Shop**: `GET /api/shops/{id}/`
  - Authentication: Bearer Token
  - Response: Detailed shop information

- **Update Shop**: `PUT /api/shops/{id}/`
  - Authentication: Bearer Token
  - Request body: Updated shop details
  - Response: Updated shop object

- **Delete Shop**: `DELETE /api/shops/{id}/`
  - Authentication: Bearer Token
  - Response: No content (204)

### Public Nearby Shop Search API

- **Search Nearby Shops**: `GET /api/nearby-shops/?latitude=28.7041&longitude=77.1025&radius=5`
  - Parameters:
    - `latitude`: User's latitude (required)
    - `longitude`: User's longitude (required)
    - `radius`: Search radius in kilometers (optional, default: 5)
  - Response: List of shops within the specified radius

## Testing

Run tests with:
```bash
python manage.py test
```

## Security Considerations

- JWT authentication for secure API access
- Role-based access control for shop management
- Password hashing and secure storage
- Token-based authentication for API endpoints

## License

This project is licensed under the MIT License.