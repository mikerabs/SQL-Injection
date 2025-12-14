-- Create database if not exists (though docker-compose creates it)
CREATE DATABASE IF NOT EXISTS pyexample;
USE pyexample;

-- Create users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE, -- usernames should be unique
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create people table
CREATE TABLE people (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    age INT,
    occupation VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data into users table
INSERT INTO users (username, password, email) VALUES
('john_doe', 'hashed_password_1', 'john@example.com'),
('jane_smith', 'hashed_password_2', 'jane@example.com'),
('bob_johnson', 'hashed_password_3', 'bob@example.com'),
('alice_smith', 'hashed_password_4', 'alice@example.com'),
('charlie_brown', 'hashed_password_5', 'charlie@example.com'),
('diana_prince', 'hashed_password_6', 'diana@example.com'),
('george_miller', 'hashed_password_7', 'george@example.com'),
('fiona_garcia', 'an_actual_password_thats_different', 'fiona@example.com'),
('george_martin', 'hashed_password_9', 'george@example.com'),
('hannah_clark', 'hashed_password_10', 'hannah@example.com');

-- Insert sample data into people table
INSERT INTO people (first_name, last_name, age, occupation) VALUES
('John', 'Doe', 30, 'Software Engineer'),
('Jane', 'Smith', 25, 'Data Scientist'),
('Bob', 'Johnson', 35, 'Product Manager'),
('Alice', 'Smith', 28, 'UX Designer'),
('Charlie', 'Brown', 40, 'DevOps Engineer'),
('Diana', 'Prince', 32, 'Security Analyst'),
('George', 'Miller', 45, 'CTO'),
('Fiona', 'Garcia', 29, 'ML Engineer'),
('George', 'Martin', 38, 'Architect'),
('Hannah', 'Clark', 27, 'Data Analyst');

-- Create application user with limited privileges
CREATE USER IF NOT EXISTS 'appuser'@'%' IDENTIFIED BY 'apppassword';
GRANT SELECT, INSERT, UPDATE, DELETE ON pyexample.* TO 'appuser'@'%';
FLUSH PRIVILEGES;
