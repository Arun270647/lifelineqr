# LifeLine QR - SQL Database Setup Guide

## Prerequisites

You need a local web server with PHP and MySQL. Choose one:

### Option 1: XAMPP (Recommended for Windows)
1. Download XAMPP from https://www.apachefriends.org/
2. Install XAMPP
3. Start Apache and MySQL from XAMPP Control Panel

### Option 2: WAMP (Windows)
1. Download WAMP from https://www.wampserver.com/
2. Install and start WAMP

### Option 3: MAMP (Mac)
1. Download MAMP from https://www.mamp.info/
2. Install and start MAMP

---

## Setup Steps

### Step 1: Move Project to Web Server Directory

**For XAMPP:**
Move the `basic` folder to: `C:\xampp\htdocs\`

**For WAMP:**
Move the `basic` folder to: `C:\wamp64\www\`

**For MAMP:**
Move the `basic` folder to: `/Applications/MAMP/htdocs/`

### Step 2: Create MySQL Database

1. Open your web browser
2. Go to: `http://localhost/phpmyadmin`
3. Click on "New" in the left sidebar
4. Create a new database named: `lifeline_qr`
5. Click on the `lifeline_qr` database
6. Click on "SQL" tab
7. Copy and paste the entire contents of `database/schema.sql`
8. Click "Go" to execute

### Step 3: Configure Database Connection

1. Open `api/config.php`
2. Update these lines if needed:
   ```php
   define('DB_HOST', 'localhost');
   define('DB_USER', 'root');          // Your MySQL username
   define('DB_PASS', '');              // Your MySQL password (usually empty for local)
   define('DB_NAME', 'lifeline_qr');
   ```

### Step 4: Update API URL in JavaScript

1. Open `js/storage-api.js`
2. Update line 4:
   ```javascript
   const API_BASE_URL = 'http://localhost/basic/api';
   ```
   Change `basic` to your folder name if different

### Step 5: Update HTML Files to Use API Version

You need to change the script references in all HTML files:

**Replace:**
```html
<script src="../js/storage.js"></script>
<script src="../js/auth.js"></script>
```

**With:**
```html
<script src="../js/storage-api.js"></script>
<script src="../js/auth-api.js"></script>
```

**Files to update:**
- pages/register-patient.html
- pages/register-doctor.html
- pages/login.html
- pages/patient-dashboard.html
- pages/doctor-dashboard.html
- pages/doctors-list.html
- pages/merchandise.html
- pages/forgot-password.html

---

## Testing the Database Connection

1. Open browser: `http://localhost/basic/api/config.php`
2. If you see a blank page with no errors = success!
3. If you see an error, check:
   - XAMPP/WAMP is running
   - Database credentials in `api/config.php` are correct
   - Database `lifeline_qr` is created

---

## Test API Endpoints

Open browser console (F12) and test:

```javascript
// Test getting doctors
fetch('http://localhost/basic/api/users.php?role=doctor')
  .then(r => r.json())
  .then(console.log);
```

---

## Using the Application

1. **Access the app:**
   ```
   http://localhost/basic/index.html
   ```

2. **Register a patient:**
   - Data will be stored in MySQL `users` table
   - QR code mapping in `qr_mappings` table

3. **Check database:**
   - Go to phpMyAdmin: `http://localhost/phpmyadmin`
   - Click `lifeline_qr` database
   - Click `users` table
   - Click "Browse" to see registered users

---

## Database Tables

After setup, you'll have these tables:

1. **users** - All patients and doctors
2. **qr_mappings** - QR code to patient mapping
3. **medical_records** - Patient document metadata
4. **orders** - Merchandise orders
5. **feedback** - Contact form submissions

---

## Common Issues

### Error: "Connection failed"
- Check if MySQL is running in XAMPP/WAMP
- Verify database credentials in `api/config.php`
- Make sure database `lifeline_qr` exists

### Error: "CORS policy"
- Make sure you're accessing via `http://localhost` not `file://`
- CORS headers are already set in `api/config.php`

### Error: "Table doesn't exist"
- Run the SQL schema from `database/schema.sql` in phpMyAdmin
- Make sure you selected the correct database

### Registration doesn't work
- Open browser console (F12) to see errors
- Check API_BASE_URL in `js/storage-api.js`
- Make sure HTML files are using `storage-api.js` and `auth-api.js`

---

## File Upload Location

Medical documents are currently stored as Base64 in the database.

For production, you should:
1. Store files on server in `uploads/` folder
2. Save only file path in database
3. Use PHP file upload handling

---

## Security Notes

⚠️ **This is a development setup. For production:**

1. Change MySQL password
2. Don't use `root` user
3. Enable HTTPS
4. Add proper authentication tokens
5. Validate and sanitize all inputs (already done in PHP)
6. Add rate limiting
7. Use environment variables for configs

---

## Quick Commands

**View all users:**
```sql
SELECT * FROM users;
```

**View QR mappings:**
```sql
SELECT u.name, qm.qr_code 
FROM users u 
JOIN qr_mappings qm ON u.id = qm.patient_id;
```

**Delete all data:**
```sql
TRUNCATE TABLE orders;
TRUNCATE TABLE medical_records;
TRUNCATE TABLE qr_mappings;
TRUNCATE TABLE users;
TRUNCATE TABLE feedback;
```

---

## Next Steps

After setup:

1. ✅ Register a test patient
2. ✅ Check database to see if data is saved
3. ✅ Login with patient credentials
4. ✅ Register a doctor
5. ✅ Test doctor searching for patient by QR

---

**Support:** If you encounter issues, check:
1. XAMPP/WAMP control panel - both Apache and MySQL are green
2. phpMyAdmin is accessible
3. Database is created and tables exist
4. API URL in JavaScript matches your setup
