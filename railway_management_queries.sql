
-- Create Database and Use It
CREATE DATABASE IF NOT EXISTS Railway_mgmt;
USE Railway_mgmt;

-- Create Tables
CREATE TABLE IF NOT EXISTS trains (
    train_id INT AUTO_INCREMENT PRIMARY KEY,
    train_name VARCHAR(100),
    source VARCHAR(100),
    destination VARCHAR(100),
    coach_type VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS passengers (
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    contact VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id INT AUTO_INCREMENT PRIMARY KEY,
    passenger_id INT,
    train_id INT,
    coach_type VARCHAR(20),
    reservation_date DATE,
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE,
    FOREIGN KEY (train_id) REFERENCES trains(train_id) ON DELETE CASCADE
);

-- Insert Sample Trains
INSERT INTO trains (train_name, source, destination, coach_type) VALUES
('Konkan Express', 'Kerala', 'Goa', '1A'),
('Kerala Superfast', 'Trivandrum', 'Bangalore', '2A'),
('Goa Link Express', 'Goa', 'Hyderabad', 'SL'),
('Bangalore Intercity', 'Bangalore', 'Chennai', '1A'),
('Deccan Queen', 'Mumbai', 'Pune', '2A'),
('Rajdhani Express', 'Delhi', 'Kolkata', '1A'),
('Coromandel Express', 'Chennai', 'Howrah', 'SL'),
('Garib Rath', 'Hyderabad', 'Mumbai', '2A'),
('Shatabdi Express', 'Delhi', 'Bhopal', '1A'),
('Vivek Express', 'Kanyakumari', 'Dibrugarh', 'SL');

-- Select Queries
SELECT * FROM trains;

SELECT * FROM trains WHERE train_id = 1;

SELECT COUNT(*) FROM reservations 
WHERE train_id = 1 AND reservation_date = '2025-07-30' AND coach_type = '1A';

-- Insert Passenger Example
INSERT INTO passengers (name, age, gender, contact)
VALUES ('Rahul', 22, 'Male', '9876543210');

-- Make Reservation Example
INSERT INTO reservations (passenger_id, train_id, coach_type, reservation_date)
VALUES (1, 3, 'SL', '2025-08-01');

-- View All Reservations
SELECT r.reservation_id, p.name, t.train_name, r.coach_type, r.reservation_date
FROM reservations r
JOIN passengers p ON r.passenger_id = p.passenger_id
JOIN trains t ON r.train_id = t.train_id;

-- View Reservation by Passenger ID
SELECT r.reservation_id, t.train_name, r.coach_type, r.reservation_date
FROM reservations r
JOIN trains t ON r.train_id = t.train_id
WHERE r.passenger_id = 1;

-- Update Train Info
UPDATE trains
SET train_name = 'New Name', source = 'New Source', destination = 'New Destination', coach_type = '2A'
WHERE train_id = 5;

-- Delete Train
DELETE FROM trains WHERE train_id = 5;

-- Delete Passenger
DELETE FROM passengers WHERE passenger_id = 3;

-- Cancel Reservation
DELETE FROM reservations WHERE reservation_id = 2;
