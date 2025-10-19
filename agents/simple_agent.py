"""
Simplified Agent Base Class - Python 3.13 Compatible
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PatientData(BaseModel):
    """Patient information model"""
    patient_id: str
    age: int
    gender: str
    symptoms: List[str]
    medical_history: List[str]
    current_medications: List[str]
    vital_signs: Dict[str, Any]
    timestamp: datetime

class Diagnosis(BaseModel):
    """Diagnosis model"""
    condition: str
    confidence: float
    reasoning: str
    supporting_evidence: List[str]
    differential_diagnoses: List[str]

class Treatment(BaseModel):
    """Treatment recommendation model"""
    treatment_type: str
    medication: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    instructions: str
    side_effects: List[str]
    contraindications: List[str]

class SimpleAgent:
    """Simplified base class for healthcare agents"""
    
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.logger = logging.getLogger(f"Agent.{name}")
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming messages - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement process_message")
    
    def log_info(self, message: str):
        """Log information message"""
        self.logger.info(f"{self.name}: {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        self.logger.error(f"{self.name}: {message}")

class SimpleSymptomAnalyzer(SimpleAgent):
    """Simplified Symptom Analyzer Agent"""
    
    def __init__(self):
        super().__init__("SymptomAnalyzer", "symptom_analysis")
        self.symptom_patterns = self.load_symptom_patterns()
    
    def load_symptom_patterns(self) -> Dict[str, List[str]]:
        """Load comprehensive symptom patterns for analysis"""
        return {
            "cardiovascular": ["chest pain", "shortness of breath", "palpitations", "dizziness", "fatigue", "arm pain", "jaw pain", "sweating", "rapid heartbeat", "swelling", "chest pressure", "chest tightness"],
            "respiratory": ["cough", "wheezing", "shortness of breath", "chest tightness", "sputum", "difficulty breathing", "mucus production", "chest discomfort", "chronic cough"],
            "gastrointestinal": ["nausea", "vomiting", "diarrhea", "constipation", "abdominal pain", "bloating", "heartburn", "weight loss", "gas", "mucus in stool", "blood from stoma", "stoma bleeding", "stoma blockage", "no output", "stoma not working", "abdominal distension", "jaundice", "back pain", "loss of appetite"],
            "neurological": ["headache", "dizziness", "confusion", "seizures", "numbness", "weakness", "memory problems", "sensitivity to light", "sensitivity to sound", "aura", "convulsions", "loss of consciousness", "staring", "uncontrollable movements", "pressure", "tightness", "neck pain", "shoulder pain"],
            "musculoskeletal": ["joint pain", "muscle pain", "stiffness", "swelling", "limited mobility", "reduced range of motion", "crepitus", "morning stiffness", "widespread pain", "muscle spasms", "radiating pain", "back pain"],
            "dermatological": ["rash", "itching", "redness", "swelling", "lesions", "dryness", "scaling", "cracking", "inflammation", "red patches", "silver scales", "thickened skin", "nail changes", "pimples", "blackheads", "whiteheads", "cystic lesions", "scarring"],
            "endocrine": ["weight loss", "weight gain", "thirst", "frequent urination", "fatigue", "increased thirst", "blurred vision", "slow healing", "cold intolerance", "heat intolerance", "tremors", "rapid heartbeat", "anxiety", "sweating"],
            "psychiatric": ["anxiety", "depression", "mood changes", "sleep problems", "concentration issues", "worry", "restlessness", "sadness", "loss of interest", "appetite changes", "irritability", "cognitive difficulties"],
            "urological": ["burning urination", "frequent urination", "urinary urgency", "lower abdominal pain", "blood in urine", "difficulty urinating", "weak stream", "incomplete emptying", "severe pain", "fever"],
            "infectious": ["fever", "chills", "body aches", "sore throat", "swollen lymph nodes", "fatigue", "loss of taste", "loss of smell", "headache", "dehydration"],
            "emergency": ["difficulty breathing", "severe pain", "loss of consciousness", "rapid breathing", "low blood pressure", "hives", "severe headache", "sudden weakness", "trouble speaking", "swelling", "rapid heartbeat", "dizziness"]
        }
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process symptom analysis request"""
        if message.get("type") == "analyze_symptoms":
            patient_data = PatientData(**message["patient_data"])
            analysis_result = await self.analyze_patient_data(patient_data)
            
            return {
                "type": "symptom_analysis_result",
                "analysis": analysis_result,
                "agent": self.name
            }
        
        return {"type": "error", "message": "Unknown message type"}
    
    async def analyze_patient_data(self, patient_data: PatientData) -> Dict[str, Any]:
        """Analyze patient symptoms and medical history"""
        analysis = {
            "patient_id": patient_data.patient_id,
            "symptom_categories": self.categorize_symptoms(patient_data.symptoms),
            "severity_assessment": self.assess_symptom_severity(patient_data.symptoms),
            "priority_level": self.determine_priority(patient_data),
            "recommended_specialists": self.recommend_specialists(patient_data.symptoms),
            "analysis_timestamp": patient_data.timestamp.isoformat()
        }
        
        self.log_info(f"Analyzed symptoms for patient {patient_data.patient_id}")
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

