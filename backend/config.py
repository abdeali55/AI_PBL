"""
Configuration management for the AI Mental Health Therapist application.
"""
from typing import Dict, List, Optional
import os


class Settings:
    """Application settings with environment variable support."""
    
    def __init__(self):
        # API Configuration
        self.backend_host = os.getenv("BACKEND_HOST", "0.0.0.0")
        self.backend_port = int(os.getenv("BACKEND_PORT", "8000"))
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:8501")
        
        # AI Model Configuration
        self.ollama_model = os.getenv("OLLAMA_MODEL", "alibayram/medgemma:4b")
        self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "350"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        self.top_p = float(os.getenv("TOP_P", "0.9"))
        
        # Location Services
        self.max_distance_km = int(os.getenv("MAX_DISTANCE_KM", "10"))
        self.ip_geolocation_timeout = int(os.getenv("IP_GEOLOCATION_TIMEOUT", "5"))
        
        # Database Configuration
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./therapists.db")
        
        # Logging Configuration
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", None)
        
        # Security
        self.rate_limit_per_minute = int(os.getenv("RATE_LIMIT_PER_MINUTE", "10"))


# Global settings instance
settings = Settings()


# Constants
class Constants:
    """Application constants."""
    
    # Emergency Services
    EMERGENCY_SERVICES = {
        "police": "100",
        "ambulance": "108",
        "women_helpline": "181",
        "child_helpline": "1098"
    }
    
    # Mental Health Helplines
    MENTAL_HEALTH_HELPLINES = {
        "kiran": "1800-599-0019",
        "vandrevala": "1860-2662-345",
        "icall": "9152987821"
    }
    
    # Major Indian Cities Coordinates
    MAJOR_CITIES = {
        "mumbai": {"lat": 19.0760, "lon": 72.8777},
        "delhi": {"lat": 28.7041, "lon": 77.1025},
        "bangalore": {"lat": 12.9716, "lon": 77.5946},
        "chennai": {"lat": 13.0827, "lon": 80.2707},
        "kolkata": {"lat": 22.5726, "lon": 88.3639},
        "hyderabad": {"lat": 17.3850, "lon": 78.4867},
        "pune": {"lat": 18.5204, "lon": 73.8567},
        "ahmedabad": {"lat": 23.0225, "lon": 72.5714}
    }
    
    # State-wise Mental Health Services
    STATE_SERVICES = {
        "maharashtra": "022-24131212",
        "delhi": "011-23389090",
        "karnataka": "080-25497777",
        "tamil_nadu": "044-28554400",
        "west_bengal": "033-24637401",
        "telangana": "040-23220000"
    }
    
    # Online Resources
    ONLINE_RESOURCES = {
        "nimhans": "www.nimhans.ac.in",
        "mohfw": "www.mohfw.gov.in",
        "psychology_today": "www.psychologytoday.com"
    }


