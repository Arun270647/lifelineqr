-- LifeLine QR - LocalStorage Database Initialization
-- This file contains SQL-like commands to initialize the LocalStorage database
-- Execute this by opening index.html in a browser - the JavaScript will automatically initialize the database

-- ===========================================
-- TABLE DEFINITIONS (LocalStorage Collections)
-- ===========================================

-- TABLE: users
-- Stores both patient and doctor accounts
-- Fields: id, role (patient/doctor), name, age, email, password (hashed), createdAt, updatedAt
-- Patient-specific: bloodGroup, allergies, medicalConditions, regularMedications, address, emergencyContacts
-- Doctor-specific: specialization, experience, hospital, contactNumber, workingHours

CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    role ENUM('patient', 'doctor') NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL, -- Base64 hashed
    
    -- Patient fields
    bloodGroup VARCHAR(5),
    allergies TEXT,
    medicalConditions TEXT,
    regularMedications TEXT,
    address TEXT,
    emergencyContacts VARCHAR(20),
    
    -- Doctor fields
    specialization VARCHAR(100),
    experience INT,
    hospital VARCHAR(255),
    contactNumber VARCHAR(20),
    workingHours VARCHAR(50),
    
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- TABLE: qr_mappings
-- Maps QR codes to patient IDs
-- Fields: id, patientId, qrCode, createdAt

CREATE TABLE qr_mappings (
    id VARCHAR(36) PRIMARY KEY,
    patientId VARCHAR(36) NOT NULL,
    qrCode VARCHAR(36) UNIQUE NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patientId) REFERENCES users(id)
);

-- TABLE: medical_records
-- Stores uploaded medical documents
-- Fields: id, patientId, filename, fileType, fileData (base64), description, uploadedAt

CREATE TABLE medical_records (
    id VARCHAR(36) PRIMARY KEY,
    patientId VARCHAR(36) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    fileType VARCHAR(50) NOT NULL,
    fileData LONGTEXT NOT NULL, -- Base64 encoded file
    description TEXT,
    uploadedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patientId) REFERENCES users(id)
);

-- TABLE: orders
-- Stores QR card merchandise orders
-- Fields: id, userId, productType, productName, price, customerName, phone, address, quantity, qrCode, status, orderDate

CREATE TABLE orders (
    id VARCHAR(36) PRIMARY KEY,
    userId VARCHAR(36) NOT NULL,
    productType ENUM('standard', 'premium') NOT NULL,
    productName VARCHAR(255) NOT NULL,
    price VARCHAR(20) NOT NULL,
    customerName VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    quantity INT NOT NULL,
    qrCode VARCHAR(36),
    status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
    orderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (userId) REFERENCES users(id),
    FOREIGN KEY (qrCode) REFERENCES qr_mappings(qrCode)
);

-- ===========================================
-- SAMPLE DATA (for testing)
-- ===========================================

-- Insert Sample Patients
INSERT INTO users (role, name, age, email, password, bloodGroup, allergies, medicalConditions, regularMedications, address, emergencyContacts)
VALUES 
('patient', 'Rahul Kumar', 28, 'rahul@example.com', 'UmFodWw= MTIzNDU2TGlmZUxpbmUgUVI=', 'O+', 'Penicillin', 'None', 'None', '123 MG Road, Bangalore', '9876543210'),
('patient', 'Priya Sharma', 35, 'priya@example.com', 'UHJpeWExMjM0NTZMaWZlTGluZSBRUg==', 'A+', 'Peanuts', 'Diabetes Type 2', 'Metformin 500mg', '45 Brigade Road, Bangalore', '9876543211'),
('patient', 'Amit Patel', 42, 'amit@example.com', 'QW1pdDEyMzQ1NkxpZmVMaW5lIFFS', 'B+', 'None', 'Hypertension', 'Amlodipine 5mg', '78 Koramangala, Bangalore', '9876543212');

