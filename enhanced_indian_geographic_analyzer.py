#!/usr/bin/env python3
"""
🇮🇳 Enhanced Indian Geographic Analyzer for RHAS v2.0
Comprehensive Indian phone number mapping, industrial analysis, and climate correlation
"""

import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class IndianLocationData:
    """Enhanced Indian location data"""
    city: str
    state: str
    district: str
    lat: float
    lon: float
    telecom_circle: str
    population: int
    industrial_zones: List[str]
    major_industries: List[str]
    water_sources: List[str]
    climate_zone: str
    pollution_level: str

class EnhancedIndianGeographicAnalyzer:
    """Enhanced geographic analyzer for Indian phone numbers and locations"""
    
    def __init__(self):
        self.indian_phone_database = self._initialize_indian_phone_database()
        self.industrial_pollution_data = self._initialize_industrial_pollution_data()
        self.climate_disease_mapping = self._initialize_climate_disease_mapping()
    
    def _initialize_indian_phone_database(self) -> Dict[str, IndianLocationData]:
        """Comprehensive Indian phone number to location mapping"""
        return {
            # Maharashtra
            '+91729': IndianLocationData('Mumbai', 'Maharashtra', 'Mumbai', 19.0760, 72.8777, 'Maharashtra', 12400000, 
                                       ['MIDC Andheri', 'Mahape Industrial Area', 'Taloja MIDC'], 
                                       ['Textiles', 'Pharmaceuticals', 'Chemicals', 'Petrochemicals', 'Engineering'],
                                       ['Vashi Creek', 'Thane Creek', 'Coastal Wells'], 'Tropical Wet', 'High'),
            '+91987': IndianLocationData('Pune', 'Maharashtra', 'Pune', 18.5204, 73.8567, 'Maharashtra', 3100000,
                                       ['Pimpri-Chinchwad', 'Bhosari MIDC', 'Aurangabad MIDC'],
                                       ['Automobiles', 'IT', 'Engineering', 'Sugar Mills'], 
                                       ['Mula River', 'Mutha River', 'Groundwater'], 'Semi-Arid', 'Medium'),
            
            # Delhi NCR
            '+9111': IndianLocationData('New Delhi', 'Delhi', 'New Delhi', 28.6139, 77.2090, 'Delhi', 32900000,
                                      ['Okhla Industrial Area', 'Mayapuri Industrial Area', 'Wazirpur Industrial Area'],
                                      ['Power Plants', 'Steel', 'Cement', 'E-waste Processing', 'Food Processing'],
                                      ['Yamuna River', 'Groundwater', 'Canal Water'], 'Semi-Arid', 'Critical'),
            '+91124': IndianLocationData('Gurgaon', 'Haryana', 'Gurgaon', 28.4595, 77.0266, 'Haryana', 1150000,
                                       ['IMT Manesar', 'HSIIDC Industrial Estate'], 
                                       ['Automobiles', 'IT', 'Manufacturing'], 
                                       ['Groundwater', 'Treated Water'], 'Semi-Arid', 'High'),
            
            # Karnataka
            '+9180': IndianLocationData('Bangalore', 'Karnataka', 'Bangalore Urban', 12.9716, 77.5946, 'Karnataka', 8400000,
                                      ['Electronic City', 'Peenya Industrial Area', 'Bommasandra Industrial Area'],
                                      ['IT/Software', 'Aerospace', 'Biotechnology', 'Textiles', 'Engineering'],
                                      ['Kaveri River', 'Groundwater', 'Lakes'], 'Tropical Savanna', 'Medium'),
            '+91821': IndianLocationData('Mysore', 'Karnataka', 'Mysore', 12.2958, 76.6394, 'Karnataka', 920000,
                                       ['Mysore Industrial Area', 'Nanjangud Industrial Area'],
                                       ['Sugar Mills', 'Silk', 'Sandalwood Oil', 'Incense'], 
                                       ['Kaveri River', 'Kabini River'], 'Tropical', 'Low'),
            
            # Tamil Nadu
            '+9144': IndianLocationData('Chennai', 'Tamil Nadu', 'Chennai', 13.0827, 80.2707, 'Tamil Nadu', 4600000,
                                      ['Ambattur Industrial Estate', 'Guindy Industrial Estate', 'Sriperumbudur'],
                                      ['Automobiles', 'Petrochemicals', 'Leather', 'IT', 'Port Activities'],
                                      ['Cooum River', 'Adyar River', 'Groundwater', 'Desalination'], 'Tropical Wet', 'High'),
            '+91427': IndianLocationData('Salem', 'Tamil Nadu', 'Salem', 11.6643, 78.1460, 'Tamil Nadu', 830000,
                                       ['Salem Industrial Estate'], 
                                       ['Steel', 'Textiles', 'Magnesite Mining', 'Silver Processing'], 
                                       ['Thirumanimutharu River', 'Groundwater'], 'Semi-Arid', 'Medium'),
            
            # West Bengal
            '+9133': IndianLocationData('Kolkata', 'West Bengal', 'Kolkata', 22.5726, 88.3639, 'West Bengal', 4500000,
                                      ['Salt Lake Electronics Complex', 'Kalyani Industrial Complex'],
                                      ['Jute', 'Engineering', 'Chemicals', 'Pharmaceuticals', 'Coal'],
                                      ['Hooghly River', 'Groundwater'], 'Tropical Wet', 'High'),
            '+91342': IndianLocationData('Asansol', 'West Bengal', 'Paschim Bardhaman', 23.6833, 86.9833, 'West Bengal', 563000,
                                       ['Burnpur Industrial Area'], 
                                       ['Coal Mining', 'Steel', 'Cement', 'Fertilizers'], 
                                       ['Damodar River', 'Groundwater'], 'Tropical', 'Critical'),
            
            # Gujarat
            '+9179': IndianLocationData('Ahmedabad', 'Gujarat', 'Ahmedabad', 23.0225, 72.5714, 'Gujarat', 5500000,
                                      ['Naroda Industrial Estate', 'Vatva GIDC', 'Sanand Industrial Area'],
                                      ['Textiles', 'Chemicals', 'Pharmaceuticals', 'Engineering', 'Automobiles'],
                                      ['Sabarmati River', 'Groundwater', 'Canal Water'], 'Semi-Arid', 'High'),
            '+91261': IndianLocationData('Surat', 'Gujarat', 'Surat', 21.1702, 72.8311, 'Gujarat', 4500000,
                                       ['Sachin GIDC', 'Pandesara GIDC'], 
                                       ['Textiles', 'Diamonds', 'Chemicals', 'Petrochemicals'], 
                                       ['Tapi River', 'Groundwater'], 'Semi-Arid', 'High'),
            
            # Uttar Pradesh
            '+91522': IndianLocationData('Lucknow', 'Uttar Pradesh', 'Lucknow', 26.8467, 80.9462, 'Uttar Pradesh', 2800000,
                                       ['Amausi Industrial Area', 'Sursand Industrial Area'],
                                       ['Chikan Embroidery', 'Chemicals', 'Pharmaceuticals', 'Engineering'],
                                       ['Gomti River', 'Groundwater'], 'Subtropical', 'Medium'),
            '+91562': IndianLocationData('Agra', 'Uttar Pradesh', 'Agra', 27.1767, 78.0081, 'Uttar Pradesh', 1600000,
                                       ['Agra Industrial Area', 'Sikandra Industrial Area'],
                                       ['Leather', 'Shoes', 'Handicrafts', 'Engineering'], 
                                       ['Yamuna River', 'Groundwater'], 'Semi-Arid', 'High'),
            
            # Rajasthan
            '+91141': IndianLocationData('Jaipur', 'Rajasthan', 'Jaipur', 26.9124, 75.7873, 'Rajasthan', 3100000,
                                       ['Sitapura Industrial Area', 'Jaipur Industrial Area'],
                                       ['Textiles', 'Gems', 'Handicrafts', 'Engineering', 'IT'],
                                       ['Groundwater', 'Dams'], 'Semi-Arid', 'Medium'),
            '+91291': IndianLocationData('Jodhpur', 'Rajasthan', 'Jodhpur', 26.2389, 73.0243, 'Rajasthan', 1000000,
                                       ['Boranada Industrial Area'], 
                                       ['Handicrafts', 'Textiles', 'Metal Processing'], 
                                       ['Groundwater'], 'Arid', 'Medium'),
            
            # Punjab
            '+91161': IndianLocationData('Ludhiana', 'Punjab', 'Ludhiana', 30.9010, 75.8573, 'Punjab', 1600000,
                                       ['Focal Point Industrial Area', 'Dhandari Kalan Industrial Area'],
                                       ['Textiles', 'Bicycles', 'Sewing Machines', 'Sports Goods'],
                                       ['Sutlej River', 'Canal Water', 'Groundwater'], 'Semi-Arid', 'High'),
            '+91172': IndianLocationData('Chandigarh', 'Punjab', 'Chandigarh', 30.7333, 76.7794, 'Punjab', 1050000,
                                       ['Industrial Area Phase I & II'], 
                                       ['IT', 'Pharmaceuticals', 'Engineering'], 
                                       ['Groundwater', 'Canal Water'], 'Semi-Arid', 'Low'),
            
            # Kerala
            '+91484': IndianLocationData('Kochi', 'Kerala', 'Ernakulam', 9.9312, 76.2673, 'Kerala', 600000,
                                       ['Cochin Port', 'Eloor Industrial Area', 'Kalamassery Industrial Area'],
                                       ['Petrochemicals', 'Fertilizers', 'Spices', 'Coir', 'Fishing'],
                                       ['Arabian Sea', 'Backwaters', 'Rivers'], 'Tropical Monsoon', 'Medium'),
            '+91471': IndianLocationData('Thiruvananthapuram', 'Kerala', 'Thiruvananthapuram', 8.5241, 76.9366, 'Kerala', 750000,
                                       ['Technopark', 'Industrial Estate'],
                                       ['IT', 'Space Technology', 'Coir', 'Cashew Processing'],
                                       ['Arabian Sea', 'Rivers'], 'Tropical', 'Low'),
            
            # Andhra Pradesh/Telangana
            '+9140': IndianLocationData('Hyderabad', 'Telangana', 'Hyderabad', 17.3850, 78.4867, 'Andhra Pradesh', 6800000,
                                      ['HITEC City', 'IDA Bollaram', 'Medchal Industrial Area'],
                                      ['IT/Biotech', 'Pharmaceuticals', 'Aerospace', 'Chemicals'],
                                      ['Hussain Sagar Lake', 'Musi River', 'Groundwater'], 'Semi-Arid', 'Medium'),
            '+91866': IndianLocationData('Vijayawada', 'Andhra Pradesh', 'Krishna', 16.5062, 80.6480, 'Andhra Pradesh', 1000000,
                                       ['Auto Nagar Industrial Estate'], 
                                       ['Automobiles', 'Textiles', 'Food Processing', 'Engineering'], 
                                       ['Krishna River', 'Canal Water'], 'Tropical', 'Medium'),
            
            # Odisha
            '+91674': IndianLocationData('Bhubaneswar', 'Odisha', 'Khorda', 20.2961, 85.8245, 'Odisha', 840000,
                                       ['Industrial Estate', 'Mancheswar Industrial Estate'],
                                       ['Textiles', 'Engineering', 'Food Processing'],
                                       ['Rivers', 'Groundwater'], 'Tropical', 'Low'),
            
            # Jharkhand
            '+91651': IndianLocationData('Ranchi', 'Jharkhand', 'Ranchi', 23.3441, 85.3096, 'Jharkhand', 1000000,
                                       ['Heavy Engineering Corporation', 'Industrial Areas'],
                                       ['Heavy Engineering', 'Steel', 'Coal Mining'],
                                       ['Subarnarekha River', 'Groundwater'], 'Tropical', 'High'),
            
            # Madhya Pradesh
            '+91755': IndianLocationData('Bhopal', 'Madhya Pradesh', 'Bhopal', 23.2599, 77.4126, 'Madhya Pradesh', 1800000,
                                       ['Mandideep Industrial Area', 'Govindpura Industrial Area'],
                                       ['Heavy Electrical', 'Pharmaceuticals', 'Textiles', 'Engineering'],
                                       ['Upper Lake', 'Lower Lake', 'Groundwater'], 'Tropical', 'Medium'),
            '+91731': IndianLocationData('Indore', 'Madhya Pradesh', 'Indore', 22.7196, 75.8577, 'Madhya Pradesh', 1900000,
                                       ['Pithampur Industrial Area', 'Sanwer Road Industrial Area'],
                                       ['Automobiles', 'Pharmaceuticals', 'IT', 'Textiles'],
                                       ['Shipra River', 'Khan River', 'Groundwater'], 'Subtropical', 'Medium'),
        }
    
    def _initialize_industrial_pollution_data(self) -> Dict[str, Dict]:
        """Industrial pollution data by region"""
        return {
            'mumbai': {
                'major_pollutants': ['Heavy Metals', 'Chemical Dyes', 'Oil Spills', 'Plastic Waste'],
                'air_quality_index': 168,  # Poor
                'water_contamination_level': 8.5,  # High
                'nearby_factories': [
                    {'name': 'Reliance Petrochemicals', 'distance_km': 8.2, 'pollutants': ['Benzene', 'Toluene']},
                    {'name': 'Tata Steel Processing', 'distance_km': 12.1, 'pollutants': ['Iron Oxide', 'Coal Dust']},
                    {'name': 'Godrej Chemicals', 'distance_km': 5.7, 'pollutants': ['Ammonia', 'Sulfur Compounds']},
                    {'name': 'Century Textiles', 'distance_km': 3.4, 'pollutants': ['Dyes', 'Bleaching Agents']}
                ],
                'environmental_risks': ['Industrial Effluent Discharge', 'Coastal Pollution', 'Air Pollution'],
                'disease_correlations': {'respiratory_infection': 0.7, 'skin_allergies': 0.6, 'gastroenteritis': 0.5}
            },
            'delhi': {
                'major_pollutants': ['Particulate Matter', 'Sulfur Dioxide', 'Coal Ash', 'Vehicle Emissions'],
                'air_quality_index': 302,  # Severe
                'water_contamination_level': 9.2,  # Critical
                'nearby_factories': [
                    {'name': 'NTPC Power Plant', 'distance_km': 15.3, 'pollutants': ['Fly Ash', 'SO2', 'NOx']},
                    {'name': 'Badarpur Thermal Plant', 'distance_km': 22.1, 'pollutants': ['Coal Dust', 'Mercury']},
                    {'name': 'Steel Authority of India', 'distance_km': 18.7, 'pollutants': ['Iron Particles', 'CO']},
                    {'name': 'Delhi Cement Works', 'distance_km': 12.5, 'pollutants': ['Cement Dust', 'Silica']}
                ],
                'environmental_risks': ['Severe Air Pollution', 'Yamuna River Contamination', 'Groundwater Pollution'],
                'disease_correlations': {'respiratory_infection': 0.9, 'asthma': 0.8, 'bronchitis': 0.7}
            },
            'bangalore': {
                'major_pollutants': ['Electronic Waste', 'Lake Foam', 'Vehicle Emissions', 'Construction Dust'],
                'air_quality_index': 135,  # Moderate
                'water_contamination_level': 6.5,  # Medium-High
                'nearby_factories': [
                    {'name': 'Hindustan Aeronautics', 'distance_km': 8.9, 'pollutants': ['Metals', 'Fuel Residues']},
                    {'name': 'Bharat Electronics', 'distance_km': 12.3, 'pollutants': ['Electronic Waste', 'Solvents']},
                    {'name': 'IT Park Generators', 'distance_km': 4.2, 'pollutants': ['Diesel Particulates']},
                    {'name': 'Mysore Chemicals', 'distance_km': 45.6, 'pollutants': ['Chemical Effluents']}
                ],
                'environmental_risks': ['Lake Pollution', 'E-waste Contamination', 'Urban Heat Island'],
                'disease_correlations': {'skin_allergies': 0.6, 'respiratory_infection': 0.5, 'gastroenteritis': 0.4}
            },
            'chennai': {
                'major_pollutants': ['Petrochemical Waste', 'Port Pollution', 'Leather Chemicals', 'Salt Water Intrusion'],
                'air_quality_index': 156,  # Poor
                'water_contamination_level': 8.1,  # High
                'nearby_factories': [
                    {'name': 'Chennai Petroleum Corporation', 'distance_km': 6.8, 'pollutants': ['Hydrocarbons', 'Sulfur']},
                    {'name': 'Madras Fertilizers', 'distance_km': 11.2, 'pollutants': ['Ammonia', 'Phosphates']},
                    {'name': 'Tamil Nadu Newsprint', 'distance_km': 28.5, 'pollutants': ['Bleaching Chemicals']},
                    {'name': 'Leather Export Units', 'distance_km': 15.7, 'pollutants': ['Chromium', 'Acids']}
                ],
                'environmental_risks': ['Coastal Pollution', 'Groundwater Salination', 'Industrial Discharge'],
                'disease_correlations': {'diarrheal_disease': 0.7, 'skin_disorders': 0.6, 'respiratory_infection': 0.5}
            },
            'kolkata': {
                'major_pollutants': ['Coal Dust', 'Industrial Metals', 'Organic Pollutants', 'River Silt'],
                'air_quality_index': 198,  # Poor
                'water_contamination_level': 8.9,  # High
                'nearby_factories': [
                    {'name': 'Eastern Coalfields', 'distance_km': 35.2, 'pollutants': ['Coal Dust', 'Heavy Metals']},
                    {'name': 'Haldia Petrochemicals', 'distance_km': 45.8, 'pollutants': ['Petrochemicals']},
                    {'name': 'IISCO Steel Plant', 'distance_km': 42.1, 'pollutants': ['Iron Particles', 'Coke']},
                    {'name': 'Titagarh Wagons', 'distance_km': 18.9, 'pollutants': ['Metal Shavings', 'Paint']}
                ],
                'environmental_risks': ['River Pollution', 'Coal Mining Effects', 'Industrial Runoff'],
                'disease_correlations': {'respiratory_infection': 0.8, 'tuberculosis': 0.6, 'gastroenteritis': 0.6}
            }
        }
    
    def _initialize_climate_disease_mapping(self) -> Dict[str, Dict]:
        """Climate conditions to disease risk mapping"""
        return {
            'cholera': {
                'high_temperature': 0.8,    # >32°C
                'heavy_monsoon': 0.9,       # >150mm in 7 days
                'flooding': 0.95,           # Flood conditions
                'high_humidity': 0.7,       # >85%
                'coastal_areas': 0.6,       # Coastal regions
                'poor_sanitation': 0.9      # Industrial pollution areas
            },
            'dengue': {
                'temperature_optimal': 0.85, # 26-30°C
                'post_monsoon': 0.8,        # Stagnant water
                'urban_density': 0.7,       # Urban heat islands
                'moderate_humidity': 0.75,   # 65-80%
                'construction_sites': 0.6    # Water accumulation
            },
            'typhoid': {
                'poor_sanitation': 0.9,
                'contaminated_water': 0.95,
                'summer_heat': 0.6,         # >35°C
                'industrial_pollution': 0.7,
                'overcrowding': 0.8
            },
            'hepatitis_a': {
                'contaminated_water': 0.9,
                'poor_hygiene': 0.8,
                'monsoon_contamination': 0.7,
                'industrial_waste': 0.6
            },
            'malaria': {
                'stagnant_water': 0.9,
                'monsoon_active': 0.8,
                'rural_areas': 0.7,
                'mining_areas': 0.6
            },
            'respiratory_infection': {
                'air_pollution': 0.9,
                'winter_months': 0.7,
                'dust_storms': 0.8,
                'industrial_emissions': 0.85
            }
        }
    
    def get_location_from_phone(self, phone_number: str) -> Optional[IndianLocationData]:
        """Extract location data from Indian phone number"""
        # Clean phone number
        phone = re.sub(r'[^\d+]', '', phone_number)
        
        # Try exact matches first
        for prefix, location in self.indian_phone_database.items():
            if phone.startswith(prefix):
                return location
        
        # Indian mobile number pattern matching
        if phone.startswith('+91') or phone.startswith('91'):
            # Remove country code
            if phone.startswith('+91'):
                mobile = phone[3:]
            else:
                mobile = phone[2:]
            
            # Mobile number series to state mapping
            series_mapping = {
                '9': 'Maharashtra',  # 9xxxxxxx series
                '8': 'Karnataka',    # 8xxxxxxx series  
                '7': 'Delhi',        # 7xxxxxxx series
                '6': 'West Bengal',  # 6xxxxxxx series
            }
            
            if len(mobile) >= 10 and mobile[0] in series_mapping:
                state = series_mapping[mobile[0]]
                # Return approximate location based on state
                for location in self.indian_phone_database.values():
                    if location.state == state:
                        return location
        
        # Default Indian location if no match
        return IndianLocationData('Delhi', 'Delhi', 'New Delhi', 28.6139, 77.2090, 'Delhi', 32900000,
                                 ['Mixed Industrial'], ['General Manufacturing'], 
                                 ['Groundwater'], 'Semi-Arid', 'Medium')
    
    def analyze_environmental_factors(self, location: IndianLocationData, symptoms: List[str]) -> Dict:
        """Analyze environmental factors that may contribute to symptoms"""
        city_key = location.city.lower()
        
        if city_key in self.industrial_pollution_data:
            pollution_data = self.industrial_pollution_data[city_key]
        else:
            # Default pollution data
            pollution_data = {
                'major_pollutants': ['General Industrial Waste'],
                'air_quality_index': 150,
                'water_contamination_level': 5.0,
                'nearby_factories': [],
                'environmental_risks': ['Industrial Activity'],
                'disease_correlations': {}
            }
        
        # Calculate environmental risk score
        environmental_risk = 0.0
        contributing_factors = []
        
        # Air quality impact
        aqi = pollution_data['air_quality_index']
        if aqi > 200:
            environmental_risk += 0.4
            contributing_factors.append(f"Severe air pollution (AQI: {aqi})")
        elif aqi > 100:
            environmental_risk += 0.2
            contributing_factors.append(f"Poor air quality (AQI: {aqi})")
        
        # Water contamination impact
        water_contamination = pollution_data['water_contamination_level']
        if water_contamination > 7.0:
            environmental_risk += 0.3
            contributing_factors.append(f"High water contamination ({water_contamination}/10)")
        elif water_contamination > 5.0:
            environmental_risk += 0.15
            contributing_factors.append(f"Moderate water contamination ({water_contamination}/10)")
        
        # Nearby factory impact
        factory_impact = 0.0
        for factory in pollution_data['nearby_factories']:
            if factory['distance_km'] <= 10.0:
                impact = max(0, (10.0 - factory['distance_km']) / 10.0) * 0.1
                factory_impact += impact
                if impact > 0.05:
                    contributing_factors.append(f"{factory['name']} at {factory['distance_km']}km")
        
        environmental_risk += factory_impact
        
        # Disease-specific correlations
        disease_risks = {}
        for symptom in symptoms:
            for disease, correlations in self.climate_disease_mapping.items():
                if symptom.lower() in disease.lower() or any(s in symptom.lower() for s in ['fever', 'diarrhea', 'cough', 'respiratory']):
                    if disease in pollution_data['disease_correlations']:
                        disease_risks[disease] = pollution_data['disease_correlations'][disease]
        
        return {
            'environmental_risk_score': min(1.0, environmental_risk),
            'air_quality_index': aqi,
            'water_contamination_level': water_contamination,
            'contributing_factors': contributing_factors,
            'disease_correlations': disease_risks,
            'major_pollutants': pollution_data['major_pollutants'],
            'nearby_industries': [f['name'] for f in pollution_data['nearby_factories'][:3]]
        }

# Global instance for easy import
enhanced_indian_analyzer = EnhancedIndianGeographicAnalyzer()