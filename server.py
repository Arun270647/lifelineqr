"""
LifelineQR - Python Flask Backend
Handles doctor and patient registration via REST API,
stores data in MySQL 'lifelineqr' database.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

# ── MySQL connection config ──────────────────────────────────────────────────
# Try common MySQL root passwords so the app works on any machine.
# The first password that connects successfully will be used.
# If none work, update the password below to match YOUR MySQL root password.
_MYSQL_HOST = 'localhost'
_MYSQL_USER = 'root'
_MYSQL_DB   = 'lifelineqr'
_MYSQL_PASSWORDS_TO_TRY = [
    '',           # XAMPP / WAMP default (no password)
    'sjssjs',     # Original developer password
    'root',       # Common default
    'mysql',      # Common default
    'password',   # Common default
]

# Auto-detect the correct password
_detected_password = None
for _pwd in _MYSQL_PASSWORDS_TO_TRY:
    try:
        _test = mysql.connector.connect(
            host=_MYSQL_HOST, user=_MYSQL_USER, password=_pwd
        )
        _test.close()
        _detected_password = _pwd
        break
    except mysql.connector.Error:
        continue

if _detected_password is None:
    print("=" * 60)
    print("  ERROR: Could not connect to MySQL with any known password!")
    print("  Open server.py and add your MySQL root password to")
    print("  the _MYSQL_PASSWORDS_TO_TRY list (around line 24).")
    print("=" * 60)
    _detected_password = ''  # fallback – will fail with a clear message at runtime

DB_CONFIG = {
    'host': _MYSQL_HOST,
    'user': _MYSQL_USER,
    'password': _detected_password,
    'database': _MYSQL_DB
}

def get_db():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


def _bootstrap_database():
    """Create the database and tables if they do not exist."""
    try:
        conn = mysql.connector.connect(
            host=_MYSQL_HOST, user=_MYSQL_USER, password=_detected_password
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{_MYSQL_DB}`")
        cursor.close()
        conn.close()

        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS patients (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                blood_group VARCHAR(5),
                allergies TEXT,
                medical_conditions TEXT,
                regular_medications TEXT,
                address TEXT,
                emergency_contacts VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doctors (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                age INT NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                specialization VARCHAR(100),
                experience INT,
                hospital VARCHAR(255),
                contact_number VARCHAR(20),
                working_hours VARCHAR(50),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL,
                file_data LONGTEXT NOT NULL,
                description TEXT,
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert default admin if not exists
        cursor.execute("""
            INSERT IGNORE INTO admins (username, password)
            VALUES ('admin', 'admin@123')
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("  ✓ Database and tables verified / created")
    except mysql.connector.Error as err:
        print(f"  ✗ Database bootstrap error: {err}")


_bootstrap_database()


# ── Patient endpoints ────────────────────────────────────────────────────────

