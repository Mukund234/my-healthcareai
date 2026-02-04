"""
Age-group specific risk logic and thresholds.
Different age groups have different risk factors and thresholds.
"""

class AgeGroup:
    CHILD = "child"  # 0-17
    ADULT = "adult"  # 18-64
    SENIOR = "senior"  # 65+

def get_age_group(age):
    """Determine age group from age"""
    if age < 18:
        return AgeGroup.CHILD
    elif age < 65:
        return AgeGroup.ADULT
    else:
        return AgeGroup.SENIOR

def adjust_risk_for_age_group(risk_scores, age):
    """
    Adjust risk scores based on age group
    Different conditions have different prevalence in different age groups
    """
    age_group = get_age_group(age)
    adjusted_scores = risk_scores.copy()
    
    if age_group == AgeGroup.CHILD:
        # Children: Focus on growth, nutrition, stress (academic)
        # Lower diabetes/cardiovascular risk naturally
        adjusted_scores['diabetes_risk'] *= 0.5
        adjusted_scores['cardiovascular_risk'] *= 0.3
        adjusted_scores['hypertension_risk'] *= 0.6
        # Stress from academics can be high
        adjusted_scores['stress_burnout_risk'] *= 1.2
        
    elif age_group == AgeGroup.SENIOR:
        # Seniors: Higher baseline risk for most conditions
        adjusted_scores['diabetes_risk'] *= 1.3
        adjusted_scores['cardiovascular_risk'] *= 1.5
        adjusted_scores['hypertension_risk'] *= 1.4
        
    # Cap all scores at 1.0
    for key in adjusted_scores:
        adjusted_scores[key] = min(adjusted_scores[key], 1.0)
    
    return adjusted_scores

def get_age_specific_recommendations(age, risk_type, severity):
    """
    Get age-appropriate recommendations
    """
    age_group = get_age_group(age)
    
    recommendations = {
        'child': {
            'obesity': [
                "Encourage 60 minutes of active play daily",
                "Limit screen time to 2 hours per day",
                "Ensure balanced meals with fruits and vegetables",
                "Involve family in physical activities"
            ],
            'stress_burnout': [
                "Ensure 9-11 hours of sleep per night",
                "Balance study time with play and relaxation",
                "Encourage talking about feelings with parents/counselors",
                "Limit academic pressure and extracurricular overload"
            ],
            'diabetes': [
                "Maintain healthy weight through balanced diet",
                "Reduce sugary drinks and snacks",
                "Regular physical activity and outdoor play",
                "Consult pediatrician for family history concerns"
            ]
        },
        'adult': {
            'obesity': [
                "Aim for 150 minutes of moderate exercise weekly",
                "Adopt a balanced diet with portion control",
                "Track daily calorie intake",
                "Consider consulting a nutritionist"
            ],
            'diabetes': [
                "Monitor blood sugar if family history exists",
                "Reduce refined carbohydrates and sugar intake",
                "Maintain healthy BMI (18.5-24.9)",
                "Get annual health checkups"
            ],
            'hypertension': [
                "Reduce sodium intake to <2300mg/day",
                "Exercise regularly (30 min/day, 5 days/week)",
                "Manage stress through meditation or yoga",
                "Limit alcohol consumption"
            ],
            'cardiovascular': [
                "Quit smoking immediately if applicable",
                "Eat heart-healthy foods (omega-3, fiber)",
                "Monitor cholesterol levels annually",
                "Maintain healthy blood pressure"
            ],
            'stress_burnout': [
                "Ensure 7-9 hours of quality sleep",
                "Practice stress management techniques",
                "Take regular breaks from work",
                "Consider professional counseling if needed"
            ]
        },
        'senior': {
            'diabetes': [
                "Regular blood sugar monitoring",
                "Follow prescribed medication schedule",
                "Gentle exercise like walking 20-30 min daily",
                "Regular doctor visits every 3-6 months"
            ],
            'hypertension': [
                "Daily blood pressure monitoring",
                "Low-sodium diet strictly",
                "Medication compliance",
                "Regular cardiology checkups"
            ],
            'cardiovascular': [
                "Cardiac health monitoring",
                "Avoid strenuous activities without doctor approval",
                "Heart-healthy Mediterranean diet",
                "Regular ECG and stress tests"
            ],
            'obesity': [
                "Gentle, low-impact exercises (swimming, walking)",
                "Nutritionist-guided meal planning",
                "Monitor for joint issues",
                "Focus on maintaining rather than rapid weight loss"
            ]
        }
    }
    
    # Map risk types to recommendation keys
    risk_map = {
        'obesity_risk': 'obesity',
        'diabetes_risk': 'diabetes',
        'hypertension_risk': 'hypertension',
        'cardiovascular_risk': 'cardiovascular',
        'stress_burnout_risk': 'stress_burnout'
    }
    
    rec_key = risk_map.get(risk_type, 'obesity')
    
    if age_group in recommendations and rec_key in recommendations[age_group]:
        return recommendations[age_group][rec_key]
    
    # Fallback to adult recommendations
    if rec_key in recommendations['adult']:
        return recommendations['adult'][rec_key]
    
    return ["Consult a healthcare provider for personalized advice"]

def should_trigger_doctor_consult(age, risk_scores, severity_levels):
    """
    Determine if doctor consultation should be recommended
    Returns: 'none', 'suggested', 'urgent'
    """
    age_group = get_age_group(age)
    
    # Count high-risk conditions
    high_risk_count = sum(1 for sev in severity_levels.values() if sev == 'high')
    moderate_risk_count = sum(1 for sev in severity_levels.values() if sev == 'moderate')
    
    # Urgent cases
    if high_risk_count >= 2:
        return 'urgent'
    
    if age_group == AgeGroup.SENIOR and high_risk_count >= 1:
        return 'urgent'
    
    # Suggested cases
    if high_risk_count >= 1:
        return 'suggested'
    
    if moderate_risk_count >= 3:
        return 'suggested'
    
    if age_group == AgeGroup.CHILD and moderate_risk_count >= 2:
        return 'suggested'
    
    return 'none'
