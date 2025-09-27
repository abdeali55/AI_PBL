"""
Service for location-based functionality and geolocation services.
"""
import requests
from typing import Optional, Dict, Any, Tuple
from config import settings, Constants
from logging_config import logger, LoggingMixin
from models import Location
from utils import validate_coordinates, determine_city_from_coordinates


class LocationService(LoggingMixin):
    """Service for location-based operations."""
    
    def __init__(self):
        """Initialize the location service."""
        self.timeout = settings.ip_geolocation_timeout
        self.major_cities = Constants.MAJOR_CITIES
    
    def get_ip_location(self) -> Optional[Location]:
        """
        Get approximate location based on IP address.
        
        Returns:
            Location object with IP-based coordinates, or None if failed
        """
        try:
            self.logger.info("Fetching IP-based location")
            
            response = requests.get(
                "http://ip-api.com/json/", 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("status") == "success":
                    lat = data.get("lat", 0)
                    lon = data.get("lon", 0)
                    city = data.get("city", "Unknown")
                    country = data.get("country", "Unknown")
                    
                    if lat != 0 and lon != 0:
                        location = Location(
                            latitude=lat,
                            longitude=lon,
                            accuracy=10000,  # IP location is less accurate
                            source="ip_location",
                            city=city,
                            country=country
                        )
                        
                        self.logger.info(f"IP location set to {city}, {country}")
                        return location
                    else:
                        self.logger.warning("Invalid coordinates from IP geolocation")
                else:
                    self.logger.error("IP geolocation service returned error status")
            else:
                self.logger.error(f"IP geolocation request failed with status {response.status_code}")
                
        except requests.RequestException as e:
            self.logger.error(f"Network error getting IP location: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error getting IP location: {str(e)}")
        
        return None
    
    def get_city_coordinates(self, city_name: str) -> Optional[Location]:
        """
        Get coordinates for a major city.
        
        Args:
            city_name: Name of the city
            
        Returns:
            Location object with city coordinates, or None if city not found
        """
        city_lower = city_name.lower().strip()
        
        if city_lower in self.major_cities:
            coords = self.major_cities[city_lower]
            location = Location(
                latitude=coords["lat"],
                longitude=coords["lon"],
                accuracy=5000,  # Approximate accuracy for city-level location
                source="city_input",
                city=city_name.title()
            )
            
            self.logger.info(f"City coordinates set for {city_name.title()}")
            return location
        
        self.logger.warning(f"City '{city_name}' not found in major cities database")
        return None
    

    
    def create_location_from_coordinates(
        self, 
        latitude: float, 
        longitude: float,
        source: str = "manual_coords"
    ) -> Optional[Location]:
        """
        Create a location object from coordinates.
        
        Args:
            latitude: Latitude coordinate
            longitude: Longitude coordinate
            source: Source of the coordinates
            
        Returns:
            Location object if coordinates are valid, None otherwise
        """
        if not validate_coordinates(latitude, longitude):
            self.logger.error(f"Invalid coordinates: {latitude}, {longitude}")
            return None
        
        location = Location(
            latitude=latitude,
            longitude=longitude,
            accuracy=100,  # Manual input accuracy
            source=source
        )
        
        self.logger.info(f"Location created from coordinates: {latitude}, {longitude}")
        return location
    

    
    def get_location_info(self, location: Location) -> Dict[str, Any]:
        """
        Get additional information about a location.
        
        Args:
            location: Location object
            
        Returns:
            Dictionary with location information
        """
        info = {
            "coordinates": f"{location.latitude}, {location.longitude}",
            "accuracy": f"{location.accuracy} meters" if location.accuracy else "Unknown",
            "source": location.source or "Unknown"
        }
        
        if location.city:
            info["city"] = location.city
        if location.country:
            info["country"] = location.country
        
        # Determine city from coordinates if not already set
        if not location.city and location.latitude != 0.0 and location.longitude != 0.0:
            detected_city = determine_city_from_coordinates(
                location.latitude, 
                location.longitude
            )
            if detected_city and detected_city != "Unknown":
                info["detected_city"] = detected_city
        
        return info

