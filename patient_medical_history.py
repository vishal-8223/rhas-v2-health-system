#!/usr/bin/env python3
"""
🏥 Patient Medical History & Profile System
Generates personalized medical histories and patient details for each health report
"""

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import json
from datetime import datetime, timedelta
import random
import hashlib

class PatientMedicalHistorySystem:
    
    def __init__(self):
        self.init_patient_database()
        self.load_medical_templates()
        print("🏥 Patient Medical History System initialized")
    
    def init_patient_database(self):
        """Initialize patient profiles database"""
        try:
            conn = sqlite3.connect('rhas_messages.db')
            cursor = conn.cursor()
            
            # Create patient profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patient_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT UNIQUE NOT NULL,
                    patient_name TEXT,
                    age INTEGER,
                    gender TEXT,
                    blood_group TEXT,
                    occupation TEXT,
                    address TEXT,
                    emergency_contact TEXT,
                    chronic_conditions TEXT,
                    allergies TEXT,
                    current_medications TEXT,
                    last_checkup_date TEXT,
                    doctor_name TEXT,
                    insurance_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create medical history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patient_medical_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT NOT NULL,
                    visit_date TEXT NOT NULL,
                    symptoms TEXT,
                    diagnosis TEXT,
                    treatment_given TEXT,
                    medications_prescribed TEXT,
                    doctor_notes TEXT,
                    follow_up_required INTEGER DEFAULT 0,
                    visit_type TEXT DEFAULT 'Regular',
                    hospital_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error initializing patient database: {e}")
    
    def load_medical_templates(self):
        """Load templates for generating realistic patient data"""
        self.names = {
            'male': ['Raj Kumar', 'Amit Singh', 'Vikash Patel', 'Suresh Sharma', 'Ramesh Gupta', 'Deepak Kumar', 'Anil Verma', 'Sanjay Tiwari'],
            'female': ['Priya Sharma', 'Sunita Devi', 'Kavita Singh', 'Meera Patel', 'Pooja Gupta', 'Shanti Kumari', 'Radha Verma', 'Sita Tiwari']
        }
        
        self.occupations = [
            'Farmer', 'Daily Wage Worker', 'Shopkeeper', 'Teacher', 'Driver', 'Construction Worker', 
            'Housewife', 'Student', 'Office Worker', 'Mechanic', 'Tailor', 'Cook'
        ]
        
        self.chronic_conditions = [
            'Hypertension', 'Diabetes Type 2', 'Asthma', 'Arthritis', 'High Cholesterol', 
            'Thyroid Disorder', 'Heart Disease', 'Kidney Stones', 'Gastric Issues'
        ]
        
        self.allergies = [
            'Dust allergy', 'Pollen allergy', 'Food allergy (dairy)', 'Drug allergy (Penicillin)', 
            'Skin allergy', 'No known allergies', 'Seasonal allergies'
        ]
        
        self.medications = [
            'Paracetamol 500mg', 'Metformin 500mg', 'Amlodipine 5mg', 'Aspirin 75mg', 
            'Omeprazole 20mg', 'Salbutamol inhaler', 'Vitamin D supplements'
        ]
        
        self.doctors = [
            'Dr. Rajesh Kumar (General Medicine)', 'Dr. Priya Sharma (Family Medicine)', 
            'Dr. Amit Patel (Internal Medicine)', 'Dr. Sunita Devi (General Physician)',
            'Dr. Vikash Singh (Rural Health)', 'Dr. Meera Gupta (Community Health)'
        ]
        
        self.hospitals = [
            'Community Health Center, Block-A', 'Primary Health Center, Village', 
            'District Hospital, Main Branch', 'Rural Health Clinic', 'Government Hospital',
            'Community Medical Center'
        ]
        
        self.past_diagnoses = {
            'fever': ['Viral fever', 'Typhoid fever', 'Malaria', 'Dengue fever', 'Common cold'],
            'stomach': ['Gastroenteritis', 'Food poisoning', 'Peptic ulcer', 'Acidity', 'Indigestion'],
            'respiratory': ['Upper respiratory infection', 'Bronchitis', 'Asthma attack', 'Pneumonia'],
            'general': ['Hypertension', 'Diabetes check-up', 'Annual health check', 'Injury treatment']
        }

    def generate_patient_profile(self, phone_number):
        """Generate a unique patient profile based on phone number"""
        # Use phone number as seed for consistent data generation
        random.seed(int(hashlib.md5(phone_number.encode()).hexdigest(), 16) % (10**8))
        
        gender = random.choice(['male', 'female'])
        name = random.choice(self.names[gender])
        age = random.randint(18, 75)
        
        profile = {
            'phone_number': phone_number,
            'patient_name': name,
            'age': age,
            'gender': gender.title(),
            'blood_group': random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
            'occupation': random.choice(self.occupations),
            'address': f"House No. {random.randint(1, 999)}, {random.choice(['Village Rampur', 'Village Sundarpur', 'Block-A Colony', 'Patel Nagar', 'Gandhi Colony', 'Ambedkar Nagar'])}, {random.choice(['Dist. Barabanki', 'Dist. Sitapur', 'Dist. Hardoi', 'Dist. Lucknow'])}",
            'emergency_contact': f"+91{random.randint(7000000000, 9999999999)}",
            'chronic_conditions': ', '.join(random.sample(self.chronic_conditions, random.randint(0, 3))),
            'allergies': random.choice(self.allergies),
            'current_medications': ', '.join(random.sample(self.medications, random.randint(0, 3))),
            'last_checkup_date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
            'doctor_name': random.choice(self.doctors),
            'insurance_id': f"PMJAY{random.randint(100000000, 999999999)}" if random.random() > 0.3 else "Not enrolled"
        }
        
        return profile

    def generate_medical_history(self, phone_number, current_symptoms=None):
        """Generate realistic medical history for a patient"""
        # Use phone number as seed for consistent history
        random.seed(int(hashlib.md5(phone_number.encode()).hexdigest(), 16) % (10**8))
        
        history = []
        num_visits = random.randint(3, 12)  # 3-12 past medical visits
        
        for i in range(num_visits):
            days_ago = random.randint(30, 1095)  # 1 month to 3 years ago
            visit_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
            
            # Generate symptoms and diagnosis
            symptom_category = random.choice(['fever', 'stomach', 'respiratory', 'general'])
            past_symptoms = self.get_symptoms_for_category(symptom_category)
            diagnosis = random.choice(self.past_diagnoses[symptom_category])
            
            visit = {
                'visit_date': visit_date,
                'symptoms': past_symptoms,
                'diagnosis': diagnosis,
                'treatment_given': self.get_treatment_for_diagnosis(diagnosis),
                'medications_prescribed': ', '.join(random.sample(self.medications, random.randint(1, 3))),
                'doctor_notes': self.get_doctor_notes(diagnosis),
                'follow_up_required': 1 if random.random() > 0.7 else 0,
                'visit_type': random.choice(['Emergency', 'Regular', 'Follow-up', 'Routine Check-up']),
                'hospital_name': random.choice(self.hospitals)
            }
            
            history.append(visit)
        
        # Sort by date (most recent first)
        history.sort(key=lambda x: x['visit_date'], reverse=True)
        
        return history

    def get_symptoms_for_category(self, category):
        """Get realistic symptoms for different categories"""
        symptoms_map = {
            'fever': 'High fever, headache, body ache, weakness',
            'stomach': 'Stomach pain, nausea, vomiting, loss of appetite',
            'respiratory': 'Cough, difficulty breathing, chest congestion, sore throat',
            'general': 'General weakness, fatigue, routine check-up'
        }
        return symptoms_map.get(category, 'General health concerns')

    def get_treatment_for_diagnosis(self, diagnosis):
        """Get appropriate treatment for diagnosis"""
        treatment_map = {
            'Viral fever': 'Rest, fluid intake, fever management',
            'Typhoid fever': 'Antibiotic course, isolation, fluid therapy',
            'Malaria': 'Antimalarial medication, fever control',
            'Dengue fever': 'Supportive care, platelet monitoring, fluid management',
            'Gastroenteritis': 'ORS, bland diet, medication for symptoms',
            'Food poisoning': 'Fluid replacement, symptomatic treatment',
            'Hypertension': 'Lifestyle modification, blood pressure monitoring',
            'Diabetes check-up': 'Blood sugar monitoring, dietary advice'
        }
        return treatment_map.get(diagnosis, 'Symptomatic treatment and monitoring')

    def get_doctor_notes(self, diagnosis):
        """Get appropriate doctor notes"""
        notes_map = {
            'Viral fever': 'Patient responded well to treatment. Advised rest and adequate fluid intake.',
            'Typhoid fever': 'Complete antibiotic course essential. Follow-up required after 1 week.',
            'Malaria': 'Blood smear positive. Started on antimalarial therapy immediately.',
            'Gastroenteritis': 'Dehydration managed. Patient advised on food hygiene practices.',
            'Hypertension': 'Blood pressure controlled with medication. Regular monitoring advised.',
            'Diabetes check-up': 'HbA1c within acceptable range. Continue current medication.'
        }
        return notes_map.get(diagnosis, 'Patient condition stable. Advised follow-up as needed.')

    def get_patient_full_report(self, phone_number):
        """Get comprehensive patient report including profile and medical history"""
        try:
            conn = sqlite3.connect('rhas_messages.db')
            cursor = conn.cursor()
            
            # Check if patient profile exists
            cursor.execute('SELECT * FROM patient_profiles WHERE phone_number = ?', (phone_number,))
            existing_profile = cursor.fetchone()
            
            if not existing_profile:
                # Generate and store new patient profile
                profile = self.generate_patient_profile(phone_number)
                
                cursor.execute('''
                    INSERT INTO patient_profiles 
                    (phone_number, patient_name, age, gender, blood_group, occupation, 
                     address, emergency_contact, chronic_conditions, allergies, 
                     current_medications, last_checkup_date, doctor_name, insurance_id)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    profile['phone_number'], profile['patient_name'], profile['age'],
                    profile['gender'], profile['blood_group'], profile['occupation'],
                    profile['address'], profile['emergency_contact'], profile['chronic_conditions'],
                    profile['allergies'], profile['current_medications'], profile['last_checkup_date'],
                    profile['doctor_name'], profile['insurance_id']
                ))
                
                # Generate and store medical history
                medical_history = self.generate_medical_history(phone_number)
                
                for visit in medical_history:
                    cursor.execute('''
                        INSERT INTO patient_medical_history
                        (phone_number, visit_date, symptoms, diagnosis, treatment_given,
                         medications_prescribed, doctor_notes, follow_up_required, visit_type, hospital_name)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        phone_number, visit['visit_date'], visit['symptoms'], visit['diagnosis'],
                        visit['treatment_given'], visit['medications_prescribed'], visit['doctor_notes'],
                        visit['follow_up_required'], visit['visit_type'], visit['hospital_name']
                    ))
                
                conn.commit()
            else:
                # Load existing profile
                profile = {
                    'phone_number': existing_profile[1],
                    'patient_name': existing_profile[2],
                    'age': existing_profile[3],
                    'gender': existing_profile[4],
                    'blood_group': existing_profile[5],
                    'occupation': existing_profile[6],
                    'address': existing_profile[7],
                    'emergency_contact': existing_profile[8],
                    'chronic_conditions': existing_profile[9] or '',
                    'allergies': existing_profile[10] or '',
                    'current_medications': existing_profile[11] or '',
                    'last_checkup_date': existing_profile[12],
                    'doctor_name': existing_profile[13],
                    'insurance_id': existing_profile[14]
                }
            
            # Get medical history
            cursor.execute('''
                SELECT visit_date, symptoms, diagnosis, treatment_given, medications_prescribed,
                       doctor_notes, follow_up_required, visit_type, hospital_name
                FROM patient_medical_history 
                WHERE phone_number = ? 
                ORDER BY visit_date DESC
            ''', (phone_number,))
            
            history_rows = cursor.fetchall()
            medical_history = []
            
            for row in history_rows:
                medical_history.append({
                    'visit_date': row[0],
                    'symptoms': row[1],
                    'diagnosis': row[2],
                    'treatment_given': row[3],
                    'medications_prescribed': row[4],
                    'doctor_notes': row[5],
                    'follow_up_required': row[6],
                    'visit_type': row[7],
                    'hospital_name': row[8]
                })
            
            # Get current health reports
            cursor.execute('''
                SELECT message_body, predicted_disease, symptoms, processed_at, location_city, severity_level
                FROM health_messages 
                WHERE phone_number = ? 
                ORDER BY processed_at DESC
                LIMIT 10
            ''', (phone_number,))
            
            current_reports = cursor.fetchall()
            
            conn.close()
            
            return {
                'profile': profile,
                'medical_history': medical_history,
                'current_reports': current_reports,
                'total_visits': len(medical_history),
                'last_visit': medical_history[0]['visit_date'] if medical_history else 'No previous visits'
            }
            
        except Exception as e:
            print(f"Error getting patient report: {e}")
            return None

