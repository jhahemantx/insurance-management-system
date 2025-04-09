-- Create Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create Policies Table
CREATE TABLE IF NOT EXISTS policies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    policy_name VARCHAR(255) NOT NULL,
    policy_type VARCHAR(255) NOT NULL,
    premium_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Create Claims Table
CREATE TABLE IF NOT EXISTS claims (
    id INT PRIMARY KEY AUTO_INCREMENT,
    policy_id INT NOT NULL,
    claim_date DATE NOT NULL,
    claim_amount DECIMAL(10,2) NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') NOT NULL DEFAULT 'Pending',
    FOREIGN KEY (policy_id) REFERENCES policies(id) ON DELETE CASCADE
);

-- Insert Sample Data
INSERT INTO users (name, email, password) VALUES 
('John Doe', 'john@example.com', 'password123'),
('Jane Smith', 'jane@example.com', 'securepass');

INSERT INTO policies (user_id, policy_name, policy_type, premium_amount) VALUES
(1, 'Health Insurance Plan A', 'Health', 5000.00),
(1, 'Car Insurance Basic', 'Vehicle', 3000.00),
(2, 'Life Insurance Gold', 'Life', 7000.00);

INSERT INTO claims (policy_id, claim_date, claim_amount, status) VALUES
(1, '2024-03-30', 2000.00, 'Approved'),
(2, '2024-03-28', 1500.00, 'Pending');
