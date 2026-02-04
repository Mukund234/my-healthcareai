"""
WHO-aligned risk calculation rules for health conditions.
Based on WHO guidelines and validated health metrics.
"""

def calculate_bmi(weight_kg, height_cm):
    """Calculate Body Mass Index"""
    height_m = height_cm / 100
    return weight_kg / (height_m ** 2)

def get_bmi_category(bmi):
    """Categorize BMI according to WHO standards"""
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 25:
        return "normal"
    elif 25 <= bmi < 30:
        return "overweight"
    else:
        return "obese"

def calculate_obesity_risk(assessment_data):
    """
    Calculate obesity risk based on WHO guidelines
    Returns: risk_score (0-1), severity (low/moderate/high)
    """
    bmi = calculate_bmi(assessment_data['weight_kg'], assessment_data['height_cm'])
    age = assessment_data['age']
    activity_level = assessment_data.get('activity_level', 'sedentary')
    
    risk_score = 0.0
    
    # BMI contribution
    if bmi >= 30:
        risk_score += 0.6
    elif bmi >= 25:
        risk_score += 0.3
    elif bmi < 18.5:
        risk_score += 0.2
    
    # Activity level contribution
    activity_scores = {
        'sedentary': 0.3,
        'light': 0.2,
        'moderate': 0.1,
        'active': 0.0,
        'very_active': 0.0
    }
    risk_score += activity_scores.get(activity_level, 0.2)
    
    # Age adjustment
    if age > 40:
        risk_score += 0.1
    
    # Cap at 1.0
    risk_score = min(risk_score, 1.0)
    
    # Determine severity
    if risk_score >= 0.7:
        severity = "high"
    elif risk_score >= 0.4:
        severity = "moderate"
    else:
        severity = "low"
    
    return risk_score, severity

def calculate_diabetes_risk(assessment_data):
    """
    Calculate diabetes risk based on WHO/ADA guidelines
    Returns: risk_score (0-1), severity (low/moderate/high)
    """
    bmi = calculate_bmi(assessment_data['weight_kg'], assessment_data['height_cm'])
    age = assessment_data['age']
    family_history = assessment_data.get('family_history', {})
    activity_level = assessment_data.get('activity_level', 'sedentary')
    
    risk_score = 0.0
    
    # Age factor
    if age >= 45:
        risk_score += 0.2
    elif age >= 35:
        risk_score += 0.1
    
    # BMI factor
    if bmi >= 30:
        risk_score += 0.3
    elif bmi >= 25:
        risk_score += 0.2
    
    # Family history
    if family_history.get('diabetes', False):
        risk_score += 0.3
    
    # Physical activity
    if activity_level in ['sedentary', 'light']:
        risk_score += 0.2
    
    # Cap at 1.0
    risk_score = min(risk_score, 1.0)
    
    # Determine severity
    if risk_score >= 0.7:
        severity = "high"
    elif risk_score >= 0.4:
        severity = "moderate"
    else:
        severity = "low"
    
    return risk_score, severity

def calculate_hypertension_risk(assessment_data):
    """
    Calculate hypertension risk based on WHO guidelines
    Returns: risk_score (0-1), severity (low/moderate/high)
    """
    age = assessment_data['age']
    bmi = calculate_bmi(assessment_data['weight_kg'], assessment_data['height_cm'])
    family_history = assessment_data.get('family_history', {})
    stress_level = assessment_data.get('stress_level', 5)
    smoking = assessment_data.get('smoking', False)
    alcohol = assessment_data.get('alcohol_consumption', 'none')
    bp_systolic = assessment_data.get('blood_pressure_systolic')
    
    risk_score = 0.0
    
    # Age factor
    if age >= 55:
        risk_score += 0.2
    elif age >= 45:
        risk_score += 0.15
    
    # BMI factor
    if bmi >= 30:
        risk_score += 0.25
    elif bmi >= 25:
        risk_score += 0.15
    
    # Family history
    if family_history.get('hypertension', False):
        risk_score += 0.2
    
    # Lifestyle factors
    if smoking:
        risk_score += 0.15
    
    if alcohol in ['moderate', 'heavy']:
        risk_score += 0.1
    
    # Stress
    if stress_level >= 7:
        risk_score += 0.15
    elif stress_level >= 5:
        risk_score += 0.1
    
    # Blood pressure if available
    if bp_systolic:
        if bp_systolic >= 140:
            risk_score += 0.4
        elif bp_systolic >= 130:
            risk_score += 0.2
    
    # Cap at 1.0
    risk_score = min(risk_score, 1.0)
    
    # Determine severity
    if risk_score >= 0.7:
        severity = "high"
    elif risk_score >= 0.4:
        severity = "moderate"
    else:
        severity = "low"
    
    return risk_score, severity

def calculate_cardiovascular_risk(assessment_data):
    """
    Calculate cardiovascular disease risk
    Returns: risk_score (0-1), severity (low/moderate/high)
    """
    age = assessment_data['age']
    gender = assessment_data['gender']
    bmi = calculate_bmi(assessment_data['weight_kg'], assessment_data['height_cm'])
    smoking = assessment_data.get('smoking', False)
    activity_level = assessment_data.get('activity_level', 'sedentary')
    family_history = assessment_data.get('family_history', {})
    
    risk_score = 0.0
    
    # Age and gender
    if gender == 'male':
        if age >= 45:
            risk_score += 0.2
    else:  # female
        if age >= 55:
            risk_score += 0.2
    
    # BMI
    if bmi >= 30:
        risk_score += 0.2
    
    # Smoking - major risk factor
    if smoking:
        risk_score += 0.3
    
    # Physical inactivity
    if activity_level in ['sedentary', 'light']:
        risk_score += 0.2
    
    # Family history
    if family_history.get('heart_disease', False):
        risk_score += 0.25
    
    # Cap at 1.0
    risk_score = min(risk_score, 1.0)
    
    # Determine severity
    if risk_score >= 0.7:
        severity = "high"
    elif risk_score >= 0.4:
        severity = "moderate"
    else:
        severity = "low"
    
    return risk_score, severity

def calculate_stress_burnout_risk(assessment_data):
    """
    Calculate stress and burnout risk
    Returns: risk_score (0-1), severity (low/moderate/high)
    """
    stress_level = assessment_data.get('stress_level', 5)
    sleep_hours = assessment_data.get('sleep_hours', 7)
    activity_level = assessment_data.get('activity_level', 'moderate')
    
    risk_score = 0.0
    
    # Stress level (1-10 scale)
    if stress_level >= 8:
        risk_score += 0.5
    elif stress_level >= 6:
        risk_score += 0.3
    elif stress_level >= 4:
        risk_score += 0.1
    
    # Sleep deprivation
    if sleep_hours < 6:
        risk_score += 0.3
    elif sleep_hours < 7:
        risk_score += 0.15
    elif sleep_hours > 9:
        risk_score += 0.1
    
    # Physical activity helps reduce stress
    if activity_level == 'sedentary':
        risk_score += 0.2
    
    # Cap at 1.0
    risk_score = min(risk_score, 1.0)
    
    # Determine severity
    if risk_score >= 0.7:
        severity = "high"
    elif risk_score >= 0.4:
        severity = "moderate"
    else:
        severity = "low"
    
    return risk_score, severity
