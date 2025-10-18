import os
from dotenv import load_dotenv
import streamlit as st

# Try to load from Streamlit secrets first (for cloud deployment)
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (FileNotFoundError, KeyError):
    # Fall back to .env file (for local development)
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    st.error("⚠️ GEMINI_API_KEY not found!")
    st.stop()

MODEL_NAME = 'gemini-2.0-flash-001'



# import os
# from dotenv import load_dotenv


# ###############################################
# # Gemini API KEY/Basic Configuration          #
# # Load environment variables from .env file   #
# ###############################################
# load_dotenv()
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# if not GEMINI_API_KEY:
#     print("Error: GEMINI_API_KEY not found.")
#     print("Please ensure you have a .env file in the same directory")
#     print("with the line: GEMINI_API_KEY='YOUR_API_KEY'")
#     exit()  # Exit if the key is not found

# MODEL_NAME = 'gemini-2.0-flash-001'

