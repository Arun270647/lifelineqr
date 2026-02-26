# LifeLine QR - Emergency Medical Information System

A web-based emergency medical information system that uses QR codes to provide instant access to student medical data during emergencies.

## 📈 Project Journey & Evolution

Built from scratch, LifeLine QR has evolved significantly to accommodate robust requirements and advanced technology stacks:

- **Phase 1: Prototype Development**  
  Originally built strictly using HTML, CSS, and Vanilla JavaScript, relying entirely on LocalStorage and IndexedDB to simulate a backend for demo purposes.
- **Phase 2: PHP & MySQL Integration**  
  Transitioned from LocalStorage to a live MySQL database using PHP scripts (`api/` folder). This added data persistence, secure storage, and a structured backend for the application.
- **Phase 3: Python Flask REST API & Admin Architecture**  
  Implemented a full-fledged Python Flask backend (`server.py`) providing modern REST API capabilities. This phase fully centralized the database management (MySQL database named `lifelineqr`), added real administrative access, and structured the user base for scale.

---

## 🌟 Features

### For Students
- **Profile Management**: Register and create a comprehensive medical profile.
- **Critical Info Storage**: Store details like blood group, allergies, regular medications, and emergency contacts.
- **Document Management**: Upload and manage medical documents (PDF/JPG/PNG) securely to the database.
- **QR Code Handling**: Generate, download, and store a unique QR code ID directly linked to the user's medical profile.
- **QR Medical Cards**: Merchandise module to view and order physical QR medical cards.

### For Doctors
- **Professional Registration**: Register as a medical professional, logging specialization and hospital data.
- **Quick Search via QR**: Search and look up students instantly by scanning/entering their unique QR code ID.
- **Complete Profiling**: Gain read-only access to a student's full medical profile and uploaded historical medical documents during treatments.

### For Admins
- **Admin Dashboard**: Specialized endpoints for super admins.
- **Data Overview**: Keep track of total registered students, doctors, and uploaded documents.
- **User Management**: Have the authority to revoke/delete students and malicious doctor accounts to maintain the platform's integrity.

### For Public/First Responders
- **Instant Emergency Access**: Scan a user's QR code to view critical survival information.
- **Crucial Details Included**: Blood group, allergies, existing conditions, and emergency contacts are shown immediately.
- **No Login Required**: Instant unauthenticated access during golden-hour emergencies.

---

## 🛠️ Technology Stack

- **Frontend Core**: HTML5, CSS3, Vanilla JavaScript
- **Backend Alternatives Included**:
  - *Current Recommended Backend*: Python 3 (Flask, Flask-CORS)
  - *Legacy API Backend*: PHP
- **Database**: 
  - *Current*: MySQL (`mysql-connector-python` or PHP PDO)
  - *Legacy Prototype*: Browser LocalStorage / IndexedDB
- **Third-Party Libraries**: QRCode.js (Frontend QR Generation)

---

## 📁 Project Structure

```text
basic/
├── index.html              # Landing Page
├── server.py               # Main Python Flask backend server and API endpoints
├── database.sql            # Legacy LocalStorage initialization guide
├── requirements.txt        # Python pip dependencies
├── css/
│   ├── global.css          # Global styling and CSS variables
│   ├── components.css      # Reusable frontend components
│   └── pages.css           # Highly-specific page styles
├── js/
│   ├── config.js           # Configuration and application constants
│   ├── auth-api.js         # API-driven authentication logic
│   ├── storage-api.js      # API-driven data interactions
│   ├── auth.js & storage.js# Legacy LocalStorage versions 
│   ├── validation.js       # Form validation engine
│   ├── qr-handler.js       # QR code handling library integration
│   ├── router.js           # Navigation system
│   └── main.js             # Main application orchestrator
├── api/                    # PHP backend variant (auth.php, users.php, records.php)
└── pages/
    ├── role-selection.html # Student/Doctor choice
    ├── register-student.html
    ├── register-doctor.html
    ├── login.html
    ├── student-dashboard.html
    ├── doctor-dashboard.html
    └── ...                 # Merchandise, contact, and doctor-lists
```

---

## 🚀 Setup & Installation Guide

LifeLine QR gives you the flexibility to choose how you wish to run the backend engine.

### Option 1: Python Flask Backend (Recommended)

This is the most feature-rich execution path supporting the admin panel out of the box.

1. **Prerequisites**: Make sure you have Python 3 and MySQL server installed.
2. **Install Dependencies**:
   ```bash
   pip install flask flask-cors mysql-connector-python werkzeug
   ```
3. **Database Configuration**:
   The Python server will auto-detect generic MySQL root passwords or an empty password.
   If your MySQL requires a custom password, edit Line 23 of `server.py` (`_MYSQL_PASSWORDS_TO_TRY`).
4. **Boot Server**:
   ```bash
   python server.py
   ```
   *The script will automatically connect to MySQL, create the `lifelineqr` database, and bootstrap all required tables!*
5. **Start Client**: Simply open `index.html` in your web browser. Ensure the scripts in HTML point to the `*-api.js` variants.

### Option 2: PHP Backend (XAMPP/WAMP)

1. Move the `basic` folder into your `htdocs` (XAMPP) or `www` (WAMP) directory.
2. Start Apache and MySQL from your control panel.
3. Access `http://localhost/phpmyadmin` and create a database named `lifeline_qr`.
4. Import the SQL file from the `database/schema.sql` (if available, or follow `DATABASE_SETUP.md`) or use phpMyAdmin to execute queries.
5. In `api/config.php`, ensure database credentials (`DB_USER`, `DB_PASS`) match your setup.
6. Open your browser to `http://localhost/basic/index.html`.

### Option 3: LocalStorage (No Backend Prototype)

1. If you wish to use the original UI without persisting to a live database, simply change your `.html` file inclusions:
   - Change `<script src="../js/storage-api.js"></script>` to `<script src="../js/storage.js"></script>`.
   - Change `<script src="../js/auth-api.js"></script>` to `<script src="../js/auth.js"></script>`.
2. Open `index.html` in your browser. All interactions will be sandboxed to browser LocalStorage.

---

## 🔒 Security & Medical Data Notes

⚠️ **Important**: This is primarily an educational/demonstration project.

- For LocalStorage: Medical data is unencrypted on your browser.
- For Databases: Files are uploaded and stored primarily as Base64 strings.
- Passwords rely on secure hashing in the Python implementation (`werkzeug.security`).
- For true production deployment, you must:
  - Add SSL/HTTPS encryption.
  - Implement HIPAA/medical data compliances.
  - Separate static files/uploads directly to a file server or S3 bucket instead of the database.

---

## 📞 Support

For any technical integration queries or emergency support regarding deployments:
- **Email**: support@lifelineqr.com
- **Phone**: +91 98765 43210

**Developed by**: Track My Academy - Dev Ops  
