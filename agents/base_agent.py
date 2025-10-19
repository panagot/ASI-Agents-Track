"""
Base Healthcare Agent - Common functionality for all healthcare agents
"""

from datetime import datetime
from uuid import uuid4
from typing import Dict, List, Any, Optional
from uagents import Agent, Context, Protocol
from uagents.setup import fund_agent_if_low
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from pydantic import BaseModel
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PatientData(BaseModel):
    """Patient information model"""
    patient_id: str
    age: int
    gender: str
    symptoms: List[str]
    medical_history: List[str]
    current_medications: List[str]
    vital_signs: Dict[str, Any]
    timestamp: datetime

class Diagnosis(BaseModel):
    """Diagnosis model"""
    condition: str
    confidence: float
    reasoning: str
    supporting_evidence: List[str]
    differential_diagnoses: List[str]

class Treatment(BaseModel):
    """Treatment recommendation model"""
    treatment_type: str
    medication: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    instructions: str
    side_effects: List[str]
    contraindications: List[str]

class AgentMessage(BaseModel):
    """Message format for agent communication"""
    message_type: str
    sender_agent: str
    content: Dict[str, Any]
    timestamp: datetime
    message_id: str

class BaseHealthcareAgent:
    """Base class for all healthcare agents"""
    
    def __init__(self, name: str, agent_type: str, seed_phrase: str):
        self.name = name
        self.agent_type = agent_type
        self.agent = Agent(name=name, seed=seed_phrase)
        self.chat_proto = Protocol(spec=chat_protocol_spec)
        self.setup_agent()
    
    def setup_agent(self):
        """Setup agent with chat protocol"""
        # Initialize the chat protocol
        self.chat_proto = Protocol(spec=chat_protocol_spec)
        
        # Handle incoming chat messages
        @self.chat_proto.on_message(ChatMessage)
        async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
            await self.process_message(ctx, sender, msg)
        
        # Handle acknowledgements
        @self.chat_proto.on_message(ChatAcknowledgement)
        async def handle_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
            logger.info(f"{self.name} received acknowledgement from {sender}")
        
        # Include the chat protocol
        self.agent.include(self.chat_proto, publish_manifest=True)
    
    async def process_message(self, ctx: Context, sender: str, msg: ChatMessage):
        """Process incoming messages - to be implemented by subclasses"""
        # Always send acknowledgement
        await ctx.send(sender, ChatAcknowledgement(
            timestamp=datetime.utcnow(),
            acknowledged_msg_id=msg.msg_id
        ))
        
        # Process content
        for item in msg.content:
            if isinstance(item, StartSessionContent):
                logger.info(f"{self.name} started session with {sender}")
            elif isinstance(item, TextContent):
                await self.handle_text_message(ctx, sender, item.text)
            elif isinstance(item, EndSessionContent):
                logger.info(f"{self.name} ended session with {sender}")
    
    async def handle_text_message(self, ctx: Context, sender: str, text: str):
        """Handle text messages - to be implemented by subclasses"""
        pass
    
    def create_text_chat(self, text: str, end_session: bool = False) -> ChatMessage:
        """Create a text chat message"""
        content = [TextContent(type="text", text=text)]
        return ChatMessage(
            timestamp=datetime.utcnow(),
            msg_id=uuid4(),
            content=content,
        )
    
    def create_agent_message(self, message_type: str, content: Dict[str, Any]) -> AgentMessage:
        """Create a structured agent message"""
        return AgentMessage(
            message_type=message_type,
            sender_agent=self.name,
            content=content,
            timestamp=datetime.utcnow(),
            message_id=str(uuid4())
        )
    
    async def send_message(self, ctx: Context, recipient: str, message: str):
        """Send a message to another agent"""
        chat_message = self.create_text_chat(message)
        await ctx.send(recipient, chat_message)
        logger.info(f"{self.name} sent message to {recipient}: {message}")
    
    def run(self):
        """Run the agent"""
        fund_agent_if_low(self.agent.wallet.address())
        self.agent.run()

