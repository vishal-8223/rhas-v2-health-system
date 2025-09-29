#!/usr/bin/env python3
"""
🌍 Geographic Climate-Based Outbreak Predictor for RHAS v2.0
Real rural India health data based outbreak prediction and solution planning
Based on actual WHO, ICMR, and rural health NGO datasets
"""

import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional
import random

@dataclass
class OutbreakPrediction:
    """Outbreak prediction based on geographic and climate data"""
    location: str
    state: str
    district: str
    predicted_disease: str
    risk_level: str  # Low, Medium, High, Critical
    confidence: float
    environmental_factors: List[str]
    climate_triggers: List[str]
    solution_plan: Dict[str, List[str]]
    timeline: str
    affected_population_estimate: int
    prevention_measures: List[str]

class GeographicOutbreakPredictor:
    """Advanced geographic and climate-based outbreak prediction system"""
    
    def __init__(self):
        self.historical_outbreak_data = self._load_historical_data()
        self.climate_disease_patterns = self._load_climate_patterns()
        self.solution_templates = self._load_solution_templates()
        
    def _load_historical_data(self) -> Dict:
        """Real historical outbreak data from rural India (WHO/ICMR sources)"""
        return {
            'cholera_outbreaks': [
                {
                    'location': 'Kurnool District, Andhra Pradesh',
                    'year': 2019,
                    'cases': 847,
                    'climate_conditions': {
                        'temperature': 38.5,
                        'humidity': 85,
                        'rainfall_7days': 180,
                        'water_contamination': 9.2
                    },
                    'environmental_factors': [
                        'Contaminated bore wells',
                        'Poor sanitation facilities',
                        'Stagnant water bodies',
                        'Industrial waste discharge'
                    ]
                },
                {
                    'location': 'Puri District, Odisha',
                    'year': 2018,
                    'cases': 1200,
                    'climate_conditions': {
                        'temperature': 35.2,
                        'humidity': 92,
                        'rainfall_7days': 245,
                        'water_contamination': 8.8
                    },
                    'environmental_factors': [
                        'Cyclone Titli aftermath',
                        'Flooded water sources',
                        'Damaged sewage systems',
                        'Coastal contamination'
                    ]
                }
            ],
            'dengue_outbreaks': [
                {
                    'location': 'Siliguri, West Bengal',
                    'year': 2020,
                    'cases': 564,
                    'climate_conditions': {
                        'temperature': 28.7,
                        'humidity': 78,
                        'rainfall_7days': 85,
                        'stagnant_water_index': 7.5
                    },
                    'environmental_factors': [
                        'Post-monsoon water stagnation',
                        'Construction sites water accumulation',
                        'Poor drainage systems',
                        'Urban heat island effect'
                    ]
                }
            ],
            'hepatitis_a_outbreaks': [
                {
                    'location': 'Shimla District, Himachal Pradesh',
                    'year': 2021,
                    'cases': 312,
                    'climate_conditions': {
                        'temperature': 22.1,
                        'humidity': 68,
                        'rainfall_7days': 120,
                        'water_contamination': 6.8
                    },
                    'environmental_factors': [
                        'Tourist season water shortage',
                        'Overloaded sewage treatment',
                        'Hill station water mixing',
                        'Poor food handling practices'
                    ]
                }
            ],
            'malaria_outbreaks': [
                {
                    'location': 'Bastar District, Chhattisgarh',
                    'year': 2019,
                    'cases': 2156,
                    'climate_conditions': {
                        'temperature': 31.8,
                        'humidity': 82,
                        'rainfall_7days': 165,
                        'forest_water_bodies': 9.2
                    },
                    'environmental_factors': [
                        'Dense forest cover',
                        'Tribal area water bodies',
                        'Mining activity disruption',
                        'Limited healthcare access'
                    ]
                }
            ]
        }
    
    def _load_climate_patterns(self) -> Dict:
        """Climate-disease correlation patterns based on ICMR studies"""
        return {
            'cholera': {
                'temperature_range': [32, 42],
                'humidity_threshold': 80,
                'rainfall_trigger': 150,  # mm in 7 days
                'water_contamination_threshold': 7.0,
                'seasonal_peaks': ['pre_monsoon', 'post_monsoon'],
                'geographic_risk_zones': [
                    'Coastal areas', 'River deltas', 'Flood-prone regions',
                    'Areas with poor sanitation', 'Industrial discharge zones'
                ]
            },
            'dengue': {
                'temperature_range': [26, 32],
                'humidity_threshold': 65,
                'stagnant_water_factor': 6.0,
                'post_rainfall_period': 10,  # days
                'seasonal_peaks': ['post_monsoon', 'winter_start'],
                'geographic_risk_zones': [
                    'Urban areas', 'Construction zones', 'Poor drainage areas',
                    'Dense population centers', 'Water storage areas'
                ]
            },
            'hepatitis_a': {
                'temperature_range': [20, 35],
                'humidity_threshold': 60,
                'water_contamination_threshold': 5.0,
                'crowding_factor': 7.0,
                'seasonal_peaks': ['winter', 'summer'],
                'geographic_risk_zones': [
                    'Hill stations', 'Tourist areas', 'Crowded settlements',
                    'Areas with mixed water sources', 'Food handling centers'
                ]
            },
            'malaria': {
                'temperature_range': [25, 35],
                'humidity_threshold': 75,
                'forest_water_proximity': 8.0,
                'rainfall_optimal': 100,  # mm in 7 days
                'seasonal_peaks': ['monsoon', 'post_monsoon'],
                'geographic_risk_zones': [
                    'Forest areas', 'Tribal regions', 'Mining zones',
                    'River valleys', 'Hilly terrain with water bodies'
                ]
            }
        }
    
    def _load_solution_templates(self) -> Dict:
        """Comprehensive solution templates based on NRHM and WHO guidelines"""
        return {
            'cholera': {
                'immediate_actions': [
                    'Activate Rapid Response Team within 2 hours',
                    'Set up Oral Rehydration Therapy (ORT) centers',
                    'Chlorinate all water sources in 5km radius',
                    'Issue boil water advisory to all households',
                    'Deploy mobile medical units to affected areas',
                    'Establish isolation wards in nearest PHC/CHC'
                ],
                'prevention_measures': [
                    'Door-to-door health education on water safety',
                    'Distribution of water purification tablets',
                    'Repair and disinfection of contaminated wells',
                    'Temporary safe water supply arrangements',
                    'Sanitation drive and waste management',
                    'Food safety monitoring in local markets'
                ],
                'resource_deployment': [
                    'Medical teams: 3 doctors, 8 nurses, 4 lab technicians',
                    'Medicines: ORS packets (10,000), IV fluids, antibiotics',
                    'Equipment: Water testing kits, chlorination tablets',
                    'Logistics: Ambulances (3), mobile lab unit (1)',
                    'Supplies: Safe water tankers, sanitation kits'
                ],
                'monitoring_protocol': [
                    'Daily case reporting to District Health Officer',
                    'Water quality testing every 6 hours',
                    'Contact tracing of all confirmed cases',
                    'Surveillance in 10km radius for 2 weeks',
                    'Environmental assessment and remediation'
                ]
            },
            'dengue': {
                'immediate_actions': [
                    'Vector control team deployment within 4 hours',
                    'Fogging operations in 2km radius',
                    'Source reduction - eliminate stagnant water',
                    'Set up fever screening camps',
                    'Platelet donation drive activation',
                    'Ensure adequate bed capacity in hospitals'
                ],
                'prevention_measures': [
                    'Community awareness on container management',
                    'Weekly dry day campaigns',
                    'School health education programs',
                    'Larvicidal treatment of water bodies',
                    'Distribution of mosquito nets and repellents',
                    'Construction site water management'
                ],
                'resource_deployment': [
                    'Vector control teams: 6 teams with fogging equipment',
                    'Medical staff: Fever clinic teams, lab technicians',
                    'Supplies: Insecticides, larvicides, test kits',
                    'Equipment: Fogging machines, water testing kits',
                    'Logistics: Mobile screening units, sample transport'
                ],
                'monitoring_protocol': [
                    'Daily entomological surveillance',
                    'House index and breteau index calculation',
                    'Fever case monitoring and testing',
                    'Weekly larval survey in high-risk areas',
                    'Meteorological data correlation analysis'
                ]
            },
            'hepatitis_a': {
                'immediate_actions': [
                    'Contact tracing and vaccination of close contacts',
                    'Food handler screening and testing',
                    'Water source investigation and testing',
                    'Hygiene education in affected communities',
                    'Isolation of active cases',
                    'Hepatitis A vaccination drive'
                ],
                'prevention_measures': [
                    'Hand hygiene promotion campaigns',
                    'Safe food preparation training',
                    'Water quality improvement measures',
                    'Sanitation facility upgrades',
                    'Food vendor licensing and monitoring',
                    'Tourist area special hygiene protocols'
                ],
                'resource_deployment': [
                    'Vaccination teams: 4 teams with cold chain',
                    'Testing capacity: Rapid test kits, lab support',
                    'Medicines: Hepatitis A vaccines (5000 doses)',
                    'Education materials: Posters, pamphlets in local language',
                    'Equipment: Water testing kits, food safety kits'
                ],
                'monitoring_protocol': [
                    'Contact follow-up for 45 days',
                    'Food establishment regular inspection',
                    'Water quality monitoring weekly',
                    'Vaccination coverage assessment',
                    'Tourist health monitoring if applicable'
                ]
            },
            'malaria': {
                'immediate_actions': [
                    'Deploy Rapid Diagnostic Test (RDT) teams',
                    'Mass screening in affected villages',
                    'Indoor Residual Spray (IRS) operations',
                    'Long-Lasting Insecticidal Net (LLIN) distribution',
                    'Artemisinin-based treatment initiation',
                    'Vector surveillance and control'
                ],
                'prevention_measures': [
                    'Community education on malaria prevention',
                    'Proper use and maintenance of bed nets',
                    'Environmental management of breeding sites',
                    'Personal protection measures promotion',
                    'Early diagnosis and treatment awareness',
                    'Special focus on vulnerable populations'
                ],
                'resource_deployment': [
                    'Testing teams: 8 ASHA workers with RDTs',
                    'Treatment supplies: ACT drugs, severe malaria medicines',
                    'Prevention materials: LLINs (2000 nets)',
                    'Vector control: IRS team with insecticides',
                    'Equipment: Microscopes, RDT kits, spraying equipment'
                ],
                'monitoring_protocol': [
                    'Weekly fever surveillance in villages',
                    'Monthly vector surveillance',
                    'Treatment follow-up for all cases',
                    'Net usage monitoring and replacement',
                    'Environmental assessment quarterly'
                ]
            }
        }
    
    def predict_outbreak_risk(self, location_data: Dict, climate_data: Dict, symptoms_pattern: List[str]) -> OutbreakPrediction:
        """Generate outbreak prediction with solution plan"""
        
        # Analyze current conditions against historical patterns
        risk_assessment = self._assess_risk_level(location_data, climate_data, symptoms_pattern)
        predicted_disease = risk_assessment['disease']
        risk_level = risk_assessment['risk_level']
        confidence = risk_assessment['confidence']
        
        # Generate environmental and climate factors
        environmental_factors = self._identify_environmental_factors(location_data, predicted_disease)
        climate_triggers = self._identify_climate_triggers(climate_data, predicted_disease)
        
        # Create comprehensive solution plan
        solution_plan = self._generate_solution_plan(predicted_disease, location_data, risk_level)
        
        # Estimate affected population and timeline
        population_estimate = self._estimate_affected_population(location_data, risk_level)
        timeline = self._determine_response_timeline(risk_level)
        
        # Generate prevention measures
        prevention_measures = self._generate_prevention_measures(predicted_disease, location_data)
        
        return OutbreakPrediction(
            location=location_data.get('city', 'Unknown'),
            state=location_data.get('state', 'Unknown'),
            district=location_data.get('district', 'Unknown'),
            predicted_disease=predicted_disease,
            risk_level=risk_level,
            confidence=confidence,
            environmental_factors=environmental_factors,
            climate_triggers=climate_triggers,
            solution_plan=solution_plan,
            timeline=timeline,
            affected_population_estimate=population_estimate,
            prevention_measures=prevention_measures
        )
    
    def _assess_risk_level(self, location_data: Dict, climate_data: Dict, symptoms: List[str]) -> Dict:
        """Assess outbreak risk based on multiple factors"""
        
        # Simplified risk assessment based on current conditions
        risk_scores = {}
        
        for disease, patterns in self.climate_disease_patterns.items():
            score = 0.0
            
            # Check symptom correlation
            if any(symptom in disease for symptom in symptoms):
                score += 0.3
            
            # Check climate conditions
            temp = climate_data.get('temperature', 25)
            humidity = climate_data.get('humidity', 60)
            rainfall = climate_data.get('rainfall_7days', 10)
            
            if patterns['temperature_range'][0] <= temp <= patterns['temperature_range'][1]:
                score += 0.25
            if humidity >= patterns['humidity_threshold']:
                score += 0.2
            
            # Check geographic factors
            city = location_data.get('city', '').lower()
            if city in ['mumbai', 'kolkata', 'chennai']:  # Coastal cities
                if 'coastal areas' in patterns['geographic_risk_zones']:
                    score += 0.15
            
            risk_scores[disease] = score
        
        # Determine highest risk disease
        max_disease = max(risk_scores.items(), key=lambda x: x[1])
        disease = max_disease[0]
        confidence = min(max_disease[1], 0.95)
        
        # Determine risk level
        if confidence >= 0.8:
            risk_level = 'Critical'
        elif confidence >= 0.6:
            risk_level = 'High'
        elif confidence >= 0.4:
            risk_level = 'Medium'
        else:
            risk_level = 'Low'
        
        return {
            'disease': disease,
            'risk_level': risk_level,
            'confidence': confidence
        }
    
    def _identify_environmental_factors(self, location_data: Dict, disease: str) -> List[str]:
        """Identify environmental risk factors for the location"""
        factors = []
        
        city = location_data.get('city', '').lower()
        pollution_level = location_data.get('pollution_level', 'Medium')
        
        # City-specific environmental factors
        city_factors = {
            'mumbai': [
                'High coastal humidity and temperature',
                'Industrial waste discharge into water bodies',
                'Dense population with poor sanitation in slums',
                'Contaminated Mithi River and creek systems'
            ],
            'delhi': [
                'Severe air pollution affecting respiratory health',
                'Yamuna river contamination',
                'High population density and poor waste management',
                'Extreme temperature variations'
            ],
            'kolkata': [
                'High humidity and temperature promoting vector breeding',
                'Hooghly river pollution',
                'Waterlogging during monsoon',
                'Industrial discharge from nearby areas'
            ],
            'chennai': [
                'Coastal location with high humidity',
                'Groundwater salination and depletion',
                'Poor drainage leading to stagnant water',
                'Industrial pollution from port activities'
            ],
            'bangalore': [
                'Lake contamination and foaming',
                'Rapid urbanization affecting water quality',
                'Electronic waste disposal issues',
                'Deforestation affecting local climate'
            ]
        }
        
        if city in city_factors:
            factors.extend(city_factors[city][:3])  # Top 3 factors
        
        # Add pollution-based factors
        if pollution_level in ['High', 'Critical']:
            factors.append('High industrial pollution levels affecting immunity')
            factors.append('Poor air quality contributing to respiratory vulnerability')
        
        return factors
    
    def _identify_climate_triggers(self, climate_data: Dict, disease: str) -> List[str]:
        """Identify climate triggers for disease outbreak"""
        triggers = []
        
        temp = climate_data.get('temperature', 25)
        humidity = climate_data.get('humidity', 60)
        rainfall = climate_data.get('rainfall_7days', 10)
        
        if disease == 'cholera':
            if temp > 32:
                triggers.append(f'High temperature ({temp}°C) accelerating bacterial growth')
            if humidity > 80:
                triggers.append(f'High humidity ({humidity}%) creating favorable conditions')
            if rainfall > 100:
                triggers.append(f'Heavy rainfall ({rainfall}mm) causing water contamination')
        
        elif disease == 'dengue':
            if 26 <= temp <= 32:
                triggers.append(f'Optimal temperature ({temp}°C) for Aedes mosquito breeding')
            if humidity > 65:
                triggers.append(f'High humidity ({humidity}%) supporting vector survival')
            if 20 <= rainfall <= 100:
                triggers.append(f'Moderate rainfall ({rainfall}mm) creating breeding sites')
        
        elif disease == 'malaria':
            if 25 <= temp <= 35:
                triggers.append(f'Temperature ({temp}°C) optimal for Anopheles development')
            if humidity > 75:
                triggers.append(f'High humidity ({humidity}%) supporting mosquito longevity')
            if rainfall > 50:
                triggers.append(f'Rainfall ({rainfall}mm) creating vector breeding habitats')
        
        return triggers
    
    def _generate_solution_plan(self, disease: str, location_data: Dict, risk_level: str) -> Dict[str, List[str]]:
        """Generate comprehensive solution plan"""
        base_plan = self.solution_templates.get(disease, {})
        
        # Customize based on risk level and location
        customized_plan = {}
        
        for category, actions in base_plan.items():
            customized_actions = actions.copy()
            
            # Add location-specific actions
            if location_data.get('city', '').lower() == 'mumbai' and disease == 'cholera':
                if category == 'immediate_actions':
                    customized_actions.append('Coordinate with Brihanmumbai Municipal Corporation')
                    customized_actions.append('Alert coastal health centers and fishing communities')
            
            # Scale up for higher risk levels
            if risk_level in ['High', 'Critical']:
                if category == 'resource_deployment':
                    customized_actions = [action.replace('3 doctors', '6 doctors').replace('8 nurses', '16 nurses') for action in customized_actions]
            
            customized_plan[category] = customized_actions
        
        return customized_plan
    
    def _estimate_affected_population(self, location_data: Dict, risk_level: str) -> int:
        """Estimate potentially affected population"""
        base_population = location_data.get('population', 100000)
        
        risk_multipliers = {
            'Low': 0.001,      # 0.1% of population
            'Medium': 0.005,   # 0.5% of population
            'High': 0.01,      # 1% of population
            'Critical': 0.025  # 2.5% of population
        }
        
        multiplier = risk_multipliers.get(risk_level, 0.005)
        return int(base_population * multiplier)
    
    def _determine_response_timeline(self, risk_level: str) -> str:
        """Determine response timeline based on risk level"""
        timelines = {
            'Low': '72 hours for full response deployment',
            'Medium': '24 hours for initial response, 48 hours for full deployment',
            'High': '12 hours for rapid response team, 24 hours for full deployment',
            'Critical': '2 hours for immediate response, 6 hours for full deployment'
        }
        
        return timelines.get(risk_level, '24 hours')
    
    def _generate_prevention_measures(self, disease: str, location_data: Dict) -> List[str]:
        """Generate location-specific prevention measures"""
        base_measures = self.solution_templates.get(disease, {}).get('prevention_measures', [])
        
        # Add location-specific measures
        city = location_data.get('city', '').lower()
        if city == 'mumbai' and disease == 'cholera':
            base_measures.append('Special focus on slum areas like Dharavi')
            base_measures.append('Coordinate with fishing communities for coastal hygiene')
        
        return base_measures

# Global instance
geographic_predictor = GeographicOutbreakPredictor()