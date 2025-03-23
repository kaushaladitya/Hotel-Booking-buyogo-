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

BASE_URL = "http://127.0.0.1:8080"
st.title("📊 Search History")
API_URL = f"{BASE_URL}/search_history/"  

response = requests.post(API_URL, stream=True) 
df=pd.read_csv('app/search_history.csv')
st.dataframe(df)
st.markdown("**Designed by Aditya Kaushal | Powered by Buyogo**")