from langchain.agents import tool
from typing import Tuple
from services.ai_service import AIService
from services.therapist_service import TherapistService
from services.government_service import GovernmentServiceProvider
from models import UserQuery
from logging_config import logger

# Initialize services
ai_service = AIService()
therapist_service = TherapistService()
government_service = GovernmentServiceProvider()


@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    
    Args:
        query: User's mental health query
        
    Returns:
        Therapeutic response from AI specialist
    """
    try:
        user_query = UserQuery(message=query)
        response = ai_service.generate_response(user_query)
        return response.response
    except Exception as e:
        logger.error(f"Error in ask_mental_health_specialist: {str(e)}")
        return "I'm having technical difficulties, but I want you to know your feelings matter. Please try again shortly."


@tool
def find_nearby_therapists_tool(location: str) -> str:
    """
    Finds and returns a comprehensive list of licensed therapists near the specified location.

    Args:
        location: The name of the city or area in which the user is seeking therapy support.

    Returns:
        A detailed string containing therapist names, specializations, and contact info.
    """
    try:
        return therapist_service.get_therapist_recommendations(location)
    except Exception as e:
        logger.error(f"Error in find_nearby_therapists_tool: {str(e)}")
        return "I'm having trouble accessing therapist information. Please try again shortly."


@tool
def get_government_services_tool(location: str = "India") -> str:
    """
    Provides government mental health service numbers and emergency contacts based on location.
    
    Args:
        location: The country or region for which to provide government services.
        
    Returns:
        A formatted string with government mental health services and emergency contacts.
    """
    try:
        return government_service.format_services_response(location)
    except Exception as e:
        logger.error(f"Error in get_government_services_tool: {str(e)}")
        return "I'm having trouble accessing government services information. Please try again shortly."


SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to three tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_tool`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.
3. `get_government_services_tool`: Use this tool when users need government mental health services, emergency contacts, or crisis helplines based on their location.

Always take necessary action. Respond kindly, clearly, and supportively. When users mention their location or ask for emergency services, proactively provide both therapist recommendations and government services.
"""

def simple_agent(user_message: str):
    """
    Simple agent that decides which tool to use based on the user's message
    """
    try:
        message_lower = user_message.lower()
        
        # Check for government services/emergency keywords
        gov_keywords = ['emergency', 'crisis', 'helpline', 'government', 'police', 'ambulance', 'suicide', 'help line', 'mental health services', 'crisis line']
        if any(keyword in message_lower for keyword in gov_keywords):
            # Extract location from message
            words = message_lower.split()
            location = "India"  # Default to India
            
            # Look for location indicators
            for i, word in enumerate(words):
                if word in ['in', 'near', 'at', 'around', 'from'] and i + 1 < len(words):
                    location = words[i + 1].capitalize()
                    break
                elif word in ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad', 'india', 'usa', 'uk']:
                    location = word.capitalize()
                    break
            
            return get_government_services_tool(location), "get_government_services_tool"
        
        # Check if user is asking about therapists/location
        therapist_keywords = ['therapist', 'counselor', 'therapy', 'psychologist', 'psychiatrist', 'mental health professional']
        if any(keyword in message_lower for keyword in therapist_keywords):
            # Extract location from message
            words = message_lower.split()
            location = None
            for i, word in enumerate(words):
                if word in ['in', 'near', 'at', 'around'] and i + 1 < len(words):
                    location = words[i + 1].capitalize()
                    break
                elif word in ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'ahmedabad']:
                    location = word.capitalize()
                    break
            
            if location:
                return find_nearby_therapists_tool(location), "find_nearby_therapists_tool"
            else:
                return "I'd be happy to help you find a therapist. Could you please specify which city or area you're looking in?", "None"
        
        # For all other queries, use the mental health specialist
        else:
            return ask_mental_health_specialist(user_message), "ask_mental_health_specialist"
            
    except Exception as e:
        print(f"Error in simple agent: {e}")
        return "I apologize, but I encountered an error processing your request. Please try again.", "Error"

def parse_response(result):
    """
    Parse the result from the simple agent
    """
    if isinstance(result, tuple):
        final_response, tool_called_name = result
    else:
        final_response = result
        tool_called_name = "None"
    
    # Ensure we have a response
    if not final_response:
        final_response = "I'm here to help. Could you please tell me more about what you'd like to discuss?"
    
    return tool_called_name, final_response
