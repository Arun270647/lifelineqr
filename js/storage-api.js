// LifeLine QR - API Storage (replaces LocalStorage with MySQL database)

// API Base URL - change this to your local server URL
const API_BASE_URL = 'http://localhost/basic/api'; // Change if needed

// Storage object with API calls
const Storage = {
    // API helper function
    async apiCall(endpoint, method = 'GET', data = null) {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };

        if (data && (method === 'POST' || method === 'PUT' || method === 'DELETE')) {
            options.body = JSON.stringify(data);
        }

        try {
            const response = await fetch(`${API_BASE_URL}/${endpoint}`, options);
            const result = await response.json();
            return result;
        } catch (error) {
            console.error('API Error:', error);
            return { success: false, error: 'Network error: ' + error.message };
        }
    },

    // Initialize - not needed for API version
    init() {
        console.log('Using API storage with MySQL database');
    }
};

// User Storage Operations
const UserStorage = {
    // Create new user
    async createUser(userData) {
        const result = await Storage.apiCall('users.php', 'POST', userData);
        return result;
    },

    // Get user by email
    async getUserByEmail(email) {
        const result = await Storage.apiCall(`users.php?email=${encodeURIComponent(email)}`);
        return result.success ? result.user : null;
    },

    // Get user by ID
    async getUserById(id) {
        const result = await Storage.apiCall(`users.php?id=${encodeURIComponent(id)}`);
        return result.success ? result.user : null;
    },

    // Update user
    async updateUser(id, updates) {
        updates.id = id;
        const result = await Storage.apiCall('users.php', 'PUT', updates);
        return result.success;
    },

    // Get all doctors
    async getAllDoctors() {
        const result = await Storage.apiCall('users.php?role=doctor');
        return result.success ? result.users : [];
    },

    // Get all patients
    async getAllPatients() {
        const result = await Storage.apiCall('users.php?role=patient');
        return result.success ? result.users : [];
    }
};

// Medical Records Storage
const MedicalRecordStorage = {
    // Add medical record
    async addRecord(patientId, record) {
        record.patientId = patientId;
        // For file data, we'll still use LocalStorage or base64 in file_path field
        record.filePath = record.fileData || ''; // Store base64 data
        const result = await Storage.apiCall('records.php', 'POST', record);
        return result.success ? result.record : null;
    },

    // Get patient's records
    async getPatientRecords(patientId) {
        const result = await Storage.apiCall(`records.php?patientId=${encodeURIComponent(patientId)}`);
        return result.success ? result.records : [];
    },

    // Delete record
    async deleteRecord(recordId) {
        const result = await Storage.apiCall('records.php', 'DELETE', { id: recordId });
        return result.success;
    }
};

// QR Storage Operations
const QRStorage = {
    // QR mapping is created automatically during user registration in users.php

    // Get patient by QR code
    async getPatientByQR(qrCode) {
        const result = await Storage.apiCall('qr.php', 'POST', {
            action: 'getPatient',
            qrCode: qrCode
        });
        return result.success ? result.patient : null;
    },

    // Get QR by patient ID
    async getQRByPatient(patientId) {
        const result = await Storage.apiCall(`qr.php?patientId=${encodeURIComponent(patientId)}`);
        return result.success ? result.mapping : null;
    }
};

// Order Storage
const OrderStorage = {
    // Create order
    async createOrder(orderData) {
        const result = await Storage.apiCall('orders.php', 'POST', orderData);
        return result.success ? result.order : null;
    },

    // Get user's orders
    async getUserOrders(userId) {
        const result = await Storage.apiCall(`orders.php?userId=${encodeURIComponent(userId)}`);
        return result.success ? result.orders : [];
    }
};

// Initialize
Storage.init();
