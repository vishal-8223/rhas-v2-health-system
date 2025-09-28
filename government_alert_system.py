#!/usr/bin/env python3
"""
🏛️ Government Health Alert & Action Tracking System
Automatically sends alerts to departments and tracks actions based on government health principles
"""

import json
import sqlite3
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import uuid

class AlertPriority(Enum):
    IMMEDIATE = "IMMEDIATE"  # Within 1 hour
    URGENT = "URGENT"       # Within 6 hours
    HIGH = "HIGH"           # Within 24 hours
    MODERATE = "MODERATE"   # Within 72 hours
    LOW = "LOW"             # Within 1 week

class AlertStatus(Enum):
    SENT = "SENT"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    OVERDUE = "OVERDUE"

class DepartmentType(Enum):
    HEALTH_MINISTRY = "HEALTH_MINISTRY"
    DISTRICT_COLLECTOR = "DISTRICT_COLLECTOR"
    CMO_OFFICE = "CMO_OFFICE"
    PHC_INCHARGE = "PHC_INCHARGE"
    EPIDEMIC_CELL = "EPIDEMIC_CELL"
    LAB_DIRECTOR = "LAB_DIRECTOR"
    VECTOR_CONTROL = "VECTOR_CONTROL"
    WATER_SANITATION = "WATER_SANITATION"
    EMERGENCY_RESPONSE = "EMERGENCY_RESPONSE"
    SURVEILLANCE_TEAM = "SURVEILLANCE_TEAM"

@dataclass
class GovernmentAlert:
    alert_id: str
    disease: str
    location: Dict[str, str]
    case_count: int
    severity: str
    priority: AlertPriority
    departments: List[DepartmentType]
    actions_required: List[str]
    timeline_hours: int
    created_at: datetime
    status: AlertStatus = AlertStatus.SENT
    acknowledged_by: List[str] = None
    actions_completed: List[str] = None
    notes: str = ""

@dataclass
class ActionItem:
    action_id: str
    alert_id: str
    department: DepartmentType
    action_description: str
    assigned_officer: str
    deadline: datetime
    status: AlertStatus
    progress_percentage: int = 0
    completion_notes: str = ""
    created_at: datetime = None

