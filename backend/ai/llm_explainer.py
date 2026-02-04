"""
LLM-based explanation generator for health risk results.
Uses OpenAI API with fallback to rule-based explanations.
"""

import os
from openai import OpenAI
from config import settings

class LLMExplainer:
    def __init__(self):
        self.client = None
        # Only initialize OpenAI client if API key is actually present
        if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip():
            try:
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                print("✅ OpenAI client initialized successfully")
            except Exception as e:
                print(f"⚠️ OpenAI client initialization failed: {e}")
                self.client = None
        else:
            print("ℹ️ No OpenAI API key found - using rule-based explanations")
    
    def generate_explanation(self, risk_results, assessment_data, language='en'):
        """
        Generate personalized explanation of health risks
        
        Args:
            risk_results: Dict with risk scores and severities
            assessment_data: Original assessment data
            language: 'en' for English, 'hi' for Hindi
        
        Returns:
            Explanation text
        """
        # Use LLM only if client is initialized
        if self.client:
            try:
                return self._generate_llm_explanation(risk_results, assessment_data, language)
            except Exception as e:
                print(f"⚠️ LLM generation failed: {e}, falling back to rule-based")
        
        # Use fast rule-based explanation
        return self._generate_rule_based_explanation(risk_results, assessment_data, language)
    
    def _generate_llm_explanation(self, risk_results, assessment_data, language):
        """Generate explanation using OpenAI API"""
        
        # Prepare context
        age = assessment_data['age']
        gender = assessment_data['gender']
        
        risk_scores = risk_results['risk_scores']
        severity_levels = risk_results['severity_levels']
        overall_severity = risk_results['overall_severity']
        
        # Find highest risks
        high_risks = [
            risk_type.replace('_risk', '').replace('_', ' ').title()
            for risk_type, score in risk_scores.items()
            if score >= 0.7
        ]
        
        moderate_risks = [
            risk_type.replace('_risk', '').replace('_', ' ').title()
            for risk_type, score in risk_scores.items()
            if 0.4 <= score < 0.7
        ]
        
        # Create prompt
        lang_instruction = "in Hindi (Devanagari script)" if language == 'hi' else "in English"
        
        prompt = f"""You are a health education assistant. Explain the following health risk assessment results {lang_instruction} in a caring, supportive, and educational tone.

Patient Profile:
- Age: {age} years
- Gender: {gender}

Risk Assessment Results:
- Overall Risk Level: {overall_severity.upper()}
- High Risk Areas: {', '.join(high_risks) if high_risks else 'None'}
- Moderate Risk Areas: {', '.join(moderate_risks) if moderate_risks else 'None'}

Instructions:
1. Start with a brief, empathetic opening
2. Explain what the risk levels mean in simple terms
3. Mention the main contributing factors (lifestyle, age, etc.)
4. Emphasize that these are PREVENTIVE indicators, not diagnoses
5. End with encouragement about prevention
6. Keep it under 150 words
7. Use simple, non-medical language

CRITICAL: Add this disclaimer at the end:
"⚠️ This is not medical advice. Consult a qualified healthcare provider for medical decisions."
"""
        
        response = self.client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=[
                {"role": "system", "content": "You are a compassionate health education assistant. You provide clear, supportive explanations about health risks while emphasizing prevention and the importance of professional medical consultation."},
                {"role": "user", "content": prompt}
            ],
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.MAX_TOKENS
        )
        
        return response.choices[0].message.content.strip()
    
    def _generate_rule_based_explanation(self, risk_results, assessment_data, language):
        """Generate explanation using predefined templates"""
        
        age = assessment_data['age']
        overall_severity = risk_results['overall_severity']
        risk_scores = risk_results['risk_scores']
        
        # Find primary concern
        primary_risk = max(risk_scores.items(), key=lambda x: x[1])
        primary_condition = primary_risk[0].replace('_risk', '').replace('_', ' ').title()
        primary_score = primary_risk[1]
        
        if language == 'hi':
            return self._generate_hindi_explanation(age, overall_severity, primary_condition, primary_score)
        
        # English explanation
        if overall_severity == 'high':
            explanation = f"""Your health risk assessment shows a HIGH overall risk level, primarily due to {primary_condition.lower()} risk.

This means you have several factors that could increase your chances of developing health issues in the future. The main contributors are likely related to your lifestyle, age ({age} years), and other health indicators.

Remember: These are PREVENTIVE indicators, not diagnoses. They help you understand where to focus your health improvement efforts.

We strongly recommend consulting a healthcare provider to discuss these results and create a personalized prevention plan.

⚠️ This is not medical advice. Consult a qualified healthcare provider for medical decisions."""
        
        elif overall_severity == 'moderate':
            explanation = f"""Your health risk assessment shows a MODERATE overall risk level, with {primary_condition.lower()} being the primary area of concern.

This means you have some factors that could increase your health risks, but there's great opportunity for prevention through lifestyle changes. At {age} years old, taking action now can make a significant difference.

Focus on the recommendations provided, especially around diet, exercise, and stress management. Small, consistent changes can greatly reduce your risk.

Consider scheduling a checkup with your doctor to discuss these findings.

⚠️ This is not medical advice. Consult a qualified healthcare provider for medical decisions."""
        
        else:  # low
            explanation = f"""Great news! Your health risk assessment shows a LOW overall risk level.

Your current lifestyle and health indicators suggest you're on a good path. Continue maintaining healthy habits like regular physical activity, balanced nutrition, and adequate sleep.

Even with low risk, it's important to stay proactive about your health. Regular checkups and maintaining healthy habits will help you stay on track.

Keep up the good work!

⚠️ This is not medical advice. Consult a qualified healthcare provider for medical decisions."""
        
        return explanation
    
    def _generate_hindi_explanation(self, age, overall_severity, primary_condition, primary_score):
        """Generate explanation in Hindi"""
        
        if overall_severity == 'high':
            return f"""आपके स्वास्थ्य जोखिम मूल्यांकन में उच्च जोखिम स्तर दिखाया गया है, मुख्य रूप से {primary_condition} के कारण।

इसका मतलब है कि आपके पास कुछ ऐसे कारक हैं जो भविष्य में स्वास्थ्य समस्याओं की संभावना बढ़ा सकते हैं। मुख्य योगदानकर्ता आपकी जीवनशैली, उम्र ({age} वर्ष), और अन्य स्वास्थ्य संकेतक हो सकते हैं।

याद रखें: ये रोकथाम संकेतक हैं, निदान नहीं। ये आपको यह समझने में मदद करते हैं कि अपने स्वास्थ्य सुधार प्रयासों को कहाँ केंद्रित करना है।

हम दृढ़ता से अनुशंसा करते हैं कि इन परिणामों पर चर्चा करने और व्यक्तिगत रोकथाम योजना बनाने के लिए स्वास्थ्य सेवा प्रदाता से परामर्श लें।

⚠️ यह चिकित्सा सलाह नहीं है। चिकित्सा निर्णयों के लिए योग्य स्वास्थ्य सेवा प्रदाता से परामर्श लें।"""
        
        elif overall_severity == 'moderate':
            return f"""आपके स्वास्थ्य जोखिम मूल्यांकन में मध्यम जोखिम स्तर दिखाया गया है, {primary_condition} मुख्य चिंता का क्षेत्र है।

इसका मतलब है कि आपके पास कुछ कारक हैं जो स्वास्थ्य जोखिम बढ़ा सकते हैं, लेकिन जीवनशैली में बदलाव के माध्यम से रोकथाम का बड़ा अवसर है। {age} वर्ष की उम्र में, अभी कार्रवाई करना महत्वपूर्ण अंतर ला सकता है।

दी गई सिफारिशों पर ध्यान दें, विशेष रूप से आहार, व्यायाम और तनाव प्रबंधन के आसपास। छोटे, निरंतर बदलाव आपके जोखिम को बहुत कम कर सकते हैं।

⚠️ यह चिकित्सा सलाह नहीं है। चिकित्सा निर्णयों के लिए योग्य स्वास्थ्य सेवा प्रदाता से परामर्श लें।"""
        
        else:
            return f"""बढ़िया खबर! आपके स्वास्थ्य जोखिम मूल्यांकन में कम जोखिम स्तर दिखाया गया है।

आपकी वर्तमान जीवनशैली और स्वास्थ्य संकेतक बताते हैं कि आप अच्छे रास्ते पर हैं। नियमित शारीरिक गतिविधि, संतुलित पोषण और पर्याप्त नींद जैसी स्वस्थ आदतों को बनाए रखना जारी रखें।

कम जोखिम के साथ भी, अपने स्वास्थ्य के बारे में सक्रिय रहना महत्वपूर्ण है।

शुभकामनाएं!

⚠️ यह चिकित्सा सलाह नहीं है। चिकित्सा निर्णयों के लिए योग्य स्वास्थ्य सेवा प्रदाता से परामर्श लें।"""

# Singleton instance
_explainer = None

def get_explainer():
    """Get or create LLM explainer instance"""
    global _explainer
    if _explainer is None:
        _explainer = LLMExplainer()
    return _explainer
