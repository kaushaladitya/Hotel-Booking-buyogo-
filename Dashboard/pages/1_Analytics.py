import streamlit as st
import os
import pandas as pd
import requests
import streamlit as st
import requests
from PIL import Image
import io
import warnings
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

cwd = os.getcwd()
analytics_options = {
    "Revenue Trend": {"endpoint": "/revenue_trend", "type": "plot"},
    "Booking lead data": {"endpoint": "/booking_lead_time", "type": "plot"},
    "Cancellation Rate": {"endpoint": "/cancellation_rate", "type": "plot"},
    'Geographical Distribution': {"endpoint": "/geo_map_image", "type": "plot"},
    "All Analytics": {"endpoint": "/get_all_analytics", "type": "plot"},    
}

BASE_URL = "http://127.0.0.1:8080" 

st.title("📊 Hotel Booking Analytics")

option = st.selectbox("Select an analysis option:", list(analytics_options.keys()))

if st.button("📊 Run Analytics", use_container_width=True):
    
    st.subheader(f"📈 Insights for {option}")
    
    with st.spinner("⏳ Processing your query... Please wait."):
        try:  
            selected_endpoint = analytics_options[option]["endpoint"]
            API_URL = f"{BASE_URL}{selected_endpoint}"  
            response = requests.post(API_URL, stream=True)  

            if response.status_code == 200:
                image_bytes = io.BytesIO(response.content)  
                image = Image.open(image_bytes)  
                st.image(image, caption=f"{option}", use_container_width=True)
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to API: {e}")

    st.markdown("**Designed by Aditya Kaushal | Powered by Buyogo**")