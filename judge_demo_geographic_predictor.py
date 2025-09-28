#!/usr/bin/env python3
"""
👨‍⚖️ Judge Demonstration: Geographic Climate-Based Outbreak Prediction
Real-time demonstration of RHAS v2.0's advanced geographic and climate analysis capabilities
"""

from flask import Flask, render_template_string, jsonify, request
from geographic_outbreak_predictor import geographic_predictor
import json
from datetime import datetime

# Judge demonstration scenarios based on real rural India health data
JUDGE_DEMO_SCENARIOS = [
    {
        'scenario_name': 'Mumbai Slum Cholera Risk Assessment',
        'description': 'High-risk cholera outbreak prediction for Mumbai slum areas during monsoon',
        'phone_number': '+919876543210',
        'location_data': {
            'city': 'Mumbai',
            'state': 'Maharashtra', 
            'district': 'Mumbai',
            'lat': 19.0760,
            'lon': 72.8777,
            'population': 12400000,
            'major_industries': ['Textiles', 'Pharmaceuticals', 'Chemicals', 'Petrochemicals'],
            'pollution_level': 'High',
            'industrial_zones': ['MIDC Andheri', 'Mahape Industrial Area', 'Taloja MIDC']
        },
        'climate_data': {
            'temperature': 34.5,
            'humidity': 89,
            'rainfall_7days': 185,
            'season': 'monsoon',
            'water_contamination': 8.7
        },
        'symptoms_pattern': ['diarrhea', 'vomiting', 'fever', 'dehydration'],
        'expected_outcome': 'CRITICAL cholera outbreak risk with comprehensive solution plan'
    },
    {
        'scenario_name': 'Delhi Vector-Borne Disease Prediction',
        'description': 'Dengue outbreak risk assessment for Delhi during post-monsoon period',
        'phone_number': '+911123456789',
        'location_data': {
            'city': 'Delhi',
            'state': 'Delhi',
            'district': 'New Delhi',
            'lat': 28.6139,
            'lon': 77.2090,
            'population': 32900000,
            'major_industries': ['Power Plants', 'Steel', 'Cement', 'E-waste Processing'],
            'pollution_level': 'Critical',
            'industrial_zones': ['Okhla Industrial Area', 'Mayapuri Industrial Area']
        },
        'climate_data': {
            'temperature': 29.2,
            'humidity': 72,
            'rainfall_7days': 55,
            'season': 'post_monsoon',
            'stagnant_water_index': 7.8
        },
        'symptoms_pattern': ['fever', 'headache', 'body_ache', 'rash'],
        'expected_outcome': 'HIGH dengue outbreak risk with vector control strategy'
    },
    {
        'scenario_name': 'Rural Chhattisgarh Malaria Hotspot',
        'description': 'Forest malaria outbreak prediction for tribal areas during monsoon',
        'phone_number': '+917712345678',
        'location_data': {
            'city': 'Bastar',
            'state': 'Chhattisgarh',
            'district': 'Bastar',
            'lat': 19.3289,
            'lon': 81.9614,
            'population': 140000,
            'major_industries': ['Mining', 'Forest Products'],
            'pollution_level': 'Medium',
            'industrial_zones': ['Mining Areas']
        },
        'climate_data': {
            'temperature': 31.8,
            'humidity': 82,
            'rainfall_7days': 165,
            'season': 'monsoon',
            'forest_water_bodies': 9.2
        },
        'symptoms_pattern': ['fever', 'chills', 'weakness', 'sweating'],
        'expected_outcome': 'HIGH malaria outbreak risk with tribal-specific intervention'
    },
    {
        'scenario_name': 'Coastal Odisha Cyclone Health Impact',
        'description': 'Post-cyclone waterborne disease outbreak prediction for coastal Odisha',
        'phone_number': '+916745678901',
        'location_data': {
            'city': 'Puri',
            'state': 'Odisha',
            'district': 'Puri',
            'lat': 19.8135,
            'lon': 85.8312,
            'population': 200000,
            'major_industries': ['Fishing', 'Tourism', 'Salt Production'],
            'pollution_level': 'High',
            'industrial_zones': ['Coastal Industrial Areas']
        },
        'climate_data': {
            'temperature': 35.2,
            'humidity': 92,
            'rainfall_7days': 245,
            'season': 'post_cyclone',
            'water_contamination': 9.5
        },
        'symptoms_pattern': ['diarrhea', 'vomiting', 'stomach_pain', 'fever'],
        'expected_outcome': 'CRITICAL cholera outbreak risk with emergency response plan'
    }
]

