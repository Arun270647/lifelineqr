<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'POST':
        // Add QR mapping or get student by QR
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (isset($data['action']) && $data['action'] === 'getStudent') {
            // Get student by QR code
            $qrCode = sanitize($conn, $data['qrCode']);
            
            $sql = "SELECT u.* FROM users u 
                    INNER JOIN qr_mappings qm ON u.id = qm.student_id 
                    WHERE qm.qr_code = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $qrCode);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $student = $result->fetch_assoc();
                unset($student['password']);
                echo json_encode(['success' => true, 'student' => $student]);
            } else {
                echo json_encode(['success' => false, 'error' => 'Invalid QR code']);
            }
        } else {
            echo json_encode(['success' => false, 'error' => 'Invalid action']);
        }
        break;
        
    case 'GET':
        // Get QR by student ID
        if (isset($_GET['studentId'])) {
            $studentId = sanitize($conn, $_GET['studentId']);
            
            $sql = "SELECT * FROM qr_mappings WHERE student_id = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $studentId);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $mapping = $result->fetch_assoc();
                echo json_encode(['success' => true, 'mapping' => $mapping]);
            } else {
                echo json_encode(['success' => false, 'error' => 'QR mapping not found']);
            }
        } else {
            echo json_encode(['success' => false, 'error' => 'Student ID required']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Method not allowed']);
        break;
}

$conn->close();
?>