-- Insert Sample Doctors
INSERT INTO users (role, name, age, email, password, specialization, experience, hospital, contactNumber, workingHours)
VALUES 
('doctor', 'Dr. Suresh Reddy', 45, 'suresh@example.com', 'RHIuU3VyZXNoMTIzNDU2TGlmZUxpbmUgUVI=', 'Cardiologist', 15, 'Apollo Hospital', '9876000001', '9:00 AM - 5:00 PM'),
('doctor', 'Dr. Anjali Menon', 38, 'anjali@example.com', 'RHIuQW5qYWxpMTIzNDU2TGlmZUxpbmUgUVI=', 'General Physician', 12, 'Fortis Hospital', '9876000002', '10:00 AM - 6:00 PM'),
('doctor', 'Dr. Vikram Singh', 52, 'vikram@example.com', 'RHIuVmlrcmFtMTIzNDU2TGlmZUxpbmUgUVI=', 'Orthopedic', 25, 'Manipal Hospital', '9876000003', '8:00 AM - 4:00 PM'),
('doctor', 'Dr. Kavita Iyer', 33, 'kavita@example.com', 'RHIuS2F2aXRhMTIzNDU2TGlmZUxpbmUgUVI=', 'Neurologist', 8, 'Columbia Asia', '9876000004', '11:00 AM - 7:00 PM');

-- Note: QR mappings are generated automatically when patients register
-- Sample QR codes would be inserted like:
INSERT INTO qr_mappings (patientId, qrCode)
VALUES 
('patient-id-1', 'qr-code-uuid-1'),
('patient-id-2', 'qr-code-uuid-2'),
('patient-id-3', 'qr-code-uuid-3');

-- ===========================================
-- USAGE INSTRUCTIONS
-- ===========================================

/*
LOCALSTORAGE IMPLEMENTATION:

1. The database is automatically initialized when you open the application
2. All data is stored in browser LocalStorage with these keys:
   - lifeline_users
   - lifeline_medical_records
   - lifeline_qr_mappings
   - lifeline_orders
   - lifeline_current_user (session data)

3. To clear all data and reset the database:
   Open browser console and run:
   localStorage.clear();
   sessionStorage.clear();
   location.reload();

4. To view stored data:
   Open browser console and run:
   console.log(JSON.parse(localStorage.getItem('lifeline_users')));
   console.log(JSON.parse(localStorage.getItem('lifeline_qr_mappings')));
   console.log(JSON.parse(localStorage.getItem('lifeline_medical_records')));
   console.log(JSON.parse(localStorage.getItem('lifeline_orders')));

5. To manually add demo data:
   Open index.html in browser
   Open console and run the following JavaScript:

   // Add a demo patient
   const demoPatient = {
       role: 'patient',
       name: 'John Doe',
       age: 30,
       email: 'john@demo.com',
       password: Utils.hashPassword('password123'),
       bloodGroup: 'O+',
       allergies: 'None',
       medicalConditions: 'None',
       regularMedications: 'None',
       address: '123 Demo Street',
       emergencyContacts: '1234567890'
   };
   const result = UserStorage.createUser(demoPatient);
   console.log('Demo patient created:', result);

   // Add a demo doctor
   const demoDoctor = {
       role: 'doctor',
       name: 'Dr. Jane Smith',
       age: 40,
       email: 'jane@demo.com',
       password: Utils.hashPassword('doctor123'),
       specialization: 'General Physician',
       experience: 10,
       hospital: 'Demo Hospital',
       contactNumber: '0987654321',
       workingHours: '9 AM - 5 PM'
   };
   const doctorResult = UserStorage.createUser(demoDoctor);
   console.log('Demo doctor created:', doctorResult);

6. Default Login Credentials:
   Use the registration pages to create new accounts
   Or use demo credentials if you manually added them

7. Data Persistence:
   - Data persists across browser sessions
   - Data is specific to the browser and domain
   - Clearing browser data will delete all records
   - No server-side storage - everything is client-side

8. File Size Limitations:
   - LocalStorage typically has a 5-10MB limit
   - Keep file uploads under 5MB
   - For production, consider using IndexedDB for larger files

9. Security Notes:
   - Passwords are encoded with Base64 (for demo purposes only)
   - In production, use proper server-side authentication
   - Medical data is stored unencrypted in LocalStorage
   - This is for educational/demonstration purposes only

10. Backup Data:
    To backup your data, run in console:
    const backup = {
        users: localStorage.getItem('lifeline_users'),
        records: localStorage.getItem('lifeline_medical_records'),
        qr: localStorage.getItem('lifeline_qr_mappings'),
        orders: localStorage.getItem('lifeline_orders')
    };
    console.log(JSON.stringify(backup));
    
    To restore:
    localStorage.setItem('lifeline_users', backup.users);
    localStorage.setItem('lifeline_medical_records', backup.records);
    localStorage.setItem('lifeline_qr_mappings', backup.qr);
    localStorage.setItem('lifeline_orders', backup.orders);
*/

-- ===========================================
-- END OF DATABASE INITIALIZATION
-- ===========================================
