from flask import Flask, request, jsonify, send_from_directory
from subscriptions_functions import create_subscription, create_payment, complete_payment
from flask_swagger_ui import get_swaggerui_blueprint
import os

app = Flask(__name__)

# Define Swagger UI blueprint
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Subscription Service API"
    }
)
app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)

# Create a static directory if it doesn't exist
os.makedirs('static', exist_ok=True)

# Create a swagger.json file in the static directory
swagger_content = '''{
  "openapi": "3.0.0",
  "info": {
    "title": "Subscription Service API",
    "description": "API for managing subscriptions and payments",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "http://localhost:5003",
      "description": "Local development server"
    }
  ],
  "paths": {
    "/create-subscription": {
      "post": {
        "summary": "Create a new subscription",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "user_id": {
                    "type": "string",
                    "description": "User ID"
                  },
                  "plan_type": {
                    "type": "string",
                    "description": "Subscription plan type (monthly or annual)"
                  }
                },
                "required": ["user_id", "plan_type"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Subscription created successfully"
          },
          "400": {
            "description": "Bad request"
          },
          "500": {
            "description": "Server error"
          }
        }
      }
    },
    "/create-payment": {
      "post": {
        "summary": "Create a payment for a subscription",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "user_id": {
                    "type": "string"
                  },
                  "sub_id": {
                    "type": "integer"
                  },
                  "amount": {
                    "type": "number"
                  }
                },
                "required": ["user_id", "sub_id", "amount"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Payment initialized successfully"
          },
          "500": {
            "description": "Server error"
          }
        }
      }
    },
    "/complete-payment": {
      "post": {
        "summary": "Complete a pending payment",
        "requestBody": {
          "required": true,
          "content": {
            "application/json": {
              "schema": {
                "type": "object",
                "properties": {
                  "user_id": {
                    "type": "string"
                  }
                },
                "required": ["user_id"]
              }
            }
          }
        },
        "responses": {
          "200": {
            "description": "Payment completed successfully"
          },
          "404": {
            "description": "No pending payment found"
          },
          "500": {
            "description": "Server error"
          }
        }
      }
    }
  }
}'''

# Create the swagger.json file
with open('static/swagger.json', 'w') as f:
    f.write(swagger_content)
import requests

def log_action(service: str, user_id: str, action: str, details: dict):
    log_url = "http://log_microservice:8001/log"  # Using container name for Docker networking
    log_data = {
        "service": service,
        "user_id": user_id,
        "action": action,
        "details": details
    }
    try:
        response = requests.post(log_url, json=log_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to log action: {e}")

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Parking Subscription and payment service is running"})


@app.route("/create-subscription", methods=["POST"])
def create_subscription_route():
    data = request.get_json()
    user_id = data.get("user_id")
    plan_type = data.get("plan_type")

    response, status_code = create_subscription(user_id, plan_type)
    
    # Log the action
    log_action(
        service="subscription_service",
        user_id=user_id,
        action="create_subscription",
        details={
            "plan_type": plan_type,
            "status_code": status_code,
            "response": response
        }
    )
    
    return jsonify(response), status_code

@app.route("/create-payment", methods=["POST"])
def create_payment_route():
    data = request.get_json()
    user_id = data.get("user_id")
    sub_id = data.get("sub_id")
    amount = data.get("amount")

    response, status_code = create_payment(user_id, sub_id, amount)
    
    # Log the action
    log_action(
        service="subscription_service",
        user_id=user_id,
        action="create_payment",
        details={
            "subscription_id": sub_id,
            "amount": amount,
            "status_code": status_code,
            "response": response
        }
    )
    
    return jsonify(response), status_code

@app.route("/complete-payment", methods=["POST"])
def complete_payment_route():
    data = request.get_json()
    user_id = data.get("user_id")

    response, status_code = complete_payment(user_id)
    
    # Log the action
    log_action(
        service="subscription_service",
        user_id=user_id,
        action="complete_payment",
        details={
            "status_code": status_code,
            "response": response
        }
    )
    
    return jsonify(response), status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)