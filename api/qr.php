<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'POST':
        // Add QR mapping or get patient by QR
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (isset($data['action']) && $data['action'] === 'getPatient') {
            // Get patient by QR code
            $qrCode = sanitize($conn, $data['qrCode']);
            
            $sql = "SELECT u.* FROM users u 
                    INNER JOIN qr_mappings qm ON u.id = qm.patient_id 
                    WHERE qm.qr_code = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $qrCode);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $patient = $result->fetch_assoc();
                unset($patient['password']);
                echo json_encode(['success' => true, 'patient' => $patient]);
            } else {
                echo json_encode(['success' => false, 'error' => 'Invalid QR code']);
            }
        } else {
            echo json_encode(['success' => false, 'error' => 'Invalid action']);
        }
        break;
        
    case 'GET':
        // Get QR by patient ID
        if (isset($_GET['patientId'])) {
            $patientId = sanitize($conn, $_GET['patientId']);
            
            $sql = "SELECT * FROM qr_mappings WHERE patient_id = ?";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $patientId);
            $stmt->execute();
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $mapping = $result->fetch_assoc();
                echo json_encode(['success' => true, 'mapping' => $mapping]);
            } else {
                echo json_encode(['success' => false, 'error' => 'QR mapping not found']);
            }
        } else {
            echo json_encode(['success' => false, 'error' => 'Patient ID required']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Method not allowed']);
        break;
}

$conn->close();
?>
