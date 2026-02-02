<?php
require_once 'config.php';

// Get request method
$method = $_SERVER['REQUEST_METHOD'];

// Handle different request types
switch ($method) {
    case 'POST':
        // Register new user
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (!$data) {
            echo json_encode(['success' => false, 'error' => 'Invalid request data']);
            exit();
        }
        
        // Validate required fields
        $requiredFields = ['email', 'password', 'name', 'role'];
        foreach ($requiredFields as $field) {
            if (!isset($data[$field]) || empty($data[$field])) {
                echo json_encode(['success' => false, 'error' => ucfirst($field) . ' is required']);
                exit();
            }
        }
        
        // Check if email already exists
        $email = sanitize($conn, $data['email']);
        $checkSql = "SELECT id FROM users WHERE email = ?";
        $stmt = $conn->prepare($checkSql);
        $stmt->bind_param('s', $email);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows > 0) {
            echo json_encode(['success' => false, 'error' => 'Email already registered']);
            exit();
        }
        
        // Generate user ID
        $userId = generateUUID();
        
        // Prepare data
        $role = sanitize($conn, $data['role']);
        $name = sanitize($conn, $data['name']);
        $age = isset($data['age']) ? intval($data['age']) : 0;
        $password = sanitize($conn, $data['password']); // Already hashed from frontend
        
        // Build insert query based on role
        if ($role === 'patient') {
            $sql = "INSERT INTO users (id, role, name, age, email, password, blood_group, allergies, 
                    medical_conditions, regular_medications, address, emergency_contacts) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            
            $stmt = $conn->prepare($sql);
            $bloodGroup = sanitize($conn, $data['bloodGroup'] ?? '');
            $allergies = sanitize($conn, $data['allergies'] ?? '');
            $conditions = sanitize($conn, $data['medicalConditions'] ?? '');
            $medications = sanitize($conn, $data['regularMedications'] ?? '');
            $address = sanitize($conn, $data['address'] ?? '');
            $emergency = sanitize($conn, $data['emergencyContacts'] ?? '');
            
            $stmt->bind_param('sssississsss', $userId, $role, $name, $age, $email, $password,
                            $bloodGroup, $allergies, $conditions, $medications, $address, $emergency);
            
        } else if ($role === 'doctor') {
            $sql = "INSERT INTO users (id, role, name, age, email, password, specialization, 
                    experience, hospital, contact_number, working_hours) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
            
            $stmt = $conn->prepare($sql);
            $specialization = sanitize($conn, $data['specialization'] ?? '');
            $experience = isset($data['experience']) ? intval($data['experience']) : 0;
            $hospital = sanitize($conn, $data['hospital'] ?? '');
            $contactNumber = sanitize($conn, $data['contactNumber'] ?? '');
            $workingHours = sanitize($conn, $data['workingHours'] ?? '');
            
            $stmt->bind_param('sssississss', $userId, $role, $name, $age, $email, $password,
                            $specialization, $experience, $hospital, $contactNumber, $workingHours);
        } else {
            echo json_encode(['success' => false, 'error' => 'Invalid role']);
            exit();
        }
        
        if ($stmt->execute()) {
            // If patient, create QR mapping
            if ($role === 'patient') {
                $qrCode = generateUUID();
                $qrId = generateUUID();
                $qrSql = "INSERT INTO qr_mappings (id, patient_id, qr_code) VALUES (?, ?, ?)";
                $qrStmt = $conn->prepare($qrSql);
                $qrStmt->bind_param('sss', $qrId, $userId, $qrCode);
                $qrStmt->execute();
            }
            
            echo json_encode([
                'success' => true,
                'user' => [
                    'id' => $userId,
                    'email' => $email,
                    'name' => $name,
                    'role' => $role
                ]
            ]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to create user']);
        }
        break;
        
    case 'GET':
        // Get user by email or ID
        if (isset($_GET['email'])) {
            $email = sanitize($conn, $_GET['email']);
            $sql = "SELECT * FROM users WHERE email = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $email);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $user = $result->fetch_assoc();
                echo json_encode(['success' => true, 'user' => $user]);
            } else {
                echo json_encode(['success' => false, 'error' => 'User not found']);
            }
        } else if (isset($_GET['id'])) {
            $id = sanitize($conn, $_GET['id']);
            $sql = "SELECT * FROM users WHERE id = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $id);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $user = $result->fetch_assoc();
                echo json_encode(['success' => true, 'user' => $user]);
            } else {
                echo json_encode(['success' => false, 'error' => 'User not found']);
            }
        } else if (isset($_GET['role'])) {
            // Get all users by role (e.g., all doctors)
            $role = sanitize($conn, $_GET['role']);
            $sql = "SELECT * FROM users WHERE role = ? ORDER BY created_at DESC";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $role);
            $stmt->execute();
            $result = $stmt->get_result();
            
            $users = [];
            while ($row = $result->fetch_assoc()) {
                unset($row['password']); // Don't send passwords
                $users[] = $row;
            }
            
            echo json_encode(['success' => true, 'users' => $users]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Missing parameters']);
        }
        break;
        
    case 'PUT':
        // Update user
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($data['id'])) {
            echo json_encode(['success' => false, 'error' => 'User ID required']);
            exit();
        }
        
        $id = sanitize($conn, $data['id']);
        unset($data['id']);
        unset($data['password']); // Don't allow password updates through this endpoint
        
        // Build update query dynamically
        $updates = [];
        $types = '';
        $values = [];
        
        foreach ($data as $key => $value) {
            $updates[] = "$key = ?";
            $types .= 's';
            $values[] = sanitize($conn, $value);
        }
        
        if (empty($updates)) {
            echo json_encode(['success' => false, 'error' => 'No data to update']);
            exit();
        }
        
        $sql = "UPDATE users SET " . implode(', ', $updates) . " WHERE id = ?";
        $types .= 's';
        $values[] = $id;
        
        $stmt = $conn->prepare($sql);
        $stmt->bind_param($types, ...$values);
        
        if ($stmt->execute()) {
            echo json_encode(['success' => true, 'message' => 'User updated successfully']);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to update user']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Method not allowed']);
        break;
}

$conn->close();
?>
