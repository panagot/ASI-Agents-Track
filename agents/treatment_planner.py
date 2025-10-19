"""
Treatment Planner Agent - Recommends treatment options based on diagnoses
"""

import json
from typing import Dict, List, Any
from agents.base_agent import BaseHealthcareAgent, PatientData, Treatment
from uagents import Context
import logging

logger = logging.getLogger(__name__)

class TreatmentPlanner(BaseHealthcareAgent):
    """Agent that plans treatments based on diagnoses and patient data"""
    
    def __init__(self, seed_phrase: str):
        super().__init__("TreatmentPlanner", "treatment_planning", seed_phrase)
        self.treatment_knowledge = self.load_treatment_knowledge()
        self.medication_interactions = self.load_medication_interactions()
    
    def load_treatment_knowledge(self) -> Dict[str, Dict[str, Any]]:
        """Load treatment knowledge base"""
        return {
            "myocardial_infarction": {
                "acute_treatment": [
                    {
                        "medication": "Aspirin",
                        "dosage": "325mg",
                        "route": "oral",
                        "frequency": "once daily",
                        "duration": "indefinite",
                        "instructions": "Take with food to reduce stomach irritation",
                        "side_effects": ["Stomach upset", "Bleeding risk"],
                        "contraindications": ["Active bleeding", "Allergy to aspirin"]
                    },
                    {
                        "medication": "Clopidogrel",
                        "dosage": "75mg",
                        "route": "oral",
                        "frequency": "once daily",
                        "duration": "12 months",
                        "instructions": "Take with or without food",
                        "side_effects": ["Bleeding risk", "Bruising"],
                        "contraindications": ["Active bleeding", "Severe liver disease"]
                    }
                ],
                "lifestyle_modifications": [
                    "Smoking cessation",
                    "Regular exercise program",
                    "Heart-healthy diet",
                    "Stress management",
                    "Weight management"
                ],
                "monitoring": [
                    "Regular follow-up appointments",
                    "Cardiac rehabilitation",
                    "Medication adherence monitoring",
                    "Symptom monitoring"
                ]
            },
            "pneumonia": {
                "acute_treatment": [
                    {
                        "medication": "Amoxicillin",
                        "dosage": "500mg",
                        "route": "oral",
                        "frequency": "three times daily",
                        "duration": "7-10 days",
                        "instructions": "Take with food to reduce stomach upset",
                        "side_effects": ["Nausea", "Diarrhea", "Allergic reactions"],
                        "contraindications": ["Penicillin allergy"]
                    }
                ],
                "supportive_care": [
                    "Rest and hydration",
                    "Fever management",
                    "Cough suppression if needed",
                    "Oxygen therapy if indicated"
                ],
                "monitoring": [
                    "Temperature monitoring",
                    "Respiratory rate monitoring",
                    "Oxygen saturation monitoring",
                    "Response to treatment assessment"
                ]
            },
            "migraine": {
                "acute_treatment": [
                    {
                        "medication": "Sumatriptan",
                        "dosage": "50mg",
                        "route": "oral",
                        "frequency": "as needed",
                        "duration": "per episode",
                        "instructions": "Take at first sign of migraine",
                        "side_effects": ["Chest tightness", "Dizziness", "Nausea"],
                        "contraindications": ["Coronary artery disease", "Uncontrolled hypertension"]
                    }
                ],
                "preventive_treatment": [
                    {
                        "medication": "Propranolol",
                        "dosage": "40mg",
                        "route": "oral",
                        "frequency": "twice daily",
                        "duration": "3-6 months",
                        "instructions": "Take with food",
                        "side_effects": ["Fatigue", "Dizziness", "Cold hands/feet"],
                        "contraindications": ["Asthma", "Heart failure", "Diabetes"]
                    }
                ],
                "lifestyle_modifications": [
                    "Regular sleep schedule",
                    "Stress management",
                    "Avoid trigger foods",
                    "Regular exercise"
                ]
            }
        }
    
    def load_medication_interactions(self) -> Dict[str, List[str]]:
        """Load medication interaction database"""
        return {
            "aspirin": ["warfarin", "clopidogrel", "ibuprofen"],
            "metformin": ["contrast dye", "alcohol"],
            "lisinopril": ["potassium supplements", "salt substitutes"],
            "warfarin": ["aspirin", "clopidogrel", "green leafy vegetables"]
        }
    
    async def handle_text_message(self, ctx: Context, sender: str, text: str):
        """Handle incoming text messages"""
        try:
            message_data = json.loads(text)
            
            if message_data.get("type") == "request_treatment":
                patient_data = PatientData(**message_data["patient_data"])
                diagnoses = message_data["diagnoses"]
                symptom_analysis = message_data.get("symptom_analysis", {})
                
                treatment_result = await self.generate_treatment_plan(patient_data, diagnoses, symptom_analysis)
                
                response = {
                    "type": "treatment_result",
                    "treatments": treatment_result,
                    "case_id": message_data.get("case_id"),
                    "agent": self.name
                }
                await self.send_message(ctx, sender, json.dumps(response))
                
        except json.JSONDecodeError:
            if "treatment" in text.lower():
                await self.send_message(ctx, sender, f"{self.name}: Ready to plan treatment. Please provide patient data and diagnoses.")
        except Exception as e:
            logger.error(f"Error in TreatmentPlanner: {e}")
            await self.send_message(ctx, sender, f"{self.name}: Error processing treatment request.")
    
    async def generate_treatment_plan(self, patient_data: PatientData, diagnoses: List[Dict[str, Any]], symptom_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate comprehensive treatment plan"""
        treatments = []
        
        # Process each diagnosis
        for diagnosis in diagnoses:
            if diagnosis["confidence"] > 0.5:  # Only treat high-confidence diagnoses
                condition = diagnosis["condition"].lower().replace(" ", "_")
                
                if condition in self.treatment_knowledge:
                    treatment_info = self.treatment_knowledge[condition]
                    
                    # Add medications
                    if "acute_treatment" in treatment_info:
                        for med in treatment_info["acute_treatment"]:
                            # Check for interactions
                            interactions = self.check_medication_interactions(med["medication"], patient_data.current_medications)
                            
                            treatment = {
                                "treatment_type": "medication",
                                "medication": med["medication"],
                                "dosage": med["dosage"],
                                "route": med["route"],
                                "frequency": med["frequency"],
                                "duration": med["duration"],
                                "instructions": med["instructions"],
                                "side_effects": med["side_effects"],
                                "contraindications": med["contraindications"],
                                "interactions": interactions,
                                "for_condition": diagnosis["condition"]
                            }
                            treatments.append(treatment)
                    
                    # Add lifestyle modifications
                    if "lifestyle_modifications" in treatment_info:
                        for modification in treatment_info["lifestyle_modifications"]:
                            treatment = {
                                "treatment_type": "lifestyle",
                                "instructions": modification,
                                "for_condition": diagnosis["condition"]
                            }
                            treatments.append(treatment)
                    
                    # Add monitoring recommendations
                    if "monitoring" in treatment_info:
                        for monitoring in treatment_info["monitoring"]:
                            treatment = {
                                "treatment_type": "monitoring",
                                "instructions": monitoring,
                                "for_condition": diagnosis["condition"]
                            }
                            treatments.append(treatment)
        
        # Add general recommendations
        general_treatments = self.generate_general_recommendations(patient_data, symptom_analysis)
        treatments.extend(general_treatments)
        
        return treatments
    
    def check_medication_interactions(self, new_medication: str, current_medications: List[str]) -> List[str]:
        """Check for medication interactions"""
        interactions = []
        new_med_lower = new_medication.lower()
        
        if new_med_lower in self.medication_interactions:
            for current_med in current_medications:
                current_med_lower = current_med.lower()
                if current_med_lower in self.medication_interactions[new_med_lower]:
                    interactions.append(f"Potential interaction with {current_med}")
        
        return interactions
    
    def generate_general_recommendations(self, patient_data: PatientData, symptom_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate general treatment recommendations"""
        recommendations = []
        
        # Age-based recommendations
        if patient_data.age > 65:
            recommendations.append({
                "treatment_type": "monitoring",
                "instructions": "Close monitoring due to advanced age",
                "for_condition": "General"
            })
        
        # Medication management
        if len(patient_data.current_medications) > 3:
            recommendations.append({
                "treatment_type": "medication_review",
                "instructions": "Review all medications for potential interactions and necessity",
                "for_condition": "General"
            })
        
        # Symptom-specific recommendations
        if "priority_level" in symptom_analysis:
            priority = symptom_analysis["priority_level"]
            if priority == "high":
                recommendations.append({
                    "treatment_type": "urgent_care",
                    "instructions": "Immediate medical attention required",
                    "for_condition": "General"
                })
        
        return recommendations

# Create and run the agent
if __name__ == "__main__":
    planner = TreatmentPlanner("treatment planner agent seed phrase")
    planner.run()

