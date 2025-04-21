# Audit-Logging-Service-with-Parking-subscription-and-payment

A microservice-based parking management system that handles subscription management and audit logging for university parking services.

---

## Tech Stack

### Backend Services:
- **Subscription Service** (Flask) – Port 5003
- **Log Microservice** (FastAPI + SQLAlchemy) – Port 8001

### Database:
- **MySQL** (for both subscription/payment data and audit logs)

### Containerization:
- **Docker + Docker Compose**

---
### Build and start the Docker containers:

```bash
docker-compose up --build
```
### Access:
Subscription Service: http://localhost:5003

Log Microservice: http://localhost:8001

Swagger Documentation: http://localhost:5003/docs

### API Endpoints
### Subscription Service (Port 5003)
GET / – Check service status

POST /create-subscription – Create a new parking subscription

POST /create-payment – Initialize payment for a subscription

POST /complete-payment – Complete a pending payment transaction

### Log Microservice (Port 8001)
GET /health – Check service health

POST /log – Create audit log entry

GET /logs – Retrieve filtered logs by service or user ID

### Database Setup
# The system uses two MySQL databases:

university_db – Stores subscription and payment data.

audit_logs_db – Stores comprehensive system audit logs.

Directory Structure
```bash
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
