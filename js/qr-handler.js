// LifeLine QR - QR Code Handler

const QRHandler = {
    // Generate QR code and display
    generateQR(elementId, data) {
        // Clear existing QR code
        const element = document.getElementById(elementId);
        if (!element) {
            console.error('QR element not found');
            return;
        }

        element.innerHTML = '';

        // Generate QR code using QRCode.js library
        new QRCode(element, {
            text: data,
            width: 200,
            height: 200,
            colorDark: '#2C5F9E',
            colorLight: '#ffffff',
            correctLevel: QRCode.CorrectLevel.H
        });
    },

    // Get student QR code
    getStudentQRCode(studentId) {
        const mapping = QRStorage.getQRByStudent(studentId);
        return mapping ? mapping.qrCode : null;
    },

    // Get student info from QR code
    getStudentFromQR(qrCode) {
        return QRStorage.getStudentByQR(qrCode);
    },

    // Get student data based on access level
    getStudentData(qrCode, isDoctor = false) {
        const student = this.getStudentFromQR(qrCode);

        if (!student) {
            return {
                success: false,
                error: 'Invalid QR code'
            };
        }

        // If not a doctor (guest access), return only emergency info
        if (!isDoctor) {
            const emergencyData = {};
            CONFIG.EMERGENCY_FIELDS.forEach(field => {
                emergencyData[field] = student[field];
            });

            return {
                success: true,
                data: emergencyData,
                accessLevel: 'emergency'
            };
        }

        // Doctor has full access (except password)
        const fullData = { ...student };
        delete fullData.password;

        // Get medical records
        const records = MedicalRecordStorage.getStudentRecords(student.id);

        return {
            success: true,
            data: fullData,
            medicalRecords: records,
            accessLevel: 'full'
        };
    },

    // Generate QR code URL
    generateQRURL(qrCode) {
        const baseURL = window.location.origin;
        return `${baseURL}/pages/view-student.html?qr=${qrCode}`;
    },

    // Download QR code as image
    downloadQR(elementId, filename = 'qr-code.png') {
        const element = document.getElementById(elementId);
        if (!element) return;

        const canvas = element.querySelector('canvas');
        if (!canvas) return;

        const link = document.createElement('a');
        link.download = filename;
        link.href = canvas.toDataURL();
        link.click();
    }
};
