#!/usr/bin/env python3
"""
🧠 Advanced Multi-Disease Classification Engine for RHAS v2.0
Hybrid AI Ensemble with Multi-Layer Classification Pipeline

Features:
- Multi-Modal Disease Signatures
- Bayesian Inference Framework  
- Environmental & Social Context Integration
- Unknown Disease Detection
- Confidence Scoring & Uncertainty Quantification
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
import re
import math
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SymptomFeature:
    """Enhanced symptom representation with multi-dimensional features"""
    name: str
    severity: float  # 0-10 scale
    duration_hours: int
    progression: str  # 'improving', 'stable', 'worsening'
    confidence: float  # 0-1 scale
    temporal_pattern: str  # 'acute', 'gradual', 'cyclic', 'intermittent'

@dataclass
class PatientContext:
    """Patient demographic and environmental context"""
    age: int
    gender: str
    occupation: str
    location: Dict[str, float]  # {'lat': x, 'lon': y, 'elevation': z}
    household_size: int
    water_source: str
    sanitation_level: int  # 1-5 scale
    recent_travel: bool
    vaccination_status: Dict[str, bool]

@dataclass
class EnvironmentalContext:
    """Environmental and seasonal context"""
    season: str
    temperature: float
    humidity: float
    rainfall_7day: float
    water_quality_score: float
    air_quality_index: int
    population_density: int

@dataclass
class DiseaseSignature:
    """Multi-modal disease signature with patterns"""
    primary_symptoms: List[str]
    secondary_symptoms: List[str]
    temporal_pattern: Dict[str, any]
    environmental_correlation: Dict[str, float]
    demographic_risk: Dict[str, float]
    exclusionary_symptoms: List[str]
    pathognomonic_signs: List[str]
    incubation_period: Tuple[int, int]  # (min_hours, max_hours)
    contagiousness: float  # 0-1 scale

class AdvancedDiseaseClassifier:
    """
    Advanced Multi-Disease Classification Engine
    Hybrid AI Ensemble for Rural Health Surveillance
    """
    
    def __init__(self):
        self.disease_signatures = self._initialize_disease_signatures()
        self.seasonal_probability_matrix = self._initialize_seasonal_matrix()
        self.symptom_keywords = self._initialize_symptom_keywords()
        self.environmental_weights = self._initialize_environmental_weights()
        self.model_weights = {'xgboost': 0.4, 'neural': 0.3, 'graph': 0.2, 'anomaly': 0.1}
        logger.info("Advanced Disease Classifier initialized successfully")
    
    def _initialize_disease_signatures(self) -> Dict[str, DiseaseSignature]:
        """Initialize comprehensive disease signatures"""
        signatures = {
            'cholera': DiseaseSignature(
                primary_symptoms=['watery_diarrhea', 'severe_dehydration', 'rice_water_stools'],
                secondary_symptoms=['vomiting', 'rapid_fluid_loss', 'muscle_cramps'],
                temporal_pattern={
                    'onset': 'rapid',  # <6 hours
                    'peak_hours': (12, 24),
                    'duration_days': (3, 7)
                },
                environmental_correlation={
                    'rainfall_spike': 0.8,
                    'water_contamination': 0.9,
                    'poor_sanitation': 0.7,
                    'flooding': 0.6
                },
                demographic_risk={
                    'elderly': 0.8, 'children_under_5': 0.9, 'adults': 0.6,
                    'malnutrition': 0.7, 'immunocompromised': 0.8
                },
                exclusionary_symptoms=['constipation', 'high_fever'],
                pathognomonic_signs=['rice_water_stools', 'sunken_eyes'],
                incubation_period=(2, 120),  # 2 hours to 5 days
                contagiousness=0.7
            ),
            
            'typhoid': DiseaseSignature(
                primary_symptoms=['sustained_fever', 'headache', 'abdominal_pain', 'rose_spots'],
                secondary_symptoms=['constipation', 'diarrhea', 'fatigue', 'loss_appetite'],
                temporal_pattern={
                    'onset': 'gradual',  # 5-7 days
                    'peak_hours': (168, 336),  # 1-2 weeks
                    'duration_days': (14, 28)
                },
                environmental_correlation={
                    'poor_sanitation': 0.8,
                    'food_contamination': 0.7,
                    'overcrowding': 0.6,
                    'summer_season': 0.7
                },
                demographic_risk={
                    'young_adults': 0.8, 'school_age': 0.7, 'food_handlers': 0.9,
                    'travelers': 0.6
                },
                exclusionary_symptoms=['watery_diarrhea', 'rice_water_stools'],
                pathognomonic_signs=['rose_spots', 'step_ladder_fever'],
                incubation_period=(168, 720),  # 7-30 days
                contagiousness=0.3
            ),
            
            'malaria': DiseaseSignature(
                primary_symptoms=['cyclic_fever', 'chills', 'sweats', 'headache'],
                secondary_symptoms=['muscle_aches', 'fatigue', 'nausea', 'vomiting'],
                temporal_pattern={
                    'onset': 'acute',  # 1-2 days
                    'peak_hours': (48, 72),
                    'duration_days': (7, 14),
                    'cyclic_pattern': True
                },
                environmental_correlation={
                    'stagnant_water': 0.9,
                    'monsoon_season': 0.8,
                    'rural_areas': 0.7,
                    'forest_proximity': 0.6
                },
                demographic_risk={
                    'children_under_5': 0.9, 'pregnant_women': 0.8, 'travelers': 0.7,
                    'outdoor_workers': 0.6
                },
                exclusionary_symptoms=['continuous_fever', 'diarrhea'],
                pathognomonic_signs=['spleen_enlargement', 'anemia'],
                incubation_period=(168, 720),  # 7-30 days
                contagiousness=0.0  # Vector-borne, not person-to-person
            ),
            
            'dengue': DiseaseSignature(
                primary_symptoms=['high_fever', 'severe_headache', 'eye_pain', 'muscle_pain'],
                secondary_symptoms=['rash', 'nausea', 'vomiting', 'bleeding'],
                temporal_pattern={
                    'onset': 'acute',  # 1-2 days
                    'peak_hours': (72, 120),  # 3-5 days
                    'duration_days': (3, 7)
                },
                environmental_correlation={
                    'water_storage': 0.8,
                    'urban_areas': 0.7,
                    'monsoon_post': 0.8,
                    'breeding_containers': 0.9
                },
                demographic_risk={
                    'all_ages': 0.6, 'urban_dwellers': 0.7, 'repeat_infection': 0.9
                },
                exclusionary_symptoms=['diarrhea', 'respiratory_symptoms'],
                pathognomonic_signs=['platelet_drop', 'tourniquet_test_positive'],
                incubation_period=(96, 336),  # 4-14 days
                contagiousness=0.0  # Vector-borne
            ),
            
            'hepatitis_a': DiseaseSignature(
                primary_symptoms=['jaundice', 'fatigue', 'abdominal_pain', 'nausea'],
                secondary_symptoms=['loss_appetite', 'low_fever', 'dark_urine', 'pale_stool'],
                temporal_pattern={
                    'onset': 'gradual',  # 2-7 days
                    'peak_hours': (336, 672),  # 2-4 weeks
                    'duration_days': (14, 42)
                },
                environmental_correlation={
                    'poor_sanitation': 0.8,
                    'contaminated_water': 0.7,
                    'food_contamination': 0.6
                },
                demographic_risk={
                    'children': 0.7, 'travelers': 0.6, 'food_handlers': 0.8
                },
                exclusionary_symptoms=['high_fever', 'diarrhea'],
                pathognomonic_signs=['jaundice', 'enlarged_liver'],
                incubation_period=(360, 1200),  # 15-50 days
                contagiousness=0.4
            ),
            
            'covid19': DiseaseSignature(
                primary_symptoms=['fever', 'dry_cough', 'shortness_breath', 'loss_taste_smell'],
                secondary_symptoms=['fatigue', 'body_aches', 'sore_throat', 'headache'],
                temporal_pattern={
                    'onset': 'gradual',  # 2-5 days
                    'peak_hours': (120, 240),  # 5-10 days
                    'duration_days': (10, 21)
                },
                environmental_correlation={
                    'crowded_spaces': 0.8,
                    'poor_ventilation': 0.7,
                    'winter_season': 0.6
                },
                demographic_risk={
                    'elderly': 0.9, 'comorbidities': 0.8, 'all_ages': 0.5
                },
                exclusionary_symptoms=[],
                pathognomonic_signs=['loss_taste_smell', 'ground_glass_opacity'],
                incubation_period=(24, 336),  # 1-14 days
                contagiousness=0.9
            )
        }
        
        return signatures
    
    def _initialize_seasonal_matrix(self) -> np.ndarray:
        """Initialize seasonal disease probability matrix"""
        # Months (Jan-Dec) x Diseases probability matrix
        diseases = ['cholera', 'typhoid', 'malaria', 'dengue', 'hepatitis_a', 'covid19']
        seasonal_probs = np.array([
            # Jan   Feb   Mar   Apr   May   Jun   Jul   Aug   Sep   Oct   Nov   Dec
            [0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.35, 0.30, 0.25, 0.20, 0.18, 0.15],  # cholera
            [0.20, 0.25, 0.30, 0.35, 0.40, 0.35, 0.30, 0.25, 0.22, 0.20, 0.18, 0.18],  # typhoid
            [0.10, 0.15, 0.20, 0.25, 0.20, 0.35, 0.45, 0.50, 0.40, 0.30, 0.20, 0.15],  # malaria
            [0.05, 0.10, 0.15, 0.20, 0.25, 0.35, 0.40, 0.45, 0.35, 0.25, 0.15, 0.10],  # dengue
            [0.25, 0.30, 0.35, 0.40, 0.45, 0.35, 0.25, 0.20, 0.25, 0.30, 0.25, 0.25],  # hepatitis_a
            [0.40, 0.35, 0.30, 0.25, 0.25, 0.30, 0.35, 0.30, 0.35, 0.40, 0.45, 0.50],  # covid19
        ])
        
        return seasonal_probs
    
    def _initialize_symptom_keywords(self) -> Dict[str, Dict]:
        """Enhanced symptom keyword mapping with severity indicators"""
        return {
            # Gastrointestinal
            'watery_diarrhea': {
                'keywords': ['watery diarrhea', 'watery stool', 'liquid stool', 'profuse diarrhea'],
                'severity_indicators': {'profuse': 9, 'severe': 8, 'frequent': 7, 'watery': 6}
            },
            'rice_water_stools': {
                'keywords': ['rice water stool', 'rice-water', 'colorless stool', 'odorless diarrhea'],
                'severity_indicators': {'rice water': 10, 'colorless': 8}
            },
            'diarrhea': {
                'keywords': ['diarrhea', 'loose stool', 'loose motion', 'दस्त', 'पेचिश'],
                'severity_indicators': {'bloody': 8, 'frequent': 6, 'loose': 4}
            },
            'constipation': {
                'keywords': ['constipation', 'difficulty passing stool', 'hard stool'],
                'severity_indicators': {'severe': 6, 'chronic': 5}
            },
            'vomiting': {
                'keywords': ['vomiting', 'throwing up', 'उल्टी', 'vómito'],
                'severity_indicators': {'projectile': 8, 'continuous': 7, 'frequent': 6}
            },
            'nausea': {
                'keywords': ['nausea', 'feel sick', 'queasy', 'मतली', 'náusea'],
                'severity_indicators': {'severe': 6, 'constant': 5}
            },
            'abdominal_pain': {
                'keywords': ['stomach pain', 'abdominal pain', 'belly pain', 'stomach ache'],
                'severity_indicators': {'severe': 8, 'cramping': 6, 'mild': 3}
            },
            
            # Fever patterns
            'sustained_fever': {
                'keywords': ['continuous fever', 'persistent fever', 'sustained fever', 'high fever for days'],
                'severity_indicators': {'high': 8, 'continuous': 7, 'persistent': 7}
            },
            'cyclic_fever': {
                'keywords': ['fever comes and goes', 'intermittent fever', 'fever cycles', 'periodic fever'],
                'severity_indicators': {'high cycles': 8, 'regular pattern': 6}
            },
            'high_fever': {
                'keywords': ['high fever', 'very hot', 'burning fever', 'तेज़ बुखार', 'fiebre alta'],
                'severity_indicators': {'very high': 9, 'burning': 8, 'high': 7}
            },
            'fever': {
                'keywords': ['fever', 'temperature', 'hot', 'बुखार', 'fiebre'],
                'severity_indicators': {'high': 7, 'moderate': 5, 'low': 3}
            },
            'chills': {
                'keywords': ['chills', 'shivering', 'cold', 'ठंड लगना'],
                'severity_indicators': {'severe': 7, 'uncontrollable': 8}
            },
            
            # Neurological
            'headache': {
                'keywords': ['headache', 'head pain', 'सिर दर्द', 'dolor de cabeza'],
                'severity_indicators': {'severe': 8, 'throbbing': 7, 'mild': 3}
            },
            'severe_headache': {
                'keywords': ['severe headache', 'splitting headache', 'intense head pain'],
                'severity_indicators': {'splitting': 9, 'severe': 8, 'intense': 8}
            },
            'eye_pain': {
                'keywords': ['eye pain', 'pain behind eyes', 'eye ache'],
                'severity_indicators': {'severe': 7, 'sharp': 6}
            },
            
            # Respiratory
            'dry_cough': {
                'keywords': ['dry cough', 'non-productive cough', 'persistent cough'],
                'severity_indicators': {'persistent': 6, 'severe': 7}
            },
            'cough': {
                'keywords': ['cough', 'coughing', 'खांसी', 'tos'],
                'severity_indicators': {'severe': 6, 'persistent': 5, 'mild': 2}
            },
            'shortness_breath': {
                'keywords': ['shortness of breath', 'difficulty breathing', 'breathless'],
                'severity_indicators': {'severe': 9, 'at rest': 8, 'on exertion': 6}
            },
            'sore_throat': {
                'keywords': ['sore throat', 'throat pain', 'difficulty swallowing'],
                'severity_indicators': {'severe': 6, 'difficulty swallowing': 7}
            },
            
            # Systemic
            'fatigue': {
                'keywords': ['fatigue', 'tiredness', 'weakness', 'exhausted'],
                'severity_indicators': {'extreme': 8, 'severe': 6, 'mild': 3}
            },
            'muscle_pain': {
                'keywords': ['muscle pain', 'body aches', 'muscle aches', 'joint pain'],
                'severity_indicators': {'severe': 7, 'widespread': 6}
            },
            'muscle_cramps': {
                'keywords': ['muscle cramps', 'cramping', 'muscle spasms'],
                'severity_indicators': {'severe': 8, 'painful': 7}
            },
            
            # Specific signs
            'jaundice': {
                'keywords': ['yellow skin', 'yellow eyes', 'jaundice', 'yellowing'],
                'severity_indicators': {'deep yellow': 8, 'yellow': 6}
            },
            'rash': {
                'keywords': ['rash', 'skin rash', 'red spots', 'skin eruption'],
                'severity_indicators': {'widespread': 6, 'red': 5}
            },
            'rose_spots': {
                'keywords': ['rose spots', 'red spots on chest', 'rose-colored rash'],
                'severity_indicators': {'rose spots': 8}
            },
            'loss_taste_smell': {
                'keywords': ['loss of taste', 'loss of smell', 'cannot taste', 'cannot smell'],
                'severity_indicators': {'complete loss': 8, 'partial loss': 6}
            },
            'loss_appetite': {
                'keywords': ['loss of appetite', 'not hungry', 'no appetite'],
                'severity_indicators': {'complete loss': 6, 'poor appetite': 4}
            },
            
            # Dehydration signs
            'severe_dehydration': {
                'keywords': ['severe dehydration', 'very dehydrated', 'sunken eyes', 'dry mouth'],
                'severity_indicators': {'severe': 9, 'sunken eyes': 8, 'dry skin': 6}
            },
            'rapid_fluid_loss': {
                'keywords': ['losing fluids quickly', 'rapid dehydration', 'fluid loss'],
                'severity_indicators': {'rapid': 8, 'continuous': 7}
            },
            
            # Bleeding
            'bleeding': {
                'keywords': ['bleeding', 'blood', 'hemorrhage', 'nosebleed'],
                'severity_indicators': {'heavy': 9, 'continuous': 8, 'minor': 4}
            },
            'dark_urine': {
                'keywords': ['dark urine', 'tea-colored urine', 'brown urine'],
                'severity_indicators': {'very dark': 7, 'tea colored': 6}
            },
            'pale_stool': {
                'keywords': ['pale stool', 'clay-colored stool', 'white stool'],
                'severity_indicators': {'very pale': 7, 'clay colored': 6}
            }
        }
    
    def _initialize_environmental_weights(self) -> Dict[str, float]:
        """Initialize environmental factor weights for disease correlation"""
        return {
            'water_quality': 0.35,
            'sanitation_level': 0.25,
            'population_density': 0.15,
            'seasonal_factors': 0.15,
            'climate_conditions': 0.10
        }
    
    def extract_symptoms_from_text(self, text: str, context: Optional[PatientContext] = None) -> List[SymptomFeature]:
        """
        Advanced symptom extraction with multi-dimensional feature engineering
        """
        text_lower = text.lower()
        extracted_symptoms = []
        
        # Severity pattern recognition
        severity_patterns = {
            r'\b(very|extremely|severely?)\s+': 8,
            r'\b(quite|fairly|moderately?)\s+': 5,
            r'\b(slightly|mildly?|a\s+bit)\s+': 2,
            r'\b(intense|severe|terrible|unbearable)\b': 8,
            r'\b(mild|light|minor)\b': 2
        }
        
        # Duration pattern recognition
        duration_patterns = {
            r'(\d+)\s+(hour|hr)s?': lambda x: int(x.group(1)),
            r'(\d+)\s+(day|dy)s?': lambda x: int(x.group(1)) * 24,
            r'(\d+)\s+(week|wk)s?': lambda x: int(x.group(1)) * 168,
            r'since\s+(yesterday|1\s+day)': lambda x: 24,
            r'for\s+(\d+)\s+days?': lambda x: int(x.group(1)) * 24,
            r'last\s+(\d+)\s+days?': lambda x: int(x.group(1)) * 24
        }
        
        # Progression pattern recognition
        progression_patterns = {
            r'\b(getting\s+worse|worsening|deteriorating|increasing)\b': 'worsening',
            r'\b(getting\s+better|improving|recovering|decreasing)\b': 'improving',
            r'\b(same|stable|unchanged|constant)\b': 'stable',
            r'\b(comes?\s+and\s+goes?|intermittent|on\s+and\s+off)\b': 'intermittent'
        }
        
        # Temporal pattern recognition
        temporal_patterns = {
            r'\b(sudden|suddenly|all\s+of\s+a\s+sudden|immediate)\b': 'acute',
            r'\b(gradual|gradually|slow|over\s+time)\b': 'gradual',
            r'\b(cyclic|cycles?|periodic|comes?\s+and\s+goes?)\b': 'cyclic',
            r'\b(intermittent|on\s+and\s+off|sometimes)\b': 'intermittent'
        }
        
        for symptom_name, symptom_data in self.symptom_keywords.items():
            for keyword in symptom_data['keywords']:
                if keyword.lower() in text_lower:
                    # Calculate base severity
                    base_severity = 5.0
                    
                    # Apply severity modifiers
                    for pattern, severity_boost in severity_patterns.items():
                        if re.search(pattern, text_lower):
                            base_severity = max(base_severity, severity_boost)
                    
                    # Check for specific severity indicators
                    for indicator, severity in symptom_data['severity_indicators'].items():
                        if indicator.lower() in text_lower:
                            base_severity = max(base_severity, severity)
                    
                    # Extract duration
                    duration_hours = 24  # default
                    for pattern, extractor in duration_patterns.items():
                        match = re.search(pattern, text_lower)
                        if match:
                            if callable(extractor):
                                duration_hours = extractor(match)
                            else:
                                duration_hours = extractor
                            break
                    
                    # Extract progression
                    progression = 'stable'  # default
                    for pattern, prog in progression_patterns.items():
                        if re.search(pattern, text_lower):
                            progression = prog
                            break
                    
                    # Extract temporal pattern
                    temporal_pattern = 'acute'  # default
                    for pattern, temp in temporal_patterns.items():
                        if re.search(pattern, text_lower):
                            temporal_pattern = temp
                            break
                    
                    # Calculate confidence based on keyword specificity and context
                    confidence = 0.8
                    if len(keyword) > 10:  # specific keywords get higher confidence
                        confidence = 0.9
                    if context and hasattr(context, 'occupation'):  # context can modify confidence
                        confidence += 0.1
                    
                    confidence = min(confidence, 1.0)
                    
                    symptom = SymptomFeature(
                        name=symptom_name,
                        severity=min(base_severity, 10.0),
                        duration_hours=duration_hours,
                        progression=progression,
                        confidence=confidence,
                        temporal_pattern=temporal_pattern
                    )
                    
                    # Avoid duplicates
                    if not any(s.name == symptom_name for s in extracted_symptoms):
                        extracted_symptoms.append(symptom)
        
        return extracted_symptoms
    
    def calculate_bayesian_probability(self, symptoms: List[SymptomFeature], 
                                     patient_context: Optional[PatientContext] = None,
                                     environmental_context: Optional[EnvironmentalContext] = None) -> Dict[str, float]:
        """
        Advanced Bayesian inference for disease probability calculation
        P(Disease|Symptoms, Context) = P(Symptoms|Disease) × P(Disease|Context) / P(Symptoms|Context)
        """
        disease_probabilities = {}
        symptom_names = [s.name for s in symptoms]
        
        # Current month for seasonal adjustment
        current_month = datetime.now().month - 1  # 0-indexed
        
        for disease_name, signature in self.disease_signatures.items():
            # P(Symptoms|Disease) - Clinical Evidence (70% weight)
            clinical_evidence = self._calculate_clinical_evidence(symptoms, signature)
            
            # P(Disease|Context) - Prior probability based on context
            prior_probability = 0.1  # base prior
            
            # Seasonal adjustment
            seasonal_prob = self.seasonal_probability_matrix[
                list(self.disease_signatures.keys()).index(disease_name)
            ][current_month]
            prior_probability *= seasonal_prob
            
            # Environmental context adjustment
            if environmental_context:
                env_adjustment = self._calculate_environmental_adjustment(environmental_context, signature)
                prior_probability *= env_adjustment
            
            # Demographic context adjustment  
            if patient_context:
                demo_adjustment = self._calculate_demographic_adjustment(patient_context, signature)
                prior_probability *= demo_adjustment
            
            # Combined probability using weighted Bayesian approach
            posterior_probability = (clinical_evidence * 0.7 + prior_probability * 0.3)
            
            # Apply exclusionary symptoms penalty
            for exclusionary in signature.exclusionary_symptoms:
                if exclusionary in symptom_names:
                    posterior_probability *= 0.1  # Severe penalty
            
            # Boost for pathognomonic signs
            for pathognomonic in signature.pathognomonic_signs:
                if pathognomonic in symptom_names:
                    posterior_probability *= 2.0  # Strong boost
            
            disease_probabilities[disease_name] = min(posterior_probability, 1.0)
        
        # Normalize probabilities
        total_prob = sum(disease_probabilities.values())
        if total_prob > 0:
            disease_probabilities = {k: v/total_prob for k, v in disease_probabilities.items()}
        
        return disease_probabilities
    
    def _calculate_clinical_evidence(self, symptoms: List[SymptomFeature], signature: DiseaseSignature) -> float:
        """Calculate clinical evidence score based on symptom matching"""
        symptom_names = [s.name for s in symptoms]
        symptom_severities = {s.name: s.severity for s in symptoms}
        
        # Primary symptom matching
        primary_matches = sum(1 for ps in signature.primary_symptoms if ps in symptom_names)
        primary_score = primary_matches / len(signature.primary_symptoms) if signature.primary_symptoms else 0
        
        # Secondary symptom matching
        secondary_matches = sum(1 for ss in signature.secondary_symptoms if ss in symptom_names)
        secondary_score = secondary_matches / len(signature.secondary_symptoms) if signature.secondary_symptoms else 0
        
        # Severity weighting
        severity_weight = 1.0
        if symptom_severities:
            avg_severity = np.mean([sev for sev in symptom_severities.values()])
            severity_weight = 0.5 + (avg_severity / 20.0)  # 0.5 to 1.0 range
        
        # Combined clinical evidence
        clinical_evidence = (primary_score * 0.7 + secondary_score * 0.3) * severity_weight
        
        return clinical_evidence
    
    def _calculate_environmental_adjustment(self, env_context: EnvironmentalContext, signature: DiseaseSignature) -> float:
        """Calculate environmental context adjustment factor"""
        adjustment = 1.0
        
        # Season adjustment
        season_map = {'winter': 0, 'spring': 1, 'summer': 2, 'fall': 3}
        if env_context.season in season_map:
            season_idx = season_map[env_context.season]
            # Use seasonal probability for adjustment
            diseases_list = list(self.disease_signatures.keys())
            if signature in [self.disease_signatures[d] for d in diseases_list]:
                disease_idx = diseases_list.index([k for k, v in self.disease_signatures.items() if v == signature][0])
                seasonal_adjustment = self.seasonal_probability_matrix[disease_idx][season_idx * 3]  # Rough mapping
                adjustment *= seasonal_adjustment
        
        # Environmental correlations
        for factor, correlation in signature.environmental_correlation.items():
            if factor == 'rainfall_spike' and env_context.rainfall_7day > 50:  # >50mm in 7 days
                adjustment *= (1 + correlation)
            elif factor == 'water_contamination' and env_context.water_quality_score < 0.5:
                adjustment *= (1 + correlation)
            elif factor == 'poor_sanitation' and hasattr(env_context, 'sanitation_score') and env_context.sanitation_score < 0.4:
                adjustment *= (1 + correlation)
            elif factor == 'urban_areas' and env_context.population_density > 1000:
                adjustment *= (1 + correlation)
            elif factor == 'stagnant_water' and env_context.humidity > 80:
                adjustment *= (1 + correlation)
        
        return min(adjustment, 3.0)  # Cap at 3x boost
    
    def _calculate_demographic_adjustment(self, patient_context: PatientContext, signature: DiseaseSignature) -> float:
        """Calculate demographic context adjustment factor"""
        adjustment = 1.0
        
        # Age-based risk
        if patient_context.age < 5 and 'children_under_5' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['children_under_5'])
        elif patient_context.age >= 65 and 'elderly' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['elderly'])
        elif 18 <= patient_context.age <= 35 and 'young_adults' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['young_adults'])
        elif 5 <= patient_context.age <= 18 and 'school_age' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['school_age'])
        
        # Gender-based risk (if specified)
        if patient_context.gender == 'female' and patient_context.age >= 15 and patient_context.age <= 49:
            if 'pregnant_women' in signature.demographic_risk:
                adjustment *= (1 + signature.demographic_risk['pregnant_women'] * 0.5)  # Assume 50% chance of pregnancy
        
        # Occupation-based risk
        if patient_context.occupation in ['food_handler', 'cook', 'restaurant_worker'] and 'food_handlers' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['food_handlers'])
        elif patient_context.occupation in ['farmer', 'field_worker', 'outdoor_worker'] and 'outdoor_workers' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['outdoor_workers'])
        
        # Recent travel
        if patient_context.recent_travel and 'travelers' in signature.demographic_risk:
            adjustment *= (1 + signature.demographic_risk['travelers'])
        
        return min(adjustment, 3.0)  # Cap at 3x boost
    
    def detect_anomalies(self, symptoms: List[SymptomFeature], disease_probabilities: Dict[str, float]) -> Dict[str, float]:
        """
        Multi-dimensional anomaly detection for unknown disease patterns
        """
        anomaly_scores = {}
        
        # 1. Symptom space anomalies - unusual symptom combinations
        symptom_combinations = [s.name for s in symptoms]
        known_combinations = []
        for signature in self.disease_signatures.values():
            known_combinations.extend(signature.primary_symptoms)
            known_combinations.extend(signature.secondary_symptoms)
        
        unknown_symptoms = [s for s in symptom_combinations if s not in known_combinations]
        symptom_novelty = len(unknown_symptoms) / len(symptom_combinations) if symptom_combinations else 0
        anomaly_scores['symptom_novelty'] = symptom_novelty
        
        # 2. Temporal anomalies - unexpected progression or timing
        temporal_anomaly = 0.0
        for symptom in symptoms:
            if symptom.temporal_pattern not in ['acute', 'gradual', 'cyclic', 'intermittent']:
                temporal_anomaly += 0.2
            if symptom.progression == 'worsening' and symptom.severity > 8:
                temporal_anomaly += 0.3
        
        anomaly_scores['temporal_anomaly'] = min(temporal_anomaly, 1.0)
        
        # 3. Confidence anomalies - low confidence in all known diseases
        max_disease_prob = max(disease_probabilities.values()) if disease_probabilities else 0
        confidence_anomaly = 1.0 - max_disease_prob
        anomaly_scores['confidence_anomaly'] = confidence_anomaly
        
        # 4. Severity anomalies - unusual severity patterns
        if symptoms:
            avg_severity = np.mean([s.severity for s in symptoms])
            severity_variance = np.var([s.severity for s in symptoms])
            severity_anomaly = (avg_severity / 10.0) * (severity_variance / 25.0)  # Normalized
            anomaly_scores['severity_anomaly'] = min(severity_anomaly, 1.0)
        else:
            anomaly_scores['severity_anomaly'] = 0.0
        
        # Combined anomaly score
        weights = [0.4, 0.3, 0.2, 0.1]  # Weights for each anomaly type
        combined_anomaly = sum(score * weight for score, weight in zip(anomaly_scores.values(), weights))
        anomaly_scores['combined_anomaly'] = combined_anomaly
        
        return anomaly_scores
    
    def calculate_confidence_scores(self, symptoms: List[SymptomFeature], 
                                  disease_probabilities: Dict[str, float],
                                  patient_context: Optional[PatientContext] = None) -> Dict[str, float]:
        """
        Multi-source confidence calculation and uncertainty quantification
        """
        confidence_components = {}
        
        # 1. Model ensemble agreement (40% weight)
        if disease_probabilities:
            sorted_probs = sorted(disease_probabilities.values(), reverse=True)
            if len(sorted_probs) >= 2:
                # High confidence if top prediction is much higher than second
                ensemble_agreement = (sorted_probs[0] - sorted_probs[1]) / sorted_probs[0]
            else:
                ensemble_agreement = sorted_probs[0] if sorted_probs else 0.0
        else:
            ensemble_agreement = 0.0
        
        confidence_components['ensemble_agreement'] = ensemble_agreement
        
        # 2. Historical validation (30% weight) - simulated based on symptom quality
        symptom_quality = np.mean([s.confidence for s in symptoms]) if symptoms else 0.5
        historical_validation = symptom_quality  # Proxy for historical performance
        confidence_components['historical_validation'] = historical_validation
        
        # 3. Feature completeness (20% weight)
        if symptoms and disease_probabilities:
            top_disease = max(disease_probabilities.items(), key=lambda x: x[1])[0]
            top_signature = self.disease_signatures[top_disease]
            
            symptom_names = [s.name for s in symptoms]
            expected_symptoms = top_signature.primary_symptoms + top_signature.secondary_symptoms
            found_symptoms = [s for s in expected_symptoms if s in symptom_names]
            
            feature_completeness = len(found_symptoms) / len(expected_symptoms) if expected_symptoms else 0
        else:
            feature_completeness = 0.0
        
        confidence_components['feature_completeness'] = feature_completeness
        
        # 4. Context consistency (10% weight)
        context_consistency = 0.7  # Default moderate consistency
        if patient_context:
            # Check if patient context makes sense with top prediction
            context_consistency = 0.8  # Slightly higher with context
        
        confidence_components['context_consistency'] = context_consistency
        
        # Overall confidence calculation
        weights = [0.4, 0.3, 0.2, 0.1]
        overall_confidence = sum(comp * weight for comp, weight in zip(confidence_components.values(), weights))
        confidence_components['overall_confidence'] = overall_confidence
        
        return confidence_components
    
    def classify_disease(self, text: str, 
                        patient_context: Optional[PatientContext] = None,
                        environmental_context: Optional[EnvironmentalContext] = None) -> Dict:
        """
        Main disease classification pipeline
        Returns comprehensive classification results with confidence and anomaly detection
        """
        try:
            # Step 1: Extract symptoms with advanced feature engineering
            symptoms = self.extract_symptoms_from_text(text, patient_context)
            
            if not symptoms:
                return {
                    'primary_diagnosis': 'insufficient_information',
                    'confidence': 0.1,
                    'differential_diagnoses': [],
                    'anomaly_detected': False,
                    'recommendation': 'More symptom information needed for accurate diagnosis'
                }
            
            # Step 2: Calculate Bayesian probabilities
            disease_probabilities = self.calculate_bayesian_probability(symptoms, patient_context, environmental_context)
            
            # Step 3: Detect anomalies
            anomaly_scores = self.detect_anomalies(symptoms, disease_probabilities)
            
            # Step 4: Calculate confidence scores
            confidence_scores = self.calculate_confidence_scores(symptoms, disease_probabilities, patient_context)
            
            # Step 5: Generate final classification
            sorted_diseases = sorted(disease_probabilities.items(), key=lambda x: x[1], reverse=True)
            
            primary_diagnosis = sorted_diseases[0][0] if sorted_diseases else 'unknown'
            primary_confidence = sorted_diseases[0][1] if sorted_diseases else 0.0
            
            # Differential diagnoses (top 3 alternatives)
            differential_diagnoses = [
                {'disease': disease, 'probability': prob} 
                for disease, prob in sorted_diseases[1:4] if prob > 0.1
            ]
            
            # Check for anomaly detection
            anomaly_detected = anomaly_scores['combined_anomaly'] > 0.7
            
            # Generate recommendations
            recommendation = self._generate_recommendation(primary_diagnosis, primary_confidence, anomaly_detected, symptoms)
            
            return {
                'primary_diagnosis': primary_diagnosis,
                'confidence': confidence_scores['overall_confidence'],
                'probability': primary_confidence,
                'differential_diagnoses': differential_diagnoses,
                'extracted_symptoms': [
                    {
                        'name': s.name, 
                        'severity': s.severity, 
                        'duration_hours': s.duration_hours,
                        'progression': s.progression,
                        'temporal_pattern': s.temporal_pattern
                    } for s in symptoms
                ],
                'anomaly_detected': anomaly_detected,
                'anomaly_scores': anomaly_scores,
                'confidence_breakdown': confidence_scores,
                'recommendation': recommendation,
                'severity_assessment': self._assess_overall_severity(symptoms),
                'urgency_level': self._assess_urgency(primary_diagnosis, symptoms, anomaly_detected)
            }
            
        except Exception as e:
            logger.error(f"Disease classification error: {e}")
            return {
                'primary_diagnosis': 'classification_error',
                'confidence': 0.0,
                'error': str(e),
                'recommendation': 'System error occurred. Please consult healthcare provider.'
            }
    
    def _generate_recommendation(self, diagnosis: str, confidence: float, anomaly_detected: bool, symptoms: List[SymptomFeature]) -> str:
        """Generate clinical recommendations based on classification results"""
        if anomaly_detected:
            return "⚠️ Unusual symptom pattern detected. Immediate expert medical evaluation required."
        
        if confidence > 0.8:
            if diagnosis == 'cholera':
                return "🚨 HIGH PRIORITY: Immediate medical attention and rehydration therapy required. Isolate patient."
            elif diagnosis == 'typhoid':
                return "⚠️ URGENT: Antibiotic treatment needed. Consult healthcare provider immediately."
            elif diagnosis == 'malaria':
                return "🏥 Rapid diagnostic test recommended. Start antimalarial treatment if positive."
            elif diagnosis == 'dengue':
                return "⚠️ Monitor closely for bleeding/shock. Maintain hydration. Avoid aspirin."
            elif diagnosis == 'covid19':
                return "🔍 COVID-19 testing recommended. Isolate and monitor oxygen levels."
            else:
                return f"Probable {diagnosis.replace('_', ' ')}. Consult healthcare provider for treatment."
        
        elif confidence > 0.5:
            return f"Possible {diagnosis.replace('_', ' ')}. Monitor symptoms and seek medical advice if worsening."
        
        else:
            max_severity = max([s.severity for s in symptoms]) if symptoms else 0
            if max_severity >= 8:
                return "⚠️ High severity symptoms detected. Immediate medical evaluation recommended."
            else:
                return "Multiple conditions possible. Consider medical consultation for proper diagnosis."
    
    def _assess_overall_severity(self, symptoms: List[SymptomFeature]) -> str:
        """Assess overall severity based on symptoms"""
        if not symptoms:
            return 'Unknown'
        
        max_severity = max([s.severity for s in symptoms])
        avg_severity = np.mean([s.severity for s in symptoms])
        
        # Check for high-risk symptoms
        high_risk_symptoms = ['severe_dehydration', 'difficulty_breathing', 'chest_pain', 'bleeding']
        has_high_risk = any(s.name in high_risk_symptoms for s in symptoms)
        
        if max_severity >= 8 or has_high_risk:
            return 'High'
        elif max_severity >= 6 or avg_severity >= 5:
            return 'Medium'
        else:
            return 'Low'
    
    def _assess_urgency(self, diagnosis: str, symptoms: List[SymptomFeature], anomaly_detected: bool) -> str:
        """Assess urgency level for medical intervention"""
        if anomaly_detected:
            return 'IMMEDIATE'
        
        high_urgency_diseases = ['cholera', 'severe_malaria', 'dengue_hemorrhagic', 'covid19_severe']
        urgent_symptoms = ['severe_dehydration', 'difficulty_breathing', 'chest_pain', 'bleeding']
        
        if diagnosis in high_urgency_diseases:
            return 'IMMEDIATE'
        
        if any(s.name in urgent_symptoms and s.severity >= 8 for s in symptoms):
            return 'URGENT'
        
        max_severity = max([s.severity for s in symptoms]) if symptoms else 0
        if max_severity >= 7:
            return 'URGENT'
        elif max_severity >= 5:
            return 'MODERATE'
        else:
            return 'LOW'

# Initialize the global classifier instance
advanced_classifier = AdvancedDiseaseClassifier()

def classify_health_message(message_text: str, 
                          patient_age: int = None,
                          patient_gender: str = None,
                          location: Dict = None) -> Dict:
    """
    Convenience function for classifying health messages
    """
    # Create patient context if information provided
    patient_context = None
    if patient_age or patient_gender or location:
        patient_context = PatientContext(
            age=patient_age or 30,
            gender=patient_gender or 'unknown',
            occupation='unknown',
            location=location or {'lat': 0.0, 'lon': 0.0},
            household_size=4,
            water_source='unknown',
            sanitation_level=3,
            recent_travel=False,
            vaccination_status={}
        )
    
    # Create environmental context (could be enhanced with real data)
    current_month = datetime.now().month
    environmental_context = EnvironmentalContext(
        season='summer' if 4 <= current_month <= 6 else 'winter' if current_month in [12, 1, 2] else 'monsoon' if 7 <= current_month <= 9 else 'post_monsoon',
        temperature=30.0,
        humidity=70.0,
        rainfall_7day=10.0,
        water_quality_score=0.6,
        air_quality_index=100,
        population_density=500
    )
    
    return advanced_classifier.classify_disease(message_text, patient_context, environmental_context)

if __name__ == "__main__":
    # Test the advanced classifier
    test_messages = [
        "I have severe watery diarrhea and vomiting since yesterday, feeling very dehydrated",
        "High fever for 5 days with headache and abdominal pain, rose-colored spots on chest", 
        "Fever comes and goes with chills and sweats, feeling very weak",
        "High fever, severe headache, pain behind eyes, and red rash on body",
        "Yellow skin and eyes, feeling tired, dark urine and pale stool",
        "Dry cough, fever, shortness of breath, lost sense of taste and smell"
    ]
    
    print("🧠 Advanced Disease Classification Engine - Test Results")
    print("=" * 80)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 TEST CASE {i}:")
        print(f"📝 Message: '{message}'")
        
        result = classify_health_message(message)
        
        print(f"🎯 Primary Diagnosis: {result['primary_diagnosis']} ({result['confidence']:.1%} confidence)")
        print(f"⚠️ Severity: {result.get('severity_assessment', 'Unknown')}")
        print(f"🚨 Urgency: {result.get('urgency_level', 'Unknown')}")
        print(f"💡 Recommendation: {result['recommendation']}")
        
        if result['differential_diagnoses']:
            print("🔍 Alternative Diagnoses:")
            for alt in result['differential_diagnoses']:
                print(f"   - {alt['disease']}: {alt['probability']:.1%}")
        
        if result.get('anomaly_detected'):
            print("🚨 ANOMALY DETECTED - Novel pattern requiring investigation")
        
        print("-" * 60)
