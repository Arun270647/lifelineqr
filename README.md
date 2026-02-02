# LifeLine QR - Emergency Medical Information System

A web-based emergency medical information system that uses QR codes to provide instant access to patient medical data during emergencies.

## 🌟 Features

### For Patients
- Register and create medical profile
- Store critical information (blood group, allergies, medical conditions)
- Upload medical documents (PDF, JPG, PNG)
- Generate unique QR code
- Order physical QR medical cards
- Update profile information anytime

### For Doctors
- Register as medical professional
- Search patients using QR code ID
- View complete medical profiles
- Access uploaded medical documents
- Read-only access to patient data

### For Public/First Responders
- Scan QR code to view emergency information
- Access critical details (blood group, allergies, emergency contacts)
- No login required for emergency data

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Storage**: Browser LocalStorage/IndexedDB
- **QR Generation**: QRCode.js library
- **Design**: Medical-themed responsive design

## 📁 Project Structure

```
basic/
├── index.html              # Home page
├── database.sql            # LocalStorage initialization guide
├── css/
│   ├── global.css         # Global styles and variables
│   ├── components.css     # Reusable components
│   └── pages.css          # Page-specific styles
├── js/
│   ├── config.js          # Configuration and constants
│   ├── storage.js         # LocalStorage operations
│   ├── auth.js            # Authentication logic
│   ├── validation.js      # Form validation
│   ├── qr-handler.js      # QR code handling
│   ├── router.js          # Navigation
│   └── main.js            # Main application logic
└── pages/
    ├── role-selection.html       # Choose Doctor/Patient
    ├── register-patient.html     # Patient registration
    ├── register-doctor.html      # Doctor registration
    ├── login.html                # Login page
    ├── patient-dashboard.html    # Patient dashboard
    ├── doctor-dashboard.html     # Doctor dashboard
    ├── doctors-list.html         # List of doctors
    ├── merchandise.html          # QR card shop
    ├── forgot-password.html      # Password reset
    └── contact.html              # Contact page
```

## 🚀 Getting Started

### Installation

1. **Download/Clone the project**
   - No installation required!
   - This is a pure HTML/CSS/JavaScript application

2. **Open the application**
   - Simply open `index.html` in any modern web browser
   - Recommended browsers: Chrome, Firefox, Edge, Safari

### First Time Setup

1. **Initialize Database**
   - The database (LocalStorage) is automatically initialized when you open the app
   - Check `database.sql` for detailed information about data structure

2. **Create Accounts**
   - Click "Sign Up" → Choose role (Patient/Doctor)
   - Fill in the registration form
   - For patients: QR code is automatically generated

3. **Login**
   - Use your registered email and password
   - Patients are redirected to Patient Dashboard
   - Doctors are redirected to Doctor Dashboard

## 📖 Usage Guide

### For Patients

1. **Register**
   - Click "Sign Up" → "Register as Patient"
   - Fill in personal and medical information
   - Submit to receive your QR code

2. **View/Download QR Code**
   - Login to your dashboard
   - Find your QR code in the dashboard
   - Click "Download QR Code" to save as image

3. **Upload Medical Documents**
   - Go to your dashboard
   - Use the "Upload Medical Document" section
   - Select file (PDF/JPG/PNG, max 5MB)
   - Add description and upload

4. **Order QR Card**
   - Navigate to "Merchandise" page
   - Choose Standard (₹299) or Premium (₹599) card
   - Fill in delivery details
   - Place order (simulated)

### For Doctors

1. **Register**
   - Click "Sign Up" → "Register as Doctor"
   - Fill in professional details
   - Submit to create account

2. **Search Patients**
   - Login to doctor dashboard
   - Enter patient's QR code ID
   - Click "Search Patient"
   - View complete medical profile and documents

3. **View Medical Records**
   - Patient medical documents are listed below profile
   - Click "View/Download" to access documents

### For Emergency/Public Access

1. **Scan QR Code**
   - Scan patient's QR code (feature page not included in basic version)
   - View emergency information without login:
     - Name
     - Age
     - Blood Group
     - Allergies
     - Emergency Contacts

