"""
Data models for the AI Mental Health Therapist application.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator
from enum import Enum


class TherapistType(str, Enum):
    """Types of mental health professionals."""
    PSYCHIATRIST = "Psychiatrist"
    CLINICAL_PSYCHOLOGIST = "Clinical Psychologist"
    COUNSELING_CENTER = "Counseling Center"
    MENTAL_HEALTH_CENTER = "Mental Health Center"
    WELLNESS_CENTER = "Wellness Center"
    MENTAL_HEALTH_CLINIC = "Mental Health Clinic"


class Location(BaseModel):
    """Location coordinates model."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate")
    accuracy: Optional[float] = Field(None, ge=0, description="Location accuracy in meters")
    source: Optional[str] = Field(None, description="Source of location data")
    city: Optional[str] = Field(None, description="City name")
    country: Optional[str] = Field(None, description="Country name")
    
    @validator('latitude')
    def validate_latitude(cls, v):
        if not -90 <= v <= 90:
            raise ValueError('Latitude must be between -90 and 90')
        return v
    
    @validator('longitude')
    def validate_longitude(cls, v):
        if not -180 <= v <= 180:
            raise ValueError('Longitude must be between -180 and 180')
        return v


class Therapist(BaseModel):
    """Therapist information model."""
    name: str = Field(..., min_length=1, description="Therapist name")
    type: TherapistType = Field(..., description="Type of mental health professional")
    phone: str = Field(..., min_length=10, description="Contact phone number")
    specialization: str = Field(..., min_length=1, description="Area of specialization")
    location: str = Field(..., min_length=1, description="Physical location/address")
    rating: float = Field(..., ge=0, le=5, description="Rating out of 5")
    lat: Optional[float] = Field(None, ge=-90, le=90, description="Latitude coordinate")
    lon: Optional[float] = Field(None, ge=-180, le=180, description="Longitude coordinate")
    distance: Optional[float] = Field(None, ge=0, description="Distance from user in km")
    
    @validator('phone')
    def validate_phone(cls, v):
        # Basic phone validation - should contain digits and be reasonable length
        if not any(c.isdigit() for c in v):
            raise ValueError('Phone number must contain digits')
        return v


class GovernmentService(BaseModel):
    """Government mental health service model."""
    name: str = Field(..., description="Service name")
    number: str = Field(..., description="Contact number")
    description: Optional[str] = Field(None, description="Service description")
    available_24_7: bool = Field(False, description="Whether service is available 24/7")
    toll_free: bool = Field(False, description="Whether service is toll-free")


class UserQuery(BaseModel):
    """User query model for API requests."""
    message: str = Field(..., min_length=1, max_length=1000, description="User message")
    location: Optional[Location] = Field(None, description="User location if available")
    session_id: Optional[str] = Field(None, description="Session identifier")
    
    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v.strip()


class AIResponse(BaseModel):
    """AI response model."""
    response: str = Field(..., description="AI response text")
    tool_called: str = Field(..., description="Tool that was used")
    confidence: Optional[float] = Field(None, ge=0, le=1, description="Response confidence score")
    processing_time: Optional[float] = Field(None, ge=0, description="Processing time in seconds")
    session_id: Optional[str] = Field(None, description="Session identifier")


class TherapistSearchRequest(BaseModel):
    """Request model for therapist search."""
    location: str = Field(..., min_length=1, description="Location to search in")
    specialization: Optional[str] = Field(None, description="Desired specialization")
    max_distance: Optional[float] = Field(10, ge=0, le=100, description="Maximum distance in km")
    user_coordinates: Optional[Location] = Field(None, description="User's coordinates")


class TherapistSearchResponse(BaseModel):
    """Response model for therapist search."""
    therapists: List[Therapist] = Field(..., description="List of found therapists")
    total_count: int = Field(..., ge=0, description="Total number of therapists found")
    search_location: str = Field(..., description="Location that was searched")
    search_radius: float = Field(..., ge=0, description="Search radius used")


class GovernmentServicesRequest(BaseModel):
    """Request model for government services."""
    location: str = Field(..., min_length=1, description="Location for services")
    service_type: Optional[str] = Field(None, description="Type of service needed")


class GovernmentServicesResponse(BaseModel):
    """Response model for government services."""
    services: List[GovernmentService] = Field(..., description="List of government services")
    location: str = Field(..., description="Location for which services were provided")
    emergency_services: Dict[str, str] = Field(..., description="Emergency service numbers")


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: str = Field(..., description="Error timestamp")


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Check timestamp")
    version: str = Field(..., description="Application version")
    uptime: Optional[float] = Field(None, description="Service uptime in seconds")
    dependencies: Dict[str, str] = Field(..., description="Dependency statuses")