class SimpleDiagnosisSpecialist(SimpleAgent):
    """Simplified Diagnosis Specialist Agent"""
    
    def __init__(self):
        super().__init__("DiagnosisSpecialist", "diagnosis")
        self.diagnosis_knowledge = self.load_diagnosis_knowledge()
    
    def load_diagnosis_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Load comprehensive medical diagnosis knowledge base"""
        return {
            # Cardiovascular Conditions
            "myocardial_infarction": {
                "symptoms": ["chest pain", "shortness of breath", "nausea", "sweating", "arm pain", "jaw pain"],
                "risk_factors": ["age > 65", "diabetes", "hypertension", "smoking", "family history", "high cholesterol"],
                "confidence_factors": {"chest_pain": 0.8, "shortness_of_breath": 0.7, "nausea": 0.6}
            },
            "angina": {
                "symptoms": ["chest pain", "chest pressure", "chest tightness", "shortness of breath", "fatigue"],
                "risk_factors": ["age > 65", "diabetes", "hypertension", "smoking", "family history"],
                "confidence_factors": {"chest_pain": 0.7, "chest_pressure": 0.8, "chest_tightness": 0.7}
            },
            "heart_failure": {
                "symptoms": ["shortness of breath", "fatigue", "swelling", "rapid heartbeat", "cough"],
                "risk_factors": ["age > 65", "diabetes", "hypertension", "heart disease", "kidney disease"],
                "confidence_factors": {"shortness_of_breath": 0.8, "fatigue": 0.7, "swelling": 0.6}
            },
            "stroke": {
                "symptoms": ["sudden weakness", "numbness", "confusion", "trouble speaking", "severe headache"],
                "risk_factors": ["age > 65", "diabetes", "hypertension", "smoking", "atrial fibrillation"],
                "confidence_factors": {"sudden_weakness": 0.9, "numbness": 0.8, "confusion": 0.7}
            },
            
            # Respiratory Conditions
            "pneumonia": {
                "symptoms": ["cough", "fever", "shortness of breath", "chest pain", "fatigue", "sputum"],
                "risk_factors": ["age > 65", "immunocompromised", "smoking", "chronic lung disease"],
                "confidence_factors": {"cough": 0.7, "fever": 0.8, "shortness_of_breath": 0.6}
            },
            "asthma": {
                "symptoms": ["wheezing", "shortness of breath", "chest tightness", "cough", "difficulty breathing"],
                "risk_factors": ["family history", "allergies", "smoking", "environmental factors"],
                "confidence_factors": {"wheezing": 0.9, "shortness_of_breath": 0.8, "chest_tightness": 0.7}
            },
            "copd": {
                "symptoms": ["shortness of breath", "chronic cough", "wheezing", "chest tightness", "fatigue"],
                "risk_factors": ["smoking", "age > 65", "occupational exposure", "air pollution"],
                "confidence_factors": {"shortness_of_breath": 0.8, "chronic_cough": 0.7, "wheezing": 0.6}
            },
            "bronchitis": {
                "symptoms": ["cough", "mucus production", "shortness of breath", "chest discomfort", "fatigue"],
                "risk_factors": ["smoking", "viral infection", "air pollution", "weakened immune system"],
                "confidence_factors": {"cough": 0.8, "mucus_production": 0.7, "shortness_of_breath": 0.6}
            },
            
            # Gastrointestinal Conditions
            "gastroenteritis": {
                "symptoms": ["diarrhea", "nausea", "vomiting", "abdominal pain", "fever", "dehydration"],
                "risk_factors": ["food poisoning", "viral infection", "bacterial infection", "travel"],
                "confidence_factors": {"diarrhea": 0.8, "nausea": 0.7, "vomiting": 0.7}
            },
            "peptic_ulcer": {
                "symptoms": ["abdominal pain", "nausea", "vomiting", "bloating", "heartburn", "weight loss"],
                "risk_factors": ["h pylori infection", "nsaids", "smoking", "alcohol", "stress"],
                "confidence_factors": {"abdominal_pain": 0.8, "nausea": 0.6, "heartburn": 0.7}
            },
            "irritable_bowel_syndrome": {
                "symptoms": ["abdominal pain", "bloating", "diarrhea", "constipation", "gas", "mucus in stool"],
                "risk_factors": ["stress", "food sensitivities", "family history", "anxiety"],
                "confidence_factors": {"abdominal_pain": 0.7, "bloating": 0.6, "diarrhea": 0.6}
            },
            "appendicitis": {
                "symptoms": ["abdominal pain", "nausea", "vomiting", "fever", "loss of appetite", "constipation"],
                "risk_factors": ["age 10-30", "male", "family history", "infection"],
                "confidence_factors": {"abdominal_pain": 0.8, "nausea": 0.7, "fever": 0.6}
            },
            "gallstones": {
                "symptoms": ["abdominal pain", "nausea", "vomiting", "fever", "jaundice", "back pain"],
                "risk_factors": ["female", "age > 40", "obesity", "pregnancy", "rapid weight loss"],
                "confidence_factors": {"abdominal_pain": 0.8, "nausea": 0.6, "jaundice": 0.7}
            },
            
            # Neurological Conditions
            "migraine": {
                "symptoms": ["headache", "nausea", "sensitivity to light", "sensitivity to sound", "aura"],
                "risk_factors": ["family history", "female", "stress", "hormonal changes"],
                "confidence_factors": {"headache": 0.8, "nausea": 0.6, "sensitivity_to_light": 0.7}
            },
            "tension_headache": {
                "symptoms": ["headache", "pressure", "tightness", "neck pain", "shoulder pain"],
                "risk_factors": ["stress", "anxiety", "poor posture", "lack of sleep"],
                "confidence_factors": {"headache": 0.7, "pressure": 0.6, "tightness": 0.6}
            },
            "seizure": {
                "symptoms": ["convulsions", "loss of consciousness", "confusion", "staring", "uncontrollable movements"],
                "risk_factors": ["epilepsy", "head injury", "stroke", "brain tumor", "fever"],
                "confidence_factors": {"convulsions": 0.9, "loss_of_consciousness": 0.8, "confusion": 0.6}
            },
            "concussion": {
                "symptoms": ["headache", "confusion", "memory problems", "dizziness", "nausea", "sensitivity to light"],
                "risk_factors": ["head injury", "sports", "falls", "motor vehicle accidents"],
                "confidence_factors": {"headache": 0.8, "confusion": 0.7, "memory_problems": 0.6}
            },
            
            # Urological Conditions
            "urinary_tract_infection": {
                "symptoms": ["burning urination", "frequent urination", "urinary urgency", "lower abdominal pain", "fever"],
                "risk_factors": ["female", "age > 65", "diabetes", "catheter use", "sexual activity"],
                "confidence_factors": {"burning_urination": 0.8, "frequent_urination": 0.7, "urinary_urgency": 0.6}
            },
            "kidney_stones": {
                "symptoms": ["severe pain", "blood in urine", "nausea", "vomiting", "fever", "urinary urgency"],
                "risk_factors": ["dehydration", "family history", "diet high in oxalate", "obesity"],
                "confidence_factors": {"severe_pain": 0.9, "blood_in_urine": 0.8, "nausea": 0.6}
            },
            "prostate_enlargement": {
                "symptoms": ["frequent urination", "difficulty urinating", "weak stream", "incomplete emptying", "urgency"],
                "risk_factors": ["age > 50", "family history", "diabetes", "obesity"],
                "confidence_factors": {"frequent_urination": 0.7, "difficulty_urinating": 0.8, "weak_stream": 0.7}
            },
            
            # Endocrine Conditions
            "diabetes": {
                "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision", "slow healing"],
                "risk_factors": ["family history", "obesity", "age > 45", "sedentary lifestyle", "high blood pressure"],
                "confidence_factors": {"increased_thirst": 0.8, "frequent_urination": 0.7, "fatigue": 0.6}
            },
            "hypothyroidism": {
                "symptoms": ["fatigue", "weight gain", "cold intolerance", "depression", "dry skin", "hair loss"],
                "risk_factors": ["female", "age > 60", "family history", "autoimmune disease"],
                "confidence_factors": {"fatigue": 0.7, "weight_gain": 0.6, "cold_intolerance": 0.7}
            },
            "hyperthyroidism": {
                "symptoms": ["weight loss", "rapid heartbeat", "anxiety", "tremors", "heat intolerance", "sweating"],
                "risk_factors": ["female", "family history", "autoimmune disease", "iodine deficiency"],
                "confidence_factors": {"weight_loss": 0.7, "rapid_heartbeat": 0.8, "anxiety": 0.6}
            },
            
            # Musculoskeletal Conditions
            "osteoarthritis": {
                "symptoms": ["joint pain", "stiffness", "swelling", "reduced range of motion", "crepitus"],
                "risk_factors": ["age > 65", "obesity", "joint injury", "repetitive stress", "family history"],
                "confidence_factors": {"joint_pain": 0.8, "stiffness": 0.7, "swelling": 0.6}
            },
            "rheumatoid_arthritis": {
                "symptoms": ["joint pain", "swelling", "stiffness", "fatigue", "fever", "morning stiffness"],
                "risk_factors": ["female", "age 30-60", "family history", "smoking", "obesity"],
                "confidence_factors": {"joint_pain": 0.8, "swelling": 0.7, "morning_stiffness": 0.8}
            },
            "fibromyalgia": {
                "symptoms": ["widespread pain", "fatigue", "sleep problems", "cognitive difficulties", "headaches"],
                "risk_factors": ["female", "age 30-50", "family history", "stress", "trauma"],
                "confidence_factors": {"widespread_pain": 0.8, "fatigue": 0.7, "sleep_problems": 0.6}
            },
            "back_pain": {
                "symptoms": ["back pain", "stiffness", "muscle spasms", "reduced mobility", "radiating pain"],
                "risk_factors": ["age > 30", "obesity", "sedentary lifestyle", "heavy lifting", "smoking"],
                "confidence_factors": {"back_pain": 0.8, "stiffness": 0.6, "muscle_spasms": 0.6}
            },
            
            # Dermatological Conditions
            "eczema": {
                "symptoms": ["itchy skin", "redness", "dry skin", "scaling", "cracking", "inflammation"],
                "risk_factors": ["family history", "allergies", "asthma", "stress", "irritants"],
                "confidence_factors": {"itchy_skin": 0.9, "redness": 0.7, "dry_skin": 0.6}
            },
            "psoriasis": {
                "symptoms": ["red patches", "silver scales", "itchy skin", "thickened skin", "nail changes"],
                "risk_factors": ["family history", "stress", "infection", "medications", "obesity"],
                "confidence_factors": {"red_patches": 0.8, "silver_scales": 0.9, "itchy_skin": 0.6}
            },
            "acne": {
                "symptoms": ["pimples", "blackheads", "whiteheads", "cystic lesions", "scarring"],
                "risk_factors": ["hormonal changes", "puberty", "stress", "certain medications", "diet"],
                "confidence_factors": {"pimples": 0.8, "blackheads": 0.7, "cystic_lesions": 0.6}
            },
            
            # Stoma-Related Conditions
            "stoma_bleeding": {
                "symptoms": ["blood from stoma", "stoma bleeding", "bleeding stoma", "blood in stoma bag"],
                "risk_factors": ["stoma bag", "colon perforation", "recent surgery", "anticoagulant use"],
                "confidence_factors": {"blood_from_stoma": 0.9, "stoma_bleeding": 0.9, "bleeding_stoma": 0.9}
            },
            "stoma_obstruction": {
                "symptoms": ["stoma blockage", "no output", "stoma not working", "abdominal distension"],
                "risk_factors": ["stoma bag", "colon perforation", "recent surgery", "adhesions"],
                "confidence_factors": {"stoma_blockage": 0.8, "no_output": 0.7, "abdominal_distension": 0.6}
            },
            "stoma_infection": {
                "symptoms": ["stoma infection", "redness around stoma", "stoma pain", "fever"],
                "risk_factors": ["stoma bag", "colon perforation", "recent surgery", "immunocompromised"],
                "confidence_factors": {"stoma_infection": 0.8, "redness_around_stoma": 0.7, "stoma_pain": 0.6}
            },
            
            # Infectious Diseases
            "influenza": {
                "symptoms": ["fever", "cough", "sore throat", "body aches", "fatigue", "headache"],
                "risk_factors": ["seasonal", "immunocompromised", "age > 65", "chronic conditions"],
                "confidence_factors": {"fever": 0.8, "cough": 0.7, "body_aches": 0.7}
            },
            "covid_19": {
                "symptoms": ["fever", "cough", "shortness of breath", "fatigue", "loss of taste", "loss of smell"],
                "risk_factors": ["exposure", "immunocompromised", "age > 65", "chronic conditions"],
                "confidence_factors": {"fever": 0.7, "cough": 0.6, "loss_of_taste": 0.8}
            },
            "mononucleosis": {
                "symptoms": ["fatigue", "sore throat", "fever", "swollen lymph nodes", "headache", "body aches"],
                "risk_factors": ["young adults", "close contact", "kissing", "sharing utensils"],
                "confidence_factors": {"fatigue": 0.8, "sore_throat": 0.7, "swollen_lymph_nodes": 0.8}
            },
            
            # Mental Health Conditions
            "anxiety": {
                "symptoms": ["worry", "restlessness", "fatigue", "difficulty concentrating", "irritability", "sleep problems"],
                "risk_factors": ["stress", "trauma", "family history", "chronic illness", "substance abuse"],
                "confidence_factors": {"worry": 0.8, "restlessness": 0.7, "fatigue": 0.6}
            },
            "depression": {
                "symptoms": ["sadness", "loss of interest", "fatigue", "sleep problems", "appetite changes", "concentration problems"],
                "risk_factors": ["family history", "trauma", "chronic illness", "substance abuse", "stress"],
                "confidence_factors": {"sadness": 0.8, "loss_of_interest": 0.9, "fatigue": 0.7}
            },
            
            # Emergency Conditions
            "anaphylaxis": {
                "symptoms": ["difficulty breathing", "swelling", "hives", "rapid heartbeat", "dizziness", "loss of consciousness"],
                "risk_factors": ["allergies", "food allergies", "medication allergies", "insect stings"],
                "confidence_factors": {"difficulty_breathing": 0.9, "swelling": 0.8, "hives": 0.7}
            },
            "sepsis": {
                "symptoms": ["fever", "rapid heartbeat", "rapid breathing", "confusion", "low blood pressure", "chills"],
                "risk_factors": ["infection", "immunocompromised", "age > 65", "chronic illness"],
                "confidence_factors": {"fever": 0.8, "rapid_heartbeat": 0.7, "confusion": 0.8}
            },
            
            # Additional Cardiovascular Conditions
            "atrial_fibrillation": {
                "symptoms": ["irregular heartbeat", "palpitations", "chest pain", "shortness of breath", "fatigue", "dizziness"],
                "risk_factors": ["age > 65", "hypertension", "heart disease", "diabetes", "thyroid problems"],
                "confidence_factors": {"irregular_heartbeat": 0.9, "palpitations": 0.8, "chest_pain": 0.6}
            },
            "deep_vein_thrombosis": {
                "symptoms": ["leg pain", "leg swelling", "warmth in leg", "redness", "tenderness", "vein prominence"],
                "risk_factors": ["surgery", "immobility", "pregnancy", "birth control", "cancer", "family history"],
                "confidence_factors": {"leg_pain": 0.8, "leg_swelling": 0.9, "warmth_in_leg": 0.7}
            },
            "pulmonary_embolism": {
                "symptoms": ["chest pain", "shortness of breath", "rapid heartbeat", "cough", "blood in sputum", "sweating"],
                "risk_factors": ["DVT", "surgery", "immobility", "cancer", "pregnancy", "birth control"],
                "confidence_factors": {"chest_pain": 0.8, "shortness_of_breath": 0.9, "rapid_heartbeat": 0.7}
            },
            
            # Additional Respiratory Conditions
            "pneumothorax": {
                "symptoms": ["sudden chest pain", "shortness of breath", "rapid heartbeat", "dry cough", "fatigue"],
                "risk_factors": ["tall thin males", "smoking", "lung disease", "trauma", "family history"],
                "confidence_factors": {"sudden_chest_pain": 0.9, "shortness_of_breath": 0.8, "rapid_heartbeat": 0.6}
            },
            "pleural_effusion": {
                "symptoms": ["shortness of breath", "chest pain", "dry cough", "fatigue", "fever"],
                "risk_factors": ["heart failure", "pneumonia", "cancer", "kidney disease", "liver disease"],
                "confidence_factors": {"shortness_of_breath": 0.8, "chest_pain": 0.6, "dry_cough": 0.5}
            },
            
            # Additional Gastrointestinal Conditions
            "crohns_disease": {
                "symptoms": ["abdominal pain", "diarrhea", "weight loss", "fatigue", "fever", "blood in stool"],
                "risk_factors": ["family history", "age 15-35", "smoking", "ethnicity", "urban living"],
                "confidence_factors": {"abdominal_pain": 0.8, "diarrhea": 0.7, "weight_loss": 0.6}
            },
            "ulcerative_colitis": {
                "symptoms": ["diarrhea", "blood in stool", "abdominal pain", "urgency", "fatigue", "weight loss"],
                "risk_factors": ["family history", "age 15-30", "ethnicity", "urban living", "stress"],
                "confidence_factors": {"diarrhea": 0.8, "blood_in_stool": 0.9, "abdominal_pain": 0.7}
            },
            "celiac_disease": {
                "symptoms": ["diarrhea", "abdominal pain", "bloating", "weight loss", "fatigue", "anemia"],
                "risk_factors": ["family history", "type 1 diabetes", "thyroid disease", "down syndrome"],
                "confidence_factors": {"diarrhea": 0.7, "abdominal_pain": 0.6, "bloating": 0.7}
            },
            "diverticulitis": {
                "symptoms": ["abdominal pain", "fever", "nausea", "vomiting", "constipation", "diarrhea"],
                "risk_factors": ["age > 50", "low fiber diet", "obesity", "smoking", "lack of exercise"],
                "confidence_factors": {"abdominal_pain": 0.8, "fever": 0.7, "nausea": 0.6}
            },
            
            # Additional Neurological Conditions
            "parkinsons_disease": {
                "symptoms": ["tremor", "rigidity", "bradykinesia", "postural instability", "depression", "sleep problems"],
                "risk_factors": ["age > 60", "family history", "male", "head trauma", "pesticide exposure"],
                "confidence_factors": {"tremor": 0.9, "rigidity": 0.8, "bradykinesia": 0.8}
            },
            "alzheimers_disease": {
                "symptoms": ["memory loss", "confusion", "difficulty with tasks", "personality changes", "disorientation"],
                "risk_factors": ["age > 65", "family history", "head trauma", "heart disease", "diabetes"],
                "confidence_factors": {"memory_loss": 0.9, "confusion": 0.8, "difficulty_with_tasks": 0.7}
            },
            "multiple_sclerosis": {
                "symptoms": ["fatigue", "numbness", "weakness", "vision problems", "balance problems", "bladder problems"],
                "risk_factors": ["age 20-40", "female", "family history", "vitamin D deficiency", "smoking"],
                "confidence_factors": {"fatigue": 0.8, "numbness": 0.7, "vision_problems": 0.8}
            },
            "bell_palsy": {
                "symptoms": ["facial weakness", "drooping face", "difficulty closing eye", "drooling", "taste changes"],
                "risk_factors": ["diabetes", "pregnancy", "viral infection", "stress", "autoimmune disease"],
                "confidence_factors": {"facial_weakness": 0.9, "drooping_face": 0.9, "difficulty_closing_eye": 0.8}
            },
            
            # Pediatric Conditions
            "croup": {
                "symptoms": ["barking cough", "hoarse voice", "difficulty breathing", "fever", "stridor"],
                "risk_factors": ["age 6 months to 3 years", "viral infection", "winter months"],
                "confidence_factors": {"barking_cough": 0.9, "hoarse_voice": 0.8, "stridor": 0.9}
            },
            "hand_foot_mouth": {
                "symptoms": ["fever", "sore throat", "mouth sores", "rash on hands and feet", "irritability"],
                "risk_factors": ["age under 5", "daycare attendance", "viral exposure"],
                "confidence_factors": {"mouth_sores": 0.9, "rash_hands_feet": 0.9, "fever": 0.7}
            },
            "roseola": {
                "symptoms": ["high fever", "rash after fever breaks", "irritability", "swollen lymph nodes"],
                "risk_factors": ["age 6 months to 2 years", "viral infection"],
                "confidence_factors": {"high_fever": 0.8, "rash_after_fever": 0.9, "irritability": 0.6}
            },
            "kawasaki_disease": {
                "symptoms": ["high fever", "rash", "red eyes", "swollen hands and feet", "strawberry tongue"],
                "risk_factors": ["age under 5", "asian descent", "male gender"],
                "confidence_factors": {"high_fever": 0.8, "strawberry_tongue": 0.9, "red_eyes": 0.8}
            },
            
            # Geriatric Conditions
            "delirium": {
                "symptoms": ["confusion", "disorientation", "agitation", "hallucinations", "fluctuating consciousness"],
                "risk_factors": ["age > 65", "dementia", "infection", "medication changes", "hospitalization"],
                "confidence_factors": {"confusion": 0.8, "disorientation": 0.9, "fluctuating_consciousness": 0.9}
            },
            "falls": {
                "symptoms": ["fall", "injury", "bruising", "pain", "difficulty walking"],
                "risk_factors": ["age > 65", "balance problems", "medications", "vision problems", "home hazards"],
                "confidence_factors": {"fall": 0.9, "injury": 0.8, "difficulty_walking": 0.7}
            },
            "polypharmacy": {
                "symptoms": ["confusion", "dizziness", "falls", "fatigue", "drug interactions"],
                "risk_factors": ["age > 65", "multiple medications", "multiple doctors", "chronic conditions"],
                "confidence_factors": {"confusion": 0.7, "dizziness": 0.8, "drug_interactions": 0.9}
            },
            
            # Pregnancy-Related Conditions
            "preeclampsia": {
                "symptoms": ["high blood pressure", "protein in urine", "swelling", "headache", "vision changes"],
                "risk_factors": ["first pregnancy", "age > 35", "obesity", "diabetes", "family history"],
                "confidence_factors": {"high_blood_pressure": 0.9, "protein_urine": 0.9, "swelling": 0.7}
            },
            "gestational_diabetes": {
                "symptoms": ["increased thirst", "frequent urination", "fatigue", "blurred vision"],
                "risk_factors": ["obesity", "family history", "age > 25", "previous gestational diabetes"],
                "confidence_factors": {"increased_thirst": 0.8, "frequent_urination": 0.7, "fatigue": 0.6}
            },
            "ectopic_pregnancy": {
                "symptoms": ["abdominal pain", "vaginal bleeding", "shoulder pain", "dizziness", "fainting"],
                "risk_factors": ["previous ectopic pregnancy", "pelvic inflammatory disease", "smoking", "age > 35"],
                "confidence_factors": {"abdominal_pain": 0.8, "vaginal_bleeding": 0.7, "shoulder_pain": 0.8}
            },
            
            # Rare and Complex Conditions
            "lupus": {
                "symptoms": ["butterfly rash", "joint pain", "fatigue", "fever", "hair loss", "photosensitivity"],
                "risk_factors": ["female", "age 15-45", "family history", "african american", "hispanic"],
                "confidence_factors": {"butterfly_rash": 0.9, "joint_pain": 0.7, "photosensitivity": 0.8}
            },
            "scleroderma": {
                "symptoms": ["thickened skin", "joint pain", "fatigue", "digestive problems", "shortness of breath"],
                "risk_factors": ["female", "age 30-50", "family history", "environmental exposure"],
                "confidence_factors": {"thickened_skin": 0.9, "joint_pain": 0.7, "digestive_problems": 0.6}
            },
            "sarcoidosis": {
                "symptoms": ["shortness of breath", "cough", "fatigue", "joint pain", "skin lesions"],
                "risk_factors": ["age 20-40", "african american", "family history", "environmental exposure"],
                "confidence_factors": {"shortness_of_breath": 0.8, "cough": 0.7, "skin_lesions": 0.8}
            },
            "guillain_barre": {
                "symptoms": ["weakness", "tingling", "paralysis", "difficulty breathing", "facial weakness"],
                "risk_factors": ["recent infection", "surgery", "vaccination", "age > 50"],
                "confidence_factors": {"weakness": 0.8, "tingling": 0.7, "paralysis": 0.9}
            },
            
            # Mental Health Expansion
            "bipolar_disorder": {
                "symptoms": ["mood swings", "mania", "depression", "irritability", "sleep problems", "racing thoughts"],
                "risk_factors": ["family history", "stress", "substance abuse", "age 15-25"],
                "confidence_factors": {"mood_swings": 0.8, "mania": 0.9, "racing_thoughts": 0.8}
            },
            "ptsd": {
                "symptoms": ["flashbacks", "nightmares", "anxiety", "avoidance", "hypervigilance", "mood changes"],
                "risk_factors": ["trauma", "military service", "abuse", "accidents", "natural disasters"],
                "confidence_factors": {"flashbacks": 0.9, "nightmares": 0.8, "hypervigilance": 0.8}
            },
            "ocd": {
                "symptoms": ["obsessions", "compulsions", "anxiety", "repetitive behaviors", "intrusive thoughts"],
                "risk_factors": ["family history", "stress", "trauma", "age 19-20"],
                "confidence_factors": {"obsessions": 0.9, "compulsions": 0.9, "repetitive_behaviors": 0.8}
            },
            "eating_disorder": {
                "symptoms": ["weight changes", "body image issues", "food restriction", "binge eating", "purging"],
                "risk_factors": ["female", "age 12-25", "family history", "perfectionism", "societal pressure"],
                "confidence_factors": {"weight_changes": 0.7, "body_image_issues": 0.8, "food_restriction": 0.8}
            },
            
            # Emergency and Trauma
            "shock": {
                "symptoms": ["low blood pressure", "rapid heartbeat", "confusion", "cold skin", "weakness"],
                "risk_factors": ["severe injury", "blood loss", "infection", "heart attack", "allergic reaction"],
                "confidence_factors": {"low_blood_pressure": 0.9, "rapid_heartbeat": 0.8, "cold_skin": 0.8}
            },
            "heat_stroke": {
                "symptoms": ["high body temperature", "confusion", "nausea", "rapid heartbeat", "headache"],
                "risk_factors": ["hot weather", "dehydration", "strenuous activity", "age > 65", "medications"],
                "confidence_factors": {"high_temperature": 0.9, "confusion": 0.8, "rapid_heartbeat": 0.7}
            },
            "hypothermia": {
                "symptoms": ["low body temperature", "shivering", "confusion", "slurred speech", "weakness"],
                "risk_factors": ["cold exposure", "age > 65", "alcohol use", "medications", "medical conditions"],
                "confidence_factors": {"low_temperature": 0.9, "shivering": 0.8, "confusion": 0.7}
            },
            "carbon_monoxide_poisoning": {
                "symptoms": ["headache", "nausea", "confusion", "dizziness", "chest pain", "flu-like symptoms"],
                "risk_factors": ["faulty heating", "generator use", "car exhaust", "poor ventilation"],
                "confidence_factors": {"headache": 0.8, "confusion": 0.8, "flu_like_symptoms": 0.7}
            },
            
            # Drug and Substance Related
            "drug_overdose": {
                "symptoms": ["unconsciousness", "slow breathing", "pinpoint pupils", "confusion", "seizures"],
                "risk_factors": ["substance abuse", "mental health issues", "prescription medications", "accidental ingestion"],
                "confidence_factors": {"unconsciousness": 0.9, "slow_breathing": 0.8, "pinpoint_pupils": 0.9}
            },
            "alcohol_withdrawal": {
                "symptoms": ["tremors", "anxiety", "nausea", "sweating", "hallucinations", "seizures"],
                "risk_factors": ["heavy alcohol use", "sudden cessation", "previous withdrawal", "medical conditions"],
                "confidence_factors": {"tremors": 0.8, "anxiety": 0.7, "hallucinations": 0.9}
            },
            "opioid_withdrawal": {
                "symptoms": ["muscle aches", "anxiety", "nausea", "sweating", "diarrhea", "insomnia"],
                "risk_factors": ["opioid use", "sudden cessation", "previous withdrawal", "chronic pain"],
                "confidence_factors": {"muscle_aches": 0.8, "anxiety": 0.7, "diarrhea": 0.8}
            }
        }
    
    async def process_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Process diagnosis request"""
        if message.get("type") == "request_diagnosis":
            patient_data = PatientData(**message["patient_data"])
            symptom_analysis = message.get("symptom_analysis", {})
            
            diagnosis_result = await self.generate_diagnosis(patient_data, symptom_analysis)
            
            return {
                "type": "diagnosis_result",
                "diagnoses": diagnosis_result,
                "agent": self.name
            }
        
        return {"type": "error", "message": "Unknown message type"}
    
    async def generate_diagnosis(self, patient_data: PatientData, symptom_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate diagnosis based on symptoms and analysis"""
        possible_diagnoses = self.identify_possible_diagnoses(patient_data.symptoms)
        diagnoses = []
        
        for diagnosis_name in possible_diagnoses:
            diagnosis_info = self.diagnosis_knowledge[diagnosis_name]
            confidence = self.calculate_confidence(patient_data, diagnosis_info)
            
            if confidence > 0.3:  # Only include diagnoses with reasonable confidence
                diagnosis = {
                    "condition": diagnosis_name.replace("_", " ").title(),
                    "confidence": confidence,
                    "reasoning": self.generate_reasoning(patient_data, diagnosis_info, confidence),
                    "supporting_evidence": self.identify_supporting_evidence(patient_data, diagnosis_info),
                    "differential_diagnoses": self.get_differential_diagnoses(diagnosis_name, patient_data.symptoms),
                    "urgency": self.assess_urgency(diagnosis_name, patient_data)
                }
                diagnoses.append(diagnosis)
        
        # Sort by confidence
        diagnoses.sort(key=lambda x: x["confidence"], reverse=True)
        self.log_info(f"Generated {len(diagnoses)} diagnoses for patient {patient_data.patient_id}")
        return diagnoses[:3]  # Return top 3 diagnoses
    
    def identify_possible_diagnoses(self, symptoms: List[str]) -> List[str]:
        """Identify possible diagnoses based on symptoms"""
        possible_diagnoses = set()
        
        for symptom in symptoms:
            symptom_lower = symptom.lower()
            for diagnosis_name, diagnosis_info in self.diagnosis_knowledge.items():
                for diagnosis_symptom in diagnosis_info["symptoms"]:
                    if diagnosis_symptom in symptom_lower:
                        possible_diagnoses.add(diagnosis_name)
        
        return list(possible_diagnoses)
    
    def calculate_confidence(self, patient_data: PatientData, diagnosis_info: Dict[str, Any]) -> float:
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
        
        # Confidence reasoning
        if confidence > 0.7:
            reasoning_parts.append("High confidence based on symptom presentation")
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
            for diagnosis_name, diagnosis_info in self.diagnosis_knowledge.items():
                if diagnosis_name != primary_diagnosis:
                    for diagnosis_symptom in diagnosis_info["symptoms"]:
                        if diagnosis_symptom in symptom_lower:
                            if diagnosis_name not in differentials:
                                differentials.append(diagnosis_name.replace("_", " ").title())
        
        return differentials[:2]  # Return top 2 differentials
    
    def assess_urgency(self, diagnosis_name: str, patient_data: PatientData) -> str:
        """Assess urgency of the diagnosis"""
        urgent_conditions = ["myocardial_infarction", "pneumonia", "stroke"]
        
        if diagnosis_name in urgent_conditions:
            return "urgent"
        elif patient_data.age > 65:
            return "moderate"
        else:
            return "routine"

# Global agent instances
symptom_analyzer = SimpleSymptomAnalyzer()
diagnosis_specialist = SimpleDiagnosisSpecialist()
