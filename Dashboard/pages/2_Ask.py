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

st.set_page_config(page_title="ChatBot", layout="wide")
st.subheader("💬 ChatBot")
BASE_URL="http://127.0.0.1:8080"
query = st.text_input("Enter your query:", key="request")

if st.button("📊 Submit Query", use_container_width=True):
    if not query:
        st.warning("⚠️ Please enter a query before submitting.")
    else:
        st.markdown("### 📈 Response Preview")
        with st.spinner("⏳ Processing your query... Please wait."):
            try:
                API_URL = f"{BASE_URL}/ask/"
                payload = {"query": query}
                response = requests.post(API_URL, json=payload)  

                if response.status_code == 200:
                    response_data = response.json()  
                    st.write(response_data.get("response", "No response received."))
                else:
                    st.error(f"❌ Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"🚨 Failed to connect to API: {e}")

            st.markdown("**Designed by Aditya Kaushal | Powered by Buyogo**")



