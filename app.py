import streamlit as st
from supabase import create_client, Client
from customer_module import show_customer_portal
from admin_module import show_admin_page

# --- CONFIGURATION ---
SUPABASE_URL = "https://iejnygjsanwddariukrq.supabase.co"
SUPABASE_KEY = "sb_publishable_7ies1_1JDaH1c88iYC-13w_Vtk2nzqs"

# Initialize Supabase Client
@st.cache_resource
def init_connection():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_connection()

# --- MAIN ROUTING LOGIC ---
params = st.query_params

if "id_premis" in params:
    show_customer_portal(supabase, params["id_premis"])
else:
    show_admin_page(supabase)