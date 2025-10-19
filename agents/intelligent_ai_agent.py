#!/usr/bin/env python3
"""
Intelligent AI Agent - Never Fails to Provide Results
This agent can interpret ANY symptom input and provide intelligent analysis
"""

import asyncio
import re
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class SymptomCategory(Enum):
    EMERGENCY = "emergency"
    URGENT = "urgent"
    ROUTINE = "routine"
    NON_URGENT = "non_urgent"

@dataclass
class IntelligentSymptom:
    """Intelligent symptom interpretation"""
    original_text: str
    interpreted_symptoms: List[str]
    category: SymptomCategory
    confidence: float
    reasoning: str
    related_conditions: List[str]

class IntelligentAIAgent:
    """AI Agent that can interpret ANY symptom and provide intelligent analysis"""
    
    def __init__(self):
        self.logger = logging.getLogger("IntelligentAI")
        self.symptom_patterns = self._load_intelligent_patterns()
        self.emergency_keywords = self._load_emergency_keywords()
        self.general_medical_knowledge = self._load_general_medical_knowledge()
        
    def _load_intelligent_patterns(self) -> Dict[str, List[str]]:
        """Load intelligent symptom patterns for interpretation"""
        return {
            # Color-related symptoms
            "pale_complexion": ["white", "pale", "pallor", "ashen", "gray", "wan", "sallow"],
            "redness": ["red", "flushed", "rosy", "crimson", "scarlet"],
            "yellowing": ["yellow", "jaundiced", "icteric", "golden"],
            "blue_tint": ["blue", "cyanotic", "bluish", "purple"],
            
            # Appearance-related
            "swelling": ["swollen", "puffy", "inflated", "enlarged", "bulging"],
            "rash": ["rash", "spots", "bumps", "lesions", "patches"],
            "dryness": ["dry", "flaky", "scaly", "rough", "cracked"],
            "moisture": ["wet", "moist", "sweaty", "damp", "sticky"],
            
            # Pain-related
            "pain": ["pain", "ache", "hurt", "sore", "tender", "throbbing"],
            "sharp_pain": ["sharp", "stabbing", "piercing", "cutting"],
            "dull_pain": ["dull", "aching", "heavy", "pressure"],
            "burning": ["burning", "hot", "fire", "scorching"],
            
            # Movement-related
            "weakness": ["weak", "tired", "exhausted", "fatigued", "lethargic"],
            "stiffness": ["stiff", "rigid", "tight", "tense", "frozen"],
            "tremor": ["shaking", "trembling", "quivering", "vibrating"],
            "numbness": ["numb", "tingling", "pins and needles", "dead"],
            
            # Breathing-related
            "breathing_problems": ["breath", "breathing", "air", "oxygen", "suffocating"],
            "cough": ["cough", "coughing", "hacking", "clearing throat"],
            "wheezing": ["wheezing", "whistling", "rattling", "gurgling"],
            
            # Digestive-related
            "nausea": ["nausea", "sick", "queasy", "upset stomach"],
            "vomiting": ["vomit", "throwing up", "puking", "regurgitating"],
            "diarrhea": ["diarrhea", "loose stools", "watery", "runny"],
            "constipation": ["constipation", "blocked", "hard stools", "straining"],
            
            # Neurological
            "headache": ["headache", "head pain", "migraine", "head pounding"],
            "dizziness": ["dizzy", "lightheaded", "spinning", "vertigo"],
            "confusion": ["confused", "disoriented", "foggy", "unclear"],
            "memory_problems": ["memory", "forgetful", "amnesia", "recall"],
            
            # Cardiovascular
            "chest_pain": ["chest", "heart", "cardiac", "thoracic"],
            "palpitations": ["heartbeat", "pounding", "racing", "irregular"],
            "swelling_legs": ["swollen legs", "puffy feet", "ankle swelling"],
            
            # General symptoms
            "fever": ["fever", "hot", "temperature", "burning up"],
            "chills": ["chills", "shivering", "cold", "freezing"],
            "fatigue": ["tired", "exhausted", "worn out", "drained", "weak", "lethargic", "sluggish"],
            "weight_changes": ["weight", "gained", "lost", "heavier", "lighter", "thinner", "fatter"],
            
            # Additional comprehensive symptom patterns
            "pain_patterns": ["pain", "ache", "hurt", "sore", "tender", "throbbing", "stabbing", "burning", "sharp", "dull"],
            "breathing_issues": ["breath", "breathe", "panting", "gasping", "wheezing", "coughing", "choking", "suffocating"],
            "digestive_symptoms": ["stomach", "belly", "gut", "nausea", "vomit", "diarrhea", "constipation", "bloating", "gas"],
            "neurological_symptoms": ["head", "brain", "dizzy", "confused", "memory", "thinking", "balance", "coordination"],
            "skin_conditions": ["skin", "rash", "itchy", "red", "swollen", "bumps", "spots", "patches", "scales"],
            "urinary_symptoms": ["urine", "pee", "bladder", "kidney", "burning", "frequent", "urgency", "incontinence"],
            "reproductive_symptoms": ["period", "menstrual", "pregnancy", "fertility", "hormone", "menopause"],
            "mental_health": ["anxiety", "depression", "stress", "panic", "mood", "emotion", "feeling", "thoughts"],
            "sleep_issues": ["sleep", "insomnia", "tired", "restless", "nightmare", "snoring", "apnea"],
            "vision_hearing": ["vision", "sight", "eye", "blind", "hearing", "ear", "deaf", "ringing", "tinnitus"],
            "mobility_issues": ["walk", "move", "mobility", "stiff", "frozen", "paralyzed", "numb", "tingling"],
            "emergency_symptoms": ["emergency", "urgent", "critical", "severe", "unbearable", "intense", "can't", "unable"]
        }
    
    def _load_emergency_keywords(self) -> List[str]:
        """Load emergency keywords for immediate attention"""
        return [
            "emergency", "urgent", "critical", "severe", "unbearable", "intense",
            "can't breathe", "can't walk", "can't move", "unconscious", "fainting",
            "chest pain", "heart attack", "stroke", "bleeding", "severe pain",
            "allergic reaction", "anaphylaxis", "seizure", "convulsions",
            "unresponsive", "not responding", "no response", "unconscious",
            "coma", "collapsed", "passed out", "blacked out", "lost consciousness",
            "not breathing", "stopped breathing", "choking", "suffocating",
            "severe bleeding", "massive bleeding", "bleeding heavily",
            "severe allergic reaction", "swelling throat", "can't swallow",
            "severe chest pain", "crushing chest pain", "heart attack symptoms",
            "stroke symptoms", "facial drooping", "arm weakness", "speech difficulty"
        ]
    
    def _load_general_medical_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Load general medical knowledge for any symptom"""
        return {
            "general_conditions": {
                "medical_emergency": {
                    "symptoms": ["unresponsive", "unconscious", "not responding", "coma", "collapsed"],
                    "treatment": "IMMEDIATE EMERGENCY MEDICAL ATTENTION - Call 911 immediately",
                    "urgency": "emergency"
                },
                "cardiac_emergency": {
                    "symptoms": ["chest pain", "heart attack", "crushing chest pain", "severe chest pain"],
                    "treatment": "IMMEDIATE EMERGENCY MEDICAL ATTENTION - Call 911, administer aspirin if conscious",
                    "urgency": "emergency"
                },
                "stroke_emergency": {
                    "symptoms": ["stroke", "facial drooping", "arm weakness", "speech difficulty", "sudden weakness"],
                    "treatment": "IMMEDIATE EMERGENCY MEDICAL ATTENTION - Call 911, note time of onset",
                    "urgency": "emergency"
                },
                "respiratory_emergency": {
                    "symptoms": ["can't breathe", "not breathing", "choking", "suffocating", "stopped breathing"],
                    "treatment": "IMMEDIATE EMERGENCY MEDICAL ATTENTION - Call 911, begin CPR if trained",
                    "urgency": "emergency"
                },
                "allergic_emergency": {
                    "symptoms": ["severe allergic reaction", "anaphylaxis", "swelling throat", "can't swallow"],
                    "treatment": "IMMEDIATE EMERGENCY MEDICAL ATTENTION - Call 911, use epinephrine if available",
                    "urgency": "emergency"
                },
                "dehydration": {
                    "symptoms": ["pale", "white", "dry", "tired", "weak"],
                    "treatment": "Increase fluid intake, monitor hydration",
                    "urgency": "moderate"
                },
                "anemia": {
                    "symptoms": ["pale", "white", "tired", "weak", "fatigue"],
                    "treatment": "Iron supplements, dietary changes, medical evaluation",
                    "urgency": "routine"
                },
                "metabolic_disorder": {
                    "symptoms": ["pale", "white", "tired", "weak", "fatigue", "weight changes"],
                    "treatment": "Medical evaluation, blood tests, dietary assessment",
                    "urgency": "moderate"
                },
                "vitamin_deficiency": {
                    "symptoms": ["pale", "tired", "weak", "fatigue", "hair loss", "brittle nails"],
                    "treatment": "Vitamin supplements, dietary changes, medical evaluation",
                    "urgency": "routine"
                },
                "thyroid_disorder": {
                    "symptoms": ["pale", "tired", "weight changes", "mood changes", "temperature sensitivity"],
                    "treatment": "Thyroid function tests, hormone replacement if needed",
                    "urgency": "moderate"
                },
                "heart_condition": {
                    "symptoms": ["pale", "tired", "shortness of breath", "chest discomfort", "fatigue"],
                    "treatment": "Cardiac evaluation, ECG, echocardiogram, medical management",
                    "urgency": "urgent"
                },
                "kidney_disease": {
                    "symptoms": ["pale", "tired", "swelling", "urinary changes", "fatigue"],
                    "treatment": "Kidney function tests, dietary modifications, medical management",
                    "urgency": "moderate"
                },
                "liver_disease": {
                    "symptoms": ["pale", "tired", "yellowing", "abdominal discomfort", "fatigue"],
                    "treatment": "Liver function tests, dietary changes, medical evaluation",
                    "urgency": "moderate"
                },
                "cancer": {
                    "symptoms": ["pale", "tired", "weight loss", "fatigue", "unexplained symptoms"],
                    "treatment": "Comprehensive medical evaluation, imaging studies, specialist referral",
                    "urgency": "urgent"
                },
                "autoimmune_disease": {
                    "symptoms": ["pale", "tired", "joint pain", "fatigue", "general malaise"],
                    "treatment": "Autoimmune panel, specialist referral, immune modulation",
                    "urgency": "moderate"
                },
                "chronic_fatigue": {
                    "symptoms": ["tired", "fatigue", "weak", "exhausted", "sleep problems"],
                    "treatment": "Sleep study, stress management, gradual activity increase",
                    "urgency": "routine"
                },
                "depression": {
                    "symptoms": ["tired", "fatigue", "mood changes", "sleep problems", "appetite changes"],
                    "treatment": "Mental health evaluation, counseling, medication if needed",
                    "urgency": "moderate"
                },
                "sleep_disorder": {
                    "symptoms": ["tired", "fatigue", "sleep problems", "daytime sleepiness"],
                    "treatment": "Sleep study, sleep hygiene, medical evaluation",
                    "urgency": "routine"
                },
                "diabetes": {
                    "symptoms": ["tired", "thirst", "frequent urination", "weight changes", "fatigue"],
                    "treatment": "Blood glucose monitoring, dietary changes, medication if needed",
                    "urgency": "moderate"
                },
                "hypertension": {
                    "symptoms": ["tired", "headache", "dizziness", "fatigue", "chest discomfort"],
                    "treatment": "Blood pressure monitoring, lifestyle changes, medication if needed",
                    "urgency": "moderate"
                },
                "infection": {
                    "symptoms": ["tired", "fever", "fatigue", "general malaise", "body aches"],
                    "treatment": "Infection workup, antibiotics if bacterial, supportive care",
                    "urgency": "moderate"
                },
                
                # AI-Powered Universal Fallbacks
                "general_medical_condition": {
                    "symptoms": ["any", "symptom", "presentation", "complaint"],
                    "treatment": "Comprehensive medical evaluation, diagnostic workup, specialist referral if needed",
                    "urgency": "moderate"
                },
                "symptom_of_unknown_origin": {
                    "symptoms": ["unexplained", "unclear", "vague", "nonspecific"],
                    "treatment": "Detailed history, physical examination, laboratory studies, imaging if indicated",
                    "urgency": "moderate"
                },
                "chronic_condition": {
                    "symptoms": ["persistent", "ongoing", "chronic", "long-term"],
                    "treatment": "Chronic disease management, regular monitoring, lifestyle modifications",
                    "urgency": "routine"
                },
                "acute_condition": {
                    "symptoms": ["sudden", "acute", "recent", "new onset"],
                    "treatment": "Immediate evaluation, acute management, monitoring for complications",
                    "urgency": "urgent"
                },
                "psychosomatic_condition": {
                    "symptoms": ["stress-related", "anxiety-related", "psychosomatic", "functional"],
                    "treatment": "Stress management, counseling, relaxation techniques, medical evaluation",
                    "urgency": "routine"
                },
                "medication_side_effect": {
                    "symptoms": ["drug-related", "medication-related", "side effect", "adverse reaction"],
                    "treatment": "Medication review, dose adjustment, alternative medications, monitoring",
                    "urgency": "moderate"
                },
                "allergic_reaction": {
                    "symptoms": ["allergic", "hypersensitivity", "reaction", "intolerance"],
                    "treatment": "Allergen avoidance, antihistamines, epinephrine if severe, allergy testing",
                    "urgency": "urgent"
                },
                "deficiency_disorder": {
                    "symptoms": ["deficiency", "malnutrition", "vitamin", "mineral"],
                    "treatment": "Nutritional assessment, supplementation, dietary counseling, monitoring",
                    "urgency": "routine"
                },
                "hormonal_imbalance": {
                    "symptoms": ["hormonal", "endocrine", "metabolic", "hormone"],
                    "treatment": "Hormone testing, endocrine evaluation, hormone replacement if needed",
                    "urgency": "moderate"
                },
                "inflammatory_condition": {
                    "symptoms": ["inflammatory", "inflammation", "swelling", "redness"],
                    "treatment": "Anti-inflammatory medications, rest, ice, elevation, medical evaluation",
                    "urgency": "moderate"
                },
                "degenerative_condition": {
                    "symptoms": ["degenerative", "progressive", "worsening", "chronic"],
                    "treatment": "Symptom management, physical therapy, adaptive devices, regular monitoring",
                    "urgency": "routine"
                },
                "genetic_condition": {
                    "symptoms": ["genetic", "hereditary", "familial", "inherited"],
                    "treatment": "Genetic counseling, family history assessment, specialized care, monitoring",
                    "urgency": "moderate"
                },
                "environmental_exposure": {
                    "symptoms": ["environmental", "exposure", "toxin", "pollutant"],
                    "treatment": "Exposure cessation, decontamination, supportive care, monitoring",
                    "urgency": "urgent"
                },
                "occupational_condition": {
                    "symptoms": ["occupational", "work-related", "job-related", "industrial"],
                    "treatment": "Workplace evaluation, protective measures, medical monitoring, job modification",
                    "urgency": "moderate"
                },
                "lifestyle_related": {
                    "symptoms": ["lifestyle", "diet-related", "exercise-related", "stress-related"],
                    "treatment": "Lifestyle modifications, dietary changes, exercise program, stress management",
                    "urgency": "routine"
                },
                "age_related": {
                    "symptoms": ["age-related", "aging", "elderly", "pediatric"],
                    "treatment": "Age-appropriate care, specialized evaluation, family involvement, monitoring",
                    "urgency": "moderate"
                },
                "gender_specific": {
                    "symptoms": ["gender-specific", "male-specific", "female-specific", "reproductive"],
                    "treatment": "Gender-appropriate evaluation, specialized care, reproductive health assessment",
                    "urgency": "moderate"
                },
                "seasonal_condition": {
                    "symptoms": ["seasonal", "weather-related", "climate-related", "environmental"],
                    "treatment": "Seasonal management, environmental modifications, preventive measures",
                    "urgency": "routine"
                },
                "travel_related": {
                    "symptoms": ["travel-related", "tropical", "imported", "exotic"],
                    "treatment": "Travel history assessment, tropical medicine evaluation, specialized testing",
                    "urgency": "moderate"
                },
                "immunocompromised": {
                    "symptoms": ["immunocompromised", "immunosuppressed", "immune", "defense"],
                    "treatment": "Immunocompromised care, infection prevention, specialized monitoring",
                    "urgency": "urgent"
                },
                "stress_anxiety": {
                    "symptoms": ["tired", "weak", "nervous", "worried", "tense"],
                    "treatment": "Stress management, relaxation, counseling",
                    "urgency": "routine"
                },
                "vitamin_deficiency": {
                    "symptoms": ["tired", "weak", "pale", "dry", "brittle"],
                    "treatment": "Vitamin supplements, dietary changes",
                    "urgency": "routine"
                },
                "circulation_problems": {
                    "symptoms": ["pale", "white", "cold", "numb", "tingling"],
                    "treatment": "Improve circulation, medical evaluation",
                    "urgency": "moderate"
                },
                "metabolic_disorder": {
                    "symptoms": ["tired", "weak", "pale", "weight changes"],
                    "treatment": "Medical evaluation, blood tests, treatment",
                    "urgency": "moderate"
                }
            }
        }
    
    async def analyze_any_symptom(self, symptom_text: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze ANY symptom text and provide intelligent interpretation"""
        try:
            # Step 1: Intelligent symptom interpretation
            interpreted_symptom = self._interpret_symptom_intelligently(symptom_text)
            
            # Step 2: Generate possible conditions
            possible_conditions = self._generate_possible_conditions(interpreted_symptom, patient_data)
            
            # Step 3: Assess urgency and risk
            urgency_assessment = self._assess_urgency_intelligently(interpreted_symptom, patient_data)
            
            # Step 4: Generate treatment recommendations
            treatment_recommendations = self._generate_treatment_recommendations(possible_conditions, patient_data)
            
            # Step 5: Provide general medical advice
            general_advice = self._provide_general_medical_advice(interpreted_symptom, patient_data)
            
            return {
                "symptom_interpretation": interpreted_symptom,
                "possible_conditions": possible_conditions,
                "urgency_assessment": urgency_assessment,
                "treatment_recommendations": treatment_recommendations,
                "general_advice": general_advice,
                "confidence_score": self._calculate_confidence_score(interpreted_symptom, possible_conditions),
                "ai_reasoning": self._generate_ai_reasoning(interpreted_symptom, possible_conditions)
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing symptom: {str(e)}")
            # Fallback: Always provide some analysis
            return self._provide_fallback_analysis(symptom_text, patient_data)
    
    def _interpret_symptom_intelligently(self, symptom_text: str) -> IntelligentSymptom:
        """Intelligently interpret any symptom text"""
        symptom_lower = symptom_text.lower()
        
        # Find matching patterns
        interpreted_symptoms = []
        category = SymptomCategory.ROUTINE
        confidence = 0.5
        reasoning = "General symptom analysis"
        related_conditions = []
        
        # Check for emergency keywords first
        for emergency_word in self.emergency_keywords:
            if emergency_word in symptom_lower:
                category = SymptomCategory.EMERGENCY
                confidence = 0.95  # Higher confidence for emergency detection
                reasoning = f"EMERGENCY: Critical symptom detected - {emergency_word}"
                break
        
        # Pattern matching
        for pattern_name, keywords in self.symptom_patterns.items():
            for keyword in keywords:
                if keyword in symptom_lower:
                    interpreted_symptoms.append(pattern_name)
                    if category == SymptomCategory.ROUTINE:
                        category = SymptomCategory.URGENT if "pain" in pattern_name or "breathing" in pattern_name else SymptomCategory.ROUTINE
                    confidence = max(confidence, 0.7)
                    reasoning = f"Pattern matched: {pattern_name} (keyword: {keyword})"
                    break
        
        # If no patterns matched, use general interpretation
        if not interpreted_symptoms:
            interpreted_symptoms = ["general_symptom"]
            reasoning = "General symptom interpretation - no specific patterns detected"
            confidence = 0.3
        
        # Generate related conditions based on interpreted symptoms
        related_conditions = self._get_related_conditions(interpreted_symptoms)
        
        return IntelligentSymptom(
            original_text=symptom_text,
            interpreted_symptoms=interpreted_symptoms,
            category=category,
            confidence=confidence,
            reasoning=reasoning,
            related_conditions=related_conditions
        )
    
    def _generate_possible_conditions(self, interpreted_symptom: IntelligentSymptom, patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate possible medical conditions based on interpreted symptoms"""
        conditions = []
        
        # Check against general medical knowledge
        for condition_name, condition_info in self.general_medical_knowledge["general_conditions"].items():
            symptom_match_score = 0
            total_symptoms = len(condition_info["symptoms"])
            
            for interpreted_symptom_name in interpreted_symptom.interpreted_symptoms:
                for condition_symptom in condition_info["symptoms"]:
                    if condition_symptom in interpreted_symptom_name or interpreted_symptom_name in condition_symptom:
                        symptom_match_score += 1
                        break
            
            # Calculate confidence based on symptom matches
            if symptom_match_score > 0:
                confidence = min(symptom_match_score / total_symptoms + 0.3, 0.9)
                
                # Adjust confidence based on patient data
                if patient_data.get("age", 0) > 65:
                    confidence += 0.1  # Higher risk for elderly
                
                if len(patient_data.get("medical_history", [])) > 2:
                    confidence += 0.1  # Multiple comorbidities
                
                conditions.append({
                    "condition": condition_name.replace("_", " ").title(),
                    "confidence": min(confidence, 1.0),
                    "urgency": condition_info["urgency"],
                    "treatment": condition_info["treatment"],
                    "reasoning": f"Based on symptom pattern matching and general medical knowledge",
                    "supporting_evidence": condition_info["symptoms"]
                })
        
        # If no conditions found, provide general assessment
        if not conditions:
            conditions.append({
                "condition": "General Medical Assessment",
                "confidence": 0.4,
                "urgency": "routine",
                "treatment": "Medical evaluation recommended",
                "reasoning": "Symptom requires medical evaluation for proper diagnosis",
                "supporting_evidence": ["Symptom presentation", "Patient history"]
            })
        
        # Sort by confidence
        conditions.sort(key=lambda x: x["confidence"], reverse=True)
        return conditions[:3]  # Top 3 conditions
    
    def _assess_urgency_intelligently(self, interpreted_symptom: IntelligentSymptom, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Comprehensive AI-powered risk assessment for any symptom"""
        urgency = "routine"
        risk_factors = []
        risk_score = 0.0
        risk_details = {}
        
        # 1. EMERGENCY SYMPTOM ANALYSIS
        if interpreted_symptom.category == SymptomCategory.EMERGENCY:
            urgency = "emergency"
            risk_score = 0.95
            risk_factors.append("Critical emergency symptom detected")
            risk_details["emergency_type"] = self._identify_emergency_type(interpreted_symptom.original_text)
            risk_details["immediate_actions"] = self._get_emergency_actions(interpreted_symptom.original_text)
        
        # 2. SYMPTOM-SPECIFIC RISK ANALYSIS
        symptom_risk = self._analyze_symptom_specific_risks(interpreted_symptom.original_text, patient_data)
        risk_factors.extend(symptom_risk["factors"])
        risk_score += symptom_risk["score"]
        risk_details.update(symptom_risk["details"])
        
        # 3. PATIENT DEMOGRAPHIC RISK ASSESSMENT
        demographic_risk = self._assess_demographic_risks(patient_data)
        risk_factors.extend(demographic_risk["factors"])
        risk_score += demographic_risk["score"]
        risk_details.update(demographic_risk["details"])
        
        # 4. MEDICAL HISTORY RISK ANALYSIS
        history_risk = self._analyze_medical_history_risks(patient_data)
        risk_factors.extend(history_risk["factors"])
        risk_score += history_risk["score"]
        risk_details.update(history_risk["details"])
        
        # 5. MEDICATION INTERACTION RISKS
        medication_risk = self._assess_medication_risks(patient_data)
        risk_factors.extend(medication_risk["factors"])
        risk_score += medication_risk["score"]
        risk_details.update(medication_risk["details"])
        
        # 6. COMPREHENSIVE RISK STRATIFICATION
        risk_stratification = self._perform_risk_stratification(risk_score, risk_factors, patient_data)
        
        # 7. DETERMINE URGENCY LEVEL
        if risk_score >= 0.8:
            urgency = "emergency"
        elif risk_score >= 0.6:
            urgency = "urgent"
        elif risk_score >= 0.4:
            urgency = "moderate"
        else:
            urgency = "routine"
        
        return {
            "urgency": urgency,
            "overall_risk": risk_stratification["level"],
            "risk_factors": risk_factors,
            "risk_score": min(risk_score, 1.0),
            "risk_details": risk_details,
            "risk_stratification": risk_stratification,
            "recommendations": self._generate_risk_recommendations(urgency, risk_score, risk_factors)
        }
    
    def _generate_treatment_recommendations(self, conditions: List[Dict[str, Any]], patient_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate treatment recommendations for any condition"""
        treatments = []
        
        for condition in conditions:
            if condition["confidence"] > 0.4:  # Only recommend treatments for conditions with reasonable confidence
                treatments.append({
                    "treatment_type": "general",
                    "condition": condition["condition"],
                    "recommendation": condition["treatment"],
                    "confidence": condition["confidence"],
                    "urgency": condition["urgency"],
                    "instructions": f"Based on {condition['condition']} assessment",
                    "side_effects": ["Monitor for improvement or worsening"],
                    "contraindications": ["Allergic reactions to recommended treatments"]
                })
        
        # Always provide general supportive care
        treatments.append({
            "treatment_type": "supportive",
            "condition": "General Supportive Care",
            "recommendation": "Rest, adequate hydration, monitor symptoms",
            "confidence": 0.8,
            "urgency": "routine",
            "instructions": "General supportive measures for symptom management",
            "side_effects": [],
            "contraindications": []
        })
        
        return treatments
    
    def _provide_general_medical_advice(self, interpreted_symptom: IntelligentSymptom, patient_data: Dict[str, Any]) -> List[str]:
        """Provide general medical advice for any symptom"""
        advice = []
        
        # General advice based on symptom category
        if interpreted_symptom.category == SymptomCategory.EMERGENCY:
            advice.extend([
                "IMMEDIATE EMERGENCY - Call 911 immediately",
                "Do not delay - this is a medical emergency",
                "Stay with the patient until emergency services arrive",
                "If trained, begin CPR if patient is not breathing"
            ])
        elif interpreted_symptom.category == SymptomCategory.URGENT:
            advice.extend([
                "Schedule medical evaluation within 24-48 hours",
                "Monitor symptoms closely",
                "Seek immediate care if symptoms worsen"
            ])
        else:
            advice.extend([
                "Schedule routine medical evaluation",
                "Monitor symptoms for changes",
                "Maintain healthy lifestyle habits"
            ])
        
        # Age-specific advice
        age = patient_data.get("age", 0)
        if age > 65:
            advice.append("Elderly patients should be monitored more closely")
        
        # Condition-specific advice
        medical_history = patient_data.get("medical_history", [])
        if "diabetes" in " ".join(medical_history).lower():
            advice.append("Monitor blood glucose levels closely")
        if "hypertension" in " ".join(medical_history).lower():
            advice.append("Monitor blood pressure regularly")
        
        return advice
    
    def _calculate_confidence_score(self, interpreted_symptom: IntelligentSymptom, conditions: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score"""
        if not conditions:
            return 0.3
        
        # Base confidence on symptom interpretation
        base_confidence = interpreted_symptom.confidence
        
        # Adjust based on condition confidence
        avg_condition_confidence = sum(c["confidence"] for c in conditions) / len(conditions)
        
        # Combined confidence
        combined_confidence = (base_confidence + avg_condition_confidence) / 2
        
        return min(combined_confidence, 1.0)
    
    def _generate_ai_reasoning(self, interpreted_symptom: IntelligentSymptom, conditions: List[Dict[str, Any]]) -> str:
        """Generate AI reasoning for the analysis"""
        reasoning_parts = []
        
        reasoning_parts.append(f"AI interpreted '{interpreted_symptom.original_text}' as: {', '.join(interpreted_symptom.interpreted_symptoms)}")
        reasoning_parts.append(f"Confidence in interpretation: {interpreted_symptom.confidence:.2f}")
        reasoning_parts.append(f"Reasoning: {interpreted_symptom.reasoning}")
        
        if conditions:
            top_condition = conditions[0]
            reasoning_parts.append(f"Most likely condition: {top_condition['condition']} (confidence: {top_condition['confidence']:.2f})")
        
        return ". ".join(reasoning_parts) + "."
    
    def _get_related_conditions(self, interpreted_symptoms: List[str]) -> List[str]:
        """Get related conditions based on interpreted symptoms"""
        related = []
        
        for symptom in interpreted_symptoms:
            if "pale" in symptom or "white" in symptom:
                related.extend(["anemia", "dehydration", "circulation problems", "shock"])
            elif "pain" in symptom:
                related.extend(["inflammation", "injury", "infection", "chronic pain"])
            elif "breathing" in symptom:
                related.extend(["respiratory infection", "asthma", "allergic reaction"])
            elif "tired" in symptom or "weak" in symptom:
                related.extend(["fatigue", "anemia", "infection", "metabolic disorder"])
        
        return list(set(related))  # Remove duplicates
    
    def _provide_fallback_analysis(self, symptom_text: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Provide fallback analysis when main analysis fails"""
        return {
            "symptom_interpretation": {
                "original_text": symptom_text,
                "interpreted_symptoms": ["general_symptom"],
                "category": "routine",
                "confidence": 0.3,
                "reasoning": "Fallback analysis - symptom requires medical evaluation"
            },
            "possible_conditions": [{
                "condition": "Medical Evaluation Required",
                "confidence": 0.5,
                "urgency": "routine",
                "treatment": "Schedule medical evaluation for proper diagnosis",
                "reasoning": "Symptom requires professional medical assessment",
                "supporting_evidence": ["Symptom presentation", "Patient history"]
            }],
            "urgency_assessment": {
                "urgency": "routine",
                "overall_risk": "low",
                "risk_score": 0.3,
                "risk_factors": ["Symptom requires evaluation"],
                "reasoning": "Routine medical evaluation recommended"
            },
            "treatment_recommendations": [{
                "treatment_type": "evaluation",
                "condition": "Medical Assessment",
                "recommendation": "Schedule medical evaluation",
                "confidence": 0.8,
                "urgency": "routine",
                "instructions": "Professional medical evaluation recommended",
                "side_effects": [],
                "contraindications": []
            }],
            "general_advice": [
                "Schedule medical evaluation",
                "Monitor symptoms for changes",
                "Seek immediate care if symptoms worsen"
            ],
            "confidence_score": 0.4,
            "ai_reasoning": f"Fallback analysis for symptom: {symptom_text}. Medical evaluation recommended for proper diagnosis."
        }
    
    def _identify_emergency_type(self, symptom: str) -> str:
        """Identify the type of emergency based on symptom"""
        symptom_lower = symptom.lower()
        
        if any(word in symptom_lower for word in ["unresponsive", "unconscious", "coma", "collapsed"]):
            return "Loss of Consciousness"
        elif any(word in symptom_lower for word in ["chest pain", "heart attack", "crushing"]):
            return "Cardiac Emergency"
        elif any(word in symptom_lower for word in ["can't breathe", "choking", "suffocating"]):
            return "Respiratory Emergency"
        elif any(word in symptom_lower for word in ["stroke", "facial drooping", "arm weakness"]):
            return "Neurological Emergency"
        elif any(word in symptom_lower for word in ["severe bleeding", "massive bleeding"]):
            return "Hemorrhagic Emergency"
        elif any(word in symptom_lower for word in ["allergic reaction", "anaphylaxis", "swelling throat"]):
            return "Allergic Emergency"
        else:
            return "General Medical Emergency"
    
    def _get_emergency_actions(self, symptom: str) -> List[str]:
        """Get immediate actions for emergency symptoms"""
        emergency_type = self._identify_emergency_type(symptom)
        
        actions = ["Call 911 immediately", "Stay with the patient"]
        
        if emergency_type == "Loss of Consciousness":
            actions.extend(["Check breathing and pulse", "Begin CPR if trained and no pulse"])
        elif emergency_type == "Cardiac Emergency":
            actions.extend(["Administer aspirin if conscious", "Keep patient calm and still"])
        elif emergency_type == "Respiratory Emergency":
            actions.extend(["Check airway", "Begin rescue breathing if trained"])
        elif emergency_type == "Neurological Emergency":
            actions.extend(["Note time of onset", "Keep patient still", "Do not give food or water"])
        elif emergency_type == "Hemorrhagic Emergency":
            actions.extend(["Apply direct pressure to bleeding", "Elevate injured area if possible"])
        elif emergency_type == "Allergic Emergency":
            actions.extend(["Use epinephrine auto-injector if available", "Monitor breathing"])
        
        return actions
    
    def _analyze_symptom_specific_risks(self, symptom: str, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risks specific to the symptom type"""
        risk_factors = []
        risk_score = 0.0
        details = {}
        
        symptom_lower = symptom.lower()
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "").lower()
        
        # Cardiovascular symptoms
        if any(word in symptom_lower for word in ["chest", "heart", "pain", "pressure"]):
            risk_score += 0.3
            risk_factors.append("Cardiovascular symptom presentation")
            if age > 50:
                risk_score += 0.2
                risk_factors.append("Age-related cardiovascular risk")
            if gender == "male":
                risk_score += 0.1
                risk_factors.append("Male gender cardiovascular risk")
            details["cardiovascular_risk"] = "High - requires immediate evaluation"
        
        # Neurological symptoms
        elif any(word in symptom_lower for word in ["head", "brain", "dizzy", "confused", "weakness"]):
            risk_score += 0.25
            risk_factors.append("Neurological symptom presentation")
            if age > 65:
                risk_score += 0.2
                risk_factors.append("Age-related neurological risk")
            details["neurological_risk"] = "Moderate to high - requires evaluation"
        
        # Respiratory symptoms
        elif any(word in symptom_lower for word in ["breath", "cough", "wheeze", "shortness"]):
            risk_score += 0.2
            risk_factors.append("Respiratory symptom presentation")
            if age > 70:
                risk_score += 0.15
                risk_factors.append("Age-related respiratory risk")
            details["respiratory_risk"] = "Moderate - monitor closely"
        
        # Gastrointestinal symptoms
        elif any(word in symptom_lower for word in ["stomach", "nausea", "vomit", "diarrhea", "abdominal"]):
            risk_score += 0.15
            risk_factors.append("Gastrointestinal symptom presentation")
            if age > 60:
                risk_score += 0.1
                risk_factors.append("Age-related GI risk")
            details["gi_risk"] = "Low to moderate - monitor hydration"
        
        # General symptoms (pain, fatigue, etc.)
        else:
            risk_score += 0.1
            risk_factors.append("General symptom presentation")
            details["general_risk"] = "Low - routine evaluation recommended"
        
        return {
            "factors": risk_factors,
            "score": risk_score,
            "details": details
        }
    
    def _assess_demographic_risks(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks based on patient demographics"""
        risk_factors = []
        risk_score = 0.0
        details = {}
        
        age = patient_data.get("age", 0)
        gender = patient_data.get("gender", "").lower()
        
        # Age-based risk assessment
        if age >= 80:
            risk_score += 0.3
            risk_factors.append("Very advanced age (80+)")
            details["age_risk"] = "Very high - increased vulnerability"
        elif age >= 70:
            risk_score += 0.2
            risk_factors.append("Advanced age (70-79)")
            details["age_risk"] = "High - increased medical risk"
        elif age >= 60:
            risk_score += 0.15
            risk_factors.append("Elderly (60-69)")
            details["age_risk"] = "Moderate - age-related risk factors"
        elif age >= 50:
            risk_score += 0.1
            risk_factors.append("Middle-aged (50-59)")
            details["age_risk"] = "Low to moderate - baseline risk"
        elif age < 18:
            risk_score += 0.1
            risk_factors.append("Pediatric patient")
            details["age_risk"] = "Special considerations for pediatric care"
        
        # Gender-based risk factors
        if gender == "male":
            risk_score += 0.05
            risk_factors.append("Male gender - higher cardiovascular risk")
            details["gender_risk"] = "Increased cardiovascular risk"
        elif gender == "female":
            risk_score += 0.03
            risk_factors.append("Female gender - hormonal considerations")
            details["gender_risk"] = "Hormonal and reproductive health considerations"
        
        return {
            "factors": risk_factors,
            "score": risk_score,
            "details": details
        }
    
    def _analyze_medical_history_risks(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze risks based on medical history"""
        risk_factors = []
        risk_score = 0.0
        details = {}
        
        medical_history = patient_data.get("medical_history", [])
        
        # High-risk chronic conditions
        high_risk_conditions = {
            "diabetes": {"score": 0.2, "description": "Diabetes - metabolic complications risk"},
            "hypertension": {"score": 0.15, "description": "Hypertension - cardiovascular risk"},
            "heart disease": {"score": 0.25, "description": "Heart disease - cardiac complications risk"},
            "kidney disease": {"score": 0.2, "description": "Kidney disease - renal complications risk"},
            "liver disease": {"score": 0.2, "description": "Liver disease - hepatic complications risk"},
            "cancer": {"score": 0.3, "description": "Cancer history - increased vulnerability"},
            "stroke": {"score": 0.25, "description": "Stroke history - neurological risk"},
            "copd": {"score": 0.2, "description": "COPD - respiratory complications risk"},
            "asthma": {"score": 0.15, "description": "Asthma - respiratory risk"},
            "depression": {"score": 0.1, "description": "Depression - mental health considerations"},
            "anxiety": {"score": 0.1, "description": "Anxiety - mental health considerations"}
        }
        
        for condition in medical_history:
            condition_lower = condition.lower()
            for risk_condition, risk_data in high_risk_conditions.items():
                if risk_condition in condition_lower:
                    risk_score += risk_data["score"]
                    risk_factors.append(risk_data["description"])
                    details[f"condition_{risk_condition}"] = f"High risk due to {condition}"
        
        # Multiple conditions risk
        if len(medical_history) >= 3:
            risk_score += 0.15
            risk_factors.append("Multiple chronic conditions - increased complexity")
            details["multiple_conditions"] = "High complexity due to multiple comorbidities"
        
        return {
            "factors": risk_factors,
            "score": risk_score,
            "details": details
        }
    
    def _assess_medication_risks(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks based on current medications"""
        risk_factors = []
        risk_score = 0.0
        details = {}
        
        medications = patient_data.get("current_medications", [])
        
        # High-risk medication categories
        high_risk_medications = {
            "warfarin": {"score": 0.2, "description": "Anticoagulant - bleeding risk"},
            "insulin": {"score": 0.15, "description": "Insulin - hypoglycemia risk"},
            "digoxin": {"score": 0.15, "description": "Digoxin - cardiac toxicity risk"},
            "lithium": {"score": 0.2, "description": "Lithium - toxicity risk"},
            "methotrexate": {"score": 0.2, "description": "Methotrexate - toxicity risk"},
            "prednisone": {"score": 0.1, "description": "Steroid - immunosuppression risk"},
            "opioid": {"score": 0.15, "description": "Opioid - respiratory depression risk"}
        }
        
        for medication in medications:
            medication_lower = medication.lower()
            for risk_med, risk_data in high_risk_medications.items():
                if risk_med in medication_lower:
                    risk_score += risk_data["score"]
                    risk_factors.append(risk_data["description"])
                    details[f"medication_{risk_med}"] = f"High risk medication: {medication}"
        
        # Multiple medications risk
        if len(medications) >= 5:
            risk_score += 0.1
            risk_factors.append("Polypharmacy - drug interaction risk")
            details["polypharmacy"] = "High risk of drug interactions"
        
        return {
            "factors": risk_factors,
            "score": risk_score,
            "details": details
        }
    
    def _perform_risk_stratification(self, risk_score: float, risk_factors: List[str], patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive risk stratification"""
        
        # Determine risk level
        if risk_score >= 0.8:
            risk_level = "critical"
            risk_description = "Critical risk - immediate medical attention required"
        elif risk_score >= 0.6:
            risk_level = "high"
            risk_description = "High risk - urgent medical evaluation needed"
        elif risk_score >= 0.4:
            risk_level = "moderate"
            risk_description = "Moderate risk - medical evaluation recommended"
        elif risk_score >= 0.2:
            risk_level = "low"
            risk_description = "Low risk - routine medical follow-up"
        else:
            risk_level = "minimal"
            risk_description = "Minimal risk - self-monitoring sufficient"
        
        # Risk categories
        risk_categories = {
            "demographic": [f for f in risk_factors if any(word in f.lower() for word in ["age", "gender", "pediatric"])],
            "medical_history": [f for f in risk_factors if any(word in f.lower() for word in ["diabetes", "hypertension", "heart", "kidney", "cancer"])],
            "medications": [f for f in risk_factors if any(word in f.lower() for word in ["medication", "drug", "anticoagulant", "insulin"])],
            "symptom_specific": [f for f in risk_factors if any(word in f.lower() for word in ["symptom", "presentation", "emergency"])]
        }
        
        return {
            "level": risk_level,
            "description": risk_description,
            "score": risk_score,
            "categories": risk_categories,
            "total_factors": len(risk_factors),
            "primary_concerns": risk_factors[:3] if risk_factors else ["No specific risk factors identified"]
        }
    
    def _generate_risk_recommendations(self, urgency: str, risk_score: float, risk_factors: List[str]) -> List[str]:
        """Generate specific recommendations based on risk assessment"""
        recommendations = []
        
        if urgency == "emergency":
            recommendations.extend([
                "IMMEDIATE EMERGENCY MEDICAL ATTENTION REQUIRED",
                "Call 911 immediately",
                "Do not delay medical care",
                "Stay with patient until emergency services arrive"
            ])
        elif urgency == "urgent":
            recommendations.extend([
                "Seek medical attention within 24 hours",
                "Monitor symptoms closely",
                "Go to emergency room if symptoms worsen",
                "Contact healthcare provider immediately"
            ])
        elif urgency == "moderate":
            recommendations.extend([
                "Schedule medical evaluation within 48-72 hours",
                "Monitor symptoms and vital signs",
                "Seek immediate care if symptoms worsen",
                "Consider urgent care if primary care unavailable"
            ])
        else:
            recommendations.extend([
                "Schedule routine medical follow-up",
                "Monitor symptoms at home",
                "Seek medical attention if symptoms persist or worsen",
                "Maintain regular health monitoring"
            ])
        
        # Add specific recommendations based on risk factors
        if any("diabetes" in factor.lower() for factor in risk_factors):
            recommendations.append("Monitor blood glucose levels closely")
        
        if any("heart" in factor.lower() for factor in risk_factors):
            recommendations.append("Monitor heart rate and blood pressure")
        
        if any("breathing" in factor.lower() for factor in risk_factors):
            recommendations.append("Monitor respiratory rate and oxygen saturation")
        
        if any("age" in factor.lower() for factor in risk_factors):
            recommendations.append("Consider age-related vulnerability factors")
        
        return recommendations
