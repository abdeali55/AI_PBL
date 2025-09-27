"""
Service for government mental health services and emergency contacts.
"""
from typing import Dict, List, Optional
from config import Constants
from logging_config import logger, LoggingMixin
from models import GovernmentService, GovernmentServicesRequest, GovernmentServicesResponse


class GovernmentServiceProvider(LoggingMixin):
    """Service for providing government mental health services information."""
    
    def __init__(self):
        """Initialize the government service."""
        self.emergency_services = Constants.EMERGENCY_SERVICES
        self.mental_health_helplines = Constants.MENTAL_HEALTH_HELPLINES
        self.state_services = Constants.STATE_SERVICES
        self.online_resources = Constants.ONLINE_RESOURCES
    
    def get_services_for_location(self, location: str) -> GovernmentServicesResponse:
        """
        Get government mental health services for a specific location.
        
        Args:
            location: Location to get services for
            
        Returns:
            Government services response with relevant services
        """
        self.logger.info(f"Getting government services for location: {location}")
        
        # Determine if location is in India or other countries
        location_lower = location.lower()
        
        if self._is_indian_location(location_lower):
            return self._get_indian_services(location)
        elif self._is_us_location(location_lower):
            return self._get_us_services(location)
        elif self._is_uk_location(location_lower):
            return self._get_uk_services(location)
        else:
            return self._get_international_services(location)
    
    def _is_indian_location(self, location: str) -> bool:
        """Check if location is in India."""
        indian_indicators = [
            "india", "indian", "mumbai", "delhi", "bangalore", "chennai", 
            "kolkata", "hyderabad", "pune", "ahmedabad", "gurgaon", "noida"
        ]
        return any(indicator in location for indicator in indian_indicators)
    
    def _is_us_location(self, location: str) -> bool:
        """Check if location is in the US."""
        us_indicators = ["usa", "united states", "america", "us", "new york", "california", "texas"]
        return any(indicator in location for indicator in us_indicators)
    
    def _is_uk_location(self, location: str) -> bool:
        """Check if location is in the UK."""
        uk_indicators = ["uk", "united kingdom", "england", "scotland", "wales", "northern ireland", "london"]
        return any(indicator in location for indicator in uk_indicators)
    
    def _get_indian_services(self, location: str) -> GovernmentServicesResponse:
        """Get Indian government mental health services."""
        services = [
            GovernmentService(
                name="KIRAN Mental Health Rehabilitation Helpline",
                number=self.mental_health_helplines["kiran"],
                description="24/7 toll-free mental health support",
                available_24_7=True,
                toll_free=True
            ),
            GovernmentService(
                name="Vandrevala Foundation",
                number=self.mental_health_helplines["vandrevala"],
                description="24/7 toll-free mental health support",
                available_24_7=True,
                toll_free=True
            ),
            GovernmentService(
                name="iCall Suicide Prevention",
                number=self.mental_health_helplines["icall"],
                description="Suicide prevention and crisis support",
                available_24_7=True,
                toll_free=False
            )
        ]
        
        # Add state-specific services
        state_service = self._get_state_specific_service(location)
        if state_service:
            services.append(state_service)
        
        return GovernmentServicesResponse(
            services=services,
            location=location,
            emergency_services=self.emergency_services
        )
    
    def _get_us_services(self, location: str) -> GovernmentServicesResponse:
        """Get US government mental health services."""
        services = [
            GovernmentService(
                name="National Suicide Prevention Lifeline",
                number="988",
                description="24/7 toll-free suicide prevention",
                available_24_7=True,
                toll_free=True
            ),
            GovernmentService(
                name="Crisis Text Line",
                number="Text HOME to 741741",
                description="24/7 crisis text support",
                available_24_7=True,
                toll_free=True
            ),
            GovernmentService(
                name="SAMHSA National Helpline",
                number="1-800-662-4357",
                description="24/7 substance abuse and mental health support",
                available_24_7=True,
                toll_free=True
            )
        ]
        
        emergency_services = {
            "emergency": "911",
            "domestic_violence": "1-800-799-7233",
            "child_abuse": "1-800-4-A-CHILD"
        }
        
        return GovernmentServicesResponse(
            services=services,
            location=location,
            emergency_services=emergency_services
        )
    
    def _get_uk_services(self, location: str) -> GovernmentServicesResponse:
        """Get UK government mental health services."""
        services = [
            GovernmentService(
                name="Samaritans",
                number="116 123",
                description="24/7 free mental health support",
                available_24_7=True,
                toll_free=True
            ),
            GovernmentService(
                name="Crisis Text Line UK",
                number="Text SHOUT to 85258",
                description="24/7 crisis text support",
                available_24_7=True,
                toll_free=True
            ),
            GovernmentService(
                name="Mind Infoline",
                number="0300 123 3393",
                description="Mental health information and support",
                available_24_7=False,
                toll_free=True
            )
        ]
        
        emergency_services = {
            "emergency": "999",
            "non_emergency_police": "101",
            "nhs_111": "111"
        }
        
        return GovernmentServicesResponse(
            services=services,
            location=location,
            emergency_services=emergency_services
        )
    
    def _get_international_services(self, location: str) -> GovernmentServicesResponse:
        """Get international mental health services."""
        services = [
            GovernmentService(
                name="International Association for Suicide Prevention",
                number="www.iasp.info/resources/Crisis_Centres/",
                description="Global crisis center directory",
                available_24_7=False,
                toll_free=False
            ),
            GovernmentService(
                name="Befrienders Worldwide",
                number="www.befrienders.org",
                description="Global emotional support",
                available_24_7=False,
                toll_free=False
            )
        ]
        
        emergency_services = {
            "local_emergency": "Contact local emergency services",
            "crisis_text": "Text HOME to 741741 (US/UK/Canada)"
        }
        
        return GovernmentServicesResponse(
            services=services,
            location=location,
            emergency_services=emergency_services
        )
    
    def _get_state_specific_service(self, location: str) -> Optional[GovernmentService]:
        """Get state-specific mental health service."""
        location_lower = location.lower()
        
        # Map cities to states
        city_to_state = {
            "mumbai": "maharashtra",
            "pune": "maharashtra",
            "delhi": "delhi",
            "bangalore": "karnataka",
            "chennai": "tamil_nadu",
            "kolkata": "west_bengal",
            "hyderabad": "telangana"
        }
        
        state = None
        for city, state_name in city_to_state.items():
            if city in location_lower:
                state = state_name
                break
        
        if state and state in self.state_services:
            return GovernmentService(
                name=f"{state.replace('_', ' ').title()} Mental Health Services",
                number=self.state_services[state],
                description=f"State-specific mental health services for {state.replace('_', ' ').title()}",
                available_24_7=False,
                toll_free=False
            )
        
        return None
    
    def format_services_response(self, location: str) -> str:
        """
        Get formatted government services response for a location.
        
        Args:
            location: Location to get services for
            
        Returns:
            Formatted string with government services
        """
        services_response = self.get_services_for_location(location)
        
        if self._is_indian_location(location.lower()):
            return self._format_indian_services_text(services_response)
        elif self._is_us_location(location.lower()):
            return self._format_us_services_text(services_response)
        elif self._is_uk_location(location.lower()):
            return self._format_uk_services_text(services_response)
        else:
            return self._format_international_services_text(services_response)
    
    def _format_indian_services_text(self, response: GovernmentServicesResponse) -> str:
        """Format Indian services as text."""
        text = f"""🇮🇳 **Government Mental Health Services - India**

**National Mental Health Helpline:**
• **KIRAN Mental Health Rehabilitation Helpline**: {self.mental_health_helplines['kiran']} (24/7, Toll-free)
• **Vandrevala Foundation**: {self.mental_health_helplines['vandrevala']} / 1800-2333-330 (24/7, Toll-free)

**Emergency Services:**
• **Police**: {self.emergency_services['police']}
• **Ambulance**: {self.emergency_services['ambulance']}
• **Women Helpline**: {self.emergency_services['women_helpline']} (24/7)
• **Child Helpline**: {self.emergency_services['child_helpline']} (24/7)

**State-wise Mental Health Services:**
• **Maharashtra (Mumbai/Pune)**: {self.state_services['maharashtra']}
• **Delhi**: {self.state_services['delhi']}
• **Karnataka (Bangalore)**: {self.state_services['karnataka']}
• **Tamil Nadu (Chennai)**: {self.state_services['tamil_nadu']}
• **West Bengal (Kolkata)**: {self.state_services['west_bengal']}
• **Telangana (Hyderabad)**: {self.state_services['telangana']}

**Specialized Services:**
• **Suicide Prevention**: {self.mental_health_helplines['icall']} (iCall, TISS)
• **LGBTQ+ Support**: 022-25563291 (Humsafar Trust)
• **Domestic Violence**: {self.emergency_services['women_helpline']} (Women Helpline)

**Online Resources:**
• **National Institute of Mental Health & Neurosciences (NIMHANS)**: {self.online_resources['nimhans']}
• **Ministry of Health & Family Welfare**: {self.online_resources['mohfw']}

*All services are confidential and free of cost.*"""
        
        return text
    
    def _format_us_services_text(self, response: GovernmentServicesResponse) -> str:
        """Format US services as text."""
        return """🇺🇸 **Government Mental Health Services - United States**

**National Mental Health Helplines:**
• **National Suicide Prevention Lifeline**: 988 (24/7, Toll-free)
• **Crisis Text Line**: Text HOME to 741741 (24/7)
• **SAMHSA National Helpline**: 1-800-662-4357 (24/7, Toll-free)

**Emergency Services:**
• **Emergency Services**: 911
• **National Domestic Violence Hotline**: 1-800-799-7233
• **Childhelp National Child Abuse Hotline**: 1-800-4-A-CHILD

**Veterans Services:**
• **Veterans Crisis Line**: 1-800-273-8255, Press 1
• **Veterans Crisis Text Line**: Text 838255

**Online Resources:**
• **SAMHSA**: www.samhsa.gov
• **National Institute of Mental Health**: www.nimh.nih.gov
• **Mental Health America**: www.mhanational.org

*All services are confidential and free of cost.*"""
    
    def _format_uk_services_text(self, response: GovernmentServicesResponse) -> str:
        """Format UK services as text."""
        return """🇬🇧 **Government Mental Health Services - United Kingdom**

**National Mental Health Helplines:**
• **Samaritans**: 116 123 (24/7, Free)
• **Crisis Text Line UK**: Text SHOUT to 85258
• **Mind Infoline**: 0300 123 3393 (Mon-Fri, 9am-6pm)

**Emergency Services:**
• **Emergency Services**: 999
• **Non-emergency Police**: 101
• **NHS 111**: 111 (24/7, Free)

**Specialized Services:**
• **CALM (Campaign Against Living Miserably)**: 0800 58 58 58 (5pm-midnight)
• **Papyrus (Young People)**: 0800 068 41 41
• **Refuge (Domestic Violence)**: 0808 2000 247

**Online Resources:**
• **NHS Mental Health**: www.nhs.uk/mental-health
• **Mind**: www.mind.org.uk
• **Rethink Mental Illness**: www.rethink.org

*All services are confidential and free of cost.*"""
    
    def _format_international_services_text(self, response: GovernmentServicesResponse) -> str:
        """Format international services as text."""
        return f"""🌍 **International Mental Health Resources**

**Global Emergency Services:**
• **International Association for Suicide Prevention**: www.iasp.info/resources/Crisis_Centres/
• **Befrienders Worldwide**: www.befrienders.org
• **International Crisis Text Line**: Text HOME to 741741 (US/UK/Canada)

**Online Resources:**
• **World Health Organization Mental Health**: www.who.int/mental_health
• **Mental Health Foundation**: www.mentalhealth.org.uk
• **International Mental Health**: www.mentalhealth.org

**For {response.location}:**
Please contact your local emergency services or search for mental health services in your specific country/region. Most countries have national mental health helplines and emergency services.

*Remember: You are not alone. Help is available 24/7 in most countries.*"""

