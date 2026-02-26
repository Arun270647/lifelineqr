<?php
// Database Configuration
// =====================
// If you get "Access denied" errors, update DB_USER and DB_PASS below
// to match your MySQL credentials.
//
// XAMPP default  → user: root, password: (empty)
// WAMP default   → user: root, password: (empty)
// MySQL install  → user: root, password: (whatever you set during install)
//
// To check or reset your MySQL root password:
//   1. Open phpMyAdmin → http://localhost/phpmyadmin
//   2. Go to "User accounts" tab
//   3. Look at the root user row — that shows the auth method
//   4. Click "Edit privileges" → "Change password" to set a new one.
//      Then paste the same password below in DB_PASS.

define('DB_HOST', 'localhost');
define('DB_USER', 'root');          // Change this to your MySQL username
define('DB_PASS', '');              // ← PUT YOUR MYSQL PASSWORD HERE (leave empty if none)
define('DB_NAME', 'lifeline_qr');

// ── Connect to the database ────────────────────────────────────────────
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

// Check connection — surface the real error
if ($conn->connect_error) {
    http_response_code(500);
    die(json_encode([
        'success' => false,
        'error'   => 'MySQL connection failed: ' . $conn->connect_error,
        'hint'    => 'Open api/config.php and set DB_PASS to your MySQL root password.'
    ]));
}

// Set charset to utf8mb4
$conn->set_charset('utf8mb4');

// ── Auto-create tables if they do not exist (safe — uses IF NOT EXISTS) ──
$conn->query("
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) PRIMARY KEY,
    role ENUM('student', 'doctor') NOT NULL,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,

    -- Student fields
    blood_group VARCHAR(5) DEFAULT NULL,
    allergies TEXT DEFAULT NULL,
    medical_conditions TEXT DEFAULT NULL,
    regular_medications TEXT DEFAULT NULL,
    address TEXT DEFAULT NULL,
    emergency_contacts VARCHAR(20) DEFAULT NULL,

    -- Doctor fields
    specialization VARCHAR(100) DEFAULT NULL,
    experience INT DEFAULT NULL,
    hospital VARCHAR(255) DEFAULT NULL,
    contact_number VARCHAR(20) DEFAULT NULL,
    working_hours VARCHAR(50) DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
");

$conn->query("
CREATE TABLE IF NOT EXISTS qr_mappings (
    id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(36) NOT NULL,
    qr_code VARCHAR(36) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_qr_code (qr_code),
    INDEX idx_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
");

$conn->query("
CREATE TABLE IF NOT EXISTS medical_records (
    id VARCHAR(36) PRIMARY KEY,
    student_id VARCHAR(36) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    description TEXT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_student_id (student_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
");

$conn->query("
CREATE TABLE IF NOT EXISTS orders (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) NOT NULL,
    product_type ENUM('standard', 'premium') NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    price VARCHAR(20) NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    quantity INT NOT NULL,
    qr_code VARCHAR(36) DEFAULT NULL,
    status ENUM('pending', 'processing', 'shipped', 'delivered') DEFAULT 'pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
");

$conn->query("
CREATE TABLE IF NOT EXISTS feedback (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    subject VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
");

// Helper function to generate UUID
function generateUUID() {
    return sprintf('%04x%04x-%04x-%04x-%04x-%04x%04x%04x',
        mt_rand(0, 0xffff), mt_rand(0, 0xffff),
        mt_rand(0, 0xffff),
        mt_rand(0, 0x0fff) | 0x4000,
        mt_rand(0, 0x3fff) | 0x8000,
        mt_rand(0, 0xffff), mt_rand(0, 0xffff), mt_rand(0, 0xffff)
    );
}

// Helper function to sanitize input
function sanitize($conn, $data) {
    return $conn->real_escape_string(trim($data));
}

// Enable CORS for development
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight OPTIONS request
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}
?>
