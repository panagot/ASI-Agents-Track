# Agentverse Deployment Guide

## 🚀 Deploying Healthcare AI Agents to Agentverse

This guide will help you deploy your Healthcare AI Agents to the Agentverse platform for the ASI Alliance hackathon submission.

## 📋 Prerequisites

1. **Agentverse Account**: Sign up at [Agentverse.ai](https://agentverse.ai)
2. **Python 3.8-3.12**: Required for uAgents framework
3. **Agent Code**: Use `agents/real_healthcare_agent.py`

## 🎯 Step-by-Step Deployment

### Step 1: Access Agentverse
1. Go to [Agentverse.ai](https://agentverse.ai)
2. Sign in with your account
3. Navigate to the **Agents** tab

### Step 2: Create New Agent
1. Click **"+ Launch an Agent"**
2. Select **"Create an Agentverse hosted Agent"**
3. Choose **"Blank Agent"** (we'll provide our own code)

### Step 3: Configure Agent
1. **Agent Name**: `HealthcareDiagnosisAgent`
2. **Description**: `AI agent for healthcare diagnosis and treatment planning using medical knowledge graphs`
3. **Tags**: `healthcare`, `diagnosis`, `medical`, `ai`, `innovationlab`

### Step 4: Upload Agent Code
1. Click on your agent to open the editor
2. Go to the **"Build"** tab
3. Copy the entire code from `agents/real_healthcare_agent.py`
4. Paste it into the code editor

### Step 5: Configure Agent Details
1. Go to the **"Overview"** tab
2. Click **"Edit"** to add agent description
3. Add the following description:

```
🏥 Healthcare Diagnosis Agent

I'm an AI agent specialized in healthcare diagnosis and treatment planning. I can analyze patient symptoms, provide medical diagnoses with confidence scores, and recommend appropriate treatments.

**Capabilities:**
- Symptom analysis and categorization
- Medical diagnosis with confidence scoring
- Treatment plan generation
- Risk assessment and recommendations
- Natural language processing
- ASI:One Chat Protocol integration

**Usage:**
Send me patient data in JSON format or ask me about medical symptoms and conditions. I'll provide comprehensive healthcare analysis including diagnoses, treatments, and recommendations.

**Example:**
"Analyze patient with chest pain, shortness of breath, and nausea"
"PATIENT_DATA: {\"patient_id\": \"P001\", \"age\": 65, \"symptoms\": [\"chest pain\", \"shortness of breath\"]}"
```

### Step 6: Start the Agent
1. Click the **"Start"** button
2. Wait for the agent to initialize
3. Check the **"Terminal"** tab for startup logs
4. Verify the agent is running successfully

### Step 7: Get Agent Address
1. Once started, copy the **Agent Address** from the terminal output
2. Format: `agent1q...` (long string)
3. Save this address for your hackathon submission

### Step 8: Test the Agent
1. Use the **Agentverse Chat Interface** to test your agent
2. Search for your agent by name or address
3. Send test messages to verify functionality

## 🧪 Testing Your Deployed Agent

### Test Case 1: Structured Data
```
PATIENT_DATA: {
  "patient_id": "TEST001",
  "age": 65,
  "gender": "Male",
  "symptoms": ["chest pain", "shortness of breath", "nausea"],
  "medical_history": ["diabetes", "hypertension"],
  "current_medications": ["metformin", "lisinopril"],
  "vital_signs": {"blood_pressure": "140/90"}
}
```

### Test Case 2: Natural Language
```
"I have chest pain and shortness of breath. What could be wrong?"
```

### Expected Response
The agent should respond with:
- Symptom analysis
- Possible diagnoses with confidence scores
- Treatment recommendations
- Risk assessment
- Next steps

## 🔗 ASI:One Integration

### Enable ASI:One Compatibility
1. Your agent already includes Chat Protocol implementation
2. The agent is automatically discoverable by ASI:One
3. Users can interact with your agent through ASI:One interface

### Test with ASI:One
1. Go to [ASI:One](https://asi.one)
2. Start a new chat
3. Toggle the "Agents" switch
4. Ask: "I need help with medical diagnosis"
5. ASI:One should suggest your Healthcare Diagnosis Agent

## 📊 Agent Performance Monitoring

### Key Metrics to Monitor
- **Response Time**: Should be < 5 seconds
- **Accuracy**: Verify diagnosis confidence scores
- **Uptime**: Agent should stay running
- **Error Rate**: Monitor for processing errors

### Troubleshooting
- **Agent Won't Start**: Check Python syntax and imports
- **No Response**: Verify Chat Protocol implementation
- **Errors**: Check terminal logs for debugging info

## 🏆 Hackathon Submission

### Required Information
1. **Agent Address**: `agent1q...` (from Agentverse)
2. **GitHub Repository**: Link to your code
3. **Demo Video**: 3-5 minute demonstration
4. **README**: Comprehensive documentation

### Submission Checklist
- ✅ Agent deployed to Agentverse
- ✅ Chat Protocol working
- ✅ ASI:One integration verified
- ✅ Agent address obtained
- ✅ Test cases passing
- ✅ Documentation complete

## 🎯 Success Criteria

Your agent should demonstrate:
- **Multi-agent Collaboration**: Healthcare agents working together
- **Medical Knowledge Integration**: MeTTa-style knowledge graphs
- **Natural Language Processing**: Conversational interface
- **Real-world Application**: Practical healthcare use case
- **ASI Alliance Technologies**: uAgents, Chat Protocol, Agentverse

## 📞 Support

If you encounter issues:
1. Check the [Innovation Lab Documentation](https://innovationlab.fetch.ai)
2. Review the [Agentverse Help](https://agentverse.ai/help)
3. Join the [Fetch.ai Discord](https://discord.gg/fetchai)
4. Check the [GitHub Examples](https://github.com/fetchai/innovation-lab-examples)

---

**Good luck with your hackathon submission!** 🏆

Your Healthcare AI Agents system demonstrates exactly what the ASI Alliance is looking for - innovative, practical AI agents that solve real-world problems using their cutting-edge technologies.