# Therapist Database (to be moved to actual database later)
THERAPIST_DATABASE = {
    "mumbai": [
        {
            "name": "Dr. Ayesha Kapoor",
            "type": "Clinical Psychologist",
            "phone": "+91 22-1234-5678",
            "specialization": "Anxiety, Depression, Trauma",
            "location": "Bandra West, Mumbai",
            "rating": 4.8,
            "lat": 19.0760,
            "lon": 72.8777
        },
        {
            "name": "Dr. James Patel",
            "type": "Psychiatrist",
            "phone": "+91 22-9876-5432",
            "specialization": "Bipolar Disorder, Schizophrenia",
            "location": "Andheri West, Mumbai",
            "rating": 4.6,
            "lat": 19.0821,
            "lon": 72.8866
        },
        {
            "name": "MindCare Counseling Center",
            "type": "Counseling Center",
            "phone": "+91 22-2222-3333",
            "specialization": "Family Therapy, Couples Counseling",
            "location": "Powai, Mumbai",
            "rating": 4.7,
            "lat": 19.0692,
            "lon": 72.8984
        },
        {
            "name": "Dr. Priya Sharma",
            "type": "Clinical Psychologist",
            "phone": "+91 22-4444-5555",
            "specialization": "Child & Adolescent Therapy",
            "location": "Juhu, Mumbai",
            "rating": 4.9,
            "lat": 19.1079,
            "lon": 72.8265
        }
    ],
    "delhi": [
        {
            "name": "Dr. Rajesh Kumar",
            "type": "Psychiatrist",
            "phone": "+91 11-1111-2222",
            "specialization": "Mood Disorders, Addiction",
            "location": "Connaught Place, Delhi",
            "rating": 4.5,
            "lat": 28.6315,
            "lon": 77.2167
        },
        {
            "name": "Wellness Hub Delhi",
            "type": "Wellness Center",
            "phone": "+91 11-3333-4444",
            "specialization": "Stress Management, Work-life Balance",
            "location": "Gurgaon, Delhi NCR",
            "rating": 4.6,
            "lat": 28.4595,
            "lon": 77.0266
        },
        {
            "name": "Dr. Sunita Reddy",
            "type": "Clinical Psychologist",
            "phone": "+91 11-5555-6666",
            "specialization": "Eating Disorders, Body Image",
            "location": "South Delhi",
            "rating": 4.8,
            "lat": 28.5355,
            "lon": 77.3910
        }
    ],
    "bangalore": [
        {
            "name": "Dr. Lakshmi Nair",
            "type": "Psychiatrist",
            "phone": "+91 80-9999-0000",
            "specialization": "Anxiety, Panic Disorders",
            "location": "Koramangala, Bangalore",
            "rating": 4.7,
            "lat": 12.9279,
            "lon": 77.6271
        },
        {
            "name": "Bangalore Mental Health Center",
            "type": "Mental Health Center",
            "phone": "+91 80-7777-8888",
            "specialization": "Child & Adolescent Therapy",
            "location": "Indiranagar, Bangalore",
            "rating": 4.6,
            "lat": 12.9716,
            "lon": 77.6412
        },
        {
            "name": "Dr. Amit Banerjee",
            "type": "Clinical Psychologist",
            "phone": "+91 80-1111-3333",
            "specialization": "Relationship Counseling",
            "location": "Whitefield, Bangalore",
            "rating": 4.9,
            "lat": 12.9698,
            "lon": 77.7500
        }
    ],
    "chennai": [
        {
            "name": "Dr. Meera Krishnan",
            "type": "Psychiatrist",
            "phone": "+91 44-2222-3333",
            "specialization": "Depression, PTSD",
            "location": "T. Nagar, Chennai",
            "rating": 4.6,
            "lat": 13.0418,
            "lon": 80.2341
        },
        {
            "name": "Chennai Counseling Center",
            "type": "Counseling Center",
            "phone": "+91 44-4444-5555",
            "specialization": "Family Therapy, Grief Counseling",
            "location": "Anna Nagar, Chennai",
            "rating": 4.5,
            "lat": 13.0827,
            "lon": 80.2707
        }
    ],
    "kolkata": [
        {
            "name": "Dr. Sushmita Das",
            "type": "Clinical Psychologist",
            "phone": "+91 33-1111-2222",
            "specialization": "Anxiety, Phobias",
            "location": "Salt Lake, Kolkata",
            "rating": 4.7,
            "lat": 22.5937,
            "lon": 88.4009
        },
        {
            "name": "Kolkata Mental Health Clinic",
            "type": "Mental Health Clinic",
            "phone": "+91 33-3333-4444",
            "specialization": "Addiction Counseling",
            "location": "Park Street, Kolkata",
            "rating": 4.4,
            "lat": 22.5448,
            "lon": 88.3426
        }
    ],
    "hyderabad": [
        {
            "name": "Dr. Ravi Teja",
            "type": "Psychiatrist",
            "phone": "+91 40-5555-6666",
            "specialization": "Bipolar Disorder, ADHD",
            "location": "Banjara Hills, Hyderabad",
            "rating": 4.8,
            "lat": 17.4065,
            "lon": 78.4772
        },
        {
            "name": "Hyderabad Wellness Center",
            "type": "Wellness Center",
            "phone": "+91 40-7777-8888",
            "specialization": "Stress Management, Mindfulness",
            "location": "Gachibowli, Hyderabad",
            "rating": 4.6,
            "lat": 17.4399,
            "lon": 78.3483
        }
    ]
}