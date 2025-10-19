"""
Healthcare AI Agents - Simplified Main Application (Python 3.13 Compatible)
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
import uvicorn
from agents.simple_agent import SimpleSymptomAnalyzer, SimpleDiagnosisSpecialist, PatientData
from agents.intelligent_ai_agent import IntelligentAIAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Healthcare AI Agents", description="Collaborative AI agents for healthcare diagnosis")

# Mount static files and templates
try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception:
    logger.warning("Static files directory not found, skipping static file mounting")

templates = Jinja2Templates(directory="templates")

# Global agent instances
agents = {}
intelligent_ai = IntelligentAIAgent()

class PatientRequest(BaseModel):
    """Patient data request model"""
    patient_id: str
    age: int
    gender: str
    symptoms: list[str]
    medical_history: list[str]
    current_medications: list[str]
    vital_signs: Dict[str, Any]

class AgentResponse(BaseModel):
    """Agent response model"""
    success: bool
    message: str
    data: Dict[str, Any] = {}

@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    logger.info("Starting Healthcare AI Agents...")
    
    try:
        # Initialize simplified agents
        agents["symptom_analyzer"] = SimpleSymptomAnalyzer()
        agents["diagnosis_specialist"] = SimpleDiagnosisSpecialist()
        
        logger.info("All agents initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing agents: {e}")

@app.get("/")
async def root(request: Request):
    """Main page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/agents")
async def get_agents():
    """Get list of available agents"""
    return {
        "agents": [
            {
                "name": "Symptom Analyzer",
                "type": "symptom_analysis",
                "description": "Analyzes patient symptoms and medical history",
                "status": "active"
            },
            {
                "name": "Diagnosis Specialist",
                "type": "diagnosis",
                "description": "Provides medical diagnosis based on symptoms",
                "status": "active"
            }
        ]
    }

