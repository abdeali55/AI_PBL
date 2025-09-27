# Step1: Setup Streamlit
import streamlit as st
from streamlit.components.v1 import html as components_html
import requests

# Must be the first Streamlit command
st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("🧠 SafeSpace – AI Mental Health Therapist")

# Initialize session state variables
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "geolocation" not in st.session_state:
    st.session_state.geolocation = None

BACKEND_URL = "http://localhost:8000/ask"






# Uses a small JS snippet to request location and write lat/lon to URL params,
# which Streamlit reads back into session state.
query_params = st.query_params
if "lat" in query_params and "lon" in query_params:
    try:
        lat = float(query_params.get("lat", 0))
        lon = float(query_params.get("lon", 0))
        acc = float(query_params.get("acc", 0))
        source = query_params.get("source", "gps")
        
        # Only set if we have valid coordinates
        if lat != 0.0 or lon != 0.0:
            st.session_state["geolocation"] = {
                "latitude": lat,
                "longitude": lon,
                "accuracy": acc,
                "source": source
            }
            # Clear URL parameters after processing
            st.query_params.clear()
    except (ValueError, TypeError):
        # Invalid coordinates in URL, ignore
        pass

with st.sidebar:
    st.subheader("📍 Location Services")
    
    # Location input options
    location_method = st.radio(
        "Choose location method:",
        ["🌍 Use GPS", "🌐 Use IP Location", "🏙️ Enter City/Area", "📍 Enter Coordinates"],
        help="Select how you'd like to provide your location"
    )
    
    if location_method == "🌍 Use GPS":
        if st.button("📍 Get My Location", type="primary"):
            # Use a more reliable geolocation approach
            geolocation_js = """
            <script>
            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(
                        function(position) {
                            const lat = position.coords.latitude;
                            const lon = position.coords.longitude;
                            const acc = position.coords.accuracy;
                            
                            // Update URL parameters to pass data back to Streamlit
                            const url = new URL(window.location);
                            url.searchParams.set('lat', lat.toString());
                            url.searchParams.set('lon', lon.toString());
                            url.searchParams.set('acc', acc.toString());
                            url.searchParams.set('source', 'gps');
                            
                            window.location.href = url.toString();
                        },
                        function(error) {
                            let message = "Location access failed: ";
                            switch(error.code) {
                                case error.PERMISSION_DENIED:
                                    message += "Please allow location access and try again.";
                                    break;
                                case error.POSITION_UNAVAILABLE:
                                    message += "Location information is unavailable.";
                                    break;
                                case error.TIMEOUT:
                                    message += "Location request timed out.";
                                    break;
                                default:
                                    message += "An unknown error occurred.";
                                    break;
                            }
                            alert(message);
                        },
                        {
                            enableHighAccuracy: true,
                            timeout: 15000,
                            maximumAge: 300000
                        }
                    );
                } else {
                    alert("Geolocation is not supported by this browser.");
                }
            }
            getLocation();
            </script>
            """
            
            components_html(geolocation_js, height=0)
    
    elif location_method == "🌐 Use IP Location":
        st.info("🌐 This will use your approximate location based on your IP address.")
        if st.button("🌐 Get IP Location", type="primary"):
            try:
                # Use backend API for IP location
                response = requests.post("http://localhost:8000/location/ip")
                if response.status_code == 200:
                    location_data = response.json()
                    st.session_state["geolocation"] = {
                        "latitude": location_data["latitude"],
                        "longitude": location_data["longitude"],
                        "accuracy": location_data.get("accuracy", 10000),
                        "source": "ip_location",
                        "city": location_data.get("city", "Unknown"),
                        "country": location_data.get("country", "Unknown")
                    }
                    city = location_data.get("city", "Unknown")
                    country = location_data.get("country", "Unknown")
                    st.success(f"Location set to {city}, {country}!")
                    st.rerun()
                else:
                    st.error("Could not determine location from IP address.")
            except requests.RequestException:
                st.error("Network error: Could not connect to location service.")
            except Exception as e:
                st.error(f"Error getting IP location: {str(e)}")
            
    elif location_method == "🏙️ Enter City/Area":
        city_input = st.text_input("Enter your city or area:", placeholder="e.g., Mumbai, Delhi, Bangalore")
        if st.button("📍 Use This Location", type="primary") and city_input:
            # Use backend API to get city coordinates
            try:
                response = requests.get(f"http://localhost:8000/location/city/{city_input}")
                if response.status_code == 200:
                    location_data = response.json()
                    st.session_state["geolocation"] = {
                        "latitude": location_data["latitude"],
                        "longitude": location_data["longitude"],
                        "accuracy": location_data.get("accuracy", 5000),
                        "source": "city_input",
                        "city": city_input.title()
                    }
                    st.success(f"Location set to {city_input.title()}!")
                    st.rerun()
                else:
                    st.warning(f"City '{city_input}' not found in our database. Please try a major city or use coordinates.")
            except requests.RequestException:
                st.error("Unable to connect to location service. Please try again later.")
            except Exception as e:
                st.error(f"Error getting city location: {str(e)}")
    
    elif location_method == "📍 Enter Coordinates":
        col1, col2 = st.columns(2)
        with col1:
            lat_input = st.number_input("Latitude:", value=0.0, format="%.6f", step=0.000001)
        with col2:
            lon_input = st.number_input("Longitude:", value=0.0, format="%.6f", step=0.000001)
        
        if st.button("📍 Use These Coordinates", type="primary") and lat_input != 0.0 and lon_input != 0.0:
            # Validate coordinates
            if -90 <= lat_input <= 90 and -180 <= lon_input <= 180:
                st.session_state["geolocation"] = {
                    "latitude": lat_input,
                    "longitude": lon_input,
                    "accuracy": 100,  # Manual input accuracy
                    "source": "manual_coords"
                }
                st.success("Coordinates set successfully!")
                st.rerun()
            else:
                st.error("Invalid coordinates! Latitude must be between -90 and 90, Longitude between -180 and 180.")
    
    # Clear location button
    if "geolocation" in st.session_state and st.session_state["geolocation"] is not None:
        if st.button("🗑️ Clear Location"):
            st.session_state["geolocation"] = None
            st.rerun()

    # Display geolocation if available
    if "geolocation" in st.session_state and st.session_state["geolocation"] is not None:
        g = st.session_state["geolocation"]
        
        # Validate that we have real coordinates (not default 0,0)
        if g['latitude'] != 0.0 or g['longitude'] != 0.0:
            st.write("📍 Your location:")
            st.write(f"- Latitude: {g['latitude']}")
            st.write(f"- Longitude: {g['longitude']}")
            st.write(f"- Accuracy: {g['accuracy']} meters")
            
            # Show source of location
            source_map = {
                "gps": "🌍 GPS Location",
                "ip_location": "🌐 IP Location",
                "city_input": "🏙️ City Selection", 
                "manual_coords": "📍 Manual Coordinates"
            }
            source = g.get('source', 'unknown')
            if source in source_map:
                st.caption(f"Source: {source_map[source]}")
            
            # Add this section to display nearby therapists
            st.subheader("📍 Nearby Therapists")
            
            # Try to get therapists from backend API
            try:
                # Determine city from coordinates
                detected_city = "Unknown"
                if 19.0 <= g['latitude'] <= 19.2 and 72.8 <= g['longitude'] <= 72.9:
                    detected_city = "Mumbai"
                elif 28.6 <= g['latitude'] <= 28.8 and 77.0 <= g['longitude'] <= 77.3:
                    detected_city = "Delhi"
                elif 12.9 <= g['latitude'] <= 13.0 and 77.5 <= g['longitude'] <= 77.7:
                    detected_city = "Bangalore"
                elif 13.0 <= g['latitude'] <= 13.1 and 80.2 <= g['longitude'] <= 80.3:
                    detected_city = "Chennai"
                elif 22.5 <= g['latitude'] <= 22.6 and 88.3 <= g['longitude'] <= 88.4:
                    detected_city = "Kolkata"
                elif 17.3 <= g['latitude'] <= 17.4 and 78.4 <= g['longitude'] <= 78.5:
                    detected_city = "Hyderabad"
                
                if detected_city != "Unknown":
                    # Try to get therapists from backend
                    try:
                        response = requests.get(f"http://localhost:8000/therapists/location/{detected_city}")
                        if response.status_code == 200:
                            recommendations = response.json().get("recommendations", "")
                            if recommendations:
                                st.markdown(recommendations)
                            else:
                                st.info("No therapists found for your location.")
                        else:
                            st.info("Unable to load therapist information. Please try again later.")
                    except requests.RequestException:
                        st.info("Unable to connect to therapist service. Please try again later.")
                else:
                    st.info("No therapists found within 10km of your location.")
            except Exception as e:
                st.error(f"Error loading therapist information: {str(e)}")
            
            # Add government services section
            st.subheader("🏛️ Government Mental Health Services")
            
            # Determine location for government services
            location_for_gov = "India"  # Default
            if 'city' in g:
                location_for_gov = g['city']
            elif g['latitude'] != 0.0 and g['longitude'] != 0.0:
                # Determine city based on coordinates (simplified)
                if 19.0 <= g['latitude'] <= 19.2 and 72.8 <= g['longitude'] <= 72.9:
                    location_for_gov = "Mumbai"
                elif 28.6 <= g['latitude'] <= 28.8 and 77.0 <= g['longitude'] <= 77.3:
                    location_for_gov = "Delhi"
                elif 12.9 <= g['latitude'] <= 13.0 and 77.5 <= g['longitude'] <= 77.7:
                    location_for_gov = "Bangalore"
                elif 13.0 <= g['latitude'] <= 13.1 and 80.2 <= g['longitude'] <= 80.3:
                    location_for_gov = "Chennai"
                elif 22.5 <= g['latitude'] <= 22.6 and 88.3 <= g['longitude'] <= 88.4:
                    location_for_gov = "Kolkata"
                elif 17.3 <= g['latitude'] <= 17.4 and 78.4 <= g['longitude'] <= 78.5:
                    location_for_gov = "Hyderabad"
            
            # Get government services from backend API
            try:
                response = requests.get(f"http://localhost:8000/government-services/{location_for_gov}")
                if response.status_code == 200:
                    services_data = response.json()
                    services_text = services_data.get("services", "")
                    if services_text:
                        st.markdown(services_text)
                    else:
                        st.info("Government services information is not available at the moment.")
                else:
                    st.error("Unable to load government services information.")
            except requests.RequestException:
                st.error("Unable to connect to government services. Please try again later.")
            except Exception as e:
                st.error(f"Error loading government services: {str(e)}")
        else:
            st.warning("⚠️ Location not properly set. Please try again or use a different method.")
    
# Step2: User is able to ask question
# Chat input
user_input = st.chat_input("What's on your mind today?")
if user_input:
    # Append user message
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    try:
        # Make API request
        response = requests.post(BACKEND_URL, json={"message": user_input})
        
        # Check status code first
        if response.status_code == 200:
            try:
                # Parse JSON once
                data = response.json()
                st.session_state.chat_history.append({
                    "role": "assistant", 
                    "content": f'{data["response"]} WITH TOOL: [{data["tool_called"]}]'
                })
            except ValueError:
                st.error(f"Invalid JSON response: {response.text}")
        else:
            st.error(f"Request failed with status {response.status_code}: {response.text}")
            
    except requests.RequestException as e:
        st.error(f"Failed to connect to backend: {str(e)}")

# Step3: Show response from backend
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])