#!/usr/bin/env python3
"""
🏛️ Enhanced Government Alert Details System
Provides personalized, real-time alert details for different diseases and locations
"""

import sqlite3
import json
from datetime import datetime, timedelta
import random
import hashlib

class EnhancedGovernmentAlertDetails:
    
    def __init__(self):
        self.load_alert_templates()
        print("🏛️ Enhanced Government Alert Details System initialized")
    
    def load_alert_templates(self):
        """Load detailed templates for different diseases and scenarios"""
        self.disease_templates = {
            'cholera': {
                'severity': 'CRITICAL',
                'priority': 'IMMEDIATE',
                'timeline_hours': 1,
                'environmental_factors': [
                    'Contaminated water sources identified within 2km radius',
                    'Poor sanitation infrastructure in affected slum areas',
                    'Recent monsoon flooding creating stagnant water pools',
                    'Industrial waste discharge affecting local water supply',
                    'High population density (>15,000 people per km²)',
                    'Limited access to clean water and proper toilets'
                ],
                'immediate_actions': [
                    'Emergency medical teams deployed to affected areas',
                    'Mobile rehydration therapy centers established',
                    'Water quality testing initiated at all sources',
                    'Public health advisory issued through all channels',
                    'Isolation facilities set up for severe cases',
                    'Emergency supplies (ORS, IV fluids) dispatched'
                ],
                'resource_deployment': {
                    'medical_teams': 8,
                    'ambulances': 12,
                    'isolation_beds': 50,
                    'medical_officers': 15,
                    'testing_kits': 1000,
                    'budget': '₹25,00,000'
                },
                'progress_milestones': [
                    {'time': '09:15', 'action': 'First case reported to PHC', 'status': 'completed'},
                    {'time': '10:30', 'action': 'Emergency response team activated', 'status': 'completed'},
                    {'time': '11:45', 'action': 'Water samples collected for testing', 'status': 'completed'},
                    {'time': '13:20', 'action': 'Lab results confirm cholera outbreak', 'status': 'completed'},
                    {'time': '14:00', 'action': 'Public health alert issued', 'status': 'completed'},
                    {'time': '15:30', 'action': 'Medical camps established', 'status': 'in_progress'},
                    {'time': '17:00', 'action': 'Water supply isolation completed', 'status': 'pending'},
                    {'time': '19:00', 'action': 'Door-to-door screening initiated', 'status': 'pending'}
                ]
            },
            'dengue': {
                'severity': 'HIGH',
                'priority': 'HIGH',
                'timeline_hours': 12,
                'environmental_factors': [
                    'Post-monsoon stagnant water in construction sites',
                    'Favorable temperature range (25-30°C) for Aedes mosquitos',
                    'Urban areas with poor drainage systems',
                    'Recent rainfall creating breeding opportunities',
                    'High humidity levels (>70%) supporting vector survival',
                    'Construction activity leaving water containers exposed'
                ],
                'immediate_actions': [
                    'Vector control teams deployed for breeding site elimination',
                    'Fogging operations initiated in affected neighborhoods',
                    'Fever screening camps established at community centers',
                    'Platelet count monitoring for suspected cases',
                    'Community awareness drives launched',
                    'Hospital preparedness for severe dengue cases'
                ],
                'resource_deployment': {
                    'medical_teams': 6,
                    'ambulances': 8,
                    'isolation_beds': 30,
                    'medical_officers': 10,
                    'testing_kits': 500,
                    'budget': '₹18,00,000'
                },
                'progress_milestones': [
                    {'time': '08:45', 'action': 'Cluster of fever cases reported', 'status': 'completed'},
                    {'time': '10:15', 'action': 'Rapid diagnostic tests conducted', 'status': 'completed'},
                    {'time': '12:00', 'action': 'Dengue NS1 positive cases confirmed', 'status': 'completed'},
                    {'time': '13:30', 'action': 'Vector surveillance initiated', 'status': 'completed'},
                    {'time': '15:00', 'action': 'Breeding site elimination started', 'status': 'in_progress'},
                    {'time': '17:30', 'action': 'Fogging operations scheduled', 'status': 'in_progress'},
                    {'time': '20:00', 'action': 'Community education programs', 'status': 'pending'},
                    {'time': '22:00', 'action': 'Hospital bed preparation', 'status': 'pending'}
                ]
            },
            'covid19': {
                'severity': 'HIGH',
                'priority': 'IMMEDIATE',
                'timeline_hours': 2,
                'environmental_factors': [
                    'High population density facilitating rapid transmission',
                    'Poor ventilation in crowded living conditions',
                    'Social gatherings and religious events as super-spreaders',
                    'Air pollution levels affecting respiratory immunity',
                    'Cold weather conditions supporting virus survival',
                    'Limited mask compliance in rural areas'
                ],
                'immediate_actions': [
                    'Contact tracing initiated for all positive cases',
                    'RT-PCR testing camps established at multiple locations',
                    'Quarantine facilities prepared for confirmed cases',
                    'Health screening at community entry points',
                    'COVID appropriate behavior awareness campaigns',
                    'Hospital ICU bed capacity assessment completed'
                ],
                'resource_deployment': {
                    'medical_teams': 12,
                    'ambulances': 15,
                    'isolation_beds': 80,
                    'medical_officers': 20,
                    'testing_kits': 2000,
                    'budget': '₹40,00,000'
                },
                'progress_milestones': [
                    {'time': '07:30', 'action': 'Positive case reported from testing', 'status': 'completed'},
                    {'time': '08:15', 'action': 'Contact tracing team deployed', 'status': 'completed'},
                    {'time': '09:00', 'action': 'Close contacts identified and tested', 'status': 'completed'},
                    {'time': '10:30', 'action': 'Cluster investigation initiated', 'status': 'completed'},
                    {'time': '12:00', 'action': 'Quarantine protocols activated', 'status': 'in_progress'},
                    {'time': '14:00', 'action': 'Public health measures implemented', 'status': 'in_progress'},
                    {'time': '16:00', 'action': 'Vaccination drive assessment', 'status': 'pending'},
                    {'time': '18:00', 'action': 'Community lockdown evaluation', 'status': 'pending'}
                ]
            },
            'typhoid': {
                'severity': 'MODERATE',
                'priority': 'URGENT',
                'timeline_hours': 6,
                'environmental_factors': [
                    'Contaminated food sources identified in local markets',
                    'Poor food handling practices at street vendors',
                    'Inadequate sanitation facilities in affected areas',
                    'Contaminated water supply affecting multiple households',
                    'Overcrowded living conditions facilitating spread',
                    'Inadequate waste disposal systems'
                ],
                'immediate_actions': [
                    'Food safety inspection of local vendors and markets',
                    'Water quality testing at community sources',
                    'Antibiotic treatment for confirmed cases',
                    'Health education on food and water safety',
                    'Vaccination campaign planning for high-risk groups',
                    'Surveillance of food handlers in the area'
                ],
                'resource_deployment': {
                    'medical_teams': 4,
                    'ambulances': 6,
                    'isolation_beds': 20,
                    'medical_officers': 8,
                    'testing_kits': 300,
                    'budget': '₹12,00,000'
                },
                'progress_milestones': [
                    {'time': '09:00', 'action': 'Food poisoning cases reported', 'status': 'completed'},
                    {'time': '11:30', 'action': 'Stool samples collected for testing', 'status': 'completed'},
                    {'time': '14:15', 'action': 'Typhoid confirmed by culture', 'status': 'completed'},
                    {'time': '15:45', 'action': 'Food source investigation started', 'status': 'in_progress'},
                    {'time': '17:30', 'action': 'Water system inspection', 'status': 'in_progress'},
                    {'time': '19:00', 'action': 'Community health education', 'status': 'pending'},
                    {'time': '21:00', 'action': 'Vaccination planning', 'status': 'pending'}
                ]
            },
            'malaria': {
                'severity': 'HIGH',
                'priority': 'HIGH',
                'timeline_hours': 24,
                'environmental_factors': [
                    'Forest areas with stagnant water bodies nearby',
                    'Monsoon season creating ideal breeding conditions',
                    'Tribal areas with limited access to preventive measures',
                    'Temperature range (20-30°C) optimal for mosquito breeding',
                    'High humidity supporting vector development',
                    'Inadequate bed net distribution in rural areas'
                ],
                'immediate_actions': [
                    'Rapid diagnostic tests for fever cases in area',
                    'Anti-malarial drug distribution to affected families',
                    'Insecticide-treated bed net distribution',
                    'Indoor residual spraying in affected households',
                    'Community health worker activation',
                    'Laboratory confirmation of parasite species'
                ],
                'resource_deployment': {
                    'medical_teams': 5,
                    'ambulances': 7,
                    'isolation_beds': 25,
                    'medical_officers': 9,
                    'testing_kits': 400,
                    'budget': '₹15,00,000'
                },
                'progress_milestones': [
                    {'time': '08:00', 'action': 'Fever cases reported from tribal area', 'status': 'completed'},
                    {'time': '10:30', 'action': 'Blood smears collected for testing', 'status': 'completed'},
                    {'time': '13:00', 'action': 'Malaria parasite confirmed', 'status': 'completed'},
                    {'time': '15:00', 'action': 'Anti-malarial treatment initiated', 'status': 'in_progress'},
                    {'time': '17:00', 'action': 'Vector control measures started', 'status': 'in_progress'},
                    {'time': '19:30', 'action': 'Bed net distribution', 'status': 'pending'},
                    {'time': '21:00', 'action': 'Community education program', 'status': 'pending'}
                ]
            },
            'hepatitis_a': {
                'severity': 'MODERATE',
                'priority': 'URGENT',
                'timeline_hours': 12,
                'environmental_factors': [
                    'Contaminated water sources affecting multiple families',
                    'Poor sanitation practices in community',
                    'Overcrowded living conditions',
                    'Inadequate food safety measures',
                    'Limited access to clean water and toilets',
                    'High population mobility spreading infection'
                ],
                'immediate_actions': [
                    'Liver function monitoring for affected patients',
                    'Hepatitis A vaccination for close contacts',
                    'Water source decontamination and chlorination',
                    'Food safety education in affected community',
                    'Contact isolation and monitoring',
                    'Immunoglobulin administration for high-risk contacts'
                ],
                'resource_deployment': {
                    'medical_teams': 3,
                    'ambulances': 4,
                    'isolation_beds': 15,
                    'medical_officers': 6,
                    'testing_kits': 200,
                    'budget': '₹10,00,000'
                },
                'progress_milestones': [
                    {'time': '10:00', 'action': 'Jaundice cases reported', 'status': 'completed'},
                    {'time': '12:30', 'action': 'Liver function tests conducted', 'status': 'completed'},
                    {'time': '15:00', 'action': 'Hepatitis A IgM positive', 'status': 'completed'},
                    {'time': '16:30', 'action': 'Contact tracing initiated', 'status': 'in_progress'},
                    {'time': '18:00', 'action': 'Water source investigation', 'status': 'in_progress'},
                    {'time': '20:00', 'action': 'Vaccination of contacts', 'status': 'pending'},
                    {'time': '22:00', 'action': 'Community hygiene education', 'status': 'pending'}
                ]
            }
        }
    
    def get_personalized_alert_details(self, alert_id, disease, location, case_count):
        """Generate personalized alert details based on disease type and context"""
        if disease.lower() not in self.disease_templates:
            disease = 'general_illness'
        
        template = self.disease_templates[disease.lower()]
        
        # Generate personalized details using alert_id as seed for consistency
        random.seed(int(hashlib.md5(alert_id.encode()).hexdigest(), 16) % (10**8))
        
        # Customize resource deployment based on case count
        multiplier = max(1, case_count / 5)
        resources = {
            'medical_teams': max(1, int(template['resource_deployment']['medical_teams'] * multiplier)),
            'ambulances': max(1, int(template['resource_deployment']['ambulances'] * multiplier)),
            'isolation_beds': max(5, int(template['resource_deployment']['isolation_beds'] * multiplier)),
            'medical_officers': max(2, int(template['resource_deployment']['medical_officers'] * multiplier)),
            'testing_kits': max(50, int(template['resource_deployment']['testing_kits'] * multiplier)),
            'budget': f"₹{int(float(template['resource_deployment']['budget'].replace('₹','').replace(',','')) * multiplier):,}"
        }
        
        # Generate location-specific environmental factors
        location_factors = self.get_location_specific_factors(location, disease)
        environmental_factors = template['environmental_factors'] + location_factors
        
        # Generate progress timeline with current time
        current_hour = datetime.now().hour
        progress_timeline = []
        for i, milestone in enumerate(template['progress_milestones']):
            milestone_hour = int(milestone['time'].split(':')[0])
            if milestone_hour <= current_hour:
                status = 'completed'
            elif milestone_hour == current_hour + 1:
                status = 'in_progress'
            else:
                status = 'pending'
            
            progress_timeline.append({
                'time': milestone['time'],
                'action': milestone['action'],
                'status': status,
                'location': location
            })
        
        # Generate real-time updates
        updates = self.generate_real_time_updates(disease, location, case_count)
        
        return {
            'alert_id': alert_id,
            'disease': disease,
            'location': location,
            'case_count': case_count,
            'severity': template['severity'],
            'priority': template['priority'],
            'timeline_hours': template['timeline_hours'],
            'environmental_factors': environmental_factors,
            'immediate_actions': template['immediate_actions'],
            'resource_deployment': resources,
            'progress_timeline': progress_timeline,
            'real_time_updates': updates,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_location_specific_factors(self, location, disease):
        """Get location-specific environmental factors"""
        location_factors = {
            'Mumbai': [
                'High coastal humidity affecting disease spread',
                'Dharavi slum area with 1M+ population density',
                'Monsoon flooding in low-lying areas',
                'Industrial discharge from MIDC areas'
            ],
            'Delhi': [
                'Severe air pollution (AQI >300) affecting immunity',
                'Dense urban population in NCR region',
                'Yamuna river pollution affecting water quality',
                'Cold weather supporting pathogen survival'
            ],
            'Bangalore': [
                'Tech hub with high population mobility',
                'Lake contamination affecting water sources',
                'Urban heat island effect',
                'Rapid urbanization straining infrastructure'
            ],
            'Chennai': [
                'Coastal city with high humidity levels',
                'Monsoon season water stagnation',
                'Industrial pollution in surrounding areas',
                'Dense population in fishing communities'
            ]
        }
        
        return location_factors.get(location, [
            f'{location} specific geographic risk factors identified',
            'Local environmental conditions assessed',
            'Regional health infrastructure evaluated'
        ])
    
    def generate_real_time_updates(self, disease, location, case_count):
        """Generate realistic real-time updates"""
        updates = []
        current_time = datetime.now()
        
        # Generate updates for last few hours
        for i in range(5):
            update_time = current_time - timedelta(hours=i)
            update = {
                'time': update_time.strftime('%H:%M'),
                'update': self.get_disease_specific_update(disease, location, i),
                'priority': 'HIGH' if i < 2 else 'MEDIUM'
            }
            updates.append(update)
        
        return updates
    
    def get_disease_specific_update(self, disease, location, hour_offset):
        """Get disease-specific real-time updates"""
        updates_map = {
            'cholera': [
                f'Water testing completed at {random.randint(5,15)} sources in {location}',
                f'Emergency rehydration center set up at Community Health Center',
                f'Mobile medical units deployed to affected slum areas',
                f'Public health advisory broadcast on local radio and TV',
                f'{random.randint(50,200)} households surveyed for symptoms'
            ],
            'dengue': [
                f'Fogging operations completed in {random.randint(3,8)} sectors of {location}',
                f'Breeding site elimination: {random.randint(85,95)}% completion rate',
                f'Fever clinics established at {random.randint(4,10)} primary health centers',
                f'{random.randint(100,500)} rapid diagnostic tests conducted',
                f'Vector surveillance teams deployed to construction sites'
            ],
            'covid19': [
                f'Contact tracing: {random.randint(25,100)} close contacts identified',
                f'RT-PCR testing facility established at {location} district hospital',
                f'{random.randint(200,1000)} people screened at entry points',
                f'Quarantine facility prepared with {random.randint(50,200)} bed capacity',
                f'Vaccination drive planning meeting completed'
            ],
            'typhoid': [
                f'Food vendor inspection completed at {random.randint(20,50)} locations',
                f'Water quality testing: {random.randint(3,8)} contaminated sources identified',
                f'Antibiotic treatment started for {random.randint(15,30)} confirmed cases',
                f'Health education conducted in {random.randint(5,12)} communities',
                f'Food safety protocols implemented at local markets'
            ],
            'malaria': [
                f'Indoor residual spraying completed in {random.randint(200,500)} houses',
                f'Bed net distribution: {random.randint(1000,2000)} nets distributed',
                f'Blood smear testing: {random.randint(100,300)} samples processed',
                f'Community health workers activated in {random.randint(8,15)} villages',
                f'Anti-malarial drug stock replenished at PHCs'
            ]
        }
        
        disease_updates = updates_map.get(disease, [
            f'Medical surveillance increased in {location} area',
            f'Health department coordination meeting completed',
            f'Laboratory testing capacity expanded',
            f'Community awareness programs initiated',
            f'Emergency response protocols activated'
        ])
        
        return disease_updates[hour_offset % len(disease_updates)]

def create_enhanced_government_alert_routes(app):
    """Add enhanced government alert routes to existing Flask app"""
    alert_system = EnhancedGovernmentAlertDetails()
    
    @app.route('/enhanced-alert-details/<alert_id>')
    def enhanced_alert_details(alert_id):
        """Show enhanced personalized alert details"""
        try:
            # Get alert details from database
            conn = sqlite3.connect('government_alerts.db')
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT alert_id, disease, location_city, case_count, severity, priority
                FROM government_alerts 
                WHERE alert_id = ?
            """, (alert_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return "Alert not found", 404
            
            # Generate enhanced details
            enhanced_details = alert_system.get_personalized_alert_details(
                result[0], result[1], result[2], result[3]
            )
            
            return enhanced_details
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For testing purposes
    system = EnhancedGovernmentAlertDetails()
    details = system.get_personalized_alert_details(
        'RHAS-CHOLERA-123', 'cholera', 'Mumbai', 5
    )
    print(json.dumps(details, indent=2))