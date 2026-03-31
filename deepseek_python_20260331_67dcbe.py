# DS V25 timber AI buddy.py
import streamlit as st
import pandas as pd
import re
import math
import json
from datetime import datetime
import os

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(layout="wide", page_title="Timber AI Buddy V25", page_icon="🪵")
st.title("🪵 DS V25 Timber AI Buddy")
st.caption("Professional Timber & Plywood Quoting System")

# ==============================
# CONFIG MANAGEMENT (OFFLINE PRICING)
# ==============================
CONFIG_PATH = "config/prices.json"

def load_prices():
    """Load prices from JSON file with fallback defaults"""
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            return config
        else:
            # Create default config if not exists
            default_config = {
                "timber": {
                    "Kapur": 3800,
                    "Balau": 5500,
                    "Chengal": 6000,
                    "Mixed Keruing": 650,
                    "Pure Keruing": 1000
                },
                "plywood": {
                    "Marine": {
                        "6": 25.5, "9": 37.0, "12": 45, "15": 56, "18": 68.5, "25": 95
                    },
                    "Furniture": {
                        "3": 15, "6": 17.5, "9": 19.5, "12": 23.8, "15": 26.8, "18": 31.5, "25": 45
                    },
                    "MR": {
                        "3": 4.1, "6": 6.8, "9": 10.5, "12": 15, "15": 19.5, "18": 21.7
                    }
                },
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "25.0"
            }
            # Ensure config directory exists
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            with open(CONFIG_PATH, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    except Exception as e:
        st.error(f"Error loading config: {e}")
        return None

def save_prices(timber_prices, plywood_prices):
    """Save updated prices to JSON file"""
    config = {
        "timber": timber_prices,
        "plywood": plywood_prices,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": "25.0"
    }
    
    try:
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
        return True, "Prices saved successfully!"
    except Exception as e:
        return False, f"Error saving: {e}"

# ==============================
# LOAD CURRENT PRICES
# ==============================
prices = load_prices()
if prices is None:
    st.stop()

timber_prices = prices["timber"]
plywood_prices = prices["plywood"]

# Display last updated info
col_info1, col_info2, col_info3 = st.columns(3)
with col_info1:
    st.info(f"📅 Prices updated: {prices.get('last_updated', 'Unknown')}")
with col_info2:
    st.info(f"📌 Version: {prices.get('version', '25.0')}")
with col_info3:
    if st.button("🔄 Refresh Prices", help="Reload prices from config file"):
        st.cache_data.clear()
        st.rerun()

# ==============================
# RESET FUNCTION
# ==============================
def reset_all():
    for k in list(st.session_state.keys()):
        if k not in ['prices_loaded']:  # Preserve price cache
            del st.session_state[k]
    st.rerun()

# ==============================
# PRICE MANAGEMENT SECTION (OFFLINE EDITOR)
# ==============================
with st.expander("💰 Price Management (Edit Offline - Saves to JSON)", expanded=False):
    st.warning("⚠️ Changes save to config/prices.json locally. Commit & push to GitHub for Streamlit Cloud.")
    
    tab1, tab2, tab3 = st.tabs(["Timber Prices", "Plywood Prices", "Instructions"])
    
    with tab1:
        st.subheader("Timber Rates ($/ton)")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        edited_timber = {}
        with col1:
            edited_timber["Kapur"] = st.number_input("Kapur", value=float(timber_prices["Kapur"]), step=50, key="edit_kapur")
        with col2:
            edited_timber["Balau"] = st.number_input("Balau", value=float(timber_prices["Balau"]), step=50, key="edit_balau")
        with col3:
            edited_timber["Chengal"] = st.number_input("Chengal", value=float(timber_prices["Chengal"]), step=50, key="edit_chengal")
        with col4:
            edited_timber["Mixed Keruing"] = st.number_input("Mixed Keruing", value=float(timber_prices["Mixed Keruing"]), step=50, key="edit_mixed")
        with col5:
            edited_timber["Pure Keruing"] = st.number_input("Pure Keruing", value=float(timber_prices["Pure Keruing"]), step=50, key="edit_pure")
    
    with tab2:
        st.subheader("Plywood Prices ($/sheet)")
        
        # Display current plywood prices in editable JSON format
        plywood_json = st.text_area(
            "Edit Plywood Prices (JSON format)",
            value=json.dumps(plywood_prices, indent=2),
            height=400,
            help="Format: {'Grade': {'thickness': price, ...}, ...}"
        )
        
        # Validate JSON
        try:
            test_json = json.loads(plywood_json)
            st.success("✅ Valid JSON format")
        except json.JSONDecodeError as e:
            st.error(f"❌ Invalid JSON: {e}")
    
    with tab3:
        st.markdown("""
        ### How to Update Prices Offline:
        
        **Option 1: Edit directly in this app**
        1. Modify prices above
        2. Click "Save Prices to File" button
        3. File saves to `config/prices.json`
        4. Commit and push to GitHub
        
        **Option 2: Edit JSON file directly**
        1. Open `config/prices.json` in any text editor
        2. Update the numbers
        3. Save file
        4. Commit and push to GitHub
        
        **Option 3: GitHub web interface**
        1. Go to your GitHub repository
        2. Navigate to `config/prices.json`
        3. Click edit (pencil icon)
        4. Modify prices
        5. Commit changes
        
        **After updating:**
        - Streamlit Cloud auto-deploys within 1-2 minutes
        - Click "Refresh Prices" button above to reload
        """)
    
    col_save1, col_save2 = st.columns(2)
    with col_save1:
        if st.button("💾 Save Prices to JSON File", type="primary"):
            try:
                new_plywood = json.loads(plywood_json)
                success, message = save_prices(edited_timber, new_plywood)
                if success:
                    st.success(message)
                    st.info("🔄 Click 'Refresh Prices' above to reload into app")
                    # ✅ FIXED: No global declaration needed
                    st.cache_data.clear()
                else:
                    st.error(message)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
    with col_save2:
        if st.button("🗑️ Reset to Default Prices"):
            default_config = {
                "timber": {
                    "Kapur": 3800, "Balau": 5500, "Chengal": 6000,
                    "Mixed Keruing": 650, "Pure Keruing": 1000
                },
                "plywood": {
                    "Marine": {"6": 25.5, "9": 37.0, "12": 45, "15": 56, "18": 68.5, "25": 95},
                    "Furniture": {"3": 15, "6": 17.5, "9": 19.5, "12": 23.8, "15": 26.8, "18": 31.5, "25": 45},
                    "MR": {"3": 4.1, "6": 6.8, "9": 10.5, "12": 15, "15": 19.5, "18": 21.7}
                },
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "version": "25.0"
            }
            with open(CONFIG_PATH, 'w') as f:
                json.dump(default_config, f, indent=2)
            st.success("Reset to default prices!")
            st.cache_data.clear()
            st.rerun()

# ==============================
# DISPLAY CURRENT RATES
# ==============================
st.subheader("💰 Current Market Rates")
col_r1, col_r2, col_r3, col_r4, col_r5 = st.columns(5)
with col_r1:
    st.metric("Kapur", f"${timber_prices['Kapur']}/ton")
with col_r2:
    st.metric("Balau", f"${timber_prices['Balau']}/ton")
with col_r3:
    st.metric("Chengal", f"${timber_prices['Chengal']}/ton")
with col_r4:
    st.metric("Mixed Keruing", f"${timber_prices['Mixed Keruing']}/ton")
with col_r5:
    st.metric("Pure Keruing", f"${timber_prices['Pure Keruing']}/ton")

# ==============================
# MODE SELECTION
# ==============================
mode = st.radio(
    "Select Mode",
    ["Customer Enquiry", "Manual Table"],
    horizontal=True
)

# ==============================
# CONSTANTS
# ==============================
inch_to_mm = {
    1: 20, 2: 43, 3: 70, 4: 93, 6: 143, 8: 193
}

# ==============================
# HELPER FUNCTIONS
# ==============================
def mm_to_inch(mm):
    for inch, val in inch_to_mm.items():
        if abs(mm - val) <= 5:
            return inch
    return max(round(mm / 25.4), 1)

def m_to_ft(m):
    if m <= 2.4:
        return 8
    elif m <= 3.0:
        return 10
    elif m <= 3.6:
        return 12
    elif m <= 4.2:
        return 14
    else:
        return round(m * 3.28084)

def calc(thk, wid, length, rate):
    raw = 7200 / (thk * wid * length)
    pcs_per_ton = round(raw, 3)
    pcs = max(math.floor(raw), 1)
    price = round(rate / pcs, 2)
    return pcs_per_ton, pcs, price

def is_keruing(species):
    return species in ["Mixed Keruing", "Pure Keruing"]

def validate_dimensions(thk, wid, length):
    """Validate timber dimensions"""
    errors = []
    if thk < 1 or thk > 12:
        errors.append("Thickness should be 1-12 inches")
    if wid < 2 or wid > 24:
        errors.append("Width should be 2-24 inches")
    if length < 4 or length > 20:
        errors.append("Length should be 4-20 feet")
    return errors

# ==============================
# MAIN FORM
# ==============================
with st.form("main_form"):
    
    if mode == "Customer Enquiry":
        enquiry = st.text_area("Customer Enquiry", height=200, 
                               placeholder="Example:\nKapur 20mm x 100mm x 2.4m 50pcs\nBalau 1\" x 3\" x 8ft 100pcs")
        
        # Sample button for testing
        if st.form_submit_button("Load Sample Enquiry"):
            enquiry = """Kapur 20mm x 100mm x 2.4m 50pcs
Balau 1" x 3" x 8ft 100pcs
Chengal 25mm x 150mm x 3.0m 25pcs"""
            st.rerun()
    
    if mode == "Manual Table":
        st.subheader("📋 Timber Order Table")
        
        timber_df = pd.DataFrame([{
            "Species": "Kapur",
            "Thickness": None,
            "T Unit": "mm",
            "Width": None,
            "W Unit": "mm",
            "Length": None,
            "L Unit": "m",
            "Qty": None
        }])
        
        timber_table = st.data_editor(
            timber_df,
            num_rows="dynamic",
            use_container_width=True,
            key="timber",
            column_config={
                "Species": st.column_config.SelectboxColumn(
                    options=["Kapur", "Balau", "Chengal", "Mixed Keruing", "Pure Keruing"]
                ),
                "T Unit": st.column_config.SelectboxColumn(
                    options=["mm", "inch"]
                ),
                "W Unit": st.column_config.SelectboxColumn(
                    options=["mm", "inch"]
                ),
                "L Unit": st.column_config.SelectboxColumn(
                    options=["m", "ft"]
                )
            }
        )
        
        st.subheader("📋 Plywood Order Table")
        
        plywood_df = pd.DataFrame([{
            "Type": "Marine",
            "Thickness": None,
            "Qty": None
        }])
        
        plywood_table = st.data_editor(
            plywood_df,
            num_rows="dynamic",
            use_container_width=True,
            key="plywood",
            column_config={
                "Type": st.column_config.SelectboxColumn(
                    options=["Marine", "Furniture", "MR"]
                )
            }
        )
    
    colA, colB = st.columns(2)
    generate = colA.form_submit_button("🚀 Generate Quote", type="primary", use_container_width=True)
    refresh = colB.form_submit_button("🔄 Refresh", use_container_width=True)

# ==============================
# HANDLE REFRESH
# ==============================
if refresh:
    reset_all()

# ==============================
# GENERATION ENGINE (Rest of your code remains the same)
# ==============================
if generate:
    internal_view = []
    customer_reply = []
    grand_total = 0
    errors = []
    
    # Add the rest of your generation code here
    # (Keep everything from your original generation engine)
    
    if mode == "Customer Enquiry":
        # ... your existing customer enquiry code ...
        pass
    
    if mode == "Manual Table":
        # ... your existing manual table code ...
        pass

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🪵 DS V25 Timber AI Buddy | Powered by Streamlit | Prices stored in config/prices.json")