class GovernmentHealthAlertSystem:
    """
    Government Health Alert System following WHO and Indian health ministry protocols
    """
    
    def __init__(self):
        self.init_database()
        self.load_government_protocols()
        self.load_department_contacts()
        print("🏛️ Government Health Alert System initialized")
    
    def init_database(self):
        """Initialize alert tracking database"""
        conn = sqlite3.connect('government_alerts.db')
        cursor = conn.cursor()
        
        # Alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS government_alerts (
                alert_id TEXT PRIMARY KEY,
                disease TEXT NOT NULL,
                location_city TEXT,
                location_state TEXT,
                case_count INTEGER,
                severity TEXT,
                priority TEXT,
                departments TEXT,
                actions_required TEXT,
                timeline_hours INTEGER,
                status TEXT,
                acknowledged_by TEXT,
                actions_completed TEXT,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Action items table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS action_items (
                action_id TEXT PRIMARY KEY,
                alert_id TEXT,
                department TEXT,
                action_description TEXT,
                assigned_officer TEXT,
                deadline TIMESTAMP,
                status TEXT,
                progress_percentage INTEGER DEFAULT 0,
                completion_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (alert_id) REFERENCES government_alerts (alert_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_government_protocols(self):
        """Load government health protocols for different diseases"""
        self.protocols = {
            'cholera': {
                'priority': AlertPriority.IMMEDIATE,
                'timeline_hours': 1,
                'departments': [
                    DepartmentType.HEALTH_MINISTRY,
                    DepartmentType.DISTRICT_COLLECTOR,
                    DepartmentType.CMO_OFFICE,
                    DepartmentType.EPIDEMIC_CELL,
                    DepartmentType.WATER_SANITATION,
                    DepartmentType.LAB_DIRECTOR
                ],
                'actions': [
                    "Activate epidemic response team immediately",
                    "Isolate affected area and restrict movement",
                    "Set up emergency rehydration centers",
                    "Test water sources in 5km radius",
                    "Deploy rapid response medical teams",
                    "Issue public health advisory",
                    "Coordinate with media for awareness",
                    "Arrange emergency medical supplies"
                ]
            },
            'typhoid': {
                'priority': AlertPriority.URGENT,
                'timeline_hours': 6,
                'departments': [
                    DepartmentType.CMO_OFFICE,
                    DepartmentType.PHC_INCHARGE,
                    DepartmentType.EPIDEMIC_CELL,
                    DepartmentType.WATER_SANITATION,
                    DepartmentType.LAB_DIRECTOR
                ],
                'actions': [
                    "Investigate food and water sources",
                    "Contact tracing of affected individuals",
                    "Set up temporary treatment centers",
                    "Distribute preventive medications",
                    "Water quality testing and chlorination",
                    "Health education in affected areas"
                ]
            },
            'malaria': {
                'priority': AlertPriority.HIGH,
                'timeline_hours': 24,
                'departments': [
                    DepartmentType.CMO_OFFICE,
                    DepartmentType.VECTOR_CONTROL,
                    DepartmentType.PHC_INCHARGE,
                    DepartmentType.SURVEILLANCE_TEAM
                ],
                'actions': [
                    "Deploy vector control teams",
                    "Spray anti-larvicide in water bodies",
                    "Distribute bed nets and repellents",
                    "Set up fever surveillance camps",
                    "Stock anti-malarial drugs",
                    "Community awareness programs"
                ]
            },
            'dengue': {
                'priority': AlertPriority.HIGH,
                'timeline_hours': 12,
                'departments': [
                    DepartmentType.CMO_OFFICE,
                    DepartmentType.VECTOR_CONTROL,
                    DepartmentType.EMERGENCY_RESPONSE,
                    DepartmentType.SURVEILLANCE_TEAM
                ],
                'actions': [
                    "Eliminate breeding sites immediately",
                    "Deploy fogging operations",
                    "Set up dengue screening camps",
                    "Monitor platelet counts of patients",
                    "Stock IV fluids and supportive care",
                    "Issue dengue prevention guidelines"
                ]
            },
            'covid19': {
                'priority': AlertPriority.IMMEDIATE,
                'timeline_hours': 2,
                'departments': [
                    DepartmentType.HEALTH_MINISTRY,
                    DepartmentType.DISTRICT_COLLECTOR,
                    DepartmentType.CMO_OFFICE,
                    DepartmentType.EPIDEMIC_CELL,
                    DepartmentType.LAB_DIRECTOR,
                    DepartmentType.EMERGENCY_RESPONSE
                ],
                'actions': [
                    "Activate COVID response protocol",
                    "Contact tracing and quarantine",
                    "Set up testing facilities",
                    "Arrange isolation centers",
                    "Deploy health screening teams",
                    "Issue lockdown advisories if needed",
                    "Coordinate with central authorities"
                ]
            },
            'hepatitis_a': {
                'priority': AlertPriority.URGENT,
                'timeline_hours': 12,
                'departments': [
                    DepartmentType.CMO_OFFICE,
                    DepartmentType.WATER_SANITATION,
                    DepartmentType.PHC_INCHARGE,
                    DepartmentType.LAB_DIRECTOR
                ],
                'actions': [
                    "Investigate water contamination sources",
                    "Provide hepatitis A vaccination",
                    "Set up liver function monitoring",
                    "Ensure safe drinking water supply",
                    "Health education on hygiene",
                    "Monitor food handlers in area"
                ]
            }
        }
    
    def load_department_contacts(self):
        """Load department contact information"""
        self.departments = {
            DepartmentType.HEALTH_MINISTRY: {
                'name': 'Ministry of Health & Family Welfare',
                'contact_person': 'Dr. Rajesh Kumar (Joint Secretary)',
                'phone': '+91-11-23061863',
                'email': 'jshealth@mohfw.gov.in',
                'designation': 'Joint Secretary (Public Health)'
            },
            DepartmentType.DISTRICT_COLLECTOR: {
                'name': 'District Collector Office',
                'contact_person': 'Mrs. Priya Sharma (District Collector)',
                'phone': '+91-80-22340000',
                'email': 'collector@district.gov.in',
                'designation': 'District Collector'
            },
            DepartmentType.CMO_OFFICE: {
                'name': 'Chief Medical Officer',
                'contact_person': 'Dr. Amit Patel (CMO)',
                'phone': '+91-80-22350000',
                'email': 'cmo@health.gov.in',
                'designation': 'Chief Medical Officer'
            },
            DepartmentType.PHC_INCHARGE: {
                'name': 'Primary Health Center',
                'contact_person': 'Dr. Sunita Devi (PHC Incharge)',
                'phone': '+91-80-22360000',
                'email': 'phc@health.gov.in',
                'designation': 'PHC Medical Officer'
            },
            DepartmentType.EPIDEMIC_CELL: {
                'name': 'State Epidemic Cell',
                'contact_person': 'Dr. Vikash Singh (Epidemiologist)',
                'phone': '+91-80-22370000',
                'email': 'epidemic@health.gov.in',
                'designation': 'State Epidemiologist'
            },
            DepartmentType.LAB_DIRECTOR: {
                'name': 'Public Health Laboratory',
                'contact_person': 'Dr. Sarah Johnson (Lab Director)',
                'phone': '+91-80-22380000',
                'email': 'lab@health.gov.in',
                'designation': 'Laboratory Director'
            },
            DepartmentType.VECTOR_CONTROL: {
                'name': 'Vector Control Department',
                'contact_person': 'Mr. Ravi Kumar (Vector Control Officer)',
                'phone': '+91-80-22390000',
                'email': 'vector@health.gov.in',
                'designation': 'Vector Control Officer'
            },
            DepartmentType.WATER_SANITATION: {
                'name': 'Water & Sanitation Department',
                'contact_person': 'Eng. Meera Patel (Executive Engineer)',
                'phone': '+91-80-22400000',
                'email': 'water@urban.gov.in',
                'designation': 'Executive Engineer (Water)'
            },
            DepartmentType.EMERGENCY_RESPONSE: {
                'name': '108 Emergency Response',
                'contact_person': 'Mr. Suresh Reddy (Emergency Coordinator)',
                'phone': '+91-80-108',
                'email': 'emergency@108.gov.in',
                'designation': 'Emergency Response Coordinator'
            },
            DepartmentType.SURVEILLANCE_TEAM: {
                'name': 'Disease Surveillance Team',
                'contact_person': 'Dr. Kavitha Rao (Surveillance Officer)',
                'phone': '+91-80-22410000',
                'email': 'surveillance@health.gov.in',
                'designation': 'Disease Surveillance Officer'
            }
        }
    
    def trigger_government_alert(self, disease: str, location: Dict[str, str], 
                                case_count: int = 1, severity: str = "High",
                                additional_context: str = "") -> str:
        """
        Trigger government alert based on disease detection
        """
        if disease.lower() not in self.protocols:
            # Default protocol for unknown diseases
            protocol = {
                'priority': AlertPriority.HIGH,
                'timeline_hours': 24,
                'departments': [DepartmentType.CMO_OFFICE, DepartmentType.EPIDEMIC_CELL],
                'actions': ["Investigate unknown disease pattern", "Consult specialists"]
            }
        else:
            protocol = self.protocols[disease.lower()]
        
        # Generate alert ID
        alert_id = f"RHAS-{disease.upper()}-{int(time.time())}"
        
        # Create government alert
        alert = GovernmentAlert(
            alert_id=alert_id,
            disease=disease,
            location=location,
            case_count=case_count,
            severity=severity,
            priority=protocol['priority'],
            departments=protocol['departments'],
            actions_required=protocol['actions'],
            timeline_hours=protocol['timeline_hours'],
            created_at=datetime.now(),
            acknowledged_by=[],
            actions_completed=[],
            notes=additional_context
        )
        
        # Save to database
        self.save_alert(alert)
        
        # Create action items for each department
        self.create_action_items(alert)
        
        # Send notifications (simulated)
        self.send_department_notifications(alert)
        
        print(f"🚨 GOVERNMENT ALERT TRIGGERED: {alert_id}")
        print(f"   Disease: {disease.title()}")
        print(f"   Priority: {protocol['priority'].value}")
        print(f"   Departments: {len(protocol['departments'])} notified")
        print(f"   Timeline: {protocol['timeline_hours']} hours")
        
        return alert_id
    
    def save_alert(self, alert: GovernmentAlert):
        """Save alert to database"""
        conn = sqlite3.connect('government_alerts.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO government_alerts 
            (alert_id, disease, location_city, location_state, case_count, severity, 
             priority, departments, actions_required, timeline_hours, status, 
             acknowledged_by, actions_completed, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            alert.alert_id,
            alert.disease,
            alert.location.get('city', 'Unknown'),
            alert.location.get('state', 'Unknown'),
            alert.case_count,
            alert.severity,
            alert.priority.value,
            json.dumps([dept.value for dept in alert.departments]),
            json.dumps(alert.actions_required),
            alert.timeline_hours,
            alert.status.value,
            json.dumps(alert.acknowledged_by or []),
            json.dumps(alert.actions_completed or []),
            alert.notes
        ))
        
        conn.commit()
        conn.close()
    
    def create_action_items(self, alert: GovernmentAlert):
        """Create specific action items for each department"""
        conn = sqlite3.connect('government_alerts.db')
        cursor = conn.cursor()
        
        deadline = alert.created_at + timedelta(hours=alert.timeline_hours)
        
        for dept in alert.departments:
            # Create action items based on department responsibilities
            dept_actions = self.get_department_specific_actions(dept, alert.disease)
            
            for i, action_desc in enumerate(dept_actions):
                action_id = f"{alert.alert_id}-{dept.value}-{i}-{int(time.time() * 1000)}"
                
                action = ActionItem(
                    action_id=action_id,
                    alert_id=alert.alert_id,
                    department=dept,
                    action_description=action_desc,
                    assigned_officer=self.departments[dept]['contact_person'],
                    deadline=deadline,
                    status=AlertStatus.SENT,
                    created_at=datetime.now()
                )
                
                cursor.execute('''
                    INSERT INTO action_items 
                    (action_id, alert_id, department, action_description, assigned_officer,
                     deadline, status, progress_percentage, completion_notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    action.action_id,
                    action.alert_id,
                    action.department.value,
                    action.action_description,
                    action.assigned_officer,
                    action.deadline.isoformat(),
                    action.status.value,
                    action.progress_percentage,
                    action.completion_notes
                ))
        
        conn.commit()
        conn.close()
    
    def get_department_specific_actions(self, dept: DepartmentType, disease: str) -> List[str]:
        """Get specific actions for each department based on disease"""
        actions_map = {
            DepartmentType.HEALTH_MINISTRY: [
                f"Coordinate national response for {disease}",
                "Release emergency health advisory",
                "Mobilize central medical teams"
            ],
            DepartmentType.DISTRICT_COLLECTOR: [
                f"Declare {disease} emergency in district",
                "Coordinate inter-departmental response",
                "Ensure resource allocation"
            ],
            DepartmentType.CMO_OFFICE: [
                f"Activate {disease} treatment protocols",
                "Deploy medical teams to affected area",
                "Monitor case progression"
            ],
            DepartmentType.PHC_INCHARGE: [
                f"Set up {disease} screening at PHC",
                "Provide immediate medical care",
                "Report daily case numbers"
            ],
            DepartmentType.EPIDEMIC_CELL: [
                f"Investigate {disease} outbreak pattern",
                "Conduct epidemiological survey",
                "Implement containment measures"
            ],
            DepartmentType.LAB_DIRECTOR: [
                f"Set up {disease} testing facilities",
                "Process samples within 24 hours",
                "Maintain testing quality standards"
            ],
            DepartmentType.VECTOR_CONTROL: [
                f"Deploy vector control for {disease}",
                "Eliminate breeding sites",
                "Conduct fogging operations"
            ],
            DepartmentType.WATER_SANITATION: [
                f"Test water sources for {disease} contamination",
                "Ensure safe drinking water supply",
                "Implement sanitation measures"
            ],
            DepartmentType.EMERGENCY_RESPONSE: [
                f"Prepare ambulances for {disease} cases",
                "Set up emergency hotlines",
                "Coordinate patient transport"
            ],
            DepartmentType.SURVEILLANCE_TEAM: [
                f"Monitor {disease} spread patterns",
                "Conduct active case finding",
                "Update surveillance database"
            ]
        }
        
        return actions_map.get(dept, [f"Take appropriate action for {disease}"])
    
    def send_department_notifications(self, alert: GovernmentAlert):
        """Send notifications to departments (simulated)"""
        for dept in alert.departments:
            dept_info = self.departments[dept]
            
            message = f"""
🚨 URGENT HEALTH ALERT - {alert.priority.value}

Alert ID: {alert.alert_id}
Disease: {alert.disease.title()}
Location: {alert.location.get('city', 'Unknown')}, {alert.location.get('state', 'Unknown')}
Cases: {alert.case_count}
Severity: {alert.severity}

TO: {dept_info['contact_person']}
DESIGNATION: {dept_info['designation']}

IMMEDIATE ACTION REQUIRED:
Timeline: {alert.timeline_hours} hours from now

Your assigned actions will be sent separately.
Please acknowledge receipt immediately.

Contact: RHAS Emergency Coordination
Phone: +91-80-RHAS-911
            """
            
            print(f"📤 ALERT SENT to {dept.value}: {dept_info['contact_person']}")
    
    def update_action_status(self, action_id: str, status: AlertStatus, 
                           progress: int = 0, notes: str = ""):
        """Update action item status"""
        conn = sqlite3.connect('government_alerts.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE action_items 
            SET status = ?, progress_percentage = ?, completion_notes = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE action_id = ?
        ''', (status.value, progress, notes, action_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Action {action_id} updated: {status.value} ({progress}%)")
    
    def get_active_alerts(self) -> List[Dict]:
        """Get all active government alerts"""
        conn = sqlite3.connect('government_alerts.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM government_alerts 
            WHERE status != 'COMPLETED'
            ORDER BY created_at DESC
        ''')
        
        alerts = []
        for row in cursor.fetchall():
            alerts.append({
                'alert_id': row[0],
                'disease': row[1],
                'location': f"{row[2]}, {row[3]}",
                'case_count': row[4],
                'severity': row[5],
                'priority': row[6],
                'status': row[9],
                'created_at': row[14]
            })
        
        conn.close()
        return alerts
    
    def get_action_status(self, alert_id: str) -> List[Dict]:
        """Get action status for an alert"""
        conn = sqlite3.connect('government_alerts.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT action_id, department, action_description, assigned_officer,
                   deadline, status, progress_percentage, completion_notes,
                   created_at, updated_at
            FROM action_items 
            WHERE alert_id = ?
            ORDER BY created_at
        ''', (alert_id,))
        
        actions = []
        for row in cursor.fetchall():
            actions.append({
                'action_id': row[0],
                'department': row[1],
                'description': row[2],
                'assigned_officer': row[3],
                'deadline': row[4],
                'status': row[5],
                'progress': row[6],
                'notes': row[7],
                'created_at': row[8],
                'updated_at': row[9]
            })
        
        conn.close()
        return actions

# Global instance
gov_alert_system = GovernmentHealthAlertSystem()

def trigger_disease_alert(disease: str, location: Dict[str, str], case_count: int = 1, 
                         severity: str = "High") -> str:
    """
    Public function to trigger government alerts from disease detection
    """
    return gov_alert_system.trigger_government_alert(disease, location, case_count, severity)

def get_alert_dashboard_data() -> Dict:
    """
    Get government alert data for dashboard display
    """
    active_alerts = gov_alert_system.get_active_alerts()
    
    # Get action summary
    conn = sqlite3.connect('government_alerts.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM government_alerts WHERE status = "SENT"')
    pending_alerts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM government_alerts WHERE status = "IN_PROGRESS"')
    active_alerts_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM government_alerts WHERE status = "COMPLETED"')
    completed_alerts = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM action_items WHERE status = "COMPLETED"')
    completed_actions = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM action_items WHERE status != "COMPLETED"')
    pending_actions = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        'active_alerts': active_alerts,
        'pending_alerts': pending_alerts,
        'active_alerts_count': active_alerts_count,
        'completed_alerts': completed_alerts,
        'completed_actions': completed_actions,
        'pending_actions': pending_actions,
        'total_departments': len(gov_alert_system.departments)
    }

if __name__ == "__main__":
    # Test the system
    print("🏛️ Testing Government Health Alert System")
    
    # Simulate disease detections
    test_cases = [
        ("cholera", {"city": "Mumbai", "state": "Maharashtra"}, 3, "High"),
        ("dengue", {"city": "Delhi", "state": "Delhi"}, 5, "High"),
        ("covid19", {"city": "Bangalore", "state": "Karnataka"}, 1, "Medium")
    ]
    
    for disease, location, cases, severity in test_cases:
        alert_id = trigger_disease_alert(disease, location, cases, severity)
        print(f"Alert {alert_id} triggered for {disease}")
        
        # Simulate some action updates
        actions = gov_alert_system.get_action_status(alert_id)
        if actions:
            # Acknowledge first action
            gov_alert_system.update_action_status(
                actions[0]['action_id'], 
                AlertStatus.ACKNOWLEDGED, 
                10, 
                "Alert received and team mobilized"
            )
    
    # Show dashboard data
    dashboard_data = get_alert_dashboard_data()
    print("\n📊 Government Alert Dashboard Summary:")
    print(f"   Active Alerts: {dashboard_data['active_alerts_count']}")
    print(f"   Completed Actions: {dashboard_data['completed_actions']}")
    print(f"   Pending Actions: {dashboard_data['pending_actions']}")
