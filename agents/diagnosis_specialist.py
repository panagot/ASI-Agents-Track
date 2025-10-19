"""
Diagnosis Specialist Agent - Uses medical knowledge to suggest diagnoses
"""

import json
from typing import Dict, List, Any, Tuple
from agents.base_agent import BaseHealthcareAgent, PatientData, Diagnosis
from uagents import Context
import logging

logger = logging.getLogger(__name__)

class DiagnosisSpecialist(BaseHealthcareAgent):
    """Agent that specializes in medical diagnosis using knowledge base"""
    
    def __init__(self, seed_phrase: str):
        super().__init__("DiagnosisSpecialist", "diagnosis", seed_phrase)
        self.diagnosis_knowledge = self.load_diagnosis_knowledge()
        self.symptom_diagnosis_mapping = self.load_symptom_diagnosis_mapping()
    
    def load_diagnosis_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Load medical diagnosis knowledge base"""
        return {
            "myocardial_infarction": {
                "symptoms": ["chest pain", "shortness of breath", "nausea", "sweating", "arm pain"],
                "risk_factors": ["age > 65", "diabetes", "hypertension", "smoking", "family history"],
                "diagnostic_criteria": ["ECG changes", "elevated troponins", "chest pain"],
                "confidence_factors": {
                    "chest_pain": 0.8,
                    "ECG_changes": 0.9,
                    "elevated_troponins": 0.95
                }
            },
            "pneumonia": {
                "symptoms": ["cough", "fever", "shortness of breath", "chest pain", "fatigue"],
                "risk_factors": ["age > 65", "immunocompromised", "smoking", "chronic lung disease"],
                "diagnostic_criteria": ["chest X-ray", "elevated WBC", "fever"],
                "confidence_factors": {
                    "chest_xray": 0.85,
                    "fever": 0.7,
                    "cough": 0.6
                }
            },
            "migraine": {
                "symptoms": ["headache", "nausea", "sensitivity to light", "sensitivity to sound"],
                "risk_factors": ["family history", "female", "stress", "hormonal changes"],
                "diagnostic_criteria": ["headache pattern", "associated symptoms"],
                "confidence_factors": {
                    "unilateral_headache": 0.7,
                    "photophobia": 0.8,
                    "nausea": 0.6
                }
            },
            "gastroenteritis": {
                "symptoms": ["nausea", "vomiting", "diarrhea", "abdominal pain", "fever"],
                "risk_factors": ["food poisoning", "viral infection", "travel"],
                "diagnostic_criteria": ["symptoms", "stool culture"],
                "confidence_factors": {
                    "diarrhea": 0.8,
                    "nausea_vomiting": 0.7,
                    "fever": 0.6
                }
            },
            "anxiety_disorder": {
                "symptoms": ["anxiety", "panic", "sweating", "palpitations", "shortness of breath"],
                "risk_factors": ["stress", "family history", "trauma"],
                "diagnostic_criteria": ["symptom duration", "functional impairment"],
                "confidence_factors": {
                    "persistent_anxiety": 0.8,
                    "panic_attacks": 0.9,
                    "functional_impairment": 0.7
                }
            }
        }
    
    def load_symptom_diagnosis_mapping(self) -> Dict[str, List[str]]:
        """Load mapping from symptoms to possible diagnoses"""
        mapping = {}
        for diagnosis, info in self.diagnosis_knowledge.items():
            for symptom in info["symptoms"]:
                if symptom not in mapping:
                    mapping[symptom] = []
                mapping[symptom].append(diagnosis)
        return mapping
    
    async def handle_text_message(self, ctx: Context, sender: str, text: str):
        """Handle incoming text messages"""
        try:
            message_data = json.loads(text)
            
            if message_data.get("type") == "request_diagnosis":
                patient_data = PatientData(**message_data["patient_data"])
                symptom_analysis = message_data.get("symptom_analysis", {})
                
                diagnosis_result = await self.generate_diagnosis(patient_data, symptom_analysis)
                
                response = {
                    "type": "diagnosis_result",
                    "diagnoses": diagnosis_result,
                    "agent": self.name
                }
                await self.send_message(ctx, sender, json.dumps(response))
                
        except json.JSONDecodeError:
            if "diagnosis" in text.lower():
                await self.send_message(ctx, sender, f"{self.name}: Ready to provide diagnosis. Please provide patient data and symptom analysis.")
        except Exception as e:
            logger.error(f"Error in DiagnosisSpecialist: {e}")
            await self.send_message(ctx, sender, f"{self.name}: Error processing diagnosis request.")
    
    async def generate_diagnosis(self, patient_data: PatientData, symptom_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate diagnosis based on symptoms and analysis"""
        possible_diagnoses = self.identify_possible_diagnoses(patient_data.symptoms)
        diagnoses = []
        
        for diagnosis_name in possible_diagnoses:
            diagnosis_info = self.diagnosis_knowledge[diagnosis_name]
            confidence = self.calculate_confidence(patient_data, diagnosis_info, symptom_analysis)
            
            if confidence > 0.3:  # Only include diagnoses with reasonable confidence
                diagnosis = {
                    "condition": diagnosis_name.replace("_", " ").title(),
                    "confidence": confidence,
                    "reasoning": self.generate_reasoning(patient_data, diagnosis_info, confidence),
                    "supporting_evidence": self.identify_supporting_evidence(patient_data, diagnosis_info),
                    "differential_diagnoses": self.get_differential_diagnoses(diagnosis_name, patient_data.symptoms),
                    "recommended_tests": self.recommend_diagnostic_tests(diagnosis_info),
                    "urgency": self.assess_urgency(diagnosis_name, patient_data)
                }
                diagnoses.append(diagnosis)
        
        # Sort by confidence
        diagnoses.sort(key=lambda x: x["confidence"], reverse=True)
        return diagnoses[:5]  # Return top 5 diagnoses
    
    def identify_possible_diagnoses(self, symptoms: List[str]) -> List[str]:
        """Identify possible diagnoses based on symptoms"""
        possible_diagnoses = set()
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for symptom_key, diagnoses in self.symptom_diagnosis_mapping.items():
                if symptom_key in symptom_lower:
                    possible_diagnoses.update(diagnoses)
        
        return list(possible_diagnoses)
    
    def calculate_confidence(self, patient_data: PatientData, diagnosis_info: Dict[str, Any], symptom_analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for a diagnosis"""
        confidence = 0.0
        symptom_count = 0
        
        # Check symptom matches
        for symptom in patient_data.symptoms:
            symptom_lower = symptom.lower()
            for diagnosis_symptom in diagnosis_info["symptoms"]:
                if diagnosis_symptom in symptom_lower:
                    confidence += 0.2
                    symptom_count += 1
                    break
        
        # Check risk factors
        for risk_factor in diagnosis_info["risk_factors"]:
            if self.check_risk_factor(patient_data, risk_factor):
                confidence += 0.1
        
        # Normalize confidence
        if symptom_count > 0:
            confidence = min(confidence, 1.0)
        
        return confidence
    
    def check_risk_factor(self, patient_data: PatientData, risk_factor: str) -> bool:
        """Check if patient has a specific risk factor"""
        risk_factor_lower = risk_factor.lower()
        
        # Age-based risk factors
        if "age > 65" in risk_factor_lower:
            return patient_data.age > 65
        elif "age < 18" in risk_factor_lower:
            return patient_data.age < 18
        
        # Medical history risk factors
        for condition in patient_data.medical_history:
            if any(keyword in condition.lower() for keyword in risk_factor_lower.split()):
                return True
        
        return False
    
    def generate_reasoning(self, patient_data: PatientData, diagnosis_info: Dict[str, Any], confidence: float) -> str:
        """Generate reasoning for the diagnosis"""
        reasoning_parts = []
        
        # Symptom-based reasoning
        matching_symptoms = []
        for symptom in patient_data.symptoms:
            symptom_lower = symptom.lower()
            for diagnosis_symptom in diagnosis_info["symptoms"]:
                if diagnosis_symptom in symptom_lower:
                    matching_symptoms.append(symptom)
                    break
        
        if matching_symptoms:
            reasoning_parts.append(f"Patient presents with {', '.join(matching_symptoms)}")
        
        # Risk factor reasoning
        matching_risk_factors = []
        for risk_factor in diagnosis_info["risk_factors"]:
            if self.check_risk_factor(patient_data, risk_factor):
                matching_risk_factors.append(risk_factor)
        
        if matching_risk_factors:
            reasoning_parts.append(f"Risk factors include: {', '.join(matching_risk_factors)}")
        
        # Confidence reasoning
        if confidence > 0.7:
            reasoning_parts.append("High confidence based on symptom presentation and risk factors")
        elif confidence > 0.5:
            reasoning_parts.append("Moderate confidence, consider additional diagnostic tests")
        else:
            reasoning_parts.append("Low confidence, consider differential diagnoses")
        
        return ". ".join(reasoning_parts) + "."
    
    def identify_supporting_evidence(self, patient_data: PatientData, diagnosis_info: Dict[str, Any]) -> List[str]:
        """Identify supporting evidence for the diagnosis"""
        evidence = []
        
        for symptom in patient_data.symptoms:
            symptom_lower = symptom.lower()
            for diagnosis_symptom in diagnosis_info["symptoms"]:
                if diagnosis_symptom in symptom_lower:
                    evidence.append(f"Patient reports {symptom}")
                    break
        
        return evidence
    
    def get_differential_diagnoses(self, primary_diagnosis: str, symptoms: List[str]) -> List[str]:
        """Get differential diagnoses to consider"""
        differentials = []
        
        # Get other diagnoses that share symptoms
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for symptom_key, diagnoses in self.symptom_diagnosis_mapping.items():
                if symptom_key in symptom_lower:
                    for diagnosis in diagnoses:
                        if diagnosis != primary_diagnosis and diagnosis not in differentials:
                            differentials.append(diagnosis.replace("_", " ").title())
        
        return differentials[:3]  # Return top 3 differentials
    
    def recommend_diagnostic_tests(self, diagnosis_info: Dict[str, Any]) -> List[str]:
        """Recommend diagnostic tests for the diagnosis"""
        return diagnosis_info.get("diagnostic_criteria", [])
    
    def assess_urgency(self, diagnosis_name: str, patient_data: PatientData) -> str:
        """Assess urgency of the diagnosis"""
        urgent_conditions = ["myocardial_infarction", "pneumonia", "stroke"]
        
        if diagnosis_name in urgent_conditions:
            return "urgent"
        elif patient_data.age > 65 or len(patient_data.current_medications) > 3:
            return "moderate"
        else:
            return "routine"

# Create and run the agent
if __name__ == "__main__":
    specialist = DiagnosisSpecialist("diagnosis specialist agent seed phrase")
    specialist.run()

