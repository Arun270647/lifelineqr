"""
LifelineQR - Python Flask Backend
Handles doctor and student registration via REST API,
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
    'MC9044PKM',  # Client's password
]

# Auto-detect the correct password
_detected_password = None
_detection_errors = []

for _pwd in _MYSQL_PASSWORDS_TO_TRY:
    try:
        _test = mysql.connector.connect(
            host=_MYSQL_HOST, user=_MYSQL_USER, password=_pwd
        )
        _test.close()
        _detected_password = _pwd
        break
    except mysql.connector.Error as err:
        _detection_errors.append((_pwd, str(err)))
        continue

if _detected_password is None:
    print("=" * 60)
    print("  ERROR: Could not connect to MySQL with any known password!")
    print(f"  We tried checking for user '{_MYSQL_USER}' but got these errors:")
    for _pwd, err in _detection_errors:
        display_pwd = "***" if _pwd else "(empty)"
        # We explicitly show if MC9044PKM was attempted so the client can see exactly why it failed
        if _pwd == 'MC9044PKM': display_pwd = 'MC9044PKM'
        print(f"  - Password [{display_pwd}]: {err}")
    print("=" * 60)
    
    import sys
    if sys.stdin.isatty() or True:  # Attempt interactive prompt if possible
        try:
            print("\nLet's configure it manually.")
            _MYSQL_USER = input(f"MySQL Username [{_MYSQL_USER}]: ").strip() or _MYSQL_USER
            import getpass
            _detected_password = getpass.getpass(f"MySQL Password for {_MYSQL_USER}: ")
            
            # verify immediately
            _test = mysql.connector.connect(host=_MYSQL_HOST, user=_MYSQL_USER, password=_detected_password)
            _test.close()
            print("  [OK] Connected successfully!")
        except Exception as e:
            print(f"  [ERR] Connection testing failed: {e}")
            _detected_password = ''  # fallback – will fail later

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
            CREATE TABLE IF NOT EXISTS students (
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
                student_class VARCHAR(10),
                section VARCHAR(5),
                roll_number VARCHAR(20),
                parent_name VARCHAR(255),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Safely add new columns if they don't exist (for existing databases)
        for col, coldef in [
            ('student_class', 'VARCHAR(10)'),
            ('section', 'VARCHAR(5)'),
            ('roll_number', 'VARCHAR(20)'),
            ('parent_name', 'VARCHAR(255)'),
        ]:
            try:
                cursor.execute(f"ALTER TABLE students ADD COLUMN {col} {coldef}")
            except mysql.connector.Error:
                pass  # column already exists

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
                is_verified BOOLEAN DEFAULT FALSE,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        for col, coldef in [
            ('is_verified', 'BOOLEAN DEFAULT FALSE')
        ]:
            try:
                cursor.execute(f"ALTER TABLE doctors ADD COLUMN {col} {coldef}")
            except mysql.connector.Error:
                pass  # column already exists

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS medical_documents (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                filename VARCHAR(255) NOT NULL,
                file_data LONGTEXT NOT NULL,
                description TEXT,
                uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Insert default admin if not exists
        cursor.execute("""
            INSERT IGNORE INTO admins (email, password)
            VALUES ('admin@lifelineqr.com', 'admin@123')
        """)

        conn.commit()
        cursor.close()
        conn.close()
        print("  [OK] Database and tables verified / created")
    except mysql.connector.Error as err:
        print(f"  [ERR] Database bootstrap error: {err}")


_bootstrap_database()


# ── Student endpoints ────────────────────────────────────────────────────────

@app.route('/api/register/student', methods=['POST'])
def register_student():
    """Register a new student."""
    data = request.get_json()

    required = ['name', 'age', 'email', 'password']
    for field in required:
        if not data.get(field):
            return jsonify({'success': False, 'error': f'{field} is required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if email already exists
        cursor.execute('SELECT id FROM students WHERE email = %s', (data['email'],))
        if cursor.fetchone():
            return jsonify({'success': False, 'error': 'Email already registered'}), 409

        hashed_pw = data['password']

        sql = '''INSERT INTO students
                 (name, age, email, password, blood_group, allergies,
                  medical_conditions, regular_medications, address, emergency_contacts,
                  student_class, section, roll_number, parent_name)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''

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
            data.get('emergencyContacts', ''),
            data.get('studentClass', ''),
            data.get('section', ''),
            data.get('rollNumber', ''),
            data.get('parentName', '')
        )

        cursor.execute(sql, values)
        conn.commit()

        student_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Student registered successfully',
            'student_id': student_id
        }), 201

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/students', methods=['GET'])
def get_students():
    """Get all students."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, age, email, blood_group, allergies, '
                       'medical_conditions, regular_medications, address, '
                       'emergency_contacts, student_class, section, roll_number, '
                       'parent_name, created_at FROM students')
        students = cursor.fetchall()

        # Convert datetime objects to strings
        for p in students:
            if p.get('created_at'):
                p['created_at'] = p['created_at'].isoformat()

        cursor.close()
        conn.close()
        return jsonify({'success': True, 'students': students})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/student/<int:student_id>', methods=['GET'])
