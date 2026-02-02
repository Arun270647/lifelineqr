<?php
require_once 'config.php';

$method = $_SERVER['REQUEST_METHOD'];

switch ($method) {
    case 'POST':
        // Create order
        $data = json_decode(file_get_contents('php://input'), true);
        
        $id = generateUUID();
        $userId = sanitize($conn, $data['userId']);
        $productType = sanitize($conn, $data['productType']);
        $productName = sanitize($conn, $data['productName']);
        $price = sanitize($conn, $data['price']);
        $customerName = sanitize($conn, $data['customerName']);
        $phone = sanitize($conn, $data['phone']);
        $address = sanitize($conn, $data['address']);
        $quantity = intval($data['quantity']);
        $qrCode = isset($data['qrCode']) ? sanitize($conn, $data['qrCode']) : NULL;
        
        $sql = "INSERT INTO orders (id, user_id, product_type, product_name, price, customer_name, 
                phone, address, quantity, qr_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param('ssssssssis', $id, $userId, $productType, $productName, $price, 
                        $customerName, $phone, $address, $quantity, $qrCode);
        
        if ($stmt->execute()) {
            echo json_encode([
                'success' => true,
                'order' => [
                    'id' => $id,
                    'status' => 'pending'
                ]
            ]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to create order']);
        }
        break;
        
    case 'GET':
        // Get orders by user ID
        if (isset($_GET['userId'])) {
            $userId = sanitize($conn, $_GET['userId']);
            
            $sql = "SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC";
            $stmt = $conn->prepare($sql);
            $stmt->bind_param('s', $userId);
            $stmt->execute();
            $result = $stmt->get_result();
            
            $orders = [];
            while ($row = $result->fetch_assoc()) {
                $orders[] = $row;
            }
            
            echo json_encode(['success' => true, 'orders' => $orders]);
        } else {
            echo json_encode(['success' => false, 'error' => 'User ID required']);
        }
        break;
        
    default:
        echo json_encode(['success' => false, 'error' => 'Method not allowed']);
        break;
}

$conn->close();
?>
