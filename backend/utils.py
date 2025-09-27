"""
Utility functions for the AI Mental Health Therapist application.
"""
from math import radians, sin, cos, sqrt, atan2
from typing import Tuple


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the distance between two points on Earth using the Haversine formula.
    
    Args:
        lat1: First point latitude
        lon1: First point longitude
        lat2: Second point latitude
        lon2: Second point longitude
        
    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate if coordinates are within valid ranges.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        True if coordinates are valid, False otherwise
    """
    return (-90 <= latitude <= 90) and (-180 <= longitude <= 180)


def determine_city_from_coordinates(latitude: float, longitude: float) -> str:
    """
    Determine the closest major city from coordinates.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        City name if found, "Unknown" otherwise
    """
    # City coordinate ranges for major Indian cities
    city_ranges = {
        "Mumbai": (19.0, 19.2, 72.8, 72.9),
        "Delhi": (28.6, 28.8, 77.0, 77.3),
        "Bangalore": (12.9, 13.0, 77.5, 77.7),
        "Chennai": (13.0, 13.1, 80.2, 80.3),
        "Kolkata": (22.5, 22.6, 88.3, 88.4),
        "Hyderabad": (17.3, 17.4, 78.4, 78.5)
    }
    
    for city, (lat_min, lat_max, lon_min, lon_max) in city_ranges.items():
        if lat_min <= latitude <= lat_max and lon_min <= longitude <= lon_max:
            return city
    
    return "Unknown"