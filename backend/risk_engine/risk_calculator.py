"""
Main risk calculation orchestrator.
Combines WHO rules and ML predictions with weighted scoring.
"""
from typing import Dict, List, Tuple

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
        who_scores, severity_levels = self._calculate_who_risks(assessment_data)
        age = assessment_data['age']
        adjusted_scores = adjust_risk_for_age_group(who_scores, age)

        ml_scores = self._calculate_ml_risks(assessment_data) if self.use_ml and self.ml_models else {}

        # Hybrid scoring: prioritize WHO rules and blend ML where available.
        final_scores = {}
        for risk_type, who_score in adjusted_scores.items():
            condition = risk_type.replace('_risk', '')
            ml_score = ml_scores.get(condition)
            if ml_score is not None:
                final_scores[risk_type] = min(1.0, (0.65 * who_score) + (0.35 * ml_score))
            else:
                final_scores[risk_type] = who_score

        for risk_type, score in final_scores.items():
            sev_key = risk_type.replace('_risk', '_severity')
            severity_levels[sev_key] = self._severity_from_score(score)

        overall_risk = sum(final_scores.values()) / len(final_scores)
        overall_severity = self._severity_from_score(overall_risk)

        recommendations = self._generate_recommendations(
            age, final_scores, severity_levels
        )

        doctor_consult = should_trigger_doctor_consult(
            age, final_scores, severity_levels
        )

        risk_explanations = self._build_risk_explanations(
            assessment_data,
            final_scores,
            severity_levels
        )
        triage = self._build_triage(assessment_data, overall_risk, overall_severity, doctor_consult)
        
        return {
            'risk_scores': final_scores,
            'severity_levels': severity_levels,
            'overall_risk_score': overall_risk,
            'overall_severity': overall_severity,
            'recommendations': recommendations,
            'doctor_consult_needed': doctor_consult,
            'calculation_method': 'hybrid' if ml_scores else 'who_rules',
            'risk_explanations': risk_explanations,
            'triage': triage
        }

    def _calculate_who_risks(self, assessment_data: Dict) -> Tuple[Dict[str, float], Dict[str, str]]:
        obesity_risk, obesity_sev = calculate_obesity_risk(assessment_data)
        diabetes_risk, diabetes_sev = calculate_diabetes_risk(assessment_data)
        hypertension_risk, hypertension_sev = calculate_hypertension_risk(assessment_data)
        cardiovascular_risk, cardiovascular_sev = calculate_cardiovascular_risk(assessment_data)
        stress_risk, stress_sev = calculate_stress_burnout_risk(assessment_data)

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
        return risk_scores, severity_levels

    def _calculate_ml_risks(self, assessment_data: Dict) -> Dict[str, float]:
        condition_map = {
            'diabetes': 'diabetes',
            'hypertension': 'hypertension',
            'cardiovascular': 'cardiovascular'
        }
        ml_scores = {}
        for output_key, model_key in condition_map.items():
            score = self.ml_models.predict_risk(assessment_data, model_key)
            if score is not None:
                ml_scores[output_key] = float(score)
        return ml_scores

    def _severity_from_score(self, score: float) -> str:
        if score >= 0.7:
            return 'high'
        if score >= 0.4:
            return 'moderate'
        return 'low'

    def _build_risk_explanations(
        self,
        assessment_data: Dict,
        risk_scores: Dict[str, float],
        severity_levels: Dict[str, str]
    ) -> List[Dict]:
        bmi = assessment_data.get('weight_kg') and assessment_data.get('height_cm')
        bmi_value = None
        if bmi:
            bmi_value = assessment_data['weight_kg'] / ((assessment_data['height_cm'] / 100) ** 2)

        explanations = []
        for risk_type, score in risk_scores.items():
            severity_key = risk_type.replace('_risk', '_severity')
            main_factors = []
            if assessment_data.get('age', 0) >= 45:
                main_factors.append("age_above_45")
            if bmi_value is not None and bmi_value >= 25:
                main_factors.append("high_bmi")
            if assessment_data.get('smoking'):
                main_factors.append("smoking")
            if assessment_data.get('stress_level', 0) >= 7:
                main_factors.append("high_stress")
            if assessment_data.get('activity_level') in ['sedentary', 'light']:
                main_factors.append("low_activity")
            if assessment_data.get('family_history'):
                main_factors.append("family_history")

            explanations.append({
                "condition": risk_type.replace('_risk', ''),
                "risk_score": round(score, 3),
                "severity": severity_levels.get(severity_key, "low"),
                "main_factors": main_factors[:4]
            })
        return explanations

    def _build_triage(
        self,
        assessment_data: Dict,
        overall_risk: float,
        overall_severity: str,
        doctor_consult: str
    ) -> Dict:
        symptoms_raw = assessment_data.get("symptoms", [])
        if isinstance(symptoms_raw, str):
            symptoms_text = symptoms_raw.lower()
        else:
            symptoms_text = " ".join(symptoms_raw).lower()

        emergency_keywords = ["chest pain", "shortness of breath", "fainting", "stroke", "seizure"]
        emergency_detected = any(keyword in symptoms_text for keyword in emergency_keywords)

        if emergency_detected or overall_risk >= 0.85:
            risk_level = "Emergency"
            urgency = "Immediate emergency care"
            next_steps = [
                "Call local emergency services now.",
                "Do not delay for online consultation.",
                "Keep someone with the patient while waiting for help."
            ]
        elif overall_severity == "high" or doctor_consult == "urgent":
            risk_level = "High"
            urgency = "Same day clinical evaluation"
            next_steps = [
                "Visit the nearest doctor or clinic today.",
                "Share this risk summary with the provider.",
                "Monitor symptoms and seek emergency care if they worsen."
            ]
        elif overall_severity == "moderate":
            risk_level = "Medium"
            urgency = "Consult within 1-3 days"
            next_steps = [
                "Book a clinic consultation soon.",
                "Start lifestyle adjustments from recommendations.",
                "Reassess if new symptoms appear."
            ]
        else:
            risk_level = "Low"
            urgency = "Routine self-care"
            next_steps = [
                "Continue healthy habits and hydration.",
                "Track symptoms for changes.",
                "Repeat assessment in 2-4 weeks."
            ]

        return {
            "risk_level": risk_level,
            "urgency": urgency,
            "next_steps": next_steps,
            "warning_signs": [
                "severe chest pain",
                "trouble breathing",
                "confusion or fainting",
                "sudden weakness on one side"
            ],
            "disclaimer": "This tool is a screening aid and not a medical diagnosis."
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
