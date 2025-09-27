"""
Service for managing therapist data and search functionality.
"""
from typing import List, Optional, Dict, Any
from config import THERAPIST_DATABASE, Constants, settings
from logging_config import logger, LoggingMixin
from models import Therapist, TherapistSearchRequest, TherapistSearchResponse, Location
from utils import calculate_distance


class TherapistService(LoggingMixin):
    """Service for therapist data management and search."""
    
    def __init__(self):
        """Initialize the therapist service."""
        self.therapist_db = THERAPIST_DATABASE
        self.max_distance = settings.max_distance_km
    

    
    def find_therapists_by_location(self, location: str) -> List[Therapist]:
        """
        Find therapists in a specific location.
        
        Args:
            location: City or area name
            
        Returns:
            List of therapists in the location
        """
        location_lower = location.lower().strip()
        
        if location_lower not in self.therapist_db:
            self.logger.warning(f"No therapists found for location: {location}")
            return []
        
        therapists_data = self.therapist_db[location_lower]
        therapists = []
        
        for therapist_data in therapists_data:
            therapist = Therapist(**therapist_data)
            therapists.append(therapist)
        
        self.logger.info(f"Found {len(therapists)} therapists in {location}")
        return therapists
    
    def find_nearby_therapists(
        self, 
        user_lat: float, 
        user_lon: float, 
        max_distance: Optional[float] = None
    ) -> List[Therapist]:
        """
        Find therapists within a specified distance of user's location.
        
        Args:
            user_lat: User's latitude
            user_lon: User's longitude
            max_distance: Maximum distance in kilometers
            
        Returns:
            List of nearby therapists sorted by distance
        """
        if max_distance is None:
            max_distance = self.max_distance
        
        nearby_therapists = []
        
        # Search through all therapists in the database
        for city, therapists_data in self.therapist_db.items():
            for therapist_data in therapists_data:
                if therapist_data.get('lat') and therapist_data.get('lon'):
                    distance = calculate_distance(
                        user_lat, user_lon,
                        therapist_data['lat'], therapist_data['lon']
                    )
                    
                    if distance <= max_distance:
                        therapist_data_copy = therapist_data.copy()
                        therapist_data_copy['distance'] = round(distance, 2)
                        therapist = Therapist(**therapist_data_copy)
                        nearby_therapists.append(therapist)
        
        # Sort by distance
        nearby_therapists.sort(key=lambda x: x.distance or 0)
        
        self.logger.info(f"Found {len(nearby_therapists)} therapists within {max_distance}km")
        return nearby_therapists
    
    def search_therapists(self, request: TherapistSearchRequest) -> TherapistSearchResponse:
        """
        Search for therapists based on various criteria.
        
        Args:
            request: Search request with location and filters
            
        Returns:
            Search response with matching therapists
        """
        self.logger.info(f"Searching therapists for location: {request.location}")
        
        therapists = []
        
        if request.user_coordinates:
            # Use coordinate-based search
            therapists = self.find_nearby_therapists(
                request.user_coordinates.latitude,
                request.user_coordinates.longitude,
                request.max_distance
            )
        else:
            # Use location-based search
            therapists = self.find_therapists_by_location(request.location)
        
        # Filter by specialization if specified
        if request.specialization:
            specialization_lower = request.specialization.lower()
            therapists = [
                t for t in therapists 
                if specialization_lower in t.specialization.lower()
            ]
        
        return TherapistSearchResponse(
            therapists=therapists,
            total_count=len(therapists),
            search_location=request.location,
            search_radius=request.max_distance or self.max_distance
        )
    
    def get_therapist_recommendations(self, location: str) -> str:
        """
        Get formatted therapist recommendations for a location.
        
        Args:
            location: Location to search in
            
        Returns:
            Formatted string with therapist recommendations
        """
        therapists = self.find_therapists_by_location(location)
        
        if not therapists:
            return self._get_general_therapist_guidance(location)
        
        result = f"🏥 **Licensed Therapists in {location.title()}:**\n\n"
        
        for therapist in therapists:
            result += f"🏥 **{therapist.name}** - {therapist.type}\n"
            result += f"   📞 {therapist.phone}\n"
            result += f"   🎯 Specialization: {therapist.specialization}\n"
            result += f"   📍 {therapist.location}\n"
            result += f"   ⭐ {therapist.rating}/5 rating\n\n"
        
        result += "💡 **Tips for choosing a therapist:**\n"
        result += "• Check their credentials and specialization\n"
        result += "• Consider your comfort level and communication style\n"
        result += "• Ask about insurance coverage and fees\n"
        result += "• Schedule a consultation to see if it's a good fit\n\n"
        result += "🆘 **If you're in immediate crisis, please contact:**\n"
        result += f"• KIRAN Mental Health Helpline: {Constants.MENTAL_HEALTH_HELPLINES['kiran']} (24/7)\n"
        result += f"• Emergency Services: {Constants.EMERGENCY_SERVICES['ambulance']} (Ambulance) or {Constants.EMERGENCY_SERVICES['police']} (Police)"
        
        return result
    
    def _get_general_therapist_guidance(self, location: str) -> str:
        """
        Get general guidance for finding therapists when no specific data is available.
        
        Args:
            location: Location that was searched
            
        Returns:
            General guidance string
        """
        return f"""🏥 **Finding Therapists in {location.title()}**

I don't have specific therapist listings for {location}, but here are some ways to find qualified mental health professionals:

**🔍 How to Find Therapists:**
• **Psychology Today Directory**: {Constants.ONLINE_RESOURCES['psychology_today']}
• **Indian Association of Clinical Psychologists**: www.iacp.in
• **Indian Psychiatric Society**: www.indianpsychiatricsociety.org
• **Local hospital psychiatry departments**
• **University counseling centers**

**📋 What to Look For:**
• Licensed clinical psychologists or psychiatrists
• Specialization in your specific concerns
• Good reviews and recommendations
• Insurance coverage or affordable fees
• Comfortable communication style

**🆘 Emergency Resources:**
• KIRAN Mental Health Helpline: {Constants.MENTAL_HEALTH_HELPLINES['kiran']} (24/7)
• Vandrevala Foundation: {Constants.MENTAL_HEALTH_HELPLINES['vandrevala']} (24/7)
• Emergency Services: {Constants.EMERGENCY_SERVICES['ambulance']} (Ambulance) or {Constants.EMERGENCY_SERVICES['police']} (Police)

**💡 Pro Tip:** Many therapists offer online consultations, so you can access help even if local options are limited."""

