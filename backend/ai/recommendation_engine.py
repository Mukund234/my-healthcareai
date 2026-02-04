"""
Personalized health recommendations based on WHO guidelines
Generates exercise and nutrition recommendations based on risk assessment
"""

from typing import Dict, List

class RecommendationEngine:
    def __init__(self):
        self.exercise_db = self._build_exercise_database()
        self.food_db = self._build_food_database()
    
    def _build_exercise_database(self) -> Dict:
        """WHO-recommended exercises by category"""
        return {
            "cardiovascular": [
                {
                    "name": "Brisk Walking",
                    "duration": "30 minutes",
                    "frequency": "5 days/week",
                    "intensity": "moderate",
                    "benefits": "Improves heart health, reduces blood pressure",
                    "who_guideline": "WHO recommends 150-300 min/week moderate activity"
                },
                {
                    "name": "Jogging",
                    "duration": "20 minutes",
                    "frequency": "3 days/week",
                    "intensity": "vigorous",
                    "benefits": "Strengthens heart, improves circulation",
                    "who_guideline": "WHO recommends 75-150 min/week vigorous activity"
                },
                {
                    "name": "Cycling",
                    "duration": "30 minutes",
                    "frequency": "4 days/week",
                    "intensity": "moderate",
                    "benefits": "Low-impact cardio, improves endurance",
                    "who_guideline": "Aerobic activity for cardiovascular health"
                },
                {
                    "name": "Swimming",
                    "duration": "30 minutes",
                    "frequency": "3 days/week",
                    "intensity": "moderate",
                    "benefits": "Full-body workout, joint-friendly",
                    "who_guideline": "Excellent for overall fitness"
                }
            ],
            "strength": [
                {
                    "name": "Bodyweight Exercises",
                    "duration": "20 minutes",
                    "frequency": "2-3 days/week",
                    "intensity": "moderate",
                    "benefits": "Builds muscle, improves metabolism",
                    "who_guideline": "WHO recommends muscle-strengthening 2+ days/week"
                },
                {
                    "name": "Resistance Band Training",
                    "duration": "25 minutes",
                    "frequency": "2 days/week",
                    "intensity": "moderate",
                    "benefits": "Increases strength, improves bone density",
                    "who_guideline": "Strength training for all major muscle groups"
                }
            ],
            "flexibility": [
                {
                    "name": "Yoga",
                    "duration": "30 minutes",
                    "frequency": "3 days/week",
                    "intensity": "light",
                    "benefits": "Reduces stress, improves flexibility",
                    "who_guideline": "Beneficial for mental and physical health"
                },
                {
                    "name": "Stretching",
                    "duration": "10 minutes",
                    "frequency": "daily",
                    "intensity": "light",
                    "benefits": "Prevents injury, improves mobility",
                    "who_guideline": "Important for overall fitness"
                }
            ],
            "weight_loss": [
                {
                    "name": "HIIT (High-Intensity Interval Training)",
                    "duration": "20 minutes",
                    "frequency": "3 days/week",
                    "intensity": "vigorous",
                    "benefits": "Burns calories, boosts metabolism",
                    "who_guideline": "Effective for weight management"
                },
                {
                    "name": "Dance Aerobics",
                    "duration": "30 minutes",
                    "frequency": "4 days/week",
                    "intensity": "moderate",
                    "benefits": "Fun cardio, burns calories",
                    "who_guideline": "Enjoyable way to meet activity goals"
                }
            ]
        }
    
    def _build_food_database(self) -> Dict:
        """WHO-recommended nutrition by health goal"""
        return {
            "heart_health": [
                {
                    "category": "Whole Grains",
                    "foods": ["Oatmeal", "Brown rice", "Whole wheat bread", "Quinoa"],
                    "serving": "3-5 servings/day",
                    "benefits": "Lowers cholesterol, improves heart health",
                    "who_guideline": "WHO recommends whole grains over refined"
                },
                {
                    "category": "Fatty Fish",
                    "foods": ["Salmon", "Mackerel", "Sardines", "Tuna"],
                    "serving": "2-3 times/week",
                    "benefits": "Rich in Omega-3, reduces heart disease risk",
                    "who_guideline": "Essential fatty acids for cardiovascular health"
                },
                {
                    "category": "Nuts & Seeds",
                    "foods": ["Almonds", "Walnuts", "Chia seeds", "Flaxseeds"],
                    "serving": "1 handful/day",
                    "benefits": "Healthy fats, reduces bad cholesterol",
                    "who_guideline": "Good source of unsaturated fats"
                }
            ],
            "diabetes_prevention": [
                {
                    "category": "Non-Starchy Vegetables",
                    "foods": ["Broccoli", "Spinach", "Cauliflower", "Bell peppers"],
                    "serving": "5+ servings/day",
                    "benefits": "Low glycemic index, high fiber",
                    "who_guideline": "WHO recommends ≥400g fruits & vegetables/day"
                },
                {
                    "category": "Legumes",
                    "foods": ["Lentils", "Chickpeas", "Black beans", "Kidney beans"],
                    "serving": "3-4 times/week",
                    "benefits": "Stabilizes blood sugar, high protein",
                    "who_guideline": "Excellent plant-based protein source"
                },
                {
                    "category": "Berries",
                    "foods": ["Blueberries", "Strawberries", "Raspberries"],
                    "serving": "1 cup/day",
                    "benefits": "Antioxidants, low sugar",
                    "who_guideline": "Part of daily fruit intake"
                }
            ],
            "weight_management": [
                {
                    "category": "Lean Proteins",
                    "foods": ["Chicken breast", "Turkey", "Tofu", "Egg whites"],
                    "serving": "2-3 servings/day",
                    "benefits": "Builds muscle, increases satiety",
                    "who_guideline": "Essential for healthy weight"
                },
                {
                    "category": "Leafy Greens",
                    "foods": ["Kale", "Spinach", "Lettuce", "Swiss chard"],
                    "serving": "Unlimited",
                    "benefits": "Low calorie, nutrient-dense",
                    "who_guideline": "Foundation of healthy diet"
                }
            ],
            "general_health": [
                {
                    "category": "Fruits",
                    "foods": ["Apples", "Bananas", "Oranges", "Grapes"],
                    "serving": "2-3 servings/day",
                    "benefits": "Vitamins, minerals, fiber",
                    "who_guideline": "Part of 400g/day recommendation"
                },
                {
                    "category": "Water",
                    "foods": ["Plain water", "Herbal tea"],
                    "serving": "8-10 glasses/day",
                    "benefits": "Hydration, supports all body functions",
                    "who_guideline": "Essential for health"
                }
            ],
            "avoid": [
                {
                    "category": "Limit These",
                    "foods": ["Sugary drinks", "Processed meats", "Trans fats", "Excessive salt"],
                    "reason": "Increases disease risk",
                    "who_guideline": "WHO: <10% energy from sugars, <5g salt/day"
                }
            ]
        }
    
    def generate_recommendations(self, risk_results: Dict, user_data: Dict) -> Dict:
        """Generate personalized exercise and nutrition recommendations"""
        
        recommendations = {
            "exercise": [],
            "nutrition": [],
            "lifestyle": [],
            "notifications": []
        }
        
        # Analyze risk levels
        high_risks = [risk for risk, data in risk_results.items() if data.get('severity') == 'high']
        moderate_risks = [risk for risk, data in risk_results.items() if data.get('severity') == 'moderate']
        
        # Exercise recommendations based on risks
        if 'cardiovascular' in high_risks or 'hypertension' in high_risks:
            recommendations["exercise"].extend(self.exercise_db["cardiovascular"][:2])
            recommendations["notifications"].append({
                "title": "❤️ Heart Health Alert",
                "body": "Start with 30 minutes of brisk walking today!",
                "schedule": "daily_morning"
            })
        
        if 'obesity' in high_risks or user_data.get('weight_kg', 0) > 0:
            bmi = self._calculate_bmi(user_data)
            if bmi >= 25:
                recommendations["exercise"].extend(self.exercise_db["weight_loss"][:2])
                recommendations["notifications"].append({
                    "title": "🏃 Weight Management",
                    "body": "Try 20 minutes of HIIT today - burn calories fast!",
                    "schedule": "3x_week"
                })
        
        if user_data.get('activity_level') in ['sedentary', 'light']:
            recommendations["exercise"].extend(self.exercise_db["cardiovascular"][:1])
            recommendations["exercise"].extend(self.exercise_db["strength"][:1])
            recommendations["notifications"].append({
                "title": "💪 Move More",
                "body": "You've been sitting too long. Take a 10-minute walk!",
                "schedule": "every_2_hours"
            })
        
        # Flexibility for stress
        if user_data.get('stress_level', 0) >= 7:
            recommendations["exercise"].extend(self.exercise_db["flexibility"][:1])
            recommendations["notifications"].append({
                "title": "🧘 Stress Relief",
                "body": "Time for yoga! Reduce stress with 15 minutes of stretching.",
                "schedule": "daily_evening"
            })
        
        # Nutrition recommendations
        if 'cardiovascular' in high_risks or 'hypertension' in high_risks:
            recommendations["nutrition"].extend(self.food_db["heart_health"])
            recommendations["notifications"].append({
                "title": "🥗 Heart-Healthy Eating",
                "body": "Add salmon to your diet this week - great for your heart!",
                "schedule": "weekly"
            })
        
        if 'diabetes' in high_risks or 'diabetes' in moderate_risks:
            recommendations["nutrition"].extend(self.food_db["diabetes_prevention"])
            recommendations["notifications"].append({
                "title": "🥦 Blood Sugar Control",
                "body": "Include more non-starchy vegetables in your meals today.",
                "schedule": "daily_meal_time"
            })
        
        if 'obesity' in high_risks:
            recommendations["nutrition"].extend(self.food_db["weight_management"])
            recommendations["notifications"].append({
                "title": "⚖️ Healthy Weight",
                "body": "Choose lean proteins and leafy greens for lunch!",
                "schedule": "daily_lunch"
            })
        
        # General health
        recommendations["nutrition"].extend(self.food_db["general_health"])
        recommendations["nutrition"].extend(self.food_db["avoid"])
        
        # Lifestyle recommendations
        if user_data.get('sleep_hours', 7) < 7:
            recommendations["lifestyle"].append({
                "category": "Sleep",
                "recommendation": "Aim for 7-9 hours of sleep per night",
                "who_guideline": "WHO recommends adequate sleep for health",
                "tips": ["Set consistent bedtime", "Avoid screens 1 hour before bed", "Create dark, quiet environment"]
            })
            recommendations["notifications"].append({
                "title": "😴 Better Sleep",
                "body": "Time to wind down. Aim for 7-9 hours tonight!",
                "schedule": "daily_bedtime"
            })
        
        if user_data.get('smoking'):
            recommendations["lifestyle"].append({
                "category": "Smoking Cessation",
                "recommendation": "Quit smoking to dramatically reduce health risks",
                "who_guideline": "WHO Framework Convention on Tobacco Control",
                "resources": ["Quitline: 1-800-QUIT-NOW", "WHO tobacco cessation guide"]
            })
        
        if user_data.get('stress_level', 0) >= 7:
            recommendations["lifestyle"].append({
                "category": "Stress Management",
                "recommendation": "Practice daily stress-reduction techniques",
                "who_guideline": "Mental health is essential for overall wellbeing",
                "tips": ["Meditation 10 min/day", "Deep breathing exercises", "Regular physical activity"]
            })
        
        # Water reminder
        recommendations["notifications"].append({
            "title": "💧 Stay Hydrated",
            "body": "Drink a glass of water now!",
            "schedule": "every_2_hours"
        })
        
        return recommendations
    
    def _calculate_bmi(self, user_data: Dict) -> float:
        """Calculate BMI"""
        weight = user_data.get('weight_kg', 0)
        height = user_data.get('height_cm', 0)
        if weight > 0 and height > 0:
            height_m = height / 100
            return weight / (height_m ** 2)
        return 0