def create_judge_demo_template():
    """Create comprehensive judge demonstration template"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>🏥 RHAS v2.0 - Geographic Outbreak Prediction Demo</title>
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
            text-align: center;
        }
        
        .header h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .header p {
            color: #666;
            font-size: 1.2em;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 30px 20px;
        }
        
        .scenarios-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .scenario-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .scenario-card:hover {
            transform: translateY(-5px);
        }
        
        .scenario-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
        }
        
        .scenario-icon {
            font-size: 2em;
            margin-right: 15px;
        }
        
        .scenario-title {
            color: #667eea;
            font-size: 1.3em;
            font-weight: bold;
        }
        
        .scenario-description {
            color: #666;
            margin-bottom: 20px;
            font-style: italic;
        }
        
        .demo-button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            transition: all 0.3s ease;
            width: 100%;
        }
        
        .demo-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102,126,234,0.3);
        }
        
        .prediction-results {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            margin-top: 30px;
            display: none;
        }
        
        .results-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .risk-level {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 25px;
            color: white;
            font-weight: bold;
            font-size: 1.2em;
            margin: 10px;
        }
        
        .risk-critical { background: #e74c3c; }
        .risk-high { background: #e67e22; }
        .risk-medium { background: #f39c12; }
        .risk-low { background: #27ae60; }
        
        .results-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 25px;
        }
        
        .result-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }
        
        .result-section h3 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .result-list {
            list-style: none;
        }
        
        .result-list li {
            padding: 8px 0;
            border-bottom: 1px solid #dee2e6;
        }
        
        .result-list li:last-child {
            border-bottom: none;
        }
        
        .solution-plan {
            background: #e8f5e8;
            border-left: 4px solid #28a745;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .environmental-factors {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .climate-triggers {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        
        .judge-notes {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
            border: 3px solid #667eea;
        }
        
        .judge-notes h2 {
            color: #667eea;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .feature-item {
            display: flex;
            align-items: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
        }
        
        .feature-icon {
            font-size: 1.5em;
            margin-right: 15px;
        }
        
        .loading {
            text-align: center;
            padding: 20px;
            font-size: 1.2em;
            color: #667eea;
        }
        
        @media (max-width: 768px) {
            .scenarios-grid {
                grid-template-columns: 1fr;
            }
            .results-grid {
                grid-template-columns: 1fr;
            }
            .features-list {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏥 RHAS v2.0 Geographic Outbreak Predictor</h1>
        <p>🌍 Real-time climate and geographic analysis for epidemic prediction</p>
        <p><strong>Based on WHO, ICMR, and Rural Health NGO datasets from actual Indian outbreaks</strong></p>
    </div>
    
    <div class="container">
        <div class="scenarios-grid">
            {% for scenario in scenarios %}
            <div class="scenario-card">
                <div class="scenario-header">
                    <div class="scenario-icon">
                        {% if 'Cholera' in scenario.scenario_name %}🦠
                        {% elif 'Dengue' in scenario.scenario_name %}🦟
                        {% elif 'Malaria' in scenario.scenario_name %}🩸
                        {% elif 'Cyclone' in scenario.scenario_name %}🌪️
                        {% else %}🏥{% endif %}
                    </div>
                    <div class="scenario-title">{{ scenario.scenario_name }}</div>
                </div>
                <div class="scenario-description">
                    {{ scenario.description }}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>📍 Location:</strong> {{ scenario.location_data.city }}, {{ scenario.location_data.state }}<br>
                    <strong>👥 Population:</strong> {{ "{:,}".format(scenario.location_data.population) }}<br>
                    <strong>🌡️ Temperature:</strong> {{ scenario.climate_data.temperature }}°C | <strong>💧 Humidity:</strong> {{ scenario.climate_data.humidity }}%<br>
                    <strong>🌧️ Rainfall (7 days):</strong> {{ scenario.climate_data.rainfall_7days }}mm | <strong>🌍 Season:</strong> {{ scenario.climate_data.season.title() }}<br>
                    <strong>🏭 Industrial Zones:</strong> {{ ", ".join(scenario.location_data.industrial_zones[:2]) }}...<br>
                    <strong>🌿 Pollution Level:</strong> <span style="color: {% if scenario.location_data.pollution_level == 'Critical' %}#e74c3c{% elif scenario.location_data.pollution_level == 'High' %}#e67e22{% else %}#f39c12{% endif %}">{{ scenario.location_data.pollution_level }}</span>
                </div>
                
                <div style="background: #f8f9fa; padding: 10px; border-radius: 8px; margin-bottom: 15px; font-size: 0.9em;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div><strong>🏭 Industries:</strong><br>{{ ", ".join(scenario.location_data.major_industries[:2]) }}</div>
                        <div><strong>🎯 Risk Indicators:</strong><br>
                        {% if 'water_contamination' in scenario.climate_data %}<span style="color: #e74c3c;">Water: {{ scenario.climate_data.water_contamination }}/10</span>{% endif %}
                        {% if 'stagnant_water_index' in scenario.climate_data %}<span style="color: #e67e22;">Stagnant Water: {{ scenario.climate_data.stagnant_water_index }}/10</span>{% endif %}
                        {% if 'forest_water_bodies' in scenario.climate_data %}<span style="color: #27ae60;">Forest Bodies: {{ scenario.climate_data.forest_water_bodies }}/10</span>{% endif %}
                        </div>
                    </div>
                </div>
                <button class="demo-button" onclick="runPrediction('{{ loop.index0 }}')">
                    🔍 Run Prediction Analysis
                </button>
            </div>
            {% endfor %}
        </div>
        
        <div id="prediction-results" class="prediction-results">
            <div class="loading" id="loading">
                🔄 Analyzing geographic and climate data...
            </div>
            <div id="results-content" style="display: none;"></div>
        </div>
        
        <div class="judge-notes">
            <h2>👨‍⚖️ Key Features for Judges</h2>
            <div class="features-list">
                <div class="feature-item">
                    <div class="feature-icon">🌍</div>
                    <div>Real geographic data integration with industrial zones and climate patterns</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📊</div>
                    <div>Historical outbreak data from WHO and ICMR studies (2018-2021)</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🎯</div>
                    <div>Climate-disease correlation analysis with temperature, humidity, and rainfall</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🚨</div>
                    <div>Risk level assessment (Low/Medium/High/Critical) with confidence scoring</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">📋</div>
                    <div>Comprehensive solution plans based on NRHM and WHO guidelines</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">⏰</div>
                    <div>Response timeline calculation and resource deployment planning</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">👥</div>
                    <div>Population impact estimation with affected area mapping</div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔬</div>
                    <div>Environmental factor analysis including pollution and water contamination</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        function runPrediction(scenarioIndex) {
            const resultsDiv = document.getElementById('prediction-results');
            const loadingDiv = document.getElementById('loading');
            const resultsContent = document.getElementById('results-content');
            
            resultsDiv.style.display = 'block';
            loadingDiv.style.display = 'block';
            resultsContent.style.display = 'none';
            
            // Scroll to results
            resultsDiv.scrollIntoView({ behavior: 'smooth' });
            
            fetch('/judge-demo/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ scenario_index: scenarioIndex })
            })
            .then(response => response.json())
            .then(data => {
                displayResults(data);
                loadingDiv.style.display = 'none';
                resultsContent.style.display = 'block';
            })
            .catch(error => {
                console.error('Error:', error);
                loadingDiv.innerHTML = '❌ Error running prediction analysis';
            });
        }
        
        function displayResults(data) {
            const resultsContent = document.getElementById('results-content');
            const riskClass = `risk-${data.risk_level.toLowerCase()}`;
            
            resultsContent.innerHTML = `
                <div class="results-header">
                    <h2>🔍 Outbreak Prediction Results</h2>
                    <div class="risk-level ${riskClass}">${data.risk_level} RISK</div>
                    <div style="margin-top: 10px;">
                        <strong>Predicted Disease:</strong> ${data.predicted_disease.replace('_', ' ').toUpperCase()}<br>
                        <strong>Confidence:</strong> ${Math.round(data.confidence * 100)}%<br>
                        <strong>Location:</strong> ${data.location}, ${data.state}<br>
                        <strong>Estimated Affected:</strong> ${data.affected_population_estimate.toLocaleString()} people<br>
                        <strong>Response Timeline:</strong> ${data.timeline}
                    </div>
                </div>
                
                <div class="results-grid">
                    <div class="result-section environmental-factors">
                        <h3>🌍 Environmental Risk Factors</h3>
                        <ul class="result-list">
                            ${data.environmental_factors.map(factor => `<li>• ${factor}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="result-section climate-triggers">
                        <h3>🌡️ Climate Triggers</h3>
                        <ul class="result-list">
                            ${data.climate_triggers.map(trigger => `<li>• ${trigger}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="result-section">
                        <h3>⚡ Immediate Actions</h3>
                        <ul class="result-list">
                            ${data.solution_plan.immediate_actions.slice(0, 4).map(action => `<li>• ${action}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="result-section">
                        <h3>🛡️ Prevention Measures</h3>
                        <ul class="result-list">
                            ${data.solution_plan.prevention_measures.slice(0, 4).map(measure => `<li>• ${measure}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="result-section">
                        <h3>🚑 Resource Deployment</h3>
                        <ul class="result-list">
                            ${data.solution_plan.resource_deployment.slice(0, 4).map(resource => `<li>• ${resource}</li>`).join('')}
                        </ul>
                    </div>
                    
                    <div class="result-section">
                        <h3>📊 Monitoring Protocol</h3>
                        <ul class="result-list">
                            ${data.solution_plan.monitoring_protocol.slice(0, 4).map(protocol => `<li>• ${protocol}</li>`).join('')}
                        </ul>
                    </div>
                </div>
                
                <div class="solution-plan">
                    <h3>📋 Complete Solution Plan Generated</h3>
                    <p><strong>This comprehensive outbreak prediction demonstrates RHAS v2.0's ability to:</strong></p>
                    <ul style="margin-left: 20px; margin-top: 10px;">
                        <li>✅ Analyze real geographic and climate data from rural India</li>
                        <li>✅ Correlate environmental factors with disease outbreak patterns</li>
                        <li>✅ Generate evidence-based solution plans following WHO/NRHM guidelines</li>
                        <li>✅ Provide accurate population impact estimates and response timelines</li>
                        <li>✅ Support public health decision-making with actionable intelligence</li>
                    </ul>
                </div>
            `;
        }
    </script>
</body>
</html>
    '''

# Create the judge demonstration app route
def create_judge_demo_route(app):
    """Add judge demonstration routes to existing Flask app"""
    
    @app.route('/judge-demo')
    def judge_demo():
        """Judge demonstration page for geographic outbreak prediction"""
        template = create_judge_demo_template()
        return render_template_string(template, scenarios=JUDGE_DEMO_SCENARIOS)
    
    @app.route('/judge-demo/predict', methods=['POST'])
    def judge_predict():
        """API endpoint for running prediction analysis"""
        try:
            data = request.get_json()
            scenario_index = int(data.get('scenario_index', 0))
            
            if 0 <= scenario_index < len(JUDGE_DEMO_SCENARIOS):
                scenario = JUDGE_DEMO_SCENARIOS[scenario_index]
                
                # Run prediction analysis
                prediction = geographic_predictor.predict_outbreak_risk(
                    scenario['location_data'],
                    scenario['climate_data'], 
                    scenario['symptoms_pattern']
                )
                
                # Convert to JSON-serializable format
                result = {
                    'location': prediction.location,
                    'state': prediction.state,
                    'district': prediction.district,
                    'predicted_disease': prediction.predicted_disease,
                    'risk_level': prediction.risk_level,
                    'confidence': prediction.confidence,
                    'environmental_factors': prediction.environmental_factors,
                    'climate_triggers': prediction.climate_triggers,
                    'solution_plan': prediction.solution_plan,
                    'timeline': prediction.timeline,
                    'affected_population_estimate': prediction.affected_population_estimate,
                    'prevention_measures': prediction.prevention_measures
                }
                
                return jsonify(result)
            else:
                return jsonify({'error': 'Invalid scenario index'}), 400
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For testing purposes
    app = Flask(__name__)
    create_judge_demo_route(app)
    app.run(debug=True, port=5001)