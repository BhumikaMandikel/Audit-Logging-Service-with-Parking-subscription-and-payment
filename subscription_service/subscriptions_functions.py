import mysql.connector
import os
from datetime import datetime, timedelta
import requests
import json

def connect_mysql():
    conn = mysql.connector.connect(
            host="db",
            user="root",
            password="ijwtbpoys",
            database="university_db"
        )
    cursor = conn.cursor(dictionary=True)

    return conn, cursor

def log_event(service, user_id, action, details):
    """Send log event to the log microservice"""
    try:
        log_data = {
            "service": service,
            "user_id": user_id,
            "action": action,
            "details": details
        }
        
        # Send log to the log microservice
        response = requests.post("http://log_microservice:8001/log", json=log_data)
        return response.status_code == 200
    except Exception as e:
        print(f"Error logging event: {str(e)}")
        return False

def create_subscription(user_id, plan_type):
    try:
        conn, cursor = connect_mysql()

        cursor.execute("SELECT * FROM subscriptions WHERE user_id = %s AND end_date > DATE(NOW())", (user_id,))
        subs = cursor.fetchone()

        if subs:
            response_data = {"message": "You already have an active subscription", "subscription": subs}
            
            # Log the failed subscription attempt
            log_event(
                service="subscription_service",
                user_id=user_id,
                action="subscription_attempt_failed",
                details={
                    "reason": "active_subscription_exists",
                    "plan_type": plan_type,
                    "existing_subscription": subs
                }
            )
            
            return response_data, 400

        amount = 500.00 if plan_type.lower() == "monthly" else 5000.00
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=30 if plan_type.lower() == "monthly" else 365)

        cursor.execute("""
            INSERT INTO subscriptions (user_id, plan_type, amount, start_date, end_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, plan_type.lower(), amount, start_date, end_date))
        conn.commit()
        sub_id = cursor.lastrowid

        # Log successful subscription creation
        log_event(
            service="subscription_service",
            user_id=user_id,
            action="subscription_created",
            details={
                "subscription_id": sub_id,
                "plan_type": plan_type,
                "amount": amount,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            }
        )

        payload = {
            "user_id": user_id,
            "sub_id": sub_id,
            "amount": amount
        }
        payment_response = requests.post("http://subscription_service:5000/create-payment", json=payload)

        if payment_response.status_code != 200:
            # Log payment initialization failure
            log_event(
                service="subscription_service",
                user_id=user_id,
                action="payment_initialization_failed",
                details={
                    "subscription_id": sub_id,
                    "amount": amount
                }
            )
            return {"message": "Subscription created but failed to initialize payment"}, 500

        return {
            "message": "Subscription created successfully",
            "subscription_id": sub_id
        }, 200

    except mysql.connector.Error as err:
        # Log database error
        log_event(
            service="subscription_service",
            user_id=user_id,
            action="subscription_error",
            details={
                "error_message": str(err),
                "plan_type": plan_type
            }
        )
        return {"error": str(err)}, 500

    finally:
        cursor.close()
        conn.close()


def create_payment(user_id, sub_id, amount):
    try:
        conn, cursor = connect_mysql()

        cursor.execute("""
            INSERT INTO payments (user_id, sub_id, amount, status, payment_date)
            VALUES (%s, %s, %s, 'pending', NOW())
        """, (user_id, sub_id, amount))
        conn.commit()
        payment_id = cursor.lastrowid

        # Log successful payment initialization
        log_event(
            service="subscription_service",
            user_id=user_id,
            action="payment_initialized",
            details={
                "payment_id": payment_id,
                "subscription_id": sub_id,
                "amount": amount,
                "status": "pending"
            }
        )

        return {
            "message": "Payment initialized",
            "payment_id": payment_id
        }, 200

    except mysql.connector.Error as err:
        # Log database error
        log_event(
            service="subscription_service",
            user_id=user_id,
            action="payment_error",
            details={
                "error_message": str(err),
                "subscription_id": sub_id,
                "amount": amount
            }
        )
        return {"error": str(err)}, 500

    finally:
        cursor.close()
        conn.close()


def complete_payment(user_id):
    try:
        conn, cursor = connect_mysql()

        cursor.execute("""
            SELECT payment_id, sub_id, amount 
            FROM payments 
            WHERE user_id = %s AND status = 'pending' 
            ORDER BY payment_date DESC 
            LIMIT 1
        """, (user_id,))
        result = cursor.fetchone()

        if not result:
            # Log no pending payments found
            log_event(
                service="subscription_service",
                user_id=user_id,
                action="payment_completion_failed",
                details={
                    "reason": "no_pending_payments"
                }
            )
            return {"message": "No pending payments found"}, 404

        payment_id = result["payment_id"]
        sub_id = result["sub_id"]
        amount = result["amount"]

        cursor.execute("""
            UPDATE payments 
            SET status = 'completed', payment_date = NOW() 
            WHERE payment_id = %s
        """, (payment_id,))
        conn.commit()

        # Log successful payment completion
        log_event(
            service="subscription_service",
            user_id=user_id,
            action="payment_completed",
            details={
                "payment_id": payment_id,
                "subscription_id": sub_id,
                "amount": amount
            }
        )

        return {"message": f"Payment {payment_id} marked as completed"}, 200

    except mysql.connector.Error as err:
        # Log database error
        log_event(
            service="subscription_service",
            user_id=user_id,
            action="payment_completion_error",
            details={
                "error_message": str(err)
            }
        )
        return {"error": str(err)}, 500

    finally:
        cursor.close()
        conn.close()