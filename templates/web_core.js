// Minimal shared helpers for website-only analysis (client-side)

export const MEDICAL_KNOWLEDGE = {
  symptomPairs: [
    ["headache", "nausea"],
    ["cough", "fever"],
    ["cough", "fatigue"],
    ["chest pain", "shortness of breath"],
  ],
  rarity: {
    meningitis: 0.9, appendicitis: 0.8, "pulmonary embolism": 0.9,
    "common cold": 0.2, migraine: 0.3, anxiety: 0.2, bronchitis: 0.3,
    pneumonia: 0.4, asthma: 0.3, flu: 0.3
  },
  conditions: {
    "Viral Upper Respiratory Infection": {
      symptoms: ["fever", "cough", "fatigue"], urgency: "routine",
      treatment: "Rest, hydration, fever reducers, monitor"
    },
    "Influenza": {
      symptoms: ["fever", "cough", "body aches", "fatigue"], urgency: "moderate",
      treatment: "Rest, hydration, antivirals if early"
    },
    "Bronchitis": {
      symptoms: ["cough", "chest", "fatigue", "fever"], urgency: "moderate",
      treatment: "Cough suppressants, bronchodilators if needed"
    },
    "Pneumonia": {
      symptoms: ["cough", "chest", "fever", "breath"], urgency: "urgent",
      treatment: "Antibiotics, rest, hydration"
    },
    "Migraine": {
      symptoms: ["headache", "nausea", "light"], urgency: "moderate",
      treatment: "Migraine meds, dark room, avoid triggers"
    },
    "Tension Headache with Nausea": {
      symptoms: ["headache", "nausea", "stress"], urgency: "routine",
      treatment: "OTC analgesics, relaxation"
    }
  }
};

export function normalizeText(text) {
  return String(text || '').toLowerCase();
}

export function matchPatterns(symptomsText) {
  const s = normalizeText(symptomsText);
  const tokens = s.split(/[^a-z]+/).filter(Boolean);
  return { s, tokens };
}

export function basicConfidence(condition, tokens) {
  const info = MEDICAL_KNOWLEDGE.conditions[condition];
  if (!info) return 0;
  let direct = 0;
  info.symptoms.forEach(sym => { if (tokens.some(t => sym.includes(t) || t.includes(sym))) direct += 1; });
  let base = direct / Math.max(1, info.symptoms.length);
  // Pair boosts
  const text = tokens.join(' ');
  MEDICAL_KNOWLEDGE.symptomPairs.forEach(([a,b]) => {
    // Phrase-aware: boost when full phrases appear in normalized text
    const hasPhrases = text.includes(a) && text.includes(b);
    const relevant = info.symptoms.some(x=>a.includes(x)||x.includes(a)) && info.symptoms.some(x=>b.includes(x)||x.includes(b));
    if (hasPhrases && relevant) base += 0.2;
  });
  const rarity = MEDICAL_KNOWLEDGE.rarity[condition.toLowerCase?.()] ?? 0.5;
  return Math.max(0.3, Math.min(base - 0.05 * rarity, 0.85));
}

export function riskAssessment(tokens) {
  const redFlags = [];
  if (tokens.includes('chest') && (tokens.includes('shortness') || tokens.includes('breath'))) redFlags.push('cardiorespiratory');
  if (tokens.includes('fever') && tokens.includes('stiffness')) redFlags.push('meningitis_risk');
  const level = redFlags.length >= 1 ? 'high' : (tokens.includes('fever') ? 'moderate' : 'low');
  return { level, red_flags: redFlags, recommendations: level==='high' ? ["Seek urgent evaluation"] : ["Monitor and rest"] };
}

export function treatmentFor(condition) {
  const info = MEDICAL_KNOWLEDGE.conditions[condition];
  return info?.treatment || 'Supportive care';
}



