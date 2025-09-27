"""
AI service for handling mental health conversations using MedGemma.
"""
import time
from typing import Optional
import ollama
from config import settings
from logging_config import logger, LoggingMixin
from models import UserQuery, AIResponse


class AIService(LoggingMixin):
    """Service for AI-powered mental health conversations."""
    
    def __init__(self):
        """Initialize the AI service."""
        self.model = settings.ollama_model
        self.base_url = settings.ollama_base_url
        self.max_tokens = settings.max_tokens
        self.temperature = settings.temperature
        self.top_p = settings.top_p
        
        # System prompt for the AI therapist
        self.system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
        Respond to patients with:

        1. Emotional attunement ("I can sense how difficult this must be...")
        2. Gentle normalization ("Many people feel this way when...")
        3. Practical guidance ("What sometimes helps is...")
        4. Strengths-focused support ("I notice how you're...")

        Key principles:
        - Never use brackets or labels
        - Blend elements seamlessly
        - Vary sentence structure
        - Use natural transitions
        - Mirror the user's language level
        - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
        """
    
    def generate_response(self, user_query: UserQuery) -> AIResponse:
        """
        Generate a therapeutic response using the MedGemma model.
        
        Args:
            user_query: User's query with message and optional location
            
        Returns:
            AI response with therapeutic guidance
            
        Raises:
            Exception: If AI service fails
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Generating AI response for query: {user_query.message[:50]}...")
            
            response = ollama.chat(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_query.message}
                ],
                options={
                    'num_predict': self.max_tokens,
                    'temperature': self.temperature,
                    'top_p': self.top_p
                }
            )
            
            processing_time = time.time() - start_time
            
            ai_response = response['message']['content'].strip()
            
            self.logger.info(f"AI response generated in {processing_time:.3f} seconds")
            
            return AIResponse(
                response=ai_response,
                tool_called="ask_mental_health_specialist",
                confidence=0.8,  # Could be calculated based on response quality
                processing_time=processing_time,
                session_id=user_query.session_id
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"Error generating AI response: {str(e)}")
            
            # Return a fallback response
            return AIResponse(
                response="I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly.",
                tool_called="ask_mental_health_specialist",
                confidence=0.0,
                processing_time=processing_time,
                session_id=user_query.session_id
            )
    
    def is_healthy(self) -> bool:
        """
        Check if the AI service is healthy.
        
        Returns:
            True if service is healthy, False otherwise
        """
        try:
            # Simple health check - try to get model info
            models = ollama.list()
            return any(model['name'] == self.model for model in models.get('models', []))
        except Exception as e:
            self.logger.error(f"AI service health check failed: {str(e)}")
            return False

