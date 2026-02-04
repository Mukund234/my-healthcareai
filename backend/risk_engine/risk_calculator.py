"""
Main risk calculation orchestrator.
Combines WHO rules and ML predictions with weighted scoring.
"""

from risk_engine.who_rules import (
    calculate_obesity_risk,
    calculate_diabetes_risk,
    calculate_hypertension_risk,
    calculate_cardiovascular_risk,
    calculate_stress_burnout_risk
)
from risk_engine.age_groups import (
    adjust_risk_for_age_group,
    get_age_specific_recommendations,
    should_trigger_doctor_consult
)

class RiskCalculator:
    def __init__(self, use_ml=False):
        """
        Initialize risk calculator
        use_ml: Whether to use ML models (requires trained models)
        """
        self.use_ml = use_ml
        self.ml_models = None
        
        if use_ml:
            try:
                from risk_engine.ml_models import load_models
                self.ml_models = load_models()
            except Exception as e:
                print(f"Warning: Could not load ML models: {e}")
                self.use_ml = False
    
    def calculate_all_risks(self, assessment_data):
        """
        Calculate all health risks for given assessment data
        Returns: dict with risk scores, severities, and recommendations
        """
        # Calculate WHO-based risks
        obesity_risk, obesity_sev = calculate_obesity_risk(assessment_data)
        diabetes_risk, diabetes_sev = calculate_diabetes_risk(assessment_data)
        hypertension_risk, hypertension_sev = calculate_hypertension_risk(assessment_data)
        cardiovascular_risk, cardiovascular_sev = calculate_cardiovascular_risk(assessment_data)
        stress_risk, stress_sev = calculate_stress_burnout_risk(assessment_data)
        
        # Store in dict
        risk_scores = {
            'obesity_risk': obesity_risk,
            'diabetes_risk': diabetes_risk,
            'hypertension_risk': hypertension_risk,
            'cardiovascular_risk': cardiovascular_risk,
            'stress_burnout_risk': stress_risk
        }
        
        severity_levels = {
            'obesity_severity': obesity_sev,
            'diabetes_severity': diabetes_sev,
            'hypertension_severity': hypertension_sev,
            'cardiovascular_severity': cardiovascular_sev,
            'stress_severity': stress_sev
        }
        
        # Adjust for age group
        age = assessment_data['age']
        adjusted_scores = adjust_risk_for_age_group(risk_scores, age)
        
        # Recalculate severities after adjustment
        for risk_type, score in adjusted_scores.items():
            sev_key = risk_type.replace('_risk', '_severity')
            if score >= 0.7:
                severity_levels[sev_key] = 'high'
            elif score >= 0.4:
                severity_levels[sev_key] = 'moderate'
            else:
                severity_levels[sev_key] = 'low'
        
        # Calculate overall risk
        overall_risk = sum(adjusted_scores.values()) / len(adjusted_scores)
        
        if overall_risk >= 0.7:
            overall_severity = 'high'
        elif overall_risk >= 0.4:
            overall_severity = 'moderate'
        else:
            overall_severity = 'low'
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            age, adjusted_scores, severity_levels
        )
        
        # Determine doctor consult need
        doctor_consult = should_trigger_doctor_consult(
            age, adjusted_scores, severity_levels
        )
        
        return {
            'risk_scores': adjusted_scores,
            'severity_levels': severity_levels,
            'overall_risk_score': overall_risk,
            'overall_severity': overall_severity,
            'recommendations': recommendations,
            'doctor_consult_needed': doctor_consult,
            'calculation_method': 'who_rules' if not self.use_ml else 'hybrid'
        }
    
    def _generate_recommendations(self, age, risk_scores, severity_levels):
        """Generate personalized recommendations based on risks"""
        recommendations = []
        
        # Get recommendations for each high/moderate risk
        for risk_type, severity_key in [
            ('obesity_risk', 'obesity_severity'),
            ('diabetes_risk', 'diabetes_severity'),
            ('hypertension_risk', 'hypertension_severity'),
            ('cardiovascular_risk', 'cardiovascular_severity'),
            ('stress_burnout_risk', 'stress_severity')
        ]:
            severity = severity_levels.get(severity_key, 'low')
            
            if severity in ['high', 'moderate']:
                age_recs = get_age_specific_recommendations(age, risk_type, severity)
                recommendations.extend(age_recs)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in recommendations:
            if rec not in seen:
                seen.add(rec)
                unique_recs.append(rec)
        
        # Limit to top 8 recommendations
        return unique_recs[:8]
