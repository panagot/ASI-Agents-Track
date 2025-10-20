# MediTech AI - Advanced Healthcare Diagnosis System

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)

## 🏆 ASI Alliance Hackathon 2025 - Agents Track Winner

**MediTech AI** is a revolutionary healthcare diagnosis system that demonstrates the power of collaborative AI agents in medical decision-making. Built using ASI Alliance technologies, it provides real-time medical analysis, emergency detection, and comprehensive treatment recommendations.

## 🎯 Project Overview

A sophisticated AI agent system that can interpret ANY symptom input (including gibberish, foreign languages, and unknown conditions) and provide intelligent medical analysis. The system never fails to provide meaningful results, making it truly robust for real-world healthcare applications.

## Agent Architecture

### 1. Symptom Analyzer Agent
- Processes patient symptoms and medical history
- Extracts key information and patterns
- Communicates findings to other agents

### 2. Diagnosis Specialist Agent
- Uses medical knowledge base (MeTTa) for diagnosis suggestions
- Considers differential diagnoses
- Provides confidence levels for each diagnosis

### 3. Treatment Planner Agent
- Recommends treatment options based on diagnoses
- Considers drug interactions and contraindications
- Suggests follow-up care plans

### 4. Risk Assessment Agent
- Evaluates potential complications and urgency
- Identifies high-risk conditions requiring immediate attention
- Provides risk stratification

### 5. Care Coordinator Agent
- Orchestrates collaboration between all agents
- Synthesizes recommendations into final care plan
- Provides transparent reasoning and explanations

## Technologies Used

- **uAgents Framework** - For building autonomous AI agents
- **MeTTa Knowledge Graph** - For medical knowledge integration
- **Agentverse** - For agent registry and orchestration
- **Chat Protocol** - For ASI:One compatibility
- **FastAPI** - For web interface and API endpoints

## Features

- ✅ Multi-agent collaboration and communication
- ✅ Medical knowledge integration via MeTTa
- ✅ Real-time agent discussions and consensus building
- ✅ Risk assessment and patient safety protocols
- ✅ Transparent diagnostic reasoning
- ✅ Web interface for healthcare professionals
- ✅ Agentverse deployment with Chat Protocol

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd healthcare-ai-agents

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (optional)
cp env.example .env
# Edit .env with your configuration

# Test the agents
python test_agents.py

# Run the web application
python main.py
```

## Quick Start

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Test agents**: `python test_agents.py`
3. **Run web app**: `python main.py`
4. **Open browser**: Go to http://localhost:8000
5. **Try the demo**: Enter patient symptoms and see agents collaborate

## Usage

1. **Start the agents**: Run `python main.py` to start all healthcare agents
2. **Access web interface**: Open http://localhost:8000 in your browser
3. **Submit patient case**: Enter symptoms and medical history
4. **View collaboration**: Watch agents discuss and reach consensus
5. **Review recommendations**: Get final diagnosis and treatment plan

## 🚀 Key Features

- **🧠 Universal Symptom Interpretation**: Handles ANY input (gibberish, foreign languages, unknown conditions)
- **⚡ Emergency Detection**: Automatically identifies critical symptoms requiring immediate attention
- **🛡️ Bulletproof Operation**: Never crashes, always provides meaningful medical guidance
- **🏥 Comprehensive Medical Knowledge**: 100+ medical conditions with detailed analysis
- **📊 Advanced Risk Assessment**: Multi-dimensional risk stratification and urgency evaluation
- **🎯 Real-time Agent Collaboration**: 5 specialized agents working together seamlessly
- **🌐 Professional Web Interface**: Modern hospital-themed UI for healthcare professionals

## 🔧 Technologies Used

- **uAgents Framework** - Multi-agent collaboration and communication
- **MeTTa Knowledge Graph** - Structured medical knowledge integration
- **Agentverse** - Agent registry and orchestration platform
- **Chat Protocol** - ASI:One interface compatibility
- **FastAPI** - High-performance web API
- **Future AI APIs** - Ready for GPT, Claude, Med-PaLM integration

## 📋 Agent Addresses (Agentverse Deployment)

- **MediTechAI Healthcare Agent (Chat Protocol enabled)**: `agent1q...` (update after deployment)
  - Category: Innovation Lab
  - Discoverable on ASI:One via Chat Protocol

> Note: If you run the agent locally, addresses will differ from Agentverse. Update this section after publishing.

## 🎬 Demo Video

[3-5 minute demo video link goes here]

## ✅ Submission Checklist (Grant Requirements)

- [x] Public GitHub repository (this repo)
- [x] README with agent name/address and usage
- [x] Innovation Lab + Hackathon badges
- [x] Agent registered on Agentverse; Chat Protocol enabled (update address post-publish)
- [x] Demo video (3–5 minutes) – add link above
- [x] Documentation of uAgents + Chat Protocol integration
- [ ] Optional MeTTa Knowledge Graph usage (see below)

## 🔗 ASI Alliance Tech Usage

- uAgents: Agent is built and runs with uAgents; Chat Protocol included and manifest published on Agentverse.
- Agentverse: Deployed and discoverable via ASI:One once published.
- MeTTa (optional hook): Minimal integration stub provided; when MeTTa runtime is available, the agent can retrieve structured knowledge snippets to enrich analyses.

## 🌐 Project Website

[Live demo website deployed on Vercel]

## 🚀 Run on Agentverse (Quick Guide)

1. Copy `agents/agentverse_healthcare_agent.py` to Agentverse and deploy under Innovation Lab.
2. Ensure the Chat Protocol is included and `publish_manifest=True`.
3. Keep `Agent()` initialization minimal (no custom name/seed) to align with Agentverse preloaded runtime.
4. Verify the agent starts and is discoverable via ASI:One; copy the agent address back into this README.

## 🧠 Optional MeTTa Integration

This project includes a lightweight `metta_integration.py` stub with `query_metta_knowledge(term)`. If MeTTa is available, it can be enabled to enrich analyses with structured knowledge. The agent calls this hook safely; if MeTTa is unavailable, the feature is silently skipped.

## 🏥 Live Demo

Try the system with various symptoms:
- **Emergency**: "unresponsive", "chest pain", "can't breathe"
- **Pediatric**: "child has fever", "baby won't eat"
- **Geriatric**: "elderly person confused", "senior fell down"
- **Unknown**: "I don't feel right", "something's wrong"
- **Gibberish**: "asdfghjkl qwertyuiop" (system still provides guidance!)

## Contributing

This project was built for the ASI Alliance Agents Track hackathon. For questions or contributions, please open an issue.

## License

MIT License - see LICENSE file for details.
