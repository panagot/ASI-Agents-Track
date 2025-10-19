"""
Care Coordinator Agent - Orchestrates collaboration between all healthcare agents
"""

import json
from typing import Dict, List, Any
from agents.base_agent import BaseHealthcareAgent, PatientData
from uagents import Context
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CareCoordinator(BaseHealthcareAgent):
    """Agent that coordinates collaboration between all healthcare agents"""
    
    def __init__(self, seed_phrase: str):
        super().__init__("CareCoordinator", "coordination", seed_phrase)
        self.agent_addresses = {
            "SymptomAnalyzer": "agent1q...",  # Will be updated with actual addresses
            "DiagnosisSpecialist": "agent1q...",
            "TreatmentPlanner": "agent1q...",
            "RiskAssessment": "agent1q..."
        }
        self.active_cases = {}
    
    async def handle_text_message(self, ctx: Context, sender: str, text: str):
        """Handle incoming text messages"""
        try:
            message_data = json.loads(text)
            
            if message_data.get("type") == "new_patient_case":
                await self.handle_new_case(ctx, message_data)
            elif message_data.get("type") == "symptom_analysis_result":
                await self.handle_symptom_analysis(ctx, message_data)
            elif message_data.get("type") == "diagnosis_result":
                await self.handle_diagnosis_result(ctx, message_data)
            elif message_data.get("type") == "treatment_result":
                await self.handle_treatment_result(ctx, message_data)
            elif message_data.get("type") == "risk_assessment_result":
                await self.handle_risk_assessment(ctx, message_data)
                
        except json.JSONDecodeError:
            if "coordinate" in text.lower() or "new case" in text.lower():
                await self.send_message(ctx, sender, f"{self.name}: Ready to coordinate healthcare case. Please provide patient data.")
        except Exception as e:
            logger.error(f"Error in CareCoordinator: {e}")
            await self.send_message(ctx, sender, f"{self.name}: Error processing coordination request.")
    
    async def handle_new_case(self, ctx: Context, message_data: Dict[str, Any]):
        """Handle a new patient case"""
        patient_data = PatientData(**message_data["patient_data"])
        case_id = patient_data.patient_id
        
        # Initialize case tracking
        self.active_cases[case_id] = {
            "patient_data": patient_data,
            "status": "initializing",
            "results": {},
            "start_time": datetime.utcnow(),
            "agents_contacted": []
        }
        
        logger.info(f"Starting new case: {case_id}")
        
        # Send patient data to Symptom Analyzer
        symptom_request = {
            "type": "analyze_symptoms",
            "patient_data": patient_data.dict(),
            "case_id": case_id
        }
        
        await self.send_message(ctx, self.agent_addresses["SymptomAnalyzer"], json.dumps(symptom_request))
        self.active_cases[case_id]["agents_contacted"].append("SymptomAnalyzer")
        
        # Send initial response
        response = {
            "type": "case_started",
            "case_id": case_id,
            "status": "Analysis in progress",
            "next_steps": ["Symptom analysis", "Diagnosis", "Treatment planning", "Risk assessment"]
        }
        
        # Send response back to original sender
        await self.send_message(ctx, message_data.get("sender", "unknown"), json.dumps(response))
    
    async def handle_symptom_analysis(self, ctx: Context, message_data: Dict[str, Any]):
        """Handle symptom analysis results"""
        case_id = message_data.get("case_id")
        if not case_id or case_id not in self.active_cases:
            return
        
        # Store symptom analysis results
        self.active_cases[case_id]["results"]["symptom_analysis"] = message_data["analysis"]
        self.active_cases[case_id]["status"] = "symptom_analysis_complete"
        
        logger.info(f"Symptom analysis complete for case: {case_id}")
        
        # Send to Diagnosis Specialist
        diagnosis_request = {
            "type": "request_diagnosis",
            "patient_data": self.active_cases[case_id]["patient_data"].dict(),
            "symptom_analysis": message_data["analysis"],
            "case_id": case_id
        }
        
        await self.send_message(ctx, self.agent_addresses["DiagnosisSpecialist"], json.dumps(diagnosis_request))
        self.active_cases[case_id]["agents_contacted"].append("DiagnosisSpecialist")
        
        # Update case status
        await self.update_case_status(ctx, case_id, "Diagnosis in progress")
    
    async def handle_diagnosis_result(self, ctx: Context, message_data: Dict[str, Any]):
        """Handle diagnosis results"""
        case_id = message_data.get("case_id")
        if not case_id or case_id not in self.active_cases:
            return
        
        # Store diagnosis results
        self.active_cases[case_id]["results"]["diagnosis"] = message_data["diagnoses"]
        self.active_cases[case_id]["status"] = "diagnosis_complete"
        
        logger.info(f"Diagnosis complete for case: {case_id}")
        
        # Send to Treatment Planner
        treatment_request = {
            "type": "request_treatment",
            "patient_data": self.active_cases[case_id]["patient_data"].dict(),
            "diagnoses": message_data["diagnoses"],
            "symptom_analysis": self.active_cases[case_id]["results"]["symptom_analysis"],
            "case_id": case_id
        }
        
        await self.send_message(ctx, self.agent_addresses["TreatmentPlanner"], json.dumps(treatment_request))
        self.active_cases[case_id]["agents_contacted"].append("TreatmentPlanner")
        
        # Send to Risk Assessment
        risk_request = {
            "type": "assess_risk",
            "patient_data": self.active_cases[case_id]["patient_data"].dict(),
            "diagnoses": message_data["diagnoses"],
            "case_id": case_id
        }
        
        await self.send_message(ctx, self.agent_addresses["RiskAssessment"], json.dumps(risk_request))
        self.active_cases[case_id]["agents_contacted"].append("RiskAssessment")
        
        # Update case status
        await self.update_case_status(ctx, case_id, "Treatment planning and risk assessment in progress")
    
    async def handle_treatment_result(self, ctx: Context, message_data: Dict[str, Any]):
        """Handle treatment planning results"""
        case_id = message_data.get("case_id")
        if not case_id or case_id not in self.active_cases:
            return
        
        # Store treatment results
        self.active_cases[case_id]["results"]["treatment"] = message_data["treatments"]
        self.active_cases[case_id]["status"] = "treatment_planning_complete"
        
        logger.info(f"Treatment planning complete for case: {case_id}")
        
        # Check if all agents have responded
        await self.check_case_completion(ctx, case_id)
    
    async def handle_risk_assessment(self, ctx: Context, message_data: Dict[str, Any]):
        """Handle risk assessment results"""
        case_id = message_data.get("case_id")
        if not case_id or case_id not in self.active_cases:
            return
        
        # Store risk assessment results
        self.active_cases[case_id]["results"]["risk_assessment"] = message_data["risk_analysis"]
        self.active_cases[case_id]["status"] = "risk_assessment_complete"
        
        logger.info(f"Risk assessment complete for case: {case_id}")
        
        # Check if all agents have responded
        await self.check_case_completion(ctx, case_id)
    
    async def check_case_completion(self, ctx: Context, case_id: str):
        """Check if all agents have completed their analysis"""
        case = self.active_cases[case_id]
        
        required_results = ["symptom_analysis", "diagnosis", "treatment", "risk_assessment"]
        completed_results = [key for key in required_results if key in case["results"]]
        
        if len(completed_results) == len(required_results):
            # All agents have completed their analysis
            await self.generate_final_report(ctx, case_id)
        else:
            # Still waiting for some agents
            missing = [r for r in required_results if r not in case["results"]]
            logger.info(f"Case {case_id} waiting for: {missing}")
    
    async def generate_final_report(self, ctx: Context, case_id: str):
        """Generate final comprehensive report"""
        case = self.active_cases[case_id]
        patient_data = case["patient_data"]
        results = case["results"]
        
        # Generate comprehensive report
        final_report = {
            "case_id": case_id,
            "patient_id": patient_data.patient_id,
            "completion_time": datetime.utcnow().isoformat(),
            "processing_time": (datetime.utcnow() - case["start_time"]).total_seconds(),
            "patient_summary": {
                "age": patient_data.age,
                "gender": patient_data.gender,
                "symptoms": patient_data.symptoms,
                "medical_history": patient_data.medical_history,
                "current_medications": patient_data.current_medications
            },
            "symptom_analysis": results["symptom_analysis"],
            "diagnoses": results["diagnosis"],
            "treatment_plan": results["treatment"],
            "risk_assessment": results["risk_assessment"],
            "recommendations": self.generate_recommendations(results),
            "next_steps": self.generate_next_steps(results),
            "agents_involved": case["agents_contacted"],
            "confidence_score": self.calculate_overall_confidence(results)
        }
        
        # Store final report
        case["final_report"] = final_report
        case["status"] = "completed"
        
        logger.info(f"Case {case_id} completed successfully")
        
        # Send final report to original requester
        response = {
            "type": "final_report",
            "report": final_report
        }
        
        # For demo purposes, send to a default address
        await self.send_message(ctx, "agent1q...", json.dumps(response))
    
    def generate_recommendations(self, results: Dict[str, Any]) -> List[str]:
        """Generate final recommendations based on all agent results"""
        recommendations = []
        
        # Based on symptom analysis
        if "priority_level" in results["symptom_analysis"]:
            priority = results["symptom_analysis"]["priority_level"]
            if priority == "high":
                recommendations.append("Immediate medical attention recommended")
            elif priority == "moderate":
                recommendations.append("Medical evaluation within 24-48 hours")
            else:
                recommendations.append("Routine medical follow-up")
        
        # Based on diagnosis
        if results["diagnosis"]:
            top_diagnosis = results["diagnosis"][0]
            if top_diagnosis["confidence"] > 0.8:
                recommendations.append(f"High confidence in {top_diagnosis['condition']} diagnosis")
            elif top_diagnosis["confidence"] > 0.5:
                recommendations.append(f"Consider {top_diagnosis['condition']} as primary diagnosis")
        
        # Based on risk assessment
        if "overall_risk" in results["risk_assessment"]:
            risk_level = results["risk_assessment"]["overall_risk"]
            if risk_level == "high":
                recommendations.append("High-risk patient - close monitoring required")
            elif risk_level == "moderate":
                recommendations.append("Moderate risk - regular follow-up recommended")
        
        return recommendations
    
    def generate_next_steps(self, results: Dict[str, Any]) -> List[str]:
        """Generate next steps for patient care"""
        next_steps = []
        
        # Diagnostic tests
        if results["diagnosis"]:
            for diagnosis in results["diagnosis"][:2]:  # Top 2 diagnoses
                if "recommended_tests" in diagnosis:
                    next_steps.extend(diagnosis["recommended_tests"])
        
        # Treatment initiation
        if results["treatment"]:
            next_steps.append("Initiate recommended treatment plan")
            next_steps.append("Monitor treatment response")
        
        # Follow-up
        next_steps.append("Schedule follow-up appointment")
        next_steps.append("Patient education on condition and treatment")
        
        return next_steps
    
    def calculate_overall_confidence(self, results: Dict[str, Any]) -> float:
        """Calculate overall confidence score for the case"""
        confidence_scores = []
        
        # Diagnosis confidence
        if results["diagnosis"]:
            confidence_scores.append(results["diagnosis"][0]["confidence"])
        
        # Symptom analysis confidence
        if "relevance_score" in results["symptom_analysis"]:
            confidence_scores.append(results["symptom_analysis"]["relevance_score"])
        
        # Risk assessment confidence
        if "confidence" in results["risk_assessment"]:
            confidence_scores.append(results["risk_assessment"]["confidence"])
        
        return sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    
    async def update_case_status(self, ctx: Context, case_id: str, status: str):
        """Update case status and notify relevant parties"""
        if case_id in self.active_cases:
            self.active_cases[case_id]["status"] = status
            logger.info(f"Case {case_id} status updated: {status}")

# Create and run the agent
if __name__ == "__main__":
    coordinator = CareCoordinator("care coordinator agent seed phrase")
    coordinator.run()

