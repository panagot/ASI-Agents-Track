"""
Risk Assessment Agent - Evaluates potential complications and urgency
"""

import json
from typing import Dict, List, Any
from agents.base_agent import BaseHealthcareAgent, PatientData
from uagents import Context
import logging

logger = logging.getLogger(__name__)

class RiskAssessment(BaseHealthcareAgent):
    """Agent that assesses patient risk and potential complications"""
    
    def __init__(self, seed_phrase: str):
        super().__init__("RiskAssessment", "risk_assessment", seed_phrase)
        self.risk_factors = self.load_risk_factors()
        self.complication_models = self.load_complication_models()
    
    def load_risk_factors(self) -> Dict[str, Dict[str, Any]]:
        """Load risk factor database"""
        return {
            "cardiovascular": {
                "age": {"high": 65, "moderate": 45},
                "conditions": ["diabetes", "hypertension", "heart disease", "smoking"],
                "medications": ["warfarin", "aspirin", "clopidogrel"],
                "vital_signs": {
                    "blood_pressure": {"high": 140, "moderate": 130},
                    "heart_rate": {"high": 100, "low": 50}
                }
            },
            "respiratory": {
                "age": {"high": 65, "moderate": 45},
                "conditions": ["asthma", "copd", "smoking", "immunocompromised"],
                "vital_signs": {
                    "oxygen_saturation": {"low": 90},
                    "respiratory_rate": {"high": 25, "low": 12}
                }
            },
            "infectious": {
                "age": {"high": 65, "moderate": 45},
                "conditions": ["immunocompromised", "diabetes", "chronic_kidney_disease"],
                "vital_signs": {
                    "temperature": {"high": 100.4, "low": 96.8}
                }
            }
        }
    
    def load_complication_models(self) -> Dict[str, Dict[str, Any]]:
        """Load complication prediction models"""
        return {
            "myocardial_infarction": {
                "complications": [
                    {
                        "name": "Heart Failure",
                        "risk_factors": ["age > 65", "diabetes", "previous MI"],
                        "probability": 0.15,
                        "severity": "high"
                    },
                    {
                        "name": "Arrhythmia",
                        "risk_factors": ["age > 65", "heart disease"],
                        "probability": 0.25,
                        "severity": "moderate"
                    },
                    {
                        "name": "Cardiogenic Shock",
                        "risk_factors": ["age > 75", "diabetes", "previous MI"],
                        "probability": 0.05,
                        "severity": "critical"
                    }
                ]
            },
            "pneumonia": {
                "complications": [
                    {
                        "name": "Respiratory Failure",
                        "risk_factors": ["age > 65", "copd", "immunocompromised"],
                        "probability": 0.20,
                        "severity": "high"
                    },
                    {
                        "name": "Sepsis",
                        "risk_factors": ["age > 65", "diabetes", "immunocompromised"],
                        "probability": 0.10,
                        "severity": "critical"
                    },
                    {
                        "name": "Pleural Effusion",
                        "risk_factors": ["age > 65", "heart failure"],
                        "probability": 0.15,
                        "severity": "moderate"
                    }
                ]
            }
        }
    
    async def handle_text_message(self, ctx: Context, sender: str, text: str):
        """Handle incoming text messages"""
        try:
            message_data = json.loads(text)
            
            if message_data.get("type") == "assess_risk":
                patient_data = PatientData(**message_data["patient_data"])
                diagnoses = message_data["diagnoses"]
                
                risk_result = await self.assess_patient_risk(patient_data, diagnoses)
                
                response = {
                    "type": "risk_assessment_result",
                    "risk_analysis": risk_result,
                    "case_id": message_data.get("case_id"),
                    "agent": self.name
                }
                await self.send_message(ctx, sender, json.dumps(response))
                
        except json.JSONDecodeError:
            if "risk" in text.lower():
                await self.send_message(ctx, sender, f"{self.name}: Ready to assess risk. Please provide patient data and diagnoses.")
        except Exception as e:
            logger.error(f"Error in RiskAssessment: {e}")
            await self.send_message(ctx, sender, f"{self.name}: Error processing risk assessment request.")
    
    async def assess_patient_risk(self, patient_data: PatientData, diagnoses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Comprehensive risk assessment"""
        risk_analysis = {
            "overall_risk": "low",
            "risk_factors": [],
            "complications": [],
            "monitoring_required": [],
            "urgency_level": "routine",
            "confidence": 0.0,
            "risk_score": 0.0
        }
        
        # Assess risk factors
        risk_factors = self.identify_risk_factors(patient_data)
        risk_analysis["risk_factors"] = risk_factors
        
        # Assess complications for each diagnosis
        complications = []
        for diagnosis in diagnoses:
            if diagnosis["confidence"] > 0.5:
                condition = diagnosis["condition"].lower().replace(" ", "_")
                if condition in self.complication_models:
                    condition_complications = self.assess_complications(patient_data, condition)
                    complications.extend(condition_complications)
        
        risk_analysis["complications"] = complications
        
        # Determine overall risk level
        risk_analysis["overall_risk"] = self.determine_overall_risk(risk_factors, complications)
        
        # Determine urgency level
        risk_analysis["urgency_level"] = self.determine_urgency(patient_data, diagnoses, complications)
        
        # Generate monitoring recommendations
        risk_analysis["monitoring_required"] = self.generate_monitoring_recommendations(patient_data, complications)
        
        # Calculate risk score and confidence
        risk_analysis["risk_score"] = self.calculate_risk_score(risk_factors, complications)
        risk_analysis["confidence"] = self.calculate_confidence(patient_data, diagnoses)
        
        return risk_analysis
    
    def identify_risk_factors(self, patient_data: PatientData) -> List[str]:
        """Identify patient risk factors"""
        risk_factors = []
        
        # Age-based risks
        if patient_data.age > 65:
            risk_factors.append("Advanced age (>65)")
        elif patient_data.age < 18:
            risk_factors.append("Pediatric patient")
        
        # Medical history risks
        for condition in patient_data.medical_history:
            condition_lower = condition.lower()
            if any(keyword in condition_lower for keyword in ["diabetes", "heart", "kidney", "liver", "lung"]):
                risk_factors.append(f"Chronic condition: {condition}")
        
        # Medication risks
        if len(patient_data.current_medications) > 3:
            risk_factors.append("Polypharmacy (>3 medications)")
        
        # Vital signs risks
        if "vital_signs" in patient_data.dict():
            vital_signs = patient_data.vital_signs
            if "blood_pressure" in vital_signs:
                bp = vital_signs["blood_pressure"]
                if isinstance(bp, str) and "/" in bp:
                    systolic = int(bp.split("/")[0])
                    if systolic > 140:
                        risk_factors.append("Hypertension")
            
            if "heart_rate" in vital_signs:
                hr = vital_signs["heart_rate"]
                if hr > 100:
                    risk_factors.append("Tachycardia")
                elif hr < 50:
                    risk_factors.append("Bradycardia")
            
            if "oxygen_saturation" in vital_signs:
                o2_sat = vital_signs["oxygen_saturation"]
                if o2_sat < 90:
                    risk_factors.append("Hypoxemia")
        
        return risk_factors
    
    def assess_complications(self, patient_data: PatientData, condition: str) -> List[Dict[str, Any]]:
        """Assess potential complications for a specific condition"""
        complications = []
        
        if condition in self.complication_models:
            condition_complications = self.complication_models[condition]["complications"]
            
            for complication in condition_complications:
                # Check if patient has risk factors for this complication
                risk_factor_count = 0
                for risk_factor in complication["risk_factors"]:
                    if self.check_risk_factor(patient_data, risk_factor):
                        risk_factor_count += 1
                
                # Calculate adjusted probability based on risk factors
                adjusted_probability = complication["probability"]
                if risk_factor_count > 0:
                    adjusted_probability *= (1 + risk_factor_count * 0.2)
                
                if adjusted_probability > 0.1:  # Only include complications with >10% probability
                    complications.append({
                        "name": complication["name"],
                        "probability": min(adjusted_probability, 1.0),
                        "severity": complication["severity"],
                        "risk_factors_present": risk_factor_count,
                        "condition": condition.replace("_", " ").title()
                    })
        
        return complications
    
    def check_risk_factor(self, patient_data: PatientData, risk_factor: str) -> bool:
        """Check if patient has a specific risk factor"""
        risk_factor_lower = risk_factor.lower()
        
        # Age-based risk factors
        if "age > 65" in risk_factor_lower:
            return patient_data.age > 65
        elif "age > 75" in risk_factor_lower:
            return patient_data.age > 75
        
        # Medical history risk factors
        for condition in patient_data.medical_history:
            if any(keyword in condition.lower() for keyword in risk_factor_lower.split()):
                return True
        
        # Medication risk factors
        for medication in patient_data.current_medications:
            if any(keyword in medication.lower() for keyword in risk_factor_lower.split()):
                return True
        
        return False
    
    def determine_overall_risk(self, risk_factors: List[str], complications: List[Dict[str, Any]]) -> str:
        """Determine overall risk level"""
        risk_score = 0
        
        # Count risk factors
        risk_score += len(risk_factors)
        
        # Count high-severity complications
        high_severity_complications = [c for c in complications if c["severity"] in ["high", "critical"]]
        risk_score += len(high_severity_complications) * 2
        
        # Count moderate-severity complications
        moderate_severity_complications = [c for c in complications if c["severity"] == "moderate"]
        risk_score += len(moderate_severity_complications)
        
        if risk_score >= 5:
            return "high"
        elif risk_score >= 2:
            return "moderate"
        else:
            return "low"
    
    def determine_urgency(self, patient_data: PatientData, diagnoses: List[Dict[str, Any]], complications: List[Dict[str, Any]]) -> str:
        """Determine urgency level for patient care"""
        # Check for critical complications
        critical_complications = [c for c in complications if c["severity"] == "critical"]
        if critical_complications:
            return "urgent"
        
        # Check for high-confidence urgent diagnoses
        urgent_conditions = ["myocardial infarction", "stroke", "sepsis"]
        for diagnosis in diagnoses:
            if diagnosis["confidence"] > 0.7:
                condition_lower = diagnosis["condition"].lower()
                if any(urgent_condition in condition_lower for urgent_condition in urgent_conditions):
                    return "urgent"
        
        # Check for high-risk patients
        if patient_data.age > 75 or len(patient_data.current_medications) > 4:
            return "moderate"
        
        return "routine"
    
    def generate_monitoring_recommendations(self, patient_data: PatientData, complications: List[Dict[str, Any]]) -> List[str]:
        """Generate monitoring recommendations based on risk assessment"""
        monitoring = []
        
        # Age-based monitoring
        if patient_data.age > 65:
            monitoring.append("Close vital signs monitoring")
            monitoring.append("Frequent assessment for deterioration")
        
        # Complication-based monitoring
        for complication in complications:
            if complication["severity"] == "critical":
                monitoring.append(f"Continuous monitoring for {complication['name']}")
            elif complication["severity"] == "high":
                monitoring.append(f"Frequent monitoring for {complication['name']}")
        
        # General monitoring
        monitoring.extend([
            "Regular symptom assessment",
            "Medication adherence monitoring",
            "Follow-up appointment scheduling"
        ])
        
        return list(set(monitoring))  # Remove duplicates
    
    def calculate_risk_score(self, risk_factors: List[str], complications: List[Dict[str, Any]]) -> float:
        """Calculate numerical risk score"""
        score = 0.0
        
        # Base score from risk factors
        score += len(risk_factors) * 0.1
        
        # Add complication scores
        for complication in complications:
            if complication["severity"] == "critical":
                score += 0.3
            elif complication["severity"] == "high":
                score += 0.2
            elif complication["severity"] == "moderate":
                score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def calculate_confidence(self, patient_data: PatientData, diagnoses: List[Dict[str, Any]]) -> float:
        """Calculate confidence in risk assessment"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence with more data
        if len(patient_data.symptoms) > 2:
            confidence += 0.1
        if len(patient_data.medical_history) > 0:
            confidence += 0.1
        if len(patient_data.current_medications) > 0:
            confidence += 0.1
        
        # Increase confidence with high-confidence diagnoses
        if diagnoses:
            avg_diagnosis_confidence = sum(d["confidence"] for d in diagnoses) / len(diagnoses)
            confidence += avg_diagnosis_confidence * 0.2
        
        return min(confidence, 1.0)  # Cap at 1.0

# Create and run the agent
if __name__ == "__main__":
    risk_assessor = RiskAssessment("risk assessment agent seed phrase")
    risk_assessor.run()

