// LifeLine QR - Configuration and Constants

const CONFIG = {
    APP_NAME: 'LifeLine QR',
    VERSION: '1.0.0',

    // LocalStorage Keys
    STORAGE_KEYS: {
        USERS: 'lifeline_users',
        MEDICAL_RECORDS: 'lifeline_medical_records',
        QR_MAPPINGS: 'lifeline_qr_mappings',
        ORDERS: 'lifeline_orders',
        CURRENT_USER: 'lifeline_current_user'
    },

    // User Roles
    ROLES: {
        STUDENT: 'student',
        DOCTOR: 'doctor'
    },

    // Blood Groups
    BLOOD_GROUPS: [
        'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'
    ],

    // Doctor Specializations
    SPECIALIZATIONS: [
        'General Physician',
        'Cardiologist',
        'Neurologist',
        'Orthopedic',
        'Pediatrician',
        'Dermatologist',
        'ENT Specialist',
        'Gynecologist',
        'Psychiatrist',
        'Dentist',
        'Ophthalmologist',
        'Radiologist',
        'Anesthesiologist',
        'Surgeon',
        'Other'
    ],

    // File Upload Settings
    FILE_UPLOAD: {
        MAX_SIZE: 5 * 1024 * 1024, // 5MB
        ALLOWED_TYPES: ['image/jpeg', 'image/png', 'application/pdf'],
        ALLOWED_EXTENSIONS: ['jpg', 'jpeg', 'png', 'pdf']
    },

    // Emergency Info Fields (visible to guest users)
    EMERGENCY_FIELDS: [
        'name',
        'age',
        'bloodGroup',
        'allergies',
        'emergencyContacts'
    ]
};

// Utility Functions
const Utils = {
    // Generate unique ID
    generateId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },

    // Simple password hashing (Base64 encoding for educational purposes)
    hashPassword(password) {
        return btoa(password + CONFIG.APP_NAME);
    },

    // Verify password
    verifyPassword(password, hash) {
        return this.hashPassword(password) === hash;
    },

    // Format date
    formatDate(date) {
        if (!date) return '';
        const d = new Date(date);
        return d.toLocaleDateString('en-IN', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    // Sanitize input
    sanitize(input) {
        if (typeof input !== 'string') return input;
        const div = document.createElement('div');
        div.textContent = input;
        return div.innerHTML;
    },

    // Show alert message
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;

        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);

        setTimeout(() => {
            alertDiv.remove();
        }, 5000);
    },

    // Show modal
    showModal(title, content) {
        const modal = document.getElementById('modal');
        if (!modal) return;

        const modalTitle = modal.querySelector('.modal-title');
        const modalBody = modal.querySelector('.modal-body');

        if (modalTitle) modalTitle.textContent = title;
        if (modalBody) modalBody.innerHTML = content;

        modal.classList.add('active');
    },

    // Close modal
    closeModal() {
        const modal = document.getElementById('modal');
        if (modal) {
            modal.classList.remove('active');
        }
    },

    // Convert file to Base64
    fileToBase64(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = () => resolve(reader.result);
            reader.onerror = error => reject(error);
            reader.readAsDataURL(file);
        });
    },

    // Get file extension
    getFileExtension(filename) {
        return filename.slice((filename.lastIndexOf('.') - 1 >>> 0) + 2).toLowerCase();
    },

    // Validate file
    validateFile(file) {
        const errors = [];

        if (file.size > CONFIG.FILE_UPLOAD.MAX_SIZE) {
            errors.push('File size must be less than 5MB');
        }

        const ext = this.getFileExtension(file.name);
        if (!CONFIG.FILE_UPLOAD.ALLOWED_EXTENSIONS.includes(ext)) {
            errors.push('Only JPG, PNG, and PDF files are allowed');
        }

        if (!CONFIG.FILE_UPLOAD.ALLOWED_TYPES.includes(file.type)) {
            errors.push('Invalid file type');
        }

        return {
            valid: errors.length === 0,
            errors
        };
    }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { CONFIG, Utils };
}