@app.post("/api/analyze-patient")
async def analyze_patient(patient_request: PatientRequest):
    """Analyze patient data using AI agents"""
    try:
        # Create patient data object
        patient_data = {
            "patient_id": patient_request.patient_id,
            "age": patient_request.age,
            "gender": patient_request.gender,
            "symptoms": patient_request.symptoms,
            "medical_history": patient_request.medical_history,
            "current_medications": patient_request.current_medications,
            "vital_signs": patient_request.vital_signs,
            "timestamp": datetime.utcnow()
        }
        
        # Simulate agent collaboration
        analysis_result = await simulate_agent_collaboration(patient_data)
        
        return AgentResponse(
            success=True,
            message="Patient analysis completed successfully",
            data=analysis_result
        )
        
    except Exception as e:
        logger.error(f"Error analyzing patient: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def simulate_agent_collaboration(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate the collaboration between agents with intelligent AI fallback"""
    
    try:
        # First, try intelligent AI analysis for any symptom
        intelligent_analysis = await intelligent_ai.analyze_any_symptom(
            " ".join(patient_data["symptoms"]), 
            patient_data
        )
        
        # Use our simplified agents for additional analysis
        symptom_analyzer = agents["symptom_analyzer"]
        diagnosis_specialist = agents["diagnosis_specialist"]
        
        # Step 1: Symptom Analysis
        symptom_message = {
            "type": "analyze_symptoms",
            "patient_data": patient_data
        }
        
        symptom_result = await symptom_analyzer.process_message(symptom_message)
        symptom_analysis = symptom_result["analysis"]
        
        # Step 2: Diagnosis
        diagnosis_message = {
            "type": "request_diagnosis",
            "patient_data": patient_data,
            "symptom_analysis": symptom_analysis
        }
        
        diagnosis_result = await diagnosis_specialist.process_message(diagnosis_message)
        diagnoses = diagnosis_result["diagnoses"]
        
        # Step 3: If no diagnoses from standard agents, use intelligent AI results
        if not diagnoses or len(diagnoses) == 0:
            diagnoses = intelligent_analysis["possible_conditions"]
            logger.info("Using intelligent AI analysis for diagnoses")
        
        # Step 4: Generate comprehensive report
        final_report = {
            "case_id": patient_data["patient_id"],
            "patient_summary": {
                "age": patient_data["age"],
                "gender": patient_data["gender"],
                "symptoms": patient_data["symptoms"],
                "medical_history": patient_data["medical_history"]
            },
            "symptom_analysis": symptom_analysis,
            "diagnoses": diagnoses,
            "treatment_plan": generate_treatment_plan(diagnoses),
            "risk_assessment": generate_risk_assessment(patient_data, diagnoses),
            "recommendations": generate_recommendations(symptom_analysis, diagnoses),
            "next_steps": generate_next_steps(diagnoses),
            "confidence_score": calculate_overall_confidence(diagnoses),
            "intelligent_ai_analysis": intelligent_analysis,  # Include intelligent AI results
            "completion_time": datetime.utcnow().isoformat()
        }
        
        return final_report
        
    except Exception as e:
        logger.error(f"Error in agent collaboration: {str(e)}")
        # Fallback to intelligent AI only
        intelligent_analysis = await intelligent_ai.analyze_any_symptom(
            " ".join(patient_data["symptoms"]), 
            patient_data
        )
        
        return {
            "case_id": patient_data["patient_id"],
            "patient_summary": {
                "age": patient_data["age"],
                "gender": patient_data["gender"],
                "symptoms": patient_data["symptoms"],
                "medical_history": patient_data["medical_history"]
            },
            "symptom_analysis": {"priority_level": intelligent_analysis["urgency_assessment"]["urgency"]},
            "diagnoses": intelligent_analysis["possible_conditions"],
            "treatment_plan": intelligent_analysis["treatment_recommendations"],
            "risk_assessment": intelligent_analysis["urgency_assessment"],
            "recommendations": intelligent_analysis["general_advice"],
            "next_steps": ["Schedule medical evaluation", "Monitor symptoms", "Follow treatment recommendations"],
            "confidence_score": intelligent_analysis["confidence_score"],
            "intelligent_ai_analysis": intelligent_analysis,
            "completion_time": datetime.utcnow().isoformat()
        }

def generate_treatment_plan(diagnoses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Generate treatment plan based on diagnoses"""
    treatments = []
    
    for diagnosis in diagnoses:
        if diagnosis["confidence"] > 0.5:
            condition = diagnosis["condition"].lower()
            
            if "myocardial infarction" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Aspirin",
                        "dosage": "325mg",
                        "duration": "Daily",
                        "instructions": "Take with food to reduce stomach irritation",
                        "side_effects": ["Stomach upset", "Bleeding risk"],
                        "contraindications": ["Active bleeding", "Allergy to aspirin"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Rest, avoid strenuous activity, monitor symptoms",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "pneumonia" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Amoxicillin",
                        "dosage": "500mg",
                        "duration": "7-10 days",
                        "instructions": "Take with food to reduce stomach upset",
                        "side_effects": ["Nausea", "Diarrhea", "Allergic reactions"],
                        "contraindications": ["Penicillin allergy"]
                    }
                ])
            elif "stoma bleeding" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "Immediate medical attention required - stoma bleeding can be serious",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "monitoring",
                        "instructions": "Monitor stoma output, check for signs of infection, maintain stoma bag hygiene",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "medication",
                        "medication": "Vitamin K",
                        "dosage": "As prescribed",
                        "duration": "As needed",
                        "instructions": "May be needed if bleeding is due to anticoagulant use",
                        "side_effects": ["Allergic reactions"],
                        "contraindications": ["Allergy to vitamin K"]
                    }
                ])
            elif "stoma obstruction" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "Stoma obstruction requires immediate medical evaluation",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "dietary",
                        "instructions": "Avoid high-fiber foods, drink plenty of fluids, consider stool softeners",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "stoma infection" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Antibiotics",
                        "dosage": "As prescribed",
                        "duration": "7-14 days",
                        "instructions": "Topical and/or oral antibiotics for stoma site infection",
                        "side_effects": ["Nausea", "Diarrhea", "Allergic reactions"],
                        "contraindications": ["Antibiotic allergy"]
                    },
                    {
                        "treatment_type": "wound_care",
                        "instructions": "Clean stoma site regularly, change stoma bag more frequently, monitor for worsening",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "angina" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Nitroglycerin",
                        "dosage": "0.4mg sublingual",
                        "duration": "As needed",
                        "instructions": "Take at first sign of chest pain, repeat every 5 minutes if needed",
                        "side_effects": ["Headache", "Dizziness", "Low blood pressure"],
                        "contraindications": ["Severe anemia", "Recent head injury"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Avoid triggers, regular exercise, healthy diet, stress management",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "heart failure" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "ACE Inhibitor",
                        "dosage": "As prescribed",
                        "duration": "Long-term",
                        "instructions": "Take as directed, monitor blood pressure and kidney function",
                        "side_effects": ["Dry cough", "Dizziness", "High potassium"],
                        "contraindications": ["Pregnancy", "Bilateral renal artery stenosis"]
                    },
                    {
                        "treatment_type": "dietary",
                        "instructions": "Low sodium diet, fluid restriction, regular weight monitoring",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "stroke" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "Immediate medical attention required - time is critical for stroke treatment",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "medication",
                        "medication": "Aspirin",
                        "dosage": "81mg daily",
                        "duration": "Long-term",
                        "instructions": "Secondary stroke prevention, take with food",
                        "side_effects": ["Bleeding risk", "Stomach upset"],
                        "contraindications": ["Active bleeding", "Allergy to aspirin"]
                    }
                ])
            elif "asthma" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Albuterol Inhaler",
                        "dosage": "2 puffs as needed",
                        "duration": "As needed",
                        "instructions": "Use for acute symptoms, shake well before use",
                        "side_effects": ["Tremors", "Rapid heartbeat", "Nervousness"],
                        "contraindications": ["Allergy to albuterol"]
                    },
                    {
                        "treatment_type": "preventive",
                        "instructions": "Avoid triggers, use peak flow meter, have action plan",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "diabetes" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Metformin",
                        "dosage": "500mg twice daily",
                        "duration": "Long-term",
                        "instructions": "Take with meals to reduce stomach upset",
                        "side_effects": ["Nausea", "Diarrhea", "Metallic taste"],
                        "contraindications": ["Kidney disease", "Liver disease"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Regular blood glucose monitoring, healthy diet, regular exercise",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "urinary tract infection" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Ciprofloxacin",
                        "dosage": "250mg twice daily",
                        "duration": "3-7 days",
                        "instructions": "Take with plenty of water, complete full course",
                        "side_effects": ["Nausea", "Diarrhea", "Sun sensitivity"],
                        "contraindications": ["Allergy to quinolones", "Pregnancy"]
                    },
                    {
                        "treatment_type": "supportive",
                        "instructions": "Increase fluid intake, urinate frequently, avoid irritants",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "kidney stones" in condition:
                treatments.extend([
                    {
                        "treatment_type": "pain_management",
                        "medication": "Ibuprofen",
                        "dosage": "400mg every 6 hours",
                        "duration": "As needed",
                        "instructions": "Take with food, do not exceed 2400mg daily",
                        "side_effects": ["Stomach upset", "Dizziness", "Headache"],
                        "contraindications": ["Active bleeding", "Kidney disease"]
                    },
                    {
                        "treatment_type": "dietary",
                        "instructions": "Increase fluid intake, limit oxalate foods, strain urine",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "anxiety" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Sertraline",
                        "dosage": "25mg daily",
                        "duration": "6-12 months",
                        "instructions": "Take at same time daily, may take 4-6 weeks to see effect",
                        "side_effects": ["Nausea", "Insomnia", "Sexual dysfunction"],
                        "contraindications": ["MAOI use", "Pregnancy"]
                    },
                    {
                        "treatment_type": "therapy",
                        "instructions": "Cognitive behavioral therapy, relaxation techniques, regular exercise",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "depression" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Fluoxetine",
                        "dosage": "20mg daily",
                        "duration": "6-12 months",
                        "instructions": "Take in morning, may take 2-4 weeks to see effect",
                        "side_effects": ["Nausea", "Insomnia", "Weight changes"],
                        "contraindications": ["MAOI use", "Pregnancy"]
                    },
                    {
                        "treatment_type": "supportive",
                        "instructions": "Regular therapy, social support, healthy lifestyle, crisis plan",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "anaphylaxis" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "medication": "Epinephrine Auto-injector",
                        "dosage": "0.3mg IM",
                        "duration": "Emergency use",
                        "instructions": "Use immediately, call 911, may repeat in 5-15 minutes",
                        "side_effects": ["Rapid heartbeat", "Tremors", "Anxiety"],
                        "contraindications": ["None in emergency"]
                    },
                    {
                        "treatment_type": "preventive",
                        "instructions": "Avoid allergens, carry epinephrine, wear medical alert bracelet",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "atrial fibrillation" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Warfarin",
                        "dosage": "As prescribed",
                        "duration": "Long-term",
                        "instructions": "Monitor INR regularly, avoid alcohol",
                        "side_effects": ["Bleeding risk", "Bruising"],
                        "contraindications": ["Active bleeding", "Pregnancy"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Limit caffeine, manage stress, regular exercise",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "deep vein thrombosis" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Heparin",
                        "dosage": "As prescribed",
                        "duration": "5-10 days",
                        "instructions": "Monitor for bleeding, avoid injury",
                        "side_effects": ["Bleeding risk", "Heparin-induced thrombocytopenia"],
                        "contraindications": ["Active bleeding", "Severe hypertension"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Compression stockings, elevate legs, avoid prolonged sitting",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "pulmonary embolism" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "IMMEDIATE HOSPITALIZATION - Call 911, oxygen therapy, anticoagulation",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "crohns disease" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Mesalamine",
                        "dosage": "As prescribed",
                        "duration": "Long-term",
                        "instructions": "Take with food, monitor for side effects",
                        "side_effects": ["Nausea", "Headache", "Rash"],
                        "contraindications": ["Sulfa allergy"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Low-residue diet, stress management, regular monitoring",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "parkinsons disease" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Levodopa/Carbidopa",
                        "dosage": "As prescribed",
                        "duration": "Long-term",
                        "instructions": "Take on empty stomach, monitor for dyskinesia",
                        "side_effects": ["Nausea", "Dyskinesia", "Hallucinations"],
                        "contraindications": ["Glaucoma", "Melanoma"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Physical therapy, speech therapy, occupational therapy",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "alzheimers disease" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Donepezil",
                        "dosage": "5-10mg daily",
                        "duration": "Long-term",
                        "instructions": "Take at bedtime, monitor for side effects",
                        "side_effects": ["Nausea", "Diarrhea", "Insomnia"],
                        "contraindications": ["Severe liver disease"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Cognitive stimulation, safety measures, caregiver support",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "multiple sclerosis" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Interferon beta",
                        "dosage": "As prescribed",
                        "duration": "Long-term",
                        "instructions": "Inject as directed, monitor for flu-like symptoms",
                        "side_effects": ["Flu-like symptoms", "Injection site reactions"],
                        "contraindications": ["Pregnancy", "Severe depression"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Physical therapy, stress management, cooling strategies",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "bell palsy" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Prednisone",
                        "dosage": "60mg daily",
                        "duration": "5 days, then taper",
                        "instructions": "Take with food, protect eye from drying",
                        "side_effects": ["Increased appetite", "Mood changes", "Insomnia"],
                        "contraindications": ["Active infection", "Uncontrolled diabetes"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Eye protection, facial exercises, massage therapy",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "croup" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Dexamethasone",
                        "dosage": "0.6mg/kg",
                        "duration": "Single dose",
                        "instructions": "Oral or IM, monitor breathing",
                        "side_effects": ["Nausea", "Insomnia", "Mood changes"],
                        "contraindications": ["Active infection", "Allergy"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Humidified air, cool mist, comfort measures",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "preeclampsia" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "IMMEDIATE OBSTETRIC EVALUATION - Call OB/GYN, monitor blood pressure",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "medication",
                        "medication": "Magnesium sulfate",
                        "dosage": "As prescribed",
                        "duration": "Until delivery",
                        "instructions": "IV administration, monitor reflexes and urine output",
                        "side_effects": ["Flushing", "Nausea", "Respiratory depression"],
                        "contraindications": ["Myasthenia gravis", "Renal failure"]
                    }
                ])
            elif "lupus" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Hydroxychloroquine",
                        "dosage": "200-400mg daily",
                        "duration": "Long-term",
                        "instructions": "Take with food, regular eye exams required",
                        "side_effects": ["Nausea", "Diarrhea", "Eye toxicity"],
                        "contraindications": ["Retinal disease", "Porphyria"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Sun protection, stress management, regular monitoring",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "bipolar disorder" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Lithium",
                        "dosage": "As prescribed",
                        "duration": "Long-term",
                        "instructions": "Monitor blood levels, maintain hydration",
                        "side_effects": ["Tremor", "Weight gain", "Kidney problems"],
                        "contraindications": ["Severe kidney disease", "Heart disease"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Regular sleep schedule, stress management, therapy",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "heat stroke" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "IMMEDIATE COOLING - Remove from heat, cool with ice, call 911",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Hydration, rest, avoid heat exposure",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "drug overdose" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "IMMEDIATE EMERGENCY - Call 911, administer naloxone if opioid, monitor breathing",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "medication",
                        "medication": "Naloxone",
                        "dosage": "0.4-2mg",
                        "duration": "Emergency use",
                        "instructions": "IV, IM, or intranasal, may repeat every 2-3 minutes",
                        "side_effects": ["Withdrawal symptoms", "Agitation", "Nausea"],
                        "contraindications": ["None in emergency"]
                    }
                ])
            elif "delirium" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "Haloperidol",
                        "dosage": "0.5-2mg",
                        "duration": "Short-term",
                        "instructions": "Low dose, monitor for side effects",
                        "side_effects": ["Extrapyramidal symptoms", "Sedation", "QT prolongation"],
                        "contraindications": ["Parkinson's disease", "QT prolongation"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Reorientation, familiar environment, family presence",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "kawasaki disease" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "IVIG",
                        "dosage": "2g/kg",
                        "duration": "Single infusion",
                        "instructions": "High-dose IV infusion over 8-12 hours",
                        "side_effects": ["Fever", "Chills", "Allergic reactions"],
                        "contraindications": ["IgA deficiency", "Severe heart failure"]
                    },
                    {
                        "treatment_type": "medication",
                        "medication": "Aspirin",
                        "dosage": "High dose initially, then low dose",
                        "duration": "6-8 weeks",
                        "instructions": "High dose until afebrile, then low dose",
                        "side_effects": ["Stomach upset", "Bleeding risk"],
                        "contraindications": ["Active bleeding", "Reye syndrome risk"]
                    }
                ])
            elif "guillain barre" in condition:
                treatments.extend([
                    {
                        "treatment_type": "medication",
                        "medication": "IVIG",
                        "dosage": "2g/kg",
                        "duration": "5 days",
                        "instructions": "IV infusion, monitor for complications",
                        "side_effects": ["Fever", "Chills", "Headache"],
                        "contraindications": ["IgA deficiency", "Severe heart failure"]
                    },
                    {
                        "treatment_type": "lifestyle",
                        "instructions": "Physical therapy, respiratory support, monitoring",
                        "side_effects": [],
                        "contraindications": []
                    }
                ])
            elif "carbon monoxide poisoning" in condition:
                treatments.extend([
                    {
                        "treatment_type": "emergency",
                        "instructions": "IMMEDIATE REMOVAL - Get to fresh air, call 911, oxygen therapy",
                        "side_effects": [],
                        "contraindications": []
                    },
                    {
                        "treatment_type": "medication",
                        "medication": "100% Oxygen",
                        "dosage": "High flow",
                        "duration": "Until CO levels normalize",
                        "instructions": "High-flow oxygen via non-rebreather mask",
                        "side_effects": ["Oxygen toxicity with prolonged use"],
                        "contraindications": ["None in acute poisoning"]
                    }
                ])
    
    return treatments

def generate_risk_assessment(patient_data: Dict[str, Any], diagnoses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate risk assessment"""
    risk_factors = []
    
    # Age-based risks
    if patient_data["age"] > 65:
        risk_factors.append("Advanced age")
    
    # Medical history risks
    for condition in patient_data["medical_history"]:
        if any(keyword in condition.lower() for keyword in ["diabetes", "heart", "kidney", "liver"]):
            risk_factors.append(f"Chronic condition: {condition}")
    
    # Determine overall risk
    overall_risk = "low"
    if len(risk_factors) > 2 or any(d["urgency"] == "urgent" for d in diagnoses):
        overall_risk = "high"
    elif len(risk_factors) > 0 or any(d["urgency"] == "moderate" for d in diagnoses):
        overall_risk = "moderate"
    
    return {
        "overall_risk": overall_risk,
        "risk_factors": risk_factors,
        "complications": ["Heart failure", "Arrhythmia"] if "myocardial infarction" in str(diagnoses).lower() else [],
        "monitoring_required": ["Vital signs", "ECG", "Cardiac enzymes"] if overall_risk == "high" else ["Regular monitoring"],
        "confidence": 0.80
    }

def generate_recommendations(symptom_analysis: Dict[str, Any], diagnoses: List[Dict[str, Any]]) -> List[str]:
    """Generate final recommendations"""
    recommendations = []
    
    # Based on symptom analysis
    if symptom_analysis.get("priority_level") == "high":
        recommendations.append("Immediate medical attention recommended")
    elif symptom_analysis.get("priority_level") == "moderate":
        recommendations.append("Medical evaluation within 24-48 hours")
    else:
        recommendations.append("Routine medical follow-up")
    
    # Based on diagnosis
    if diagnoses:
        top_diagnosis = diagnoses[0]
        if top_diagnosis["confidence"] > 0.8:
            recommendations.append(f"High confidence in {top_diagnosis['condition']} diagnosis")
        elif top_diagnosis["confidence"] > 0.5:
            recommendations.append(f"Consider {top_diagnosis['condition']} as primary diagnosis")
    
    return recommendations

def generate_next_steps(diagnoses: List[Dict[str, Any]]) -> List[str]:
    """Generate next steps for patient care"""
    next_steps = []
    
    # Diagnostic tests
    if diagnoses:
        next_steps.extend(["ECG", "Blood work", "Chest X-ray"])
    
    # Treatment initiation
    next_steps.extend([
        "Initiate recommended treatment plan",
        "Monitor treatment response",
        "Schedule follow-up appointment",
        "Patient education on condition and treatment"
    ])
    
    return next_steps

def calculate_overall_confidence(diagnoses: List[Dict[str, Any]]) -> float:
    """Calculate overall confidence score"""
    if not diagnoses:
        return 0.0
    
    return sum(d["confidence"] for d in diagnoses) / len(diagnoses)

@app.get("/api/case/{case_id}")
async def get_case(case_id: str):
    """Get case details by ID"""
    return {
        "case_id": case_id,
        "status": "completed",
        "message": "Case details would be retrieved from database"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "agents": len(agents),
        "version": "1.0.0"
    }

if __name__ == "__main__":
    # Run the FastAPI application
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
