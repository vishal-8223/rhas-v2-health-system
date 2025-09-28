#!/usr/bin/env python3
"""
🌍 Environmental & Geographic Analysis Module for RHAS v2.0
Advanced Climate, Industrial & Water Contamination Analysis

Features:
- Real-time weather data integration
- Industrial contamination source mapping
- Water body pollution analysis
- Geographic risk assessment
- Climate-disease correlation analysis
"""

import requests
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ClimateData:
    """Real-time climate conditions"""
    temperature_celsius: float
    humidity_percent: float
    rainfall_mm_7days: float
    wind_speed_kmh: float
    air_pressure_hpa: float
    uv_index: int
    season: str
    weather_pattern: str  # 'stable', 'stormy', 'dry', 'wet'

@dataclass
class IndustryData:
    """Nearby industrial contamination sources"""
    industry_type: str
    distance_km: float
    contamination_level: str  # 'low', 'medium', 'high', 'critical'
    pollutants: List[str]
    water_impact_score: float  # 0-10 scale
    air_impact_score: float    # 0-10 scale

@dataclass
class WaterBodyAnalysis:
    """Water body contamination analysis"""
    water_source_type: str  # 'river', 'lake', 'groundwater', 'well', 'municipal'
    contamination_risk: float  # 0-10 scale
    bacterial_load_estimate: str  # 'low', 'medium', 'high', 'critical'
    chemical_contamination: List[str]
    recent_pollution_events: List[str]
    safety_score: float  # 0-10 scale (10 = safest)

@dataclass
class GeographicRiskProfile:
    """Complete geographic risk assessment"""
    location: Dict[str, float]  # {'lat': x, 'lon': y, 'elevation': z}
    climate_risk_score: float
    industrial_risk_score: float
    water_contamination_score: float
    overall_disease_risk: float
    risk_factors: List[str]
    recommendations: List[str]

