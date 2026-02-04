"""
Machine Learning models for risk prediction.
Placeholder implementation - can be enhanced with actual trained models.
"""

import os
import joblib
import numpy as np
from config import settings

class MLRiskPredictor:
    def __init__(self):
        self.models = {}
        self.feature_names = [
            'age', 'bmi', 'activity_score', 'sleep_hours', 
            'stress_level', 'smoking', 'family_history_score'
        ]
    
    def load_models(self):
        """Load pre-trained models from disk"""
        model_files = {
            'diabetes': 'diabetes_model.pkl',
            'hypertension': 'hypertension_model.pkl',
            'cardiovascular': 'cardiovascular_model.pkl'
        }
        
        for condition, filename in model_files.items():
            model_path = os.path.join(settings.MODELS_DIR, filename)
            if os.path.exists(model_path):
                try:
                    self.models[condition] = joblib.load(model_path)
                except Exception as e:
                    print(f"Could not load {condition} model: {e}")
    
    def prepare_features(self, assessment_data):
        """
        Extract and engineer features from assessment data
        """
        from risk_engine.who_rules import calculate_bmi
        
        # Calculate BMI
        bmi = calculate_bmi(assessment_data['weight_kg'], assessment_data['height_cm'])
        
        # Activity level to numeric score
        activity_map = {
            'sedentary': 1,
            'light': 2,
            'moderate': 3,
            'active': 4,
            'very_active': 5
        }
        activity_score = activity_map.get(assessment_data.get('activity_level', 'sedentary'), 1)
        
        # Family history score
        family_history = assessment_data.get('family_history', {})
        family_history_score = sum([
            family_history.get('diabetes', False),
            family_history.get('hypertension', False),
            family_history.get('heart_disease', False)
        ])
        
        # Create feature vector
        features = np.array([
            assessment_data['age'],
            bmi,
            activity_score,
            assessment_data.get('sleep_hours', 7),
            assessment_data.get('stress_level', 5),
            1 if assessment_data.get('smoking', False) else 0,
            family_history_score
        ]).reshape(1, -1)
        
        return features
    
    def predict_risk(self, assessment_data, condition):
        """
        Predict risk for a specific condition using ML model
        Returns: risk_score (0-1)
        """
        if condition not in self.models:
            return None
        
        features = self.prepare_features(assessment_data)
        
        try:
            # Get probability prediction
            risk_score = self.models[condition].predict_proba(features)[0][1]
            return float(risk_score)
        except Exception as e:
            print(f"Prediction error for {condition}: {e}")
            return None
    
    def get_feature_importance(self, assessment_data, condition):
        """
        Get SHAP values for explainability
        Placeholder - requires SHAP library integration
        """
        # This would use SHAP in production
        # For now, return simple feature importance
        features = self.prepare_features(assessment_data)
        
        if condition not in self.models:
            return None
        
        try:
            # Get feature importances from the model
            if hasattr(self.models[condition], 'feature_importances_'):
                importances = self.models[condition].feature_importances_
                return dict(zip(self.feature_names, importances.tolist()))
        except:
            pass
        
        return None

def load_models():
    """Load and return ML predictor"""
    predictor = MLRiskPredictor()
    predictor.load_models()
    return predictor

def create_sample_models():
    """
    Create simple sample models for demonstration
    In production, these would be trained on real health datasets
    """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    import numpy as np
    
    # Create synthetic training data
    np.random.seed(42)
    n_samples = 1000
    
    # Features: age, bmi, activity, sleep, stress, smoking, family_history
    X = np.random.randn(n_samples, 7)
    
    # Create models directory if it doesn't exist
    os.makedirs(settings.MODELS_DIR, exist_ok=True)
    
    # Diabetes model
    y_diabetes = (X[:, 0] * 0.3 + X[:, 1] * 0.4 + X[:, 6] * 0.3 + np.random.randn(n_samples) * 0.1 > 0).astype(int)
    diabetes_model = RandomForestClassifier(n_estimators=100, random_state=42)
    diabetes_model.fit(X, y_diabetes)
    joblib.dump(diabetes_model, os.path.join(settings.MODELS_DIR, 'diabetes_model.pkl'))
    
    # Hypertension model
    y_hypertension = (X[:, 0] * 0.25 + X[:, 1] * 0.35 + X[:, 4] * 0.2 + X[:, 5] * 0.2 + np.random.randn(n_samples) * 0.1 > 0).astype(int)
    hypertension_model = RandomForestClassifier(n_estimators=100, random_state=42)
    hypertension_model.fit(X, y_hypertension)
    joblib.dump(hypertension_model, os.path.join(settings.MODELS_DIR, 'hypertension_model.pkl'))
    
    # Cardiovascular model
    y_cardio = (X[:, 0] * 0.3 + X[:, 5] * 0.4 + X[:, 6] * 0.3 + np.random.randn(n_samples) * 0.1 > 0).astype(int)
    cardio_model = LogisticRegression(random_state=42)
    cardio_model.fit(X, y_cardio)
    joblib.dump(cardio_model, os.path.join(settings.MODELS_DIR, 'cardiovascular_model.pkl'))
    
    print("Sample models created successfully!")

if __name__ == "__main__":
    # Create sample models when run directly
    create_sample_models()
