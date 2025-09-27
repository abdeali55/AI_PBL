"""
FastAPI backend for the AI Mental Health Therapist application.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import time
from datetime import datetime
from typing import Dict, Any

from ai_agent import simple_agent, parse_response
from models import UserQuery, AIResponse, ErrorResponse, HealthCheckResponse, TherapistSearchRequest, GovernmentServicesRequest
from config import settings
from logging_config import logger, setup_logging
from services.therapist_service import TherapistService
from services.government_service import GovernmentServiceProvider
from services.location_service import LocationService

# Setup logging
setup_logging()

# Initialize services
therapist_service = TherapistService()
government_service = GovernmentServiceProvider()
location_service = LocationService()

# Initialize FastAPI app
app = FastAPI(
    title="AI Mental Health Therapist API",
    description="API for AI-powered mental health conversations and therapist recommendations",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for health check
start_time = time.time()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    
    error_response = ErrorResponse(
        error="Internal server error",
        error_code="INTERNAL_ERROR",
        details={"message": "An unexpected error occurred"},
        timestamp=datetime.utcnow().isoformat()
    )
    
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )


@app.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Health check endpoint to verify service status.
    
    Returns:
        Health status and service information
    """
    try:
        uptime = time.time() - start_time
        
        # Check service dependencies
        dependencies = {
            "ai_service": "healthy",  # Could add actual health checks
            "therapist_service": "healthy",
            "government_service": "healthy"
        }
        
        return HealthCheckResponse(
            status="healthy",
            timestamp=datetime.utcnow().isoformat(),
            version="1.0.0",
            uptime=uptime,
            dependencies=dependencies
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unhealthy")


@app.post("/ask", response_model=AIResponse)
async def ask(query: UserQuery):
    """
    Main endpoint for AI mental health conversations.
    
    Args:
        query: User query with message and optional location
        
    Returns:
        AI response with therapeutic guidance
        
    Raises:
        HTTPException: If request processing fails
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing query: {query.message[:50]}...")
        
        # Validate input
        if not query.message.strip():
            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )
        
        if len(query.message) > 1000:
            raise HTTPException(
                status_code=400,
                detail="Message too long (max 1000 characters)"
            )
        
        # Use the simple agent to process the query
        result = simple_agent(query.message)
        tool_called_name, final_response = parse_response(result)
        
        processing_time = time.time() - start_time
        
        # Create response
        response = AIResponse(
            response=final_response,
            tool_called=tool_called_name,
            confidence=0.8,  # Could be calculated based on response quality
            processing_time=processing_time,
            session_id=query.session_id
        )
        
        logger.info(f"Query processed successfully in {processing_time:.3f} seconds")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        processing_time = time.time() - start_time
        logger.error(f"Error processing query: {str(e)}")
        
        # Return error response
        error_response = AIResponse(
            response="I apologize, but I encountered an error processing your request. Please try again.",
            tool_called="Error",
            confidence=0.0,
            processing_time=processing_time,
            session_id=query.session_id
        )
        
        return error_response


@app.post("/therapists/search")
async def search_therapists(request: TherapistSearchRequest):
    """
    Search for therapists based on location and criteria.
    
    Args:
        request: Therapist search request
        
    Returns:
        List of matching therapists
        
    Raises:
        HTTPException: If search fails
    """
    try:
        logger.info(f"Searching therapists for location: {request.location}")
        
        response = therapist_service.search_therapists(request)
        return response
        
    except Exception as e:
        logger.error(f"Error searching therapists: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search therapists")


@app.get("/therapists/location/{location}")
async def get_therapists_by_location(location: str):
    """
    Get therapists in a specific location.
    
    Args:
        location: City or area name
        
    Returns:
        Formatted therapist recommendations
    """
    try:
        logger.info(f"Getting therapists for location: {location}")
        
        recommendations = therapist_service.get_therapist_recommendations(location)
        return {"recommendations": recommendations}
        
    except Exception as e:
        logger.error(f"Error getting therapists: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get therapists")


@app.post("/government-services")
async def get_government_services(request: GovernmentServicesRequest):
    """
    Get government mental health services for a location.
    
    Args:
        request: Government services request
        
    Returns:
        Government services information
    """
    try:
        logger.info(f"Getting government services for location: {request.location}")
        
        response = government_service.get_services_for_location(request.location)
        return response
        
    except Exception as e:
        logger.error(f"Error getting government services: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get government services")


@app.get("/government-services/{location}")
async def get_government_services_formatted(location: str):
    """
    Get formatted government services for a location.
    
    Args:
        location: Location to get services for
        
    Returns:
        Formatted government services text
    """
    try:
        logger.info(f"Getting formatted government services for location: {location}")
        
        formatted_services = government_service.format_services_response(location)
        return {"services": formatted_services}
        
    except Exception as e:
        logger.error(f"Error getting formatted government services: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get government services")


@app.post("/location/ip")
async def get_ip_location():
    """
    Get location based on IP address.
    
    Returns:
        Location information from IP geolocation
    """
    try:
        logger.info("Getting IP-based location")
        
        location = location_service.get_ip_location()
        if location:
            return location.dict()
        else:
            raise HTTPException(status_code=404, detail="Could not determine location from IP")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting IP location: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get IP location")


@app.get("/location/city/{city_name}")
async def get_city_coordinates(city_name: str):
    """
    Get coordinates for a city.
    
    Args:
        city_name: Name of the city
        
    Returns:
        City coordinates
    """
    try:
        logger.info(f"Getting coordinates for city: {city_name}")
        
        location = location_service.get_city_coordinates(city_name)
        if location:
            return location.dict()
        else:
            raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting city coordinates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get city coordinates")


@app.get("/")
async def root():
    """
    Root endpoint with API information.
    
    Returns:
        Basic API information
    """
    return {
        "message": "AI Mental Health Therapist API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    logger.info(f"Starting AI Mental Health Therapist API on {settings.backend_host}:{settings.backend_port}")
    uvicorn.run(
        "main:app", 
        host=settings.backend_host, 
        port=settings.backend_port, 
        reload=True,
        log_level=settings.log_level.lower()
    )






