 # Qflow - Queue Management System

Qflow is a modern queue management system designed to streamline the process of managing queues in various service-oriented environments like hospitals, banks, and government offices. The system provides real-time queue management, estimated waiting times, and automated notifications.

## Features

### Core Functionality
- Real-time queue management
- Estimated waiting time calculation
- Automated ticket generation
- SMS and email notifications
- Department and service management
- Doctor/Staff management
- Queue status monitoring
- Consultation record tracking

### User Roles
1. **Admin**
   - Full system access
   - Department and service management
   - Staff management
   - System configuration

2. **Staff**
   - Queue management
   - Ticket processing
   - Consultation record management
   - Service status updates

3. **Patient/Client**
   - Ticket generation
   - Queue position tracking
   - Waiting time estimation
   - Notification management

## API Endpoints

### Authentication
- `POST /api/v1/auth/token/` - Get JWT access and refresh tokens
- `POST /api/v1/auth/token/refresh/` - Refresh access token
- `POST /api/v1/users/` - Create new user
- `GET /api/v1/users/` - List users (admin only)

### Department Management
- `GET /api/v1/departments/` - List all departments
- `POST /api/v1/departments/` - Create new department (admin only)
- `GET /api/v1/departments/{id}/` - Get department details
- `PUT /api/v1/departments/{id}/` - Update department (admin only)
- `DELETE /api/v1/departments/{id}/` - Delete department (admin only)

### Queue Management
- `GET /api/v1/queues/` - List all queues
- `POST /api/v1/queues/` - Create new queue (admin/staff)
- `GET /api/v1/queues/{id}/` - Get queue details
- `PUT /api/v1/queues/{id}/` - Update queue (admin/staff)
- `DELETE /api/v1/queues/{id}/` - Delete queue (admin only)

### Ticket Management
- `POST /api/v1/tickets/` - Generate new ticket
- `GET /api/v1/tickets/` - List tickets (filtered by user)
- `GET /api/v1/tickets/{id}/` - Get ticket details
- `PUT /api/v1/tickets/{id}/` - Update ticket status
- `GET /api/v1/tickets/my_position/` - Get user's position in queue

### Service Management
- `GET /api/v1/services/` - List all services
- `POST /api/v1/services/` - Create new service (admin)
- `GET /api/v1/services/{id}/` - Get service details
- `PUT /api/v1/services/{id}/` - Update service (admin)
- `DELETE /api/v1/services/{id}/` - Delete service (admin)

### Consultation Records
- `GET /api/v1/consultations/` - List consultation records
- `POST /api/v1/consultations/` - Create consultation record
- `GET /api/v1/consultations/{id}/` - Get consultation details
- `PUT /api/v1/consultations/{id}/` - Update consultation record

### Notifications
- `GET /api/v1/notifications/` - List user notifications
- `PUT /api/v1/notifications/{id}/` - Mark notification as read
- `DELETE /api/v1/notifications/{id}/` - Delete notification

## Waiting Time Calculation

The system calculates estimated waiting times using the following algorithm:

1. **Base Calculation**:
   ```python
   estimated_time = (position_in_queue * average_service_time) + buffer_time
   ```

2. **Factors Considered**:
   - Current position in queue
   - Average service time per ticket
   - Number of active service counters
   - Historical service times
   - Peak/off-peak hours
   - Buffer time for unexpected delays

3. **Real-time Updates**:
   - Waiting time is recalculated every 5 minutes
   - Updates are pushed to clients via WebSocket
   - Notifications are sent for significant changes

4. **Accuracy Improvements**:
   - System learns from actual service times
   - Adjusts estimates based on historical data
   - Considers staff availability
   - Accounts for breaks and shift changes

## Setup and Installation

1. **Prerequisites**:
   - Python 3.8+
   - PostgreSQL
   - Redis (for WebSocket support)

2. **Environment Setup**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

4. **Environment Variables**:
   Create a `.env` file with:
   ```
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgres://user:password@localhost:5432/qflow
   ALLOWED_HOSTS=localhost,127.0.0.1
   CORS_ALLOWED_ORIGINS=http://localhost:3000
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   FRONTEND_URL=http://localhost:3000
   ```

5. **Run the Server**:
   ```bash
   python manage.py runserver
   ```

## API Documentation

The API documentation is available at:
- Swagger UI: `http://localhost:8000/swagger/`
- ReDoc: `http://localhost:8000/redoc/`

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.