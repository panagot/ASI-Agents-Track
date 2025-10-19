"""
Symptom Analyzer Agent - Processes patient symptoms and medical history
"""

import re
from typing import Dict, List, Any
from agents.base_agent import BaseHealthcareAgent, PatientData
from uagents import Context
import json

class SymptomAnalyzer(BaseHealthcareAgent):
    """Agent that analyzes patient symptoms and medical history"""
    
    def __init__(self, seed_phrase: str):
        super().__init__("SymptomAnalyzer", "symptom_analysis", seed_phrase)
        self.symptom_patterns = self.load_symptom_patterns()
        self.medical_history_keywords = self.load_medical_keywords()
    
    def load_symptom_patterns(self) -> Dict[str, List[str]]:
        """Load symptom patterns for analysis"""
        return {
            "cardiovascular": ["chest pain", "shortness of breath", "palpitations", "dizziness", "fatigue"],
            "respiratory": ["cough", "wheezing", "shortness of breath", "chest tightness", "sputum"],
            "gastrointestinal": ["nausea", "vomiting", "diarrhea", "constipation", "abdominal pain", "bloating"],
            "neurological": ["headache", "dizziness", "confusion", "seizures", "numbness", "weakness"],
            "musculoskeletal": ["joint pain", "muscle pain", "stiffness", "swelling", "limited mobility"],
            "dermatological": ["rash", "itching", "redness", "swelling", "lesions", "dryness"],
            "endocrine": ["weight loss", "weight gain", "thirst", "frequent urination", "fatigue"],
            "psychiatric": ["anxiety", "depression", "mood changes", "sleep problems", "concentration issues"]
        }
    
    def load_medical_keywords(self) -> List[str]:
        """Load medical history keywords"""
        return [
            "diabetes", "hypertension", "heart disease", "asthma", "cancer",
            "stroke", "kidney disease", "liver disease", "thyroid", "arthritis",
            "depression", "anxiety", "allergies", "surgery", "hospitalization"
        ]
    
    async def handle_text_message(self, ctx: Context, sender: str, text: str):
        """Handle incoming text messages"""
        try:
            # Parse the message
            message_data = json.loads(text)
            
            if message_data.get("type") == "analyze_symptoms":
                patient_data = PatientData(**message_data["patient_data"])
                analysis_result = await self.analyze_patient_data(patient_data)
                
                # Send analysis back to sender
                response = {
                    "type": "symptom_analysis_result",
                    "analysis": analysis_result,
                    "agent": self.name
                }
                await self.send_message(ctx, sender, json.dumps(response))
                
        except json.JSONDecodeError:
            # Handle non-JSON messages
            if "analyze" in text.lower():
                await self.send_message(ctx, sender, f"{self.name}: Ready to analyze symptoms. Please provide patient data.")
        except Exception as e:
            logger.error(f"Error in SymptomAnalyzer: {e}")
            await self.send_message(ctx, sender, f"{self.name}: Error processing request.")
    
    async def analyze_patient_data(self, patient_data: PatientData) -> Dict[str, Any]:
        """Analyze patient symptoms and medical history"""
        analysis = {
            "patient_id": patient_data.patient_id,
            "symptom_categories": self.categorize_symptoms(patient_data.symptoms),
            "severity_assessment": self.assess_symptom_severity(patient_data.symptoms),
            "medical_history_analysis": self.analyze_medical_history(patient_data.medical_history),
            "risk_factors": self.identify_risk_factors(patient_data),
            "priority_level": self.determine_priority(patient_data),
            "recommended_specialists": self.recommend_specialists(patient_data.symptoms),
            "analysis_timestamp": patient_data.timestamp.isoformat()
        }
        
        return analysis
    
    def categorize_symptoms(self, symptoms: List[str]) -> Dict[str, List[str]]:
        """Categorize symptoms by body system"""
        categorized = {category: [] for category in self.symptom_patterns.keys()}
        categorized["other"] = []
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            categorized_flag = False
            
            for category, patterns in self.symptom_patterns.items():
                for pattern in patterns:
                    if pattern in symptom_lower:
                        categorized[category].append(symptom)
                        categorized_flag = True
                        break
                if categorized_flag:
                    break
            
            if not categorized_flag:
                categorized["other"].append(symptom)
        
        # Remove empty categories
        return {k: v for k, v in categorized.items() if v}
    
    def assess_symptom_severity(self, symptoms: List[str]) -> Dict[str, str]:
        """Assess severity of symptoms"""
        severity_keywords = {
            "severe": ["severe", "intense", "unbearable", "excruciating", "debilitating"],
            "moderate": ["moderate", "noticeable", "uncomfortable", "bothersome"],
            "mild": ["mild", "slight", "minor", "barely noticeable"]
        }
        
        severity_assessment = {}
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            severity = "mild"  # default
            
            for level, keywords in severity_keywords.items():
                if any(keyword in symptom_lower for keyword in keywords):
                    severity = level
                    break
            
            severity_assessment[symptom] = severity
        
        return severity_assessment
    
    def analyze_medical_history(self, medical_history: List[str]) -> Dict[str, Any]:
        """Analyze medical history for relevant conditions"""
        relevant_conditions = []
        for condition in medical_history:
            condition_lower = condition.lower()
            if any(keyword in condition_lower for keyword in self.medical_history_keywords):
                relevant_conditions.append(condition)
        
        return {
            "relevant_conditions": relevant_conditions,
            "total_conditions": len(medical_history),
            "relevance_score": len(relevant_conditions) / max(len(medical_history), 1)
        }
    
    def identify_risk_factors(self, patient_data: PatientData) -> List[str]:
        """Identify potential risk factors"""
        risk_factors = []
        
        # Age-based risks
        if patient_data.age > 65:
            risk_factors.append("Advanced age")
        elif patient_data.age < 18:
            risk_factors.append("Pediatric patient")
        
        # Medication interactions
        if len(patient_data.current_medications) > 3:
            risk_factors.append("Polypharmacy")
        
        # Medical history risks
        for condition in patient_data.medical_history:
            if any(keyword in condition.lower() for keyword in ["diabetes", "heart", "kidney", "liver"]):
                risk_factors.append(f"Chronic condition: {condition}")
        
        return risk_factors
    
    def determine_priority(self, patient_data: PatientData) -> str:
        """Determine priority level for patient care"""
        high_priority_symptoms = ["chest pain", "shortness of breath", "severe headache", "loss of consciousness"]
        moderate_priority_symptoms = ["fever", "abdominal pain", "dizziness", "nausea"]
        
        symptoms_lower = [s.lower() for s in patient_data.symptoms]
        
        if any(symptom in symptoms_lower for symptom in high_priority_symptoms):
            return "high"
        elif any(symptom in symptoms_lower for symptom in moderate_priority_symptoms):
            return "moderate"
        else:
            return "low"
    
    def recommend_specialists(self, symptoms: List[str]) -> List[str]:
        """Recommend specialists based on symptoms"""
        specialist_mapping = {
            "cardiologist": ["chest pain", "palpitations", "shortness of breath"],
            "pulmonologist": ["cough", "wheezing", "breathing problems"],
            "gastroenterologist": ["abdominal pain", "nausea", "vomiting", "diarrhea"],
            "neurologist": ["headache", "dizziness", "seizures", "numbness"],
            "rheumatologist": ["joint pain", "muscle pain", "stiffness"],
            "dermatologist": ["rash", "itching", "skin lesions"],
            "endocrinologist": ["weight changes", "thirst", "fatigue"],
            "psychiatrist": ["anxiety", "depression", "mood changes"]
        }
        
        recommended = []
        symptoms_lower = [s.lower() for s in symptoms]
        
        for specialist, related_symptoms in specialist_mapping.items():
            if any(symptom in symptoms_lower for symptom in related_symptoms):
                recommended.append(specialist)
        
        return recommended

# Create and run the agent
if __name__ == "__main__":
    analyzer = SymptomAnalyzer("symptom analyzer agent seed phrase")
    analyzer.run()

