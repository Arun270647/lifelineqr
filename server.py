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
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sjssjs',     # MySQL root password
    'database': 'lifelineqr'
}


def get_db():
    """Create and return a new MySQL connection."""
    return mysql.connector.connect(**DB_CONFIG)


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


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    print('=' * 50)
    print('  LifelineQR Python Backend')
    print('  Running on http://localhost:5000')
    print('=' * 50)
    app.run(debug=True, port=5000)
