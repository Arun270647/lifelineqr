<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'POST':
        // Upload medical record (metadata only - files stored separately)
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($data['patientId']) || !isset($data['filename'])) {
            echo json_encode(['success' => false, 'error' => 'Patient ID and filename required']);
            exit();
        }
        
        $id = generateUUID();
        $patientId = sanitize($conn, $data['patientId']);
        $filename = sanitize($conn, $data['filename']);
        $fileType = sanitize($conn, $data['fileType'] ?? '');
        $filePath = sanitize($conn, $data['filePath'] ?? ''); // Store file path or data
        $description = sanitize($conn, $data['description'] ?? '');
        
        $sql = "INSERT INTO medical_records (id, patient_id, filename, file_type, file_path, description) 
                VALUES (?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param('ssssss', $id, $patientId, $filename, $fileType, $filePath, $description);
        
        if ($stmt->execute()) {
            echo json_encode([
                'success' => true,
                'record' => [
                    'id' => $id,
                    'filename' => $filename,
                    'description' => $description
                ]
            ]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to add record']);
        }
        break;
        
    case 'GET':
        // Get records by patient ID
        if (isset($_GET['patientId'])) {
            $patientId = sanitize($conn, $_GET['patientId']);
            
            $sql = "SELECT * FROM medical_records WHERE patient_id = ? ORDER BY created_at DESC";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $patientId);
            $stmt->execute();
            $result = $stmt->get_result();
            
            $records = [];
            while ($row = $result->fetch_assoc()) {
                $records[] = $row;
            }
            
            echo json_encode(['success' => true, 'records' => $records]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Patient ID required']);
        }
        break;
        
    case 'DELETE':
        // Delete medical record
        $data = json_decode(file_get_contents('php://input'), true);
        
        if (!isset($data['id'])) {
            echo json_encode(['success' => false, 'error' => 'Record ID required']);
            exit();
        }
        
        $id = sanitize($conn, $data['id']);
        
        $sql = "DELETE FROM medical_records WHERE id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param('s', $id);
        
        if ($stmt->execute()) {
            echo json_encode(['success' => true, 'message' => 'Record deleted']);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to delete record']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Method not allowed']);
        break;
}

$conn->close();
?>