## 🔑 Default Credentials

Create new accounts using the registration pages. No default accounts are pre-configured.

## 🗄️ Database Management

### View Data

Open browser console (F12) and run:

```javascript
// View all users
console.log(JSON.parse(localStorage.getItem('lifeline_users')));

// View QR mappings
console.log(JSON.parse(localStorage.getItem('lifeline_qr_mappings')));

// View medical records
console.log(JSON.parse(localStorage.getItem('lifeline_medical_records')));

// View orders
console.log(JSON.parse(localStorage.getItem('lifeline_orders')));
```

### Clear All Data

```javascript
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### Backup Data

```javascript
const backup = {
    users: localStorage.getItem('lifeline_users'),
    records: localStorage.getItem('lifeline_medical_records'),
    qr: localStorage.getItem('lifeline_qr_mappings'),
    orders: localStorage.getItem('lifeline_orders')
};
console.log('BACKUP:', JSON.stringify(backup));
// Copy the output and save to a file
```

### Restore Data

```javascript
// Paste your backup data
const backup = { /* your backup data */ };
localStorage.setItem('lifeline_users', backup.users);
localStorage.setItem('lifeline_medical_records', backup.records);
localStorage.setItem('lifeline_qr_mappings', backup.qr);
localStorage.setItem('lifeline_orders', backup.orders);
location.reload();
```

## 🎨 Customization

### Change Color Theme

Edit `css/global.css`:

```css
:root {
    --primary-blue: #2C5F9E;    /* Change primary color */
    --red-accent: #DC3545;      /* Change accent color */
    --light-blue: #E3F2FD;      /* Change background highlights */
}
```

### Modify Blood Groups

Edit `js/config.js`:

```javascript
BLOOD_GROUPS: ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
```

### Add Doctor Specializations

Edit `js/config.js`:

```javascript
SPECIALIZATIONS: [
    'General Physician',
    'Cardiologist',
    // Add more here
]
```

## 📋 Features Checklist

- ✅ Patient Registration
- ✅ Doctor Registration
- ✅ Login/Logout System
- ✅ QR Code Generation
- ✅ Patient Dashboard
- ✅ Doctor Dashboard
- ✅ Medical Document Upload
- ✅ Doctors List
- ✅ Merchandise Ordering
- ✅ Forgot Password
- ✅ Contact Form
- ✅ Profile Editing
- ✅ Form Validation
- ✅ Responsive Design
- ✅ LocalStorage Database

## 🔒 Security Notes

⚠️ **Important**: This is an educational/demonstration project

- Passwords are encoded with Base64 (NOT secure for production)
- Medical data is stored unencrypted in browser LocalStorage
- No server-side validation or security
- For production use, implement:
  - Proper server-side authentication
  - HTTPS encryption
  - Database with proper security
  - HIPAA/medical data compliance

## 🐛 Troubleshooting

### QR Code Not Displaying
- Ensure QRCode.js library is loaded (check browser console)
- Check internet connection (library loads from CDN)
- Clear browser cache and reload

### Data Not Persisting
- Check if browser allows LocalStorage
- Check LocalStorage quota (usually 5-10MB)
- Try clearing browser data and reinitializing

### File Upload Fails
- Ensure file is under 5MB
- Check file type (PDF, JPG, PNG only)
- Check browser LocalStorage space

### Forgot Password Not Working
- Enter the exact email used during registration
- Email is case-sensitive (stored as lowercase)

## 📝 Browser Compatibility

- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Edge 90+
- ✅ Safari 14+
- ❌ Internet Explorer (not supported)

## 📞 Support

For issues or questions:
- Email: support@lifelineqr.com
- Phone: +91 98765 43210

## 👥 Credits

- **Developed by**: Track My Academy - Dev Ops
- **Prepared for**: Mr. Purvaj Sai
- **QR Library**: QRCode.js by davidshimjs

## 📄 License

This project is created for educational purposes.

## 🔄 Version

Version 1.0.0 - January 2026

---

**Made with ❤️ for emergency medical support**
