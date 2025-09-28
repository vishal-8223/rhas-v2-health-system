#!/usr/bin/env python3
"""
🏛️ Personalized Government Alert Status System
Creates detailed status pages for each government alert with personalized action plans
"""

from flask import Flask, render_template_string, jsonify, request
import sqlite3
import json
from datetime import datetime, timedelta
import random

class PersonalizedAlertStatusSystem:
    
    def __init__(self):
        self.load_detailed_case_data()
        print("🏛️ Personalized Alert Status System initialized")
    
    def load_detailed_case_data(self):
        """Load detailed case data for personalized status pages based on WHO and Indian guidelines"""
        self.case_details = {
            'cholera': {
                'symptoms': ['Profuse watery diarrhea ("rice-water" stools)', 'Vomiting', 'Rapid dehydration', 'Muscle cramps', 'Circulatory collapse'],
                'transmission': 'Fecal-oral route through contaminated water and food',
                'incubation': '2 hours to 5 days (usually 2-3 days)',
                'mortality_rate': 'Less than 1% with prompt treatment, up to 50-60% if untreated',
                'complications': ['Severe dehydration', 'Hypovolemic shock', 'Acute kidney injury', 'Hypoglycemia', 'Hypokalemia'],
                'who_guidelines': [
                    'WHO Cholera outbreak response guidelines (2023)',
                    'Case definition: Acute watery diarrhea with dehydration',
                    'Treatment: ORS and zinc supplementation for mild cases',
                    'Severe cases: IV fluids (Ringer lactate solution)',
                    'Antibiotic use: Only for severe cases (Azithromycin/Doxycycline)'
                ],
                'indian_guidelines': [
                    'NCDC Guidelines for Cholera Control (2022)',
                    'IDSP immediate notification within 24 hours',
                    'Water quality testing as per BIS standards',
                    'Community case management through ASHA workers',
                    'Activate Rapid Response Team within 2 hours'
                ],
                'environmental_factors': [
                    'Contaminated water sources within 2km radius (Vibrio cholerae O1/O139)',
                    'Poor sanitation infrastructure in affected slum areas',
                    'High population density (>10,000/km²) facilitating transmission',
                    'Recent monsoon flooding creating ideal conditions',
                    'Industrial waste discharge affecting local water supply',
                    'Inadequate sewage treatment facilities'
                ],
                'immediate_actions': [
                    'Deploy Rapid Response Team within 2 hours (NCDC protocol)',
                    'Set up Cholera Treatment Centers with ORS stations',
                    'Implement WHO case management protocols',
                    'Test water sources for Vibrio cholerae O1/O139',
                    'Issue emergency health advisory per IDSP guidelines',
                    'Establish IV fluid therapy for severe dehydration cases',
                    'Activate community surveillance through ASHA workers'
                ],
                'prevention_measures': [
                    'Water chlorination (0.5mg/L residual chlorine - WHO standard)',
                    'Sanitation improvement per Swachh Bharat guidelines',
                    'Community WASH education following WHO recommendations',
                    'Distribution of ORS packets and zinc tablets',
                    'Food safety enforcement as per FSSAI regulations',
                    'Vector control measures in high-risk areas'
                ],
                'laboratory_guidelines': [
                    'Stool sample collection within 24 hours of onset',
                    'Culture on TCBS agar (WHO protocol)',
                    'Serotype identification (O1 Classical/El Tor, O139)',
                    'Antimicrobial susceptibility testing',
                    'Notification to NCDC within 24 hours of confirmation'
                ],
                'treatment_protocol': [
                    'Mild dehydration: ORS 75ml/kg over 4 hours',
                    'Moderate dehydration: ORS 100ml/kg over 6 hours', 
                    'Severe dehydration: IV Ringer lactate 100ml/kg/hour',
                    'Antibiotics: Azithromycin 1g single dose (severe cases only)',
                    'Zinc supplementation: 20mg daily for 10-14 days'
                ]
            },
            'dengue': {
                'symptoms': ['High fever (40°C/104°F)', 'Intense headache', 'Retro-orbital pain', 'Myalgia/arthralgia', 'Skin rash', 'Nausea/vomiting'],
                'transmission': 'Aedes aegypti and Aedes albopictus mosquito bites (day-biting)',
                'incubation': '4-6 days (range 3-14 days)',
                'mortality_rate': '<1% with appropriate clinical management, up to 2-5% in severe cases',
                'complications': ['Dengue Hemorrhagic Fever (DHF)', 'Dengue Shock Syndrome (DSS)', 'Plasma leakage', 'Organ impairment'],
                'who_guidelines': [
                    'WHO Dengue Guidelines for Diagnosis, Treatment, Prevention (2023)',
                    'Case classification: Dengue without/with warning signs, Severe dengue',
                    'Warning signs: Abdominal pain, persistent vomiting, plasma leakage',
                    'Critical phase monitoring: Days 3-7 of illness',
                    'Fluid management based on capillary leak phase'
                ],
                'indian_guidelines': [
                    'NCVBDC National Guidelines for Clinical Management (2022)',
                    'NVBDCP surveillance and vector control protocols',
                    'State-specific outbreak response as per IDSP',
                    'Platelet transfusion criteria: <10,000-20,000/μL with bleeding',
                    'Community engagement through ASHA/ANM workers'
                ],
                'environmental_factors': [
                    'Aedes breeding in clean water containers (optimal pH 6-8)',
                    'Post-monsoon stagnant water in construction sites',
                    'Temperature range 25-30°C optimal for Aedes survival',
                    'Urban areas with poor drainage and water storage',
                    'Humidity levels >70% supporting vector development',
                    'Tire shops, flower pots, and overhead tanks as breeding sites'
                ],
                'immediate_actions': [
                    'Deploy rapid vector control teams per NVBDCP guidelines',
                    'Source reduction: eliminate all Aedes breeding sites',
                    'Establish fever screening camps at PHCs/CHCs',
                    'Implement WHO case management protocols',
                    'Monitor platelet count and hematocrit levels',
                    'Set up dengue diagnostic facilities (NS1, IgM/IgG)',
                    'Activate community surveillance through ASHA workers'
                ],
                'prevention_measures': [
                    'Integrated Vector Management (IVM) as per WHO',
                    'Community mobilization for source reduction',
                    'School-based education programs',
                    'Distribution of larvivorous fish (Gambusia)',
                    'Regular entomological surveillance',
                    'Bio-environmental control measures'
                ],
                'laboratory_guidelines': [
                    'NS1 antigen test: Days 1-7 of fever onset',
                    'IgM capture ELISA: Days 5-10 of illness',
                    'RT-PCR for serotype identification (research labs)',
                    'Complete blood count with platelet monitoring',
                    'Liver function tests and coagulation profile'
                ],
                'treatment_protocol': [
                    'Febrile phase: Paracetamol 10-15mg/kg every 6 hours',
                    'Avoid aspirin and NSAIDs (bleeding risk)',
                    'Critical phase: Monitor for plasma leakage',
                    'Fluid management: Crystalloids as per WHO guidelines',
                    'Platelet transfusion: Only if count <10,000 with bleeding'
                ],
                'vector_control': [
                    'Temephos 1% granules for drinking water containers',
                    'Bacillus thuringiensis israelensis (Bti) for large containers',
                    'Space spraying during outbreak (Malathion 5% ULV)',
                    'Indoor residual spraying not recommended for Aedes'
                ]
            },
            'covid19': {
                'symptoms': ['Fever (87.9%)', 'Dry cough (67.7%)', 'Fatigue (38.1%)', 'Anosmia/Ageusia (loss of taste/smell)', 'Dyspnea (18.6%)', 'Sore throat', 'Headache'],
                'transmission': 'Respiratory droplets, aerosols, and fomites (SARS-CoV-2)',
                'incubation': '2-14 days (median 5-6 days)',
                'mortality_rate': 'Overall CFR ~1.4% in India (varies by age: <1% <60 years, >5% >80 years)',
                'complications': ['Pneumonia', 'ARDS', 'Multi-organ failure', 'Cytokine storm', 'Thromboembolism', 'Long COVID'],
                'who_guidelines': [
                    'WHO COVID-19 Clinical Management Guidelines (2023)',
                    'Case definition: Confirmed, probable, or suspect case',
                    'Treatment: Supportive care, oxygen therapy, antivirals',
                    'Prevention: Vaccination, mask-wearing, physical distancing',
                    'Isolation: 10 days from symptom onset for mild cases'
                ],
                'indian_guidelines': [
                    'ICMR Testing Strategy and Clinical Management Protocol',
                    'MoHFW Guidelines for Home Isolation (2022)',
                    'AIIMS/ICMR Treatment Protocol for COVID-19',
                    'National COVID-19 Vaccination Strategy',
                    'Revised Discharge Policy and Home Isolation guidelines'
                ],
                'environmental_factors': [
                    'High population density facilitating transmission',
                    'Poor ventilation in crowded indoor spaces',
                    'Social/religious gatherings as super-spreader events',
                    'Air pollution (PM2.5 >40 μg/m³) affecting respiratory immunity',
                    'Cold/dry weather conditions supporting virus survival',
                    'Limited mask compliance and social distancing in rural areas'
                ],
                'immediate_actions': [
                    'Activate COVID-19 outbreak response as per ICMR guidelines',
                    'Contact tracing within 24-48 hours of case confirmation',
                    'RT-PCR testing facility with 24-hour turnaround time',
                    'Home isolation setup as per MoHFW guidelines',
                    'Hospital bed allocation and oxygen inventory check',
                    'Community health worker deployment for monitoring'
                ],
                'prevention_measures': [
                    'Universal masking (N95/surgical masks in healthcare)',
                    'Physical distancing minimum 2 meters (WHO recommendation)',
                    'Hand hygiene with 70% alcohol-based sanitizer',
                    'Vaccination drive with priority groups (NEGVAC strategy)',
                    'Environmental surface disinfection',
                    'Ventilation improvement in indoor spaces'
                ],
                'laboratory_guidelines': [
                    'RT-PCR testing: Nasopharyngeal/oropharyngeal swab',
                    'Rapid Antigen Test: For symptomatic cases in high prevalence',
                    'Sample collection within 7 days of symptom onset',
                    'Biosafety level 2+ laboratory requirements'
                ],
                'treatment_protocol': [
                    'Mild cases: Home isolation, symptomatic treatment',
                    'Moderate cases: Oxygen saturation monitoring, steroids if indicated',
                    'Severe cases: Remdesivir, mechanical ventilation',
                    'Anticoagulation: LMWH for hospitalized patients'
                ]
            }
        }
        
        self.response_teams = {
            'emergency_medical': {
                'team_size': '6-8 medical officers',
                'equipment': ['Emergency medicines', 'IV fluids', 'Oxygen cylinders', 'Diagnostic kits'],
                'deployment_time': '30 minutes'
            },
            'vector_control': {
                'team_size': '4-6 entomologists',
                'equipment': ['Fogging machines', 'Larvicides', 'Insecticides', 'Protective gear'],
                'deployment_time': '60 minutes'
            },
            'epidemiological': {
                'team_size': '3-4 epidemiologists',
                'equipment': ['Sample collection kits', 'Data collection tablets', 'GPS devices'],
                'deployment_time': '45 minutes'
            }
        }

    def get_alert_details(self, alert_id):
        """Get detailed information for a specific alert"""
        try:
            conn = sqlite3.connect('government_alerts.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT alert_id, disease, location_city, location_state, case_count, 
                       severity, priority, departments, actions_required, timeline_hours,
                       status, acknowledged_by, actions_completed, notes, created_at
                FROM government_alerts 
                WHERE alert_id = ?
            """, (alert_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return None
            
            # Parse the data
            alert_data = {
                'alert_id': result[0],
                'disease': result[1],
                'location_city': result[2] or 'Unknown',
                'location_state': result[3] or 'Unknown',
                'case_count': result[4] or 0,
                'severity': result[5] or 'Medium',
                'priority': result[6] or 'HIGH',
                'departments': json.loads(result[7]) if result[7] else [],
                'actions_required': json.loads(result[8]) if result[8] else [],
                'timeline_hours': result[9] or 24,
                'status': result[10] or 'SENT',
                'acknowledged_by': json.loads(result[11]) if result[11] else [],
                'actions_completed': json.loads(result[12]) if result[12] else [],
                'notes': result[13] or '',
                'created_at': result[14]
            }
            
            # Add detailed case information
            disease_key = alert_data['disease'].lower()
            if disease_key in self.case_details:
                alert_data.update(self.case_details[disease_key])
            
            # Generate progress tracking
            alert_data['progress'] = self.generate_progress_tracking(alert_data)
            
            # Generate resource allocation
            alert_data['resources'] = self.generate_resource_allocation(alert_data)
            
            # Generate timeline with milestones
            alert_data['detailed_timeline'] = self.generate_detailed_timeline(alert_data)
            
            return alert_data
            
        except Exception as e:
            print(f"Error getting alert details: {e}")
            return None
    
    def generate_progress_tracking(self, alert_data):
        """Generate progress tracking based on alert status and time"""
        created_time = datetime.fromisoformat(alert_data['created_at'].replace('Z', '+00:00')) if alert_data['created_at'] else datetime.now()
        time_elapsed = (datetime.now() - created_time).total_seconds() / 3600  # hours
        
        progress_items = [
            {'task': 'Alert Generated', 'status': 'COMPLETED', 'completion_time': 0},
            {'task': 'Departments Notified', 'status': 'COMPLETED' if time_elapsed > 0.5 else 'IN_PROGRESS', 'completion_time': 0.5},
            {'task': 'Response Teams Mobilized', 'status': 'COMPLETED' if time_elapsed > 1 else 'PENDING', 'completion_time': 1},
            {'task': 'Field Assessment Started', 'status': 'COMPLETED' if time_elapsed > 2 else 'PENDING', 'completion_time': 2},
            {'task': 'Medical Teams Deployed', 'status': 'COMPLETED' if time_elapsed > 3 else 'PENDING', 'completion_time': 3},
            {'task': 'Public Advisory Issued', 'status': 'COMPLETED' if time_elapsed > 4 else 'PENDING', 'completion_time': 4},
            {'task': 'Containment Measures Active', 'status': 'COMPLETED' if time_elapsed > 6 else 'PENDING', 'completion_time': 6},
            {'task': 'Situation Under Control', 'status': 'COMPLETED' if time_elapsed > 24 else 'PENDING', 'completion_time': 24}
        ]
        
        return progress_items
    
    def generate_resource_allocation(self, alert_data):
        """Generate resource allocation based on alert severity and case count"""
        case_count = alert_data['case_count']
        severity = alert_data['severity'].lower()
        
        multiplier = 1
        if severity == 'high': multiplier = 1.5
        elif severity == 'critical': multiplier = 2
        
        resources = {
            'medical_teams': max(1, int((case_count / 5) * multiplier)),
            'medical_officers': max(2, int((case_count / 3) * multiplier)),
            'paramedical_staff': max(4, int(case_count * multiplier)),
            'ambulances': max(1, int((case_count / 8) * multiplier)),
            'isolation_beds': max(5, int(case_count * 2 * multiplier)),
            'testing_kits': max(50, int(case_count * 20 * multiplier)),
            'medicines': f"{int(case_count * 10 * multiplier)} units",
            'ppe_kits': max(20, int(case_count * 5 * multiplier)),
            'budget_allocated': f"₹{int((case_count * 50000) * multiplier):,}"
        }
        
        return resources
    
    def generate_detailed_timeline(self, alert_data):
        """Generate detailed timeline with specific milestones"""
        created_time = datetime.fromisoformat(alert_data['created_at'].replace('Z', '+00:00')) if alert_data['created_at'] else datetime.now()
        
        timeline_items = []
        
        # Immediate actions (0-2 hours)
        timeline_items.append({
            'time': created_time.strftime('%Y-%m-%d %H:%M'),
            'milestone': 'Alert Generated',
            'description': f"Health alert for {alert_data['disease']} outbreak in {alert_data['location_city']}",
            'status': 'COMPLETED'
        })
        
        timeline_items.append({
            'time': (created_time + timedelta(minutes=30)).strftime('%Y-%m-%d %H:%M'),
            'milestone': 'Emergency Response Activated',
            'description': 'Rapid response teams notified and mobilized',
            'status': 'COMPLETED'
        })
        
        timeline_items.append({
            'time': (created_time + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M'),
            'milestone': 'Field Teams Deployed',
            'description': 'Medical and epidemiological teams dispatched to affected area',
            'status': 'IN_PROGRESS'
        })
        
        timeline_items.append({
            'time': (created_time + timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'),
            'milestone': 'Containment Initiated',
            'description': 'Active case finding and containment measures started',
            'status': 'PENDING'
        })
        
        timeline_items.append({
            'time': (created_time + timedelta(hours=6)).strftime('%Y-%m-%d %H:%M'),
            'milestone': 'Public Advisory Released',
            'description': 'Community health advisory and prevention guidelines issued',
            'status': 'PENDING'
        })
        
        timeline_items.append({
            'time': (created_time + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M'),
            'milestone': 'Situation Assessment',
            'description': 'Complete epidemiological assessment and control measure evaluation',
            'status': 'PENDING'
        })
        
        return timeline_items

def create_personalized_alert_template():
    """Create comprehensive personalized alert status template"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🏛️ Government Alert Status - {{ alert.alert_id }}</title>
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
        
        .alert-badge {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .priority-immediate { background: #e74c3c; }
        .priority-urgent { background: #e67e22; }
        .priority-high { background: #f39c12; }
        .priority-moderate { background: #3498db; }
        .priority-low { background: #27ae60; }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .status-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 25px;
            margin-bottom: 30px;
        }
        
        .status-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .status-card h2 {
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
        }
        
        .progress-timeline {
            margin-top: 20px;
        }
        
        .timeline-item {
            display: flex;
            align-items: center;
            padding: 12px 0;
            border-left: 3px solid #dee2e6;
            margin-left: 15px;
            padding-left: 25px;
            position: relative;
        }
        
        .timeline-item::before {
            content: '';
            position: absolute;
            left: -8px;
            top: 15px;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: #dee2e6;
        }
        
        .timeline-item.completed::before { background: #27ae60; }
        .timeline-item.in-progress::before { background: #f39c12; animation: pulse 2s infinite; }
        .timeline-item.pending::before { background: #dee2e6; }
        
        @keyframes pulse {
            0% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.2); opacity: 0.7; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        .full-width {
            grid-column: 1 / -1;
        }
        
        .resource-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }
        
        .resource-item {
            background: #e8f5e8;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            border: 2px solid #27ae60;
        }
        
        .resource-number {
            font-size: 1.5em;
            font-weight: bold;
            color: #27ae60;
            display: block;
        }
        
        .action-list {
            list-style: none;
        }
        
        .action-list li {
            padding: 10px 0;
            border-bottom: 1px solid #dee2e6;
            display: flex;
            align-items: center;
        }
        
        .action-list li::before {
            content: '✓';
            background: #27ae60;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            font-size: 0.8em;
        }
        
        .action-list li:last-child {
            border-bottom: none;
        }
        
        .environmental-factors {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
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
        
        @media (max-width: 768px) {
            .status-grid {
                grid-template-columns: 1fr;
            }
            .info-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>
            🏛️ Government Health Alert Status
            <span class="alert-badge priority-{{ alert.priority.lower() }}">{{ alert.priority }} PRIORITY</span>
        </h1>
        <p>Alert ID: <strong>{{ alert.alert_id }}</strong> | Disease: <strong>{{ alert.disease.upper() }}</strong> | Location: <strong>{{ alert.location_city }}, {{ alert.location_state }}</strong></p>
        <p>Created: {{ alert.created_at }} | Status: <strong>{{ alert.status }}</strong></p>
    </div>
    
    <div class="container">
        <a href="/government-alerts" class="back-button">← Back to All Alerts</a>
        
        <div class="status-grid">
            <div class="status-card">
                <h2>📊 Case Information</h2>
                <div class="info-grid">
                    <div class="info-item">
                        <strong>Total Cases</strong>
                        {{ alert.case_count }}
                    </div>
                    <div class="info-item">
                        <strong>Severity Level</strong>
                        {{ alert.severity }}
                    </div>
                    <div class="info-item">
                        <strong>Response Timeline</strong>
                        {{ alert.timeline_hours }} hours
                    </div>
                    <div class="info-item">
                        <strong>Transmission Method</strong>
                        {{ alert.transmission }}
                    </div>
                    <div class="info-item">
                        <strong>Incubation Period</strong>
                        {{ alert.incubation }}
                    </div>
                    <div class="info-item">
                        <strong>Mortality Rate</strong>
                        {{ alert.mortality_rate }}
                    </div>
                </div>
                
                <h3 style="color: #667eea; margin-top: 20px;">🩺 Primary Symptoms</h3>
                <ul class="action-list">
                    {% for symptom in alert.symptoms %}
                    <li>{{ symptom }}</li>
                    {% endfor %}
                </ul>
                
                <h3 style="color: #667eea; margin-top: 20px;">⚠️ Potential Complications</h3>
                <ul class="action-list">
                    {% for complication in alert.complications %}
                    <li>{{ complication }}</li>
                    {% endfor %}
                </ul>
                
                {% if alert.who_guidelines %}
                <h3 style="color: #667eea; margin-top: 20px;">🌐 WHO Guidelines</h3>
                <ul class="action-list">
                    {% for guideline in alert.who_guidelines %}
                    <li>{{ guideline }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
                
                {% if alert.indian_guidelines %}
                <h3 style="color: #667eea; margin-top: 20px;">🇮🇳 Indian Medical Guidelines</h3>
                <ul class="action-list">
                    {% for guideline in alert.indian_guidelines %}
                    <li>{{ guideline }}</li>
                    {% endfor %}
                </ul>
                {% endif %}
            </div>
            
            <div class="status-card">
                <h2>⏱️ Response Progress</h2>
                <div class="progress-timeline">
                    {% for item in alert.progress %}
                    <div class="timeline-item {{ item.status.lower().replace('_', '-') }}">
                        <div>
                            <strong>{{ item.task }}</strong>
                            <div style="font-size: 0.9em; color: #666;">
                                {% if item.status == 'COMPLETED' %}✅ Completed
                                {% elif item.status == 'IN_PROGRESS' %}🔄 In Progress
                                {% else %}⏳ Pending{% endif %}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h2>🚑 Resource Deployment</h2>
                <div class="resource-grid">
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.medical_teams }}</span>
                        Medical Teams
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.medical_officers }}</span>
                        Medical Officers
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.paramedical_staff }}</span>
                        Paramedical Staff
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.ambulances }}</span>
                        Ambulances
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.isolation_beds }}</span>
                        Isolation Beds
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.testing_kits }}</span>
                        Testing Kits
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.ppe_kits }}</span>
                        PPE Kits
                    </div>
                    <div class="resource-item">
                        <span class="resource-number">{{ alert.resources.budget_allocated }}</span>
                        Budget Allocated
                    </div>
                </div>
            </div>
            
            <div class="status-card">
                <h2>📅 Detailed Timeline</h2>
                <div class="progress-timeline">
                    {% for item in alert.detailed_timeline %}
                    <div class="timeline-item {{ item.status.lower().replace('_', '-') }}">
                        <div>
                            <strong>{{ item.milestone }}</strong>
                            <div style="font-size: 0.9em; color: #666; margin: 5px 0;">{{ item.time }}</div>
                            <div style="font-size: 0.9em;">{{ item.description }}</div>
                        </div>
                    </div>
                    {% endfor %}
                </div>
            </div>
        </div>
        
        <div class="status-card full-width">
            <h2>🌍 Environmental Risk Factors</h2>
            <div class="environmental-factors">
                <h3 style="margin-bottom: 15px;">Key Environmental Contributors</h3>
                <ul class="action-list">
                    {% for factor in alert.environmental_factors %}
                    <li>{{ factor }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h2>⚡ Immediate Actions Taken</h2>
                <ul class="action-list">
                    {% for action in alert.immediate_actions %}
                    <li>{{ action }}</li>
                    {% endfor %}
                </ul>
            </div>
            
            <div class="status-card">
                <h2>🛡️ Prevention Measures</h2>
                <ul class="action-list">
                    {% for measure in alert.prevention_measures %}
                    <li>{{ measure }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        {% if alert.laboratory_guidelines or alert.treatment_protocol %}
        <div class="status-grid">
            {% if alert.laboratory_guidelines %}
            <div class="status-card">
                <h2>🧪 Laboratory Guidelines</h2>
                <ul class="action-list">
                    {% for guideline in alert.laboratory_guidelines %}
                    <li>{{ guideline }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
            
            {% if alert.treatment_protocol %}
            <div class="status-card">
                <h2>💊 Treatment Protocol</h2>
                <ul class="action-list">
                    {% for protocol in alert.treatment_protocol %}
                    <li>{{ protocol }}</li>
                    {% endfor %}
                </ul>
            </div>
            {% endif %}
        </div>
        {% endif %}
        
        {% if alert.vector_control %}
        <div class="status-card full-width">
            <h2>🦟 Vector Control Measures</h2>
            <div class="environmental-factors">
                <h3 style="margin-bottom: 15px;">Specific Vector Control Actions</h3>
                <ul class="action-list">
                    {% for control in alert.vector_control %}
                    <li>{{ control }}</li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        {% endif %}
    </div>
</body>
</html>
    '''

def create_personalized_alert_routes(app):
    """Add personalized alert routes to existing Flask app"""
    status_system = PersonalizedAlertStatusSystem()
    
    @app.route('/alert-status/<alert_id>')
    def personalized_alert_status(alert_id):
        """Show personalized status page for specific alert"""
        alert_details = status_system.get_alert_details(alert_id)
        
        if not alert_details:
            return "Alert not found", 404
        
        template = create_personalized_alert_template()
        return render_template_string(template, alert=alert_details)
    
    @app.route('/api/alert-details/<alert_id>')
    def api_alert_details(alert_id):
        """API endpoint for alert details"""
        alert_details = status_system.get_alert_details(alert_id)
        
        if not alert_details:
            return jsonify({'error': 'Alert not found'}), 404
        
        return jsonify(alert_details)

if __name__ == '__main__':
    # For testing purposes
    app = Flask(__name__)
    create_personalized_alert_routes(app)
    app.run(debug=True, port=5002)