def get_student(student_id):
    """Get a single student by ID."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, name, age, email, blood_group, allergies, '
                       'medical_conditions, regular_medications, address, '
                       'emergency_contacts, student_class, section, roll_number, '
                       'parent_name, created_at FROM students WHERE id = %s',
                       (student_id,))
        student = cursor.fetchone()
        cursor.close()
        conn.close()

        if not student:
            return jsonify({'success': False, 'error': 'Student not found'}), 404

        if student.get('created_at'):
            student['created_at'] = student['created_at'].isoformat()

        return jsonify({'success': True, 'student': student})

    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update a student's profile."""
    data = request.get_json()

    try:
        conn = get_db()
        cursor = conn.cursor()

        sql = '''UPDATE students SET
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
            student_id
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
                  hospital, contact_number, working_hours, is_verified)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, FALSE)'''

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
                       'hospital, contact_number, working_hours, is_verified, created_at FROM doctors')
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
    """Login for both doctors and students."""
    data = request.get_json()

    email = data.get('email', '').lower()
    password = data.get('password', '')
    role = data.get('role', '')

    if not email or not password or not role:
        return jsonify({'success': False, 'error': 'Email, password, and role are required'}), 400

    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        table = 'doctors' if role == 'doctor' else 'students'
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

@app.route('/api/student/<int:student_id>/documents', methods=['POST'])
def upload_document(student_id):
    """Upload a medical document for a student."""
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
                 (student_id, filename, file_data, description)
                 VALUES (%s, %s, %s, %s)'''

        cursor.execute(sql, (student_id, filename, file_data, description))
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


@app.route('/api/student/<int:student_id>/documents', methods=['GET'])
def get_documents(student_id):
    """Get all medical documents for a student."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT id, filename, description, uploaded_at FROM medical_documents '
                       'WHERE student_id = %s ORDER BY uploaded_at DESC', (student_id,))
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
    """Authenticate a super admin using email + password."""
    data = request.get_json()
    email    = data.get('email', '').strip().lower()
    password = data.get('password', '')
    if not email or not password:
        return jsonify({'success': False, 'error': 'Email and password required'}), 400
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM admins WHERE email = %s', (email,))
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        if not admin or admin['password'] != password:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401
        return jsonify({'success': True, 'admin': {'id': admin['id'], 'email': admin['email']}})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/stats', methods=['GET'])
def admin_stats():
    """Return aggregate counts for the dashboard."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM students')
        total_students = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM doctors')
        total_doctors = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM medical_documents')
        total_docs = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM students WHERE DATE(created_at) = CURDATE()")
        new_today = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM doctors WHERE is_verified = FALSE')
        pending_doctors = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'stats': {
                'total_students': total_students,
                'total_doctors': total_doctors,
                'total_documents': total_docs,
                'new_today': new_today,
                'pending_doctors': pending_doctors
            }
        })
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500


@app.route('/api/admin/students', methods=['GET'])
def admin_get_students():
    """Full student list for admin (excludes passwords)."""
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.id, p.name, p.age, p.email, p.blood_group,
                   p.allergies, p.medical_conditions, p.regular_medications,
                   p.address, p.emergency_contacts, p.student_class, p.section,
                   p.roll_number, p.parent_name, p.created_at,
                   COUNT(d.id) AS doc_count
            FROM students p
            LEFT JOIN medical_documents d ON d.student_id = p.id
            GROUP BY p.id
            ORDER BY p.created_at DESC
        """)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for r in rows:
            if r.get('created_at'):
                r['created_at'] = r['created_at'].isoformat()
        return jsonify({'success': True, 'students': rows})
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
                   hospital, contact_number, working_hours, is_verified, created_at
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


@app.route('/api/admin/student/<int:student_id>', methods=['DELETE'])
def admin_delete_student(student_id):
    """Delete a student (and cascade their documents)."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM students WHERE id = %s', (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Student deleted'})
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


@app.route('/api/admin/doctor/<int:doctor_id>/verify', methods=['PUT'])
def admin_verify_doctor(doctor_id):
    """Verify a doctor."""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('UPDATE doctors SET is_verified = TRUE WHERE id = %s', (doctor_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'Doctor verified'})
    except mysql.connector.Error as err:
        return jsonify({'success': False, 'error': str(err)}), 500




# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('=' * 50)
    print('  LifelineQR Python Backend')
    print('  Running on http://localhost:5000')
    print('=' * 50)
    app.run(debug=True, port=5000)
