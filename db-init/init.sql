-- Create subscription tables if they don't exist
CREATE DATABASE IF NOT EXISTS university_db;
USE university_db;

CREATE TABLE IF NOT EXISTS subscriptions (
    sub_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    plan_type VARCHAR(20) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    sub_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL,
    payment_date DATETIME NOT NULL,
    FOREIGN KEY (sub_id) REFERENCES subscriptions(sub_id)
);

-- Create audit logs database and table
CREATE DATABASE IF NOT EXISTS audit_logs_db;
USE audit_logs_db;

CREATE TABLE IF NOT EXISTS audit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    service VARCHAR(100) NOT NULL,
    user_id VARCHAR(100) NOT NULL,
    action VARCHAR(100) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    details JSON,
    INDEX idx_service (service),
    INDEX idx_user_id (user_id),
    INDEX idx_action (action)
);

-- Grant privileges to users (if any specific user was defined)
GRANT ALL PRIVILEGES ON university_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON audit_logs_db.* TO 'root'@'%';
FLUSH PRIVILEGES;