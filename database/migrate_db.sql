-- LifelineQR Database Migration (MySQL 9.3 compatible)
-- Drops the 'users' table and creates separate 'doctors' and 'patients' tables

USE lifelineqr;

-- Disable foreign key checks so we can drop/recreate freely
SET FOREIGN_KEY_CHECKS = 0;

-- Drop old tables and any partially‑created tables from previous runs
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

-- Create patients table
CREATE TABLE patients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    blood_group VARCHAR(5),
    allergies TEXT,
    medical_conditions TEXT,
    regular_medications TEXT,
    address TEXT,
    emergency_contacts VARCHAR(20),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create doctors table
CREATE TABLE doctors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    specialization VARCHAR(100),
    experience INT,
    hospital VARCHAR(255),
    contact_number VARCHAR(20),
    working_hours VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
