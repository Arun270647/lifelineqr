<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'POST':
        // Login
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($data['email']) || !isset($data['password'])) {
            echo json_encode(['success' => false, 'error' => 'Email and password required']);
            exit();
        }
        
        $email = sanitize($conn, $data['email']);
        $password = sanitize($conn, $data['password']); // Already hashed
        
        $sql = "SELECT * FROM users WHERE email = ? AND password = ?";
        $stmt = $conn->prepare($sql);
        if (!$stmt) {
            echo json_encode(['success' => false, 'error' => 'DB error: ' . $conn->error]);
            exit();
        }
        $stmt->bind_param('ss', $email, $password);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows > 0) {
            $user = $result->fetch_assoc();
            unset($user['password']); // Don't send password back
            echo json_encode(['success' => true, 'user' => $user]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Invalid email or password']);
        }
        break;
        
    case 'PUT':
        // Reset password
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($data['email'])) {
            echo json_encode(['success' => false, 'error' => 'Email required']);
            exit();
        }
        
        $email = sanitize($conn, $data['email']);
        
        // Check if user exists
        $checkSql = "SELECT id FROM users WHERE email = ?";
        $stmt = $conn->prepare($checkSql);
        if (!$stmt) {
            echo json_encode(['success' => false, 'error' => 'DB error: ' . $conn->error]);
            exit();
        }
        $stmt->bind_param('s', $email);
        $stmt->execute();
        $result = $stmt->get_result();
        
        if ($result->num_rows === 0) {
            echo json_encode(['success' => false, 'error' => 'Email not found']);
            exit();
        }
        
        $user = $result->fetch_assoc();
        
        // Generate temporary password
        $tempPassword = 'Temp' . rand(1000, 9999);
        $hashedPassword = base64_encode($tempPassword . 'LifeLine QR'); // Match frontend hashing
        
        // Update password
        $updateSql = "UPDATE users SET password = ? WHERE id = ?";
        $updateStmt = $conn->prepare($updateSql);
        $updateStmt->bind_param('ss', $hashedPassword, $user['id']);
        
        if ($updateStmt->execute()) {
            echo json_encode([
                'success' => true,
                'message' => 'Password reset successful',
                'tempPassword' => $tempPassword
            ]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to reset password']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Method not allowed']);
        break;
}

$conn->close();
?>
