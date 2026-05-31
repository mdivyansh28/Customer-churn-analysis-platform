CREATE DATABASE IF NOT EXISTS customer_churn_db;

USE customer_churn_db;

-- =====================================
-- CUSTOMERS TABLE
-- =====================================

CREATE TABLE Customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(20),
    senior_citizen INT,
    partner VARCHAR(10),
    dependents VARCHAR(10),
    tenure INT,
    phone_service VARCHAR(10),
    internet_service VARCHAR(50),
    contract VARCHAR(50),
    payment_method VARCHAR(100),
    monthly_charges DECIMAL(10,2),
    total_charges DECIMAL(10,2),
    churn VARCHAR(10)
);

-- =====================================
-- PREDICTIONS TABLE
-- =====================================

CREATE TABLE Predictions (
    prediction_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50),
    churn_probability DECIMAL(5,2),
    prediction_result VARCHAR(20),
    prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
);

-- =====================================
-- RECOMMENDATIONS TABLE
-- =====================================

CREATE TABLE Recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50),
    churn_probability DECIMAL(5,2),
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_id)
    REFERENCES Customers(customer_id)
);

-- =====================================
-- SAMPLE DATA
-- =====================================

INSERT INTO Customers
VALUES
(
'7590-VHVEG',
'Female',
0,
'Yes',
'No',
1,
'No',
'DSL',
'Month-to-month',
'Electronic check',
29.85,
29.85,
'No'
);

INSERT INTO Predictions
(
customer_id,
churn_probability,
prediction_result
)
VALUES
(
'7590-VHVEG',
82.50,
'Likely Churn'
);

INSERT INTO Recommendations
(
customer_id,
churn_probability,
recommendation
)
VALUES
(
'7590-VHVEG',
82.50,
'Provide 20% discount and loyalty rewards'
);