def create_patient_report_template():
    """Create comprehensive patient medical report template"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🏥 Patient Medical Report - {{ patient.profile.patient_name }}</title>
    <meta charset="UTF-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .header {
            background: rgba(255,255,255,0.95);
            padding: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .patient-id {
            display: inline-block;
            padding: 8px 15px;
            background: #667eea;
            color: white;
            border-radius: 20px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .report-grid {
            display: grid;
            grid-template-columns: 1fr 2fr;
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .report-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .report-card h2 {
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 10px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .info-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .info-item strong {
            color: #667eea;
            display: block;
            margin-bottom: 5px;
            font-size: 0.9em;
        }
        
        .info-item span {
            font-size: 1.1em;
            font-weight: 600;
        }
        
        .medical-history {
            max-height: 600px;
            overflow-y: auto;
        }
        
        .history-item {
            background: #f8f9fa;
            margin: 10px 0;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #27ae60;
            position: relative;
        }
        
        .history-item.emergency {
            border-left-color: #e74c3c;
        }
        
        .history-item.follow-up {
            border-left-color: #f39c12;
        }
        
        .history-date {
            position: absolute;
            top: 10px;
            right: 15px;
            background: #667eea;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
        }
        
        .history-content {
            margin-top: 10px;
        }
        
        .history-content h4 {
            color: #667eea;
            margin-bottom: 8px;
        }
        
        .symptoms-list {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .treatment-list {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        
        .current-reports {
            background: #e8f5e8;
            border-left: 4px solid #28a745;
            padding: 15px;
            border-radius: 8px;
            margin: 15px 0;
        }
        
        .back-button {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            margin-bottom: 20px;
            text-decoration: none;
            display: inline-block;
        }
        
        .back-button:hover {
            background: #5a67d8;
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .stats-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .stat-item {
            background: #667eea;
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }
        
        .stat-number {
            font-size: 1.5em;
            font-weight: bold;
            display: block;
        }
        
        .print-button {
            background: #28a745;
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            margin-left: 10px;
        }
        
        @media (max-width: 768px) {
            .report-grid {
                grid-template-columns: 1fr;
            }
            .info-grid {
                grid-template-columns: 1fr;
            }
        }
        
        @media print {
            body {
                background: white;
            }
            .back-button, .print-button {
                display: none;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            🏥 Patient Medical Report
            <span class="patient-id">{{ patient.profile.phone_number }}</span>
        </h1>
        <p><strong>Patient:</strong> {{ patient.profile.patient_name }} | <strong>Age:</strong> {{ patient.profile.age }} years | <strong>Blood Group:</strong> {{ patient.profile.blood_group }}</p>
        <p><strong>Last Visit:</strong> {{ patient.last_visit }} | <strong>Total Medical Visits:</strong> {{ patient.total_visits }}</p>
    </div>
    
    <div class="container">
        <a href="/dashboard" class="back-button">← Back to Dashboard</a>
        <button onclick="window.print()" class="print-button">🖨️ Print Report</button>
        
        <div class="stats-row">
            <div class="stat-item">
                <span class="stat-number">{{ patient.total_visits }}</span>
                Total Visits
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ patient.current_reports|length }}</span>
                Current Reports
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ patient.profile.age }}</span>
                Age (Years)
            </div>
            <div class="stat-item">
                <span class="stat-number">{{ patient.profile.chronic_conditions.split(', ')|length if patient.profile.chronic_conditions else 0 }}</span>
                Chronic Conditions
            </div>
        </div>
        
        <div class="report-grid">
            <div class="report-card">
                <h2>👤 Personal Information</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Full Name</strong>
                        <span>{{ patient.profile.patient_name }}</span>
                    </div>
                    <div class="info-item">
                        <strong>Age</strong>
                        <span>{{ patient.profile.age }} years</span>
                    </div>
                    <div class="info-item">
                        <strong>Gender</strong>
                        <span>{{ patient.profile.gender }}</span>
                    </div>
                    <div class="info-item">
                        <strong>Blood Group</strong>
                        <span>{{ patient.profile.blood_group }}</span>
                    </div>
                    <div class="info-item">
                        <strong>Occupation</strong>
                        <span>{{ patient.profile.occupation }}</span>
                    </div>
                    <div class="info-item">
                        <strong>Phone Number</strong>
                        <span>{{ patient.profile.phone_number }}</span>
                    </div>
                </div>
                
                <div class="info-item" style="grid-column: 1 / -1;">
                    <strong>Address</strong>
                    <span>{{ patient.profile.address }}</span>
                </div>
                
                <div class="info-item" style="grid-column: 1 / -1;">
                    <strong>Emergency Contact</strong>
                    <span>{{ patient.profile.emergency_contact }}</span>
                </div>
                
                <h3 style="color: #667eea; margin-top: 20px;">🩺 Medical Information</h3>
                
                <div class="info-item" style="margin-top: 10px;">
                    <strong>Chronic Conditions</strong>
                    <span>{{ patient.profile.chronic_conditions or 'None reported' }}</span>
                </div>
                
                <div class="info-item">
                    <strong>Known Allergies</strong>
                    <span>{{ patient.profile.allergies or 'None reported' }}</span>
                </div>
                
                <div class="info-item">
                    <strong>Current Medications</strong>
                    <span>{{ patient.profile.current_medications or 'None currently' }}</span>
                </div>
                
                <div class="info-item">
                    <strong>Regular Doctor</strong>
                    <span>{{ patient.profile.doctor_name }}</span>
                </div>
                
                <div class="info-item">
                    <strong>Insurance ID</strong>
                    <span>{{ patient.profile.insurance_id }}</span>
                </div>
                
                <div class="info-item">
                    <strong>Last Checkup</strong>
                    <span>{{ patient.profile.last_checkup_date }}</span>
                </div>
            </div>
            
            <div class="report-card">
                <h2>📋 Medical History</h2>
                <div class="medical-history">
                    {% for visit in patient.medical_history %}
                    <div class="history-item {{ visit.visit_type.lower().replace(' ', '-').replace('_', '-') }}">
                        <div class="history-date">{{ visit.visit_date }}</div>
                        <h4>{{ visit.diagnosis }} ({{ visit.visit_type }})</h4>
                        
                        <div class="symptoms-list">
                            <strong>Symptoms:</strong> {{ visit.symptoms }}
                        </div>
                        
                        <div class="treatment-list">
                            <strong>Treatment:</strong> {{ visit.treatment_given }}
                        </div>
                        
                        <div style="margin: 10px 0;">
                            <strong>Medications Prescribed:</strong> {{ visit.medications_prescribed }}
                        </div>
                        
                        <div style="margin: 10px 0;">
                            <strong>Hospital:</strong> {{ visit.hospital_name }}
                        </div>
                        
                        <div style="font-style: italic; color: #666; margin-top: 10px;">
                            <strong>Doctor's Notes:</strong> {{ visit.doctor_notes }}
                        </div>
                        
                        {% if visit.follow_up_required %}
                        <div style="background: #fff3cd; padding: 8px; border-radius: 5px; margin-top: 10px;">
                            ⚠️ Follow-up required
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="report-card full-width">
            <h2>📱 Recent Health Reports</h2>
            {% for report in patient.current_reports %}
            <div class="current-reports">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>Date:</strong> {{ report[3] }} | 
                        <strong>Predicted Disease:</strong> {{ report[1] or 'Under analysis' }} |
                        <strong>Severity:</strong> {{ report[5] or 'Medium' }}
                    </div>
                    <div>
                        <strong>Location:</strong> {{ report[4] or 'Not specified' }}
                    </div>
                </div>
                <div style="margin-top: 10px;">
                    <strong>Original Message:</strong> {{ report[0] }}
                </div>
                <div style="margin-top: 5px; color: #666;">
                    <strong>Identified Symptoms:</strong> {{ report[2] or 'Being analyzed' }}
                </div>
            </div>
            {% endfor %}
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.95); border-radius: 10px; font-size: 0.9em; color: #666;">
            <strong>📋 Report Generated:</strong> {{ datetime.now().strftime('%Y-%m-%d %H:%M:%S') }} | 
            <strong>System:</strong> RHAS v2.0 Patient Management System
        </div>
    </div>
</body>
</html>
    '''

def create_patient_report_routes(app):
    """Add patient medical report routes to existing Flask app"""
    patient_system = PatientMedicalHistorySystem()
    
    @app.route('/patient-report/<phone_number>')
    def patient_medical_report(phone_number):
        """Show comprehensive patient medical report"""
        patient_data = patient_system.get_patient_full_report(phone_number)
        
        if not patient_data:
            return "Patient report not found", 404
        
        template = create_patient_report_template()
        return render_template_string(template, patient=patient_data, datetime=datetime)
    
    @app.route('/api/patient-data/<phone_number>')
    def api_patient_data(phone_number):
        """API endpoint for patient data"""
        patient_data = patient_system.get_patient_full_report(phone_number)
        
        if not patient_data:
            return jsonify({'error': 'Patient not found'}), 404
        
        return jsonify(patient_data)

if __name__ == '__main__':
    # For testing purposes
    app = Flask(__name__)
    create_patient_report_routes(app)
    app.run(debug=True, port=5003)