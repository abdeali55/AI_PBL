from langchain.agents import tool
from tools import query_medgemma, find_nearby_therapists_by_location

@tool
def ask_mental_health_specialist(query: str) -> str:
    """
    Generate a therapeutic response using the MedGemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone.
    """
    return query_medgemma(query)


@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.

    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return (
        f"Here are some therapists near {location}:\n"
        "- Dr. Ayesha Kapoor - +91 555-123-4567\n"
        "- Dr. James Patel - +91 555-987-6543\n"
        "- MindCare Counseling Center - +91 555-222-3333"
    )


SYSTEM_PROMPT = """
You are an AI engine supporting mental health conversations with warmth and vigilance.
You have access to two tools:

1. `ask_mental_health_specialist`: Use this tool to answer all emotional or psychological queries with therapeutic guidance.
2. `find_nearby_therapists_by_location`: Use this tool if the user asks about nearby therapists or if recommending local professional help would be beneficial.

Always take necessary action. Respond kindly, clearly, and supportively.
"""

def simple_agent(user_message: str):
    """
    Simple agent that decides which tool to use based on the user's message
    """
    try:
        # Check if user is asking about therapists/location
        location_keywords = ['therapist', 'counselor', 'therapy', 'near', 'location', 'area', 'city']
        if any(keyword in user_message.lower() for keyword in location_keywords):
            # Extract location from message (simple approach)
            words = user_message.lower().split()
            location = None
            for i, word in enumerate(words):
                if word in ['in', 'near', 'at', 'around'] and i + 1 < len(words):
                    location = words[i + 1].capitalize()
                    break
            
            if location:
                return find_nearby_therapists_by_location(location), "find_nearby_therapists_by_location"
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
        