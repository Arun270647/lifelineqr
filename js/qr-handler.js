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

    // Get patient QR code
    getPatientQRCode(patientId) {
        const mapping = QRStorage.getQRByPatient(patientId);
        return mapping ? mapping.qrCode : null;
    },

    // Get patient info from QR code
    getPatientFromQR(qrCode) {
        return QRStorage.getPatientByQR(qrCode);
    },

    // Get patient data based on access level
    getPatientData(qrCode, isDoctor = false) {
        const patient = this.getPatientFromQR(qrCode);

        if (!patient) {
            return {
                success: false,
                error: 'Invalid QR code'
            };
        }

        // If not a doctor (guest access), return only emergency info
        if (!isDoctor) {
            const emergencyData = {};
            CONFIG.EMERGENCY_FIELDS.forEach(field => {
                emergencyData[field] = patient[field];
            });

            return {
                success: true,
                data: emergencyData,
                accessLevel: 'emergency'
            };
        }

        // Doctor has full access (except password)
        const fullData = { ...patient };
        delete fullData.password;

        // Get medical records
        const records = MedicalRecordStorage.getPatientRecords(patient.id);

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
        return `${baseURL}/pages/view-patient.html?qr=${qrCode}`;
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