@app.route('/api/register/patient', methods=['POST'])
def register_patient():
    """Register a new patient."""
    data = request.get_json()

    required = ['name', 'age', 'email', 'password']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'{field} is required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute('SELECT id FROM patients WHERE email = %s', (data['email'],))
        if cursor.fetchone():
            return jsonify({'success': False, 'error': 'Email already registered'}), 409

        hashed_pw = data['password']

        sql = '''INSERT INTO patients
                 (name, age, email, password, blood_group, allergies,
                  medical_conditions, regular_medications, address, emergency_contacts)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        values = (
            data['name'],
            int(data['age']),
            data['email'].lower(),
            hashed_pw,
            data.get('bloodGroup', ''),
            data.get('allergies', ''),
            data.get('medicalConditions', ''),
            data.get('regularMedications', ''),
            data.get('address', ''),
            data.get('emergencyContacts', '')
        )

        cursor.execute(sql, values)
        conn.commit()

        patient_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Patient registered successfully',
            'patient_id': patient_id
        }), 201

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/patients', methods=['GET'])
def get_patients():
    """Get all patients."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, age, email, blood_group, allergies, '
                       'medical_conditions, regular_medications, address, '
                       'emergency_contacts, created_at FROM patients')
        patients = cursor.fetchall()

        # Convert datetime objects to strings
        for p in patients:
            if p.get('created_at'):
                p['created_at'] = p['created_at'].isoformat()

        cursor.close()
        conn.close()
        return jsonify({'success': True, 'patients': patients})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/patient/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a single patient by ID."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, age, email, blood_group, allergies, '
                       'medical_conditions, regular_medications, address, '
                       'emergency_contacts, created_at FROM patients WHERE id = %s',
                       (patient_id,))
        patient = cursor.fetchone()
        cursor.close()
        conn.close()

        if not patient:
            return jsonify({'success': False, 'error': 'Patient not found'}), 404

        if patient.get('created_at'):
            patient['created_at'] = patient['created_at'].isoformat()

        return jsonify({'success': True, 'patient': patient})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/patient/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update a patient's profile."""
    data = request.get_json()

    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = '''UPDATE patients SET
                 allergies = %s,
                 medical_conditions = %s,
                 regular_medications = %s,
                 address = %s,
                 emergency_contacts = %s
                 WHERE id = %s'''

        values = (
            data.get('allergies', ''),
            data.get('medical_conditions', ''),
            data.get('regular_medications', ''),
            data.get('address', ''),
            data.get('emergency_contacts', ''),
            patient_id
        )

        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Profile updated successfully'})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


# ── Doctor endpoints ─────────────────────────────────────────────────────────

@app.route('/api/register/doctor', methods=['POST'])
def register_doctor():
    """Register a new doctor."""
    data = request.get_json()

    required = ['name', 'age', 'email', 'password']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'{field} is required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute('SELECT id FROM doctors WHERE email = %s', (data['email'],))
        if cursor.fetchone():
            return jsonify({'success': False, 'error': 'Email already registered'}), 409

        hashed_pw = data['password']

        sql = '''INSERT INTO doctors
                 (name, age, email, password, specialization, experience,
                  hospital, contact_number, working_hours)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'''

        values = (
            data['name'],
            int(data['age']),
            data['email'].lower(),
            hashed_pw,
            data.get('specialization', ''),
            int(data.get('experience', 0)),
            data.get('hospital', ''),
            data.get('contactNumber', ''),
            data.get('workingHours', '')
        )

        cursor.execute(sql, values)
        conn.commit()

        doctor_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Doctor registered successfully',
            'doctor_id': doctor_id
        }), 201

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    """Get all doctors."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, age, email, specialization, experience, '
                       'hospital, contact_number, working_hours, created_at FROM doctors')
        doctors = cursor.fetchall()

        for d in doctors:
            if d.get('created_at'):
                d['created_at'] = d['created_at'].isoformat()

        cursor.close()
        conn.close()
        return jsonify({'success': True, 'doctors': doctors})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


# ── Login endpoint ───────────────────────────────────────────────────────────

@app.route('/api/login', methods=['POST'])
def login():
    """Login for both doctors and patients."""
    data = request.get_json()

    email = data.get('email', '').lower()
    password = data.get('password', '')
    role = data.get('role', '')

    if not email or not password or not role:
        return jsonify({'success': False, 'error': 'Email, password, and role are required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        table = 'doctors' if role == 'doctor' else 'patients'
        cursor.execute(f'SELECT * FROM {table} WHERE email = %s', (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

        if user['password'] != password:
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401

        # Remove password from response
        del user['password']
        if user.get('created_at'):
            user['created_at'] = user['created_at'].isoformat()

        user['role'] = role

        return jsonify({'success': True, 'user': user})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


# ── Medical Documents endpoints ──────────────────────────────────────────────

@app.route('/api/patient/<int:patient_id>/documents', methods=['POST'])
def upload_document(patient_id):
    """Upload a medical document for a patient."""
    data = request.get_json()

    filename = data.get('filename', '')
    file_data = data.get('fileData', '')
    description = data.get('description', 'Medical Document')

    if not filename or not file_data:
        return jsonify({'success': False, 'error': 'filename and fileData are required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = '''INSERT INTO medical_documents
                 (patient_id, filename, file_data, description)
                 VALUES (%s, %s, %s, %s)'''

        cursor.execute(sql, (patient_id, filename, file_data, description))
        conn.commit()

        doc_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Document uploaded successfully',
            'document_id': doc_id
        }), 201

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/patient/<int:patient_id>/documents', methods=['GET'])
def get_documents(patient_id):
    """Get all medical documents for a patient."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, filename, description, uploaded_at FROM medical_documents '
                       'WHERE patient_id = %s ORDER BY uploaded_at DESC', (patient_id,))
        docs = cursor.fetchall()

        for d in docs:
            if d.get('uploaded_at'):
                d['uploaded_at'] = d['uploaded_at'].isoformat()

        cursor.close()
        conn.close()

        return jsonify({'success': True, 'documents': docs})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/document/<int:doc_id>', methods=['GET'])
def get_document(doc_id):
    """Get a single document with its file data."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM medical_documents WHERE id = %s', (doc_id,))
        doc = cursor.fetchone()
        cursor.close()
        conn.close()

        if not doc:
            return jsonify({'success': False, 'error': 'Document not found'}), 404

        if doc.get('uploaded_at'):
            doc['uploaded_at'] = doc['uploaded_at'].isoformat()

        return jsonify({'success': True, 'document': doc})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/document/<int:doc_id>', methods=['DELETE'])
def delete_document(doc_id):
    """Delete a medical document."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM medical_documents WHERE id = %s', (doc_id,))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'success': True, 'message': 'Document deleted'})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


# ── Admin endpoints ───────────────────────────────────────────────────────────

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Authenticate a super admin."""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    if not username or not password:
        return jsonify({'success': False, 'error': 'Username and password required'}), 400
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE username = %s', (username,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if not admin or admin['password'] != password:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        return jsonify({'success': True, 'admin': {'id': admin['id'], 'username': admin['username']}})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """Return aggregate counts for the dashboard."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM patients')
        total_patients = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM doctors')
        total_doctors = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM medical_documents')
        total_docs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM patients WHERE DATE(created_at) = CURDATE()")
        new_today = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'stats': {
                'total_patients': total_patients,
                'total_doctors': total_doctors,
                'total_documents': total_docs,
                'new_today': new_today
            }
        })
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/patients', methods=['GET'])
def admin_get_patients():
    """Full patient list for admin (excludes passwords)."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.age, p.email, p.blood_group,
                   p.allergies, p.medical_conditions, p.regular_medications,
                   p.address, p.emergency_contacts, p.created_at,
                   COUNT(d.id) AS doc_count
            FROM patients p
            LEFT JOIN medical_documents d ON d.patient_id = p.id
            GROUP BY p.id
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for r in rows:
            if r.get('created_at'):
                r['created_at'] = r['created_at'].isoformat()
        return jsonify({'success': True, 'patients': rows})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/doctors', methods=['GET'])
def admin_get_doctors():
    """Full doctor list for admin (excludes passwords)."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, name, age, email, specialization, experience,
                   hospital, contact_number, working_hours, created_at
            FROM doctors
            ORDER BY created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for r in rows:
            if r.get('created_at'):
                r['created_at'] = r['created_at'].isoformat()
        return jsonify({'success': True, 'doctors': rows})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/patient/<int:patient_id>', methods=['DELETE'])
def admin_delete_patient(patient_id):
    """Delete a patient (and cascade their documents)."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM patients WHERE id = %s', (patient_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Patient deleted'})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/doctor/<int:doctor_id>', methods=['DELETE'])
def admin_delete_doctor(doctor_id):
    """Delete a doctor."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM doctors WHERE id = %s', (doctor_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Doctor deleted'})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('=' * 50)
    print('  LifelineQR Python Backend')
    print('  Running on http://localhost:5000')
    print('=' * 50)
    app.run(debug=True, port=5000)