class EnvironmentalGeographicAnalyzer:
    """
    Advanced Environmental & Geographic Analysis Engine
    Real-time climate, industrial, and contamination assessment
    """
    
    def __init__(self):
        self.industry_database = self._initialize_industry_database()
        self.water_body_database = self._initialize_water_body_database()
        self.climate_disease_correlations = self._initialize_climate_correlations()
        self.contamination_thresholds = self._initialize_contamination_thresholds()
        logger.info("🌍 Environmental Geographic Analyzer initialized")
    
    def _initialize_industry_database(self) -> Dict[str, List[IndustryData]]:
        """Initialize database of industrial contamination sources by region"""
        return {
            # Mumbai Metropolitan Region
            'mumbai': [
                IndustryData('textile_mills', 2.5, 'high', 
                           ['dyes', 'heavy_metals', 'organic_compounds'], 8.5, 6.0),
                IndustryData('chemical_plants', 5.2, 'critical', 
                           ['mercury', 'lead', 'chlorine', 'acids'], 9.2, 8.5),
                IndustryData('oil_refinery', 8.1, 'medium', 
                           ['petroleum_products', 'sulfur', 'benzene'], 6.8, 7.2),
                IndustryData('pharmaceutical', 3.7, 'medium', 
                           ['antibiotics', 'hormones', 'solvents'], 7.1, 5.5),
                IndustryData('tanneries', 4.3, 'high', 
                           ['chromium', 'sulfides', 'organic_waste'], 8.8, 4.2)
            ],
            # Delhi NCR Region  
            'delhi': [
                IndustryData('power_plants', 6.8, 'high', 
                           ['coal_ash', 'sulfur_dioxide', 'particulates'], 7.5, 9.1),
                IndustryData('steel_mills', 12.5, 'medium', 
                           ['iron_oxide', 'carbon_monoxide', 'dust'], 6.2, 8.3),
                IndustryData('cement_factories', 15.2, 'medium', 
                           ['limestone_dust', 'silica', 'sulfur'], 5.8, 7.9),
                IndustryData('electronic_waste', 3.2, 'critical', 
                           ['lead', 'mercury', 'cadmium', 'plastics'], 8.9, 6.7),
                IndustryData('food_processing', 7.8, 'low', 
                           ['organic_waste', 'preservatives', 'oils'], 4.2, 2.1)
            ],
            # Bangalore Region
            'bangalore': [
                IndustryData('it_parks', 2.1, 'low', 
                           ['electronic_waste', 'air_conditioning_coolants'], 3.2, 2.8),
                IndustryData('garment_factories', 8.7, 'medium', 
                           ['dyes', 'bleaching_agents', 'cotton_dust'], 6.8, 5.2),
                IndustryData('aerospace', 18.5, 'medium', 
                           ['metals', 'fuels', 'composite_materials'], 5.9, 6.8),
                IndustryData('brewery_distillery', 5.4, 'medium', 
                           ['organic_waste', 'alcohol', 'yeast'], 6.1, 3.2)
            ],
            # Chennai Region
            'chennai': [
                IndustryData('petrochemicals', 7.2, 'high', 
                           ['hydrocarbons', 'benzene', 'phenols'], 8.7, 7.8),
                IndustryData('port_activities', 3.8, 'medium', 
                           ['fuel_oils', 'cargo_chemicals', 'ballast_water'], 7.2, 5.9),
                IndustryData('leather_export', 9.5, 'high', 
                           ['chromium', 'acids', 'organic_solvents'], 8.9, 4.5),
                IndustryData('fertilizer_plants', 14.2, 'high', 
                           ['ammonia', 'phosphates', 'nitrogen_compounds'], 8.1, 7.3)
            ],
            # Kolkata Region
            'kolkata': [
                IndustryData('coal_mines', 25.8, 'critical', 
                           ['coal_dust', 'sulfur', 'heavy_metals'], 9.1, 9.5),
                IndustryData('jute_mills', 6.3, 'medium', 
                           ['organic_waste', 'retting_chemicals'], 6.2, 3.8),
                IndustryData('engineering_works', 8.9, 'medium', 
                           ['metal_shavings', 'oils', 'acids'], 6.8, 6.2),
                IndustryData('thermal_power', 12.4, 'high', 
                           ['fly_ash', 'sulfur_dioxide', 'mercury'], 8.5, 9.2)
            ]
        }
    
    def _initialize_water_body_database(self) -> Dict[str, WaterBodyAnalysis]:
        """Initialize water body contamination data by region"""
        return {
            'mumbai': WaterBodyAnalysis(
                'river', 7.8, 'high', 
                ['industrial_effluents', 'sewage', 'plastic_waste'],
                ['textile_discharge_2023', 'oil_spill_2023'],
                2.8
            ),
            'delhi': WaterBodyAnalysis(
                'river', 9.2, 'critical', 
                ['industrial_waste', 'untreated_sewage', 'agricultural_runoff'],
                ['chemical_spill_2023', 'sewage_overflow_2023'],
                1.5
            ),
            'bangalore': WaterBodyAnalysis(
                'lake', 6.5, 'medium', 
                ['urban_runoff', 'construction_debris', 'domestic_waste'],
                ['lake_foaming_2023'],
                4.2
            ),
            'chennai': WaterBodyAnalysis(
                'groundwater', 8.1, 'high', 
                ['seawater_intrusion', 'industrial_seepage', 'fertilizer_runoff'],
                ['groundwater_depletion_2023'],
                2.9
            ),
            'kolkata': WaterBodyAnalysis(
                'river', 8.9, 'critical', 
                ['coal_washery_waste', 'industrial_metals', 'organic_pollutants'],
                ['coal_dust_contamination_2023'],
                1.8
            )
        }
    
    def _initialize_climate_correlations(self) -> Dict[str, Dict[str, float]]:
        """Disease-climate correlation matrix"""
        return {
            'cholera': {
                'high_temperature': 0.7,    # >30°C increases risk
                'heavy_rainfall': 0.8,      # >100mm in 7 days
                'flooding': 0.9,            # Flood conditions
                'high_humidity': 0.6,       # >80% humidity
                'monsoon_season': 0.8
            },
            'dengue': {
                'temperature_range': 0.8,   # 25-30°C optimal for mosquitos
                'stagnant_water': 0.9,      # Post-rainfall stagnation
                'urban_heat_island': 0.6,   # Urban temperature effects  
                'moderate_humidity': 0.7,   # 60-80% humidity
                'post_monsoon': 0.8
            },
            'typhoid': {
                'poor_sanitation': 0.8,
                'water_scarcity': 0.7,      # Leads to unsafe water use
                'summer_heat': 0.6,         # >35°C
                'dust_storms': 0.5,         # Contamination spread
                'dry_season': 0.6
            },
            'malaria': {
                'stagnant_water': 0.9,
                'rural_flooding': 0.8,
                'forest_proximity': 0.7,
                'optimal_breeding_temp': 0.8, # 20-30°C
                'monsoon_active': 0.8
            },
            'hepatitis_a': {
                'poor_water_quality': 0.8,
                'overcrowding': 0.6,
                'seasonal_festivals': 0.5,   # Mass gatherings
                'monsoon_contamination': 0.7
            }
        }
    
    def _initialize_contamination_thresholds(self) -> Dict[str, float]:
        """Contamination risk thresholds"""
        return {
            'water_bacterial_safe': 2.0,
            'water_bacterial_moderate': 5.0,
            'water_bacterial_high': 8.0,
            'industrial_distance_safe': 10.0,  # km
            'industrial_distance_risk': 5.0,   # km
            'air_quality_safe': 50,            # AQI
            'air_quality_moderate': 100,
            'air_quality_unhealthy': 150
        }
    
    def get_real_time_weather(self, lat: float, lon: float) -> ClimateData:
        """Get real-time weather data (simulated for demo)"""
        # In production, this would call actual weather APIs like OpenWeatherMap
        # For demo, we'll simulate based on location and current date
        
        current_month = datetime.now().month
        
        # Simulate seasonal weather patterns for India
        if lat > 20:  # Northern India
            if 4 <= current_month <= 6:  # Summer
                temp = 35 + (lat - 20) * 0.5
                humidity = 40 + abs(hash(str(lat + lon)) % 20)
                rainfall = 2 + abs(hash(str(lat * lon)) % 15)
                season = 'summer'
            elif 7 <= current_month <= 9:  # Monsoon
                temp = 28 + abs(hash(str(lat)) % 8)
                humidity = 75 + abs(hash(str(lon)) % 15)
                rainfall = 45 + abs(hash(str(lat + lon)) % 80)
                season = 'monsoon'
            else:  # Winter/Post-monsoon
                temp = 22 + abs(hash(str(lat * 2)) % 12)
                humidity = 55 + abs(hash(str(lon * 2)) % 25)
                rainfall = 3 + abs(hash(str(lat - lon)) % 10)
                season = 'winter'
        else:  # Southern India
            temp = 30 + abs(hash(str(lat)) % 8)
            humidity = 65 + abs(hash(str(lon)) % 20)
            rainfall = 25 + abs(hash(str(lat + lon)) % 50)
            season = 'tropical'
        
        return ClimateData(
            temperature_celsius=temp,
            humidity_percent=humidity,
            rainfall_mm_7days=rainfall,
            wind_speed_kmh=12 + abs(hash(str(lat)) % 15),
            air_pressure_hpa=1013 + abs(hash(str(lon)) % 20),
            uv_index=min(11, int(temp / 4)),
            season=season,
            weather_pattern='wet' if rainfall > 30 else 'dry'
        )
    
    def analyze_industrial_contamination(self, lat: float, lon: float, city: str) -> List[IndustryData]:
        """Analyze nearby industrial contamination sources"""
        city_key = city.lower()
        
        # Get industries for the city
        if city_key in self.industry_database:
            industries = self.industry_database[city_key]
        else:
            # Default industrial profile for unknown cities
            industries = [
                IndustryData('mixed_industrial', 8.0, 'medium', 
                           ['general_pollutants', 'organic_waste'], 6.0, 5.0)
            ]
        
        # Calculate actual distance and impact based on coordinates
        # (In production, this would use actual industrial facility locations)
        relevant_industries = []
        for industry in industries:
            # Simulate distance variation based on coordinates
            distance_factor = 1 + abs(hash(str(lat + lon)) % 5) * 0.2
            adjusted_distance = industry.distance_km * distance_factor
            
            # Only include industries within 30km
            if adjusted_distance <= 30.0:
                # Adjust contamination level based on distance
                distance_impact = max(0.1, 1.0 - (adjusted_distance / 30.0))
                
                adjusted_industry = IndustryData(
                    industry_type=industry.industry_type,
                    distance_km=adjusted_distance,
                    contamination_level=industry.contamination_level,
                    pollutants=industry.pollutants,
                    water_impact_score=industry.water_impact_score * distance_impact,
                    air_impact_score=industry.air_impact_score * distance_impact
                )
                relevant_industries.append(adjusted_industry)
        
        return relevant_industries
    
    def analyze_water_contamination(self, lat: float, lon: float, city: str, 
                                   climate_data: ClimateData, 
                                   industries: List[IndustryData]) -> WaterBodyAnalysis:
        """Analyze water body contamination risk"""
        city_key = city.lower()
        
        # Get base water analysis for the city
        if city_key in self.water_body_database:
            base_analysis = self.water_body_database[city_key]
        else:
            base_analysis = WaterBodyAnalysis(
                'groundwater', 5.0, 'medium', 
                ['general_contamination'], [], 5.0
            )
        
        # Adjust contamination based on industrial proximity
        industrial_impact = 0.0
        chemical_contaminants = list(base_analysis.chemical_contamination)
        
        for industry in industries:
            if industry.distance_km <= 10.0:  # Within 10km
                impact_factor = max(0.1, 1.0 - (industry.distance_km / 10.0))
                industrial_impact += industry.water_impact_score * impact_factor * 0.1
                
                # Add industrial pollutants
                for pollutant in industry.pollutants:
                    if pollutant not in chemical_contaminants:
                        chemical_contaminants.append(pollutant)
        
        # Adjust based on climate conditions
        climate_impact = 0.0
        if climate_data.rainfall_mm_7days > 50:  # Heavy rainfall increases contamination
            climate_impact += 1.5
        if climate_data.temperature_celsius > 30:  # High temperature increases bacterial growth
            climate_impact += 1.0
        if climate_data.humidity_percent > 80:  # High humidity affects water quality
            climate_impact += 0.5
        
        # Calculate adjusted contamination risk
        base_risk = base_analysis.contamination_risk
        adjusted_risk = min(10.0, base_risk + industrial_impact + climate_impact)
        
        # Determine bacterial load based on adjusted risk
        if adjusted_risk <= 3.0:
            bacterial_load = 'low'
        elif adjusted_risk <= 6.0:
            bacterial_load = 'medium'
        elif adjusted_risk <= 8.5:
            bacterial_load = 'high'
        else:
            bacterial_load = 'critical'
        
        # Calculate safety score (inverse of risk)
        safety_score = max(0.0, 10.0 - adjusted_risk)
        
        # Add recent events based on industrial activity
        recent_events = list(base_analysis.recent_pollution_events)
        if industrial_impact > 2.0:
            recent_events.append(f'industrial_discharge_{datetime.now().year}')
        if climate_data.rainfall_mm_7days > 80:
            recent_events.append(f'runoff_contamination_{datetime.now().year}')
        
        return WaterBodyAnalysis(
            water_source_type=base_analysis.water_source_type,
            contamination_risk=adjusted_risk,
            bacterial_load_estimate=bacterial_load,
            chemical_contamination=chemical_contaminants,
            recent_pollution_events=recent_events,
            safety_score=safety_score
        )
    
    def calculate_climate_disease_risk(self, disease: str, climate_data: ClimateData) -> float:
        """Calculate disease risk based on climate conditions"""
        if disease not in self.climate_disease_correlations:
            return 0.5  # Default moderate risk
        
        correlations = self.climate_disease_correlations[disease]
        risk_score = 0.0
        total_factors = 0
        
        # Temperature-based risk
        if 'high_temperature' in correlations and climate_data.temperature_celsius > 30:
            risk_score += correlations['high_temperature'] * ((climate_data.temperature_celsius - 30) / 10)
            total_factors += 1
        
        if 'temperature_range' in correlations:
            optimal_temp = 27.5  # Middle of 25-30°C range
            temp_deviation = abs(climate_data.temperature_celsius - optimal_temp)
            temp_risk = max(0, correlations['temperature_range'] * (1 - temp_deviation / 15))
            risk_score += temp_risk
            total_factors += 1
        
        # Rainfall-based risk
        if 'heavy_rainfall' in correlations and climate_data.rainfall_mm_7days > 50:
            rainfall_factor = min(1.0, (climate_data.rainfall_mm_7days - 50) / 100)
            risk_score += correlations['heavy_rainfall'] * rainfall_factor
            total_factors += 1
        
        # Humidity-based risk  
        if 'high_humidity' in correlations and climate_data.humidity_percent > 80:
            humidity_factor = (climate_data.humidity_percent - 80) / 20
            risk_score += correlations['high_humidity'] * humidity_factor
            total_factors += 1
        
        # Seasonal risk
        seasonal_factors = ['monsoon_season', 'monsoon_active', 'post_monsoon', 'summer_heat', 'dry_season']
        for factor in seasonal_factors:
            if factor in correlations:
                if (factor == 'monsoon_season' and climate_data.season == 'monsoon') or \
                   (factor == 'summer_heat' and climate_data.season == 'summer') or \
                   (factor == 'dry_season' and climate_data.weather_pattern == 'dry'):
                    risk_score += correlations[factor]
                    total_factors += 1
        
        # Average the risk score
        if total_factors > 0:
            risk_score = risk_score / total_factors
        
        return min(1.0, risk_score)
    
    def generate_comprehensive_analysis(self, lat: float, lon: float, city: str, 
                                      disease_predictions: Dict[str, float]) -> GeographicRiskProfile:
        """Generate comprehensive environmental risk assessment"""
        
        # Get real-time climate data
        climate_data = self.get_real_time_weather(lat, lon)
        
        # Analyze industrial contamination
        industries = self.analyze_industrial_contamination(lat, lon, city)
        
        # Analyze water contamination
        water_analysis = self.analyze_water_contamination(lat, lon, city, climate_data, industries)
        
        # Calculate climate-disease risks
        climate_risks = {}
        for disease, prediction in disease_predictions.items():
            climate_risk = self.calculate_climate_disease_risk(disease, climate_data)
            climate_risks[disease] = climate_risk
        
        # Calculate overall risk scores
        climate_risk_score = sum(climate_risks.values()) / len(climate_risks) if climate_risks else 0.5
        
        industrial_risk_score = 0.0
        if industries:
            avg_water_impact = sum(i.water_impact_score for i in industries) / len(industries)
            avg_air_impact = sum(i.air_impact_score for i in industries) / len(industries)
            industrial_risk_score = (avg_water_impact + avg_air_impact) / 20  # Normalize to 0-1
        
        water_contamination_score = water_analysis.contamination_risk / 10.0  # Normalize to 0-1
        
        # Calculate overall disease risk
        overall_risk = (climate_risk_score * 0.4 + 
                       industrial_risk_score * 0.3 + 
                       water_contamination_score * 0.3)
        
        # Generate risk factors and recommendations
        risk_factors = []
        recommendations = []
        
        # Climate risk factors
        if climate_data.temperature_celsius > 35:
            risk_factors.append(f'🌡️ Extreme heat ({climate_data.temperature_celsius:.1f}°C)')
            recommendations.append('🏠 Ensure proper hydration and cooling')
        
        if climate_data.rainfall_mm_7days > 75:
            risk_factors.append(f'🌧️ Heavy rainfall ({climate_data.rainfall_mm_7days:.1f}mm)')
            recommendations.append('💧 Boil water before consumption')
        
        if climate_data.humidity_percent > 85:
            risk_factors.append(f'💨 High humidity ({climate_data.humidity_percent:.1f}%)')
            recommendations.append('🦟 Use mosquito protection measures')
        
        # Industrial risk factors
        critical_industries = [i for i in industries if i.contamination_level == 'critical' and i.distance_km <= 5.0]
        if critical_industries:
            risk_factors.append(f'🏭 Critical industrial contamination ({len(critical_industries)} sources)')
            recommendations.append('⚠️ Avoid outdoor activities during high pollution hours')
        
        # Water contamination risk factors
        if water_analysis.contamination_risk > 7.0:
            risk_factors.append(f'💧 High water contamination risk ({water_analysis.contamination_risk:.1f}/10)')
            recommendations.append('🔥 Mandatory water boiling/filtration required')
        
        if water_analysis.bacterial_load_estimate == 'critical':
            risk_factors.append('🦠 Critical bacterial contamination detected')
            recommendations.append('🚰 Use only bottled or properly treated water')
        
        # Chemical contamination
        if len(water_analysis.chemical_contamination) > 3:
            risk_factors.append(f'⚗️ Multiple chemical contaminants ({len(water_analysis.chemical_contamination)})')
            recommendations.append('🏥 Regular health monitoring recommended')
        
        return GeographicRiskProfile(
            location={'lat': lat, 'lon': lon, 'elevation': 0.0},
            climate_risk_score=climate_risk_score,
            industrial_risk_score=industrial_risk_score,  
            water_contamination_score=water_contamination_score,
            overall_disease_risk=overall_risk,
            risk_factors=risk_factors,
            recommendations=recommendations
        )

# Global instance for easy access
environmental_analyzer = EnvironmentalGeographicAnalyzer()
