// LifeLine QR - LocalStorage Operations

const Storage = {
    // Initialize database tables
    init() {
        const keys = Object.values(CONFIG.STORAGE_KEYS);
        keys.forEach(key => {
            if (!localStorage.getItem(key)) {
                localStorage.setItem(key, JSON.stringify([]));
            }
        });
    },

    // Get all records from a collection
    getAll(key) {
        try {
            const data = localStorage.getItem(key);
            return data ? JSON.parse(data) : [];
        } catch (error) {
            console.error('Error reading from storage:', error);
            return [];
        }
    },

    // Get a single record by ID
    getById(key, id) {
        const records = this.getAll(key);
        return records.find(record => record.id === id);
    },

    // Get records by field value
    getByField(key, field, value) {
        const records = this.getAll(key);
        return records.filter(record => record[field] === value);
    },

    // Find one record by field
    findOne(key, field, value) {
        const records = this.getAll(key);
        return records.find(record => record[field] === value);
    },

    // Add a new record
    add(key, record) {
        try {
            const records = this.getAll(key);

            // Add ID and timestamp if not present
            if (!record.id) {
                record.id = Utils.generateId();
            }
            if (!record.createdAt) {
                record.createdAt = new Date().toISOString();
            }

            records.push(record);
            localStorage.setItem(key, JSON.stringify(records));
            return record;
        } catch (error) {
            console.error('Error adding to storage:', error);
            return null;
        }
    },

    // Update a record
    update(key, id, updates) {
        try {
            const records = this.getAll(key);
            const index = records.findIndex(record => record.id === id);

            if (index === -1) return null;

            records[index] = {
                ...records[index],
                ...updates,
                updatedAt: new Date().toISOString()
            };

            localStorage.setItem(key, JSON.stringify(records));
            return records[index];
        } catch (error) {
            console.error('Error updating storage:', error);
            return null;
        }
    },

    // Delete a record
    delete(key, id) {
        try {
            const records = this.getAll(key);
            const filtered = records.filter(record => record.id !== id);
            localStorage.setItem(key, JSON.stringify(filtered));
            return true;
        } catch (error) {
            console.error('Error deleting from storage:', error);
            return false;
        }
    },

    // Clear all data
    clearAll() {
        Object.values(CONFIG.STORAGE_KEYS).forEach(key => {
            localStorage.setItem(key, JSON.stringify([]));
        });
    }
};

// User-specific storage operations
const UserStorage = {
    // Create new user
    createUser(userData) {
        // Check if email already exists
        const existing = Storage.findOne(CONFIG.STORAGE_KEYS.USERS, 'email', userData.email);
        if (existing) {
            return { success: false, error: 'Email already registered' };
        }

        // Hash password
        userData.password = Utils.hashPassword(userData.password);

        // Add user
        const user = Storage.add(CONFIG.STORAGE_KEYS.USERS, userData);

        if (user) {
            return { success: true, user };
        }
        return { success: false, error: 'Failed to create user' };
    },

    // Get user by email
    getUserByEmail(email) {
        return Storage.findOne(CONFIG.STORAGE_KEYS.USERS, 'email', email);
    },

    // Get user by ID
    getUserById(id) {
        return Storage.getById(CONFIG.STORAGE_KEYS.USERS, id);
    },

    // Update user
    updateUser(id, updates) {
        // Don't allow password updates through this method
        delete updates.password;
        return Storage.update(CONFIG.STORAGE_KEYS.USERS, id, updates);
    },

    // Get all doctors
    getAllDoctors() {
        return Storage.getByField(CONFIG.STORAGE_KEYS.USERS, 'role', CONFIG.ROLES.DOCTOR);
    },

    // Get all students
    getAllStudents() {
        return Storage.getByField(CONFIG.STORAGE_KEYS.USERS, 'role', CONFIG.ROLES.STUDENT);
    }
};

// Medical Records Storage
const MedicalRecordStorage = {
    // Add medical record
    addRecord(studentId, record) {
        record.studentId = studentId;
        return Storage.add(CONFIG.STORAGE_KEYS.MEDICAL_RECORDS, record);
    },

    // Get student's records
    getStudentRecords(studentId) {
        return Storage.getByField(CONFIG.STORAGE_KEYS.MEDICAL_RECORDS, 'studentId', studentId);
    },

    // Delete record
    deleteRecord(recordId) {
        return Storage.delete(CONFIG.STORAGE_KEYS.MEDICAL_RECORDS, recordId);
    }
};

// QR Mapping Storage
const QRStorage = {
    // Create QR mapping
    createMapping(studentId, qrCode) {
        const mapping = {
            studentId,
            qrCode,
            createdAt: new Date().toISOString()
        };
        return Storage.add(CONFIG.STORAGE_KEYS.QR_MAPPINGS, mapping);
    },

    // Get student by QR code
    getStudentByQR(qrCode) {
        const mapping = Storage.findOne(CONFIG.STORAGE_KEYS.QR_MAPPINGS, 'qrCode', qrCode);
        if (mapping) {
            return UserStorage.getUserById(mapping.studentId);
        }
        return null;
    },

    // Get QR by student ID
    getQRByStudent(studentId) {
        return Storage.findOne(CONFIG.STORAGE_KEYS.QR_MAPPINGS, 'studentId', studentId);
    }
};

// Order Storage
const OrderStorage = {
    // Create order
    createOrder(orderData) {
        return Storage.add(CONFIG.STORAGE_KEYS.ORDERS, orderData);
    },

    // Get user's orders
    getUserOrders(userId) {
        return Storage.getByField(CONFIG.STORAGE_KEYS.ORDERS, 'userId', userId);
    },

    // Get order by ID
    getOrderById(orderId) {
        return Storage.getById(CONFIG.STORAGE_KEYS.ORDERS, orderId);
    }
};

// Initialize storage on load
Storage.init();
