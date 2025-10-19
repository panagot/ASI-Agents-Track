"""
Healthcare AI Agents - Main Application
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel
import uvicorn
from agents.symptom_analyzer import SymptomAnalyzer
from agents.diagnosis_specialist import DiagnosisSpecialist
from agents.treatment_planner import TreatmentPlanner
from agents.risk_assessment import RiskAssessment
from agents.care_coordinator import CareCoordinator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Healthcare AI Agents", description="Collaborative AI agents for healthcare diagnosis")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Global agent instances
agents = {}
agent_addresses = {}

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
        # Initialize agents
        agents["symptom_analyzer"] = SymptomAnalyzer("symptom analyzer seed phrase")
        agents["diagnosis_specialist"] = DiagnosisSpecialist("diagnosis specialist seed phrase")
        agents["treatment_planner"] = TreatmentPlanner("treatment planner seed phrase")
        agents["risk_assessment"] = RiskAssessment("risk assessment seed phrase")
        agents["care_coordinator"] = CareCoordinator("care coordinator seed phrase")
        
        # Store agent addresses (in real implementation, these would be actual addresses)
        agent_addresses["SymptomAnalyzer"] = "agent1q..."
        agent_addresses["DiagnosisSpecialist"] = "agent1q..."
        agent_addresses["TreatmentPlanner"] = "agent1q..."
        agent_addresses["RiskAssessment"] = "agent1q..."
        agent_addresses["CareCoordinator"] = "agent1q..."
        
        # Update care coordinator with agent addresses
        agents["care_coordinator"].agent_addresses = agent_addresses
        
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
                "address": agent_addresses.get("SymptomAnalyzer", "Not deployed")
            },
            {
                "name": "Diagnosis Specialist",
                "type": "diagnosis",
                "description": "Provides medical diagnosis based on symptoms",
                "address": agent_addresses.get("DiagnosisSpecialist", "Not deployed")
            },
            {
                "name": "Treatment Planner",
                "type": "treatment_planning",
                "description": "Plans treatment options based on diagnoses",
                "address": agent_addresses.get("TreatmentPlanner", "Not deployed")
            },
            {
                "name": "Risk Assessment",
                "type": "risk_assessment",
                "description": "Assesses patient risk and potential complications",
                "address": agent_addresses.get("RiskAssessment", "Not deployed")
            },
            {
                "name": "Care Coordinator",
                "type": "coordination",
                "description": "Coordinates collaboration between all agents",
                "address": agent_addresses.get("CareCoordinator", "Not deployed")
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
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Simulate agent collaboration (in real implementation, this would be async)
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
    """Simulate the collaboration between agents"""
    
    # Simulate symptom analysis
    symptom_analysis = {
        "patient_id": patient_data["patient_id"],
        "symptom_categories": {
            "cardiovascular": ["chest pain"] if "chest pain" in patient_data["symptoms"] else [],
            "respiratory": ["shortness of breath"] if "shortness of breath" in patient_data["symptoms"] else [],
            "gastrointestinal": ["nausea"] if "nausea" in patient_data["symptoms"] else []
        },
        "severity_assessment": {symptom: "moderate" for symptom in patient_data["symptoms"]},
        "priority_level": "moderate",
        "recommended_specialists": ["cardiologist", "pulmonologist"],
        "analysis_timestamp": datetime.utcnow().isoformat()
    }
    
    # Simulate diagnosis
    diagnoses = [
        {
            "condition": "Myocardial Infarction",
            "confidence": 0.75,
            "reasoning": "Patient presents with chest pain and shortness of breath. Risk factors include age and medical history.",
            "supporting_evidence": ["Patient reports chest pain", "Patient reports shortness of breath"],
            "differential_diagnoses": ["Pneumonia", "Anxiety Disorder"],
            "recommended_tests": ["ECG", "Troponin levels", "Chest X-ray"],
            "urgency": "urgent"
        },
        {
            "condition": "Pneumonia",
            "confidence": 0.60,
            "reasoning": "Respiratory symptoms with potential infection markers.",
            "supporting_evidence": ["Patient reports shortness of breath"],
            "differential_diagnoses": ["Myocardial Infarction", "Bronchitis"],
            "recommended_tests": ["Chest X-ray", "Blood work", "Sputum culture"],
            "urgency": "moderate"
        }
    ]
    
    # Simulate treatment plan
    treatments = [
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
    ]
    
    # Simulate risk assessment
    risk_assessment = {
        "overall_risk": "moderate",
        "risk_factors": ["Advanced age", "Cardiovascular symptoms"],
        "complications": ["Heart failure", "Arrhythmia"],
        "monitoring_required": ["Vital signs", "ECG", "Cardiac enzymes"],
        "confidence": 0.80
    }
    
    # Generate final report
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
        "treatment_plan": treatments,
        "risk_assessment": risk_assessment,
        "recommendations": [
            "Immediate medical attention recommended",
            "High confidence in Myocardial Infarction diagnosis",
            "Moderate risk - regular follow-up recommended"
        ],
        "next_steps": [
            "ECG",
            "Troponin levels",
            "Chest X-ray",
            "Initiate recommended treatment plan",
            "Schedule follow-up appointment"
        ],
        "confidence_score": 0.75,
        "completion_time": datetime.utcnow().isoformat()
    }
    
    return final_report

@app.get("/api/case/{case_id}")
async def get_case(case_id: str):
    """Get case details by ID"""
    # In real implementation, this would fetch from database
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
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
