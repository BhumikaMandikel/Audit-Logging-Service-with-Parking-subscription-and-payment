# Audit-Logging-Service-with-Parking-subscription-and-payment
PES University Parking & Subscription Management System
README FILE 
A microservice-based parking management system that handles subscription management and audit logging for university parking services.
Tech Stack
Backend Services:
Subscription Service (Flask) – Port 5003
Log Microservice (FastAPI + SQLAlchemy) – Port 8001
Database: MySQL
Containerization: Docker + Docker Compose
Key Features
✅ Parking subscription management (monthly/annual plans)
✅ Payment processing system
✅ Centralized audit logging
✅ Request tracking and history
✅ API Documentation with Swagger UI
Installation
Clone the repository
Run docker-compose up --build
Access:
Subscription Service: http://localhost:5003
Log Microservice: http://localhost:8001
Swagger Documentation: http://localhost:5003/docs
API Endpoints
Subscription Service (5003)
GET / – Check service status
POST /create-subscription – Create a new parking subscription
POST /create-payment – Initialize payment for subscription
POST /complete-payment – Complete pending payment transaction
Log Microservice (8001)
GET /health – Check service health
POST /log – Create audit log entry
GET /logs – Retrieve filtered logs by service or user ID
Database Setup
Two MySQL databases:
university_db – Stores subscription and payment data
audit_logs_db – Stores comprehensive system audit logs
Directory Structure
.
├── docker-compose.yml
├── db-init/                    
├── log_microservice/           
│   ├── app/
│   │   ├── database.py         
│   │   ├── models.py           
│   │   ├── routes.py           
│   │   └── schemas.py          
│   ├── main.py                 
│   └── requirements.txt        
└── subscription_service/       
    ├── app.py                  
    ├── subscriptions_functions.py  
    ├── static/                 
    └── requirements.txt        
