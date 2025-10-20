import { matchPatterns, basicConfidence, riskAssessment, treatmentFor, MEDICAL_KNOWLEDGE } from './web_core.js';

export const SymptomAnalyzer = {
  run(input) {
    const { s, tokens } = matchPatterns(Array.isArray(input.symptoms) ? input.symptoms.join(', ') : input.symptoms);
    return { normalized: s, tokens };
  }
};

export const DiagnosisSpecialist = {
  run(tokens) {
    const scored = Object.keys(MEDICAL_KNOWLEDGE.conditions).map(name => ({
      condition: name,
      confidence: basicConfidence(name, tokens),
      urgency: MEDICAL_KNOWLEDGE.conditions[name].urgency
    })).filter(x => x.confidence >= 0.3).sort((a,b)=>b.confidence-a.confidence).slice(0,3);
    return scored;
  }
};

export const RiskAssessment = {
  run(tokens) { return riskAssessment(tokens); }
};

export const TreatmentPlanner = {
  run(topCondition) {
    return [ { treatment_type: 'Plan', instructions: treatmentFor(topCondition.condition) } ];
  }
};

export const CareCoordinator = {
  run(formData) {
    const analysis = SymptomAnalyzer.run(formData);
    const diagnoses = DiagnosisSpecialist.run(analysis.tokens);
    const risk = RiskAssessment.run(analysis.tokens);
    const plan = diagnoses.length ? TreatmentPlanner.run(diagnoses[0]) : [];
    const confidence = diagnoses.length ? diagnoses[0].confidence : 0.4;
    return {
      patient_summary: {
        age: formData.age || '—',
        gender: formData.gender || '—',
        symptoms: Array.isArray(formData.symptoms) ? formData.symptoms : String(formData.symptoms||'').split(',').map(s=>s.trim()).filter(Boolean)
      },
      confidence_score: confidence,
      diagnoses,
      treatment_plan: plan,
      intelligent_ai_analysis: { urgency_assessment: {
        overall_risk: risk.level,
        risk_score: risk.level==='high'?0.8:risk.level==='moderate'?0.5:0.2,
        risk_factors: risk.red_flags || [],
        recommendations: risk.recommendations || []
      } },
      recommendations: [ 'Hydration', 'Symptom monitoring' ],
      next_steps: risk.level==='high' ? ['Seek urgent evaluation'] : ['Rest and recheck if worse']
    };
  }
};

// Expose globally for index.html
window.WebAgents = { SymptomAnalyzer, DiagnosisSpecialist, RiskAssessment, TreatmentPlanner, CareCoordinator };


