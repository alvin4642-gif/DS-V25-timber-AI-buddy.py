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
                    "Kapur": 3800.0,
                    "Balau": 5500.0,
                    "Chengal": 6000.0,
                    "Mixed Keruing": 650.0,
                    "Pure Keruing": 1000.0
                },
                "plywood": {
                    "Marine": {
                        "6": 25.5, "9": 37.0, "12": 45.0, "15": 56.0, "18": 68.5, "25": 95.0
                    },
                    "Furniture": {
                        "3": 15.0, "6": 17.5, "9": 19.5, "12": 23.8, "15": 26.8, "18": 31.5, "25": 45.0
                    },
                    "MR": {
                        "3": 4.1, "6": 6.8, "9": 10.5, "12": 15.0, "15": 19.5, "18": 21.7
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
            edited_timber["Kapur"] = st.number_input(
                "Kapur", 
                value=float(timber_prices["Kapur"]), 
                step=50.0, 
                format="%.0f",
                key="edit_kapur"
            )
        with col2:
            edited_timber["Balau"] = st.number_input(
                "Balau", 
                value=float(timber_prices["Balau"]), 
                step=50.0,
                format="%.0f", 
                key="edit_balau"
            )
        with col3:
            edited_timber["Chengal"] = st.number_input(
                "Chengal", 
                value=float(timber_prices["Chengal"]), 
                step=50.0,
                format="%.0f", 
                key="edit_chengal"
            )
        with col4:
            edited_timber["Mixed Keruing"] = st.number_input(
                "Mixed Keruing", 
                value=float(timber_prices["Mixed Keruing"]), 
                step=50.0,
                format="%.0f", 
                key="edit_mixed"
            )
        with col5:
            edited_timber["Pure Keruing"] = st.number_input(
                "Pure Keruing", 
                value=float(timber_prices["Pure Keruing"]), 
                step=50.0,
                format="%.0f", 
                key="edit_pure"
            )
    
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
                    st.cache_data.clear()
                else:
                    st.error(message)
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
    with col_save2:
        if st.button("🗑️ Reset to Default Prices"):
            default_config = {
                "timber": {
                    "Kapur": 3800.0, "Balau": 5500.0, "Chengal": 6000.0,
                    "Mixed Keruing": 650.0, "Pure Keruing": 1000.0
                },
                "plywood": {
                    "Marine": {"6": 25.5, "9": 37.0, "12": 45.0, "15": 56.0, "18": 68.5, "25": 95.0},
                    "Furniture": {"3": 15.0, "6": 17.5, "9": 19.5, "12": 23.8, "15": 26.8, "18": 31.5, "25": 45.0},
                    "MR": {"3": 4.1, "6": 6.8, "9": 10.5, "12": 15.0, "15": 19.5, "18": 21.7}
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
    st.metric("Kapur", f"${timber_prices['Kapur']:,.0f}/ton")
with col_r2:
    st.metric("Balau", f"${timber_prices['Balau']:,.0f}/ton")
with col_r3:
    st.metric("Chengal", f"${timber_prices['Chengal']:,.0f}/ton")
with col_r4:
    st.metric("Mixed Keruing", f"${timber_prices['Mixed Keruing']:,.0f}/ton")
with col_r5:
    st.metric("Pure Keruing", f"${timber_prices['Pure Keruing']:,.0f}/ton")

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
        sample_clicked = st.form_submit_button("Load Sample Enquiry")
        if sample_clicked:
            st.session_state.sample_enquiry = """Kapur 20mm x 100mm x 2.4m 50pcs
Balau 1" x 3" x 8ft 100pcs
Chengal 25mm x 150mm x 3.0m 25pcs"""
            st.rerun()
        
        if "sample_enquiry" in st.session_state:
            enquiry = st.session_state.sample_enquiry
    
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
# GENERATION ENGINE
# ==============================
if generate:
    internal_view = []
    customer_reply = []
    grand_total = 0
    errors = []
    
    if mode == "Customer Enquiry":
        if not enquiry.strip():
            st.error("Please enter customer enquiry")
            st.stop()
        
        lines = enquiry.lower().split("\n")
        current_species = None
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            # Species detection
            if "kapur" in line:
                current_species = "Kapur"
            elif "balau" in line:
                current_species = "Balau"
            elif "chengal" in line:
                current_species = "Chengal"
            elif "mixed" in line and "keruing" in line:
                current_species = "Mixed Keruing"
            elif "pure keruing" in line:
                current_species = "Pure Keruing"
            
            if not current_species:
                continue
            
            # Extract quantity
            qty_match = re.findall(r'(\d+)\s*(pcs|nos|pieces|pc)', line)
            qty = int(qty_match[0][0]) if qty_match else 1
            
            # Extract dimensions
            size_match = re.findall(
                r'(\d+(?:\.\d+)?)\s*(mm|inch|")\s*[x*]\s*(\d+(?:\.\d+)?)\s*(mm|inch|")\s*[x*]\s*(\d+(?:\.\d+)?)\s*(m|ft|\')',
                line,
                re.IGNORECASE
            )
            
            for s in size_match:
                try:
                    v1, u1, v2, u2, v3, u3 = s
                    
                    v1 = float(v1)
                    v2 = float(v2)
                    v3 = float(v3)
                    
                    # Convert to inches and feet
                    if u1 in ["mm", "milimeter"]:
                        thk = mm_to_inch(v1)
                    else:
                        thk = int(v1)
                    
                    if u2 in ["mm", "milimeter"]:
                        wid = mm_to_inch(v2)
                    else:
                        wid = int(v2)
                    
                    if u3 in ["m", "meter"]:
                        length = m_to_ft(v3)
                    else:
                        length = int(v3)
                    
                    # Fix for length 19
                    if length == 19:
                        length = 20
                    
                    # Validation
                    dimension_errors = validate_dimensions(thk, wid, length)
                    if dimension_errors:
                        errors.extend([f"Line {line_num}: {err}" for err in dimension_errors])
                        continue
                    
                    rate = timber_prices[current_species]
                    pcs_per_ton, pcs, price = calc(thk, wid, length, rate)
                    
                    # Size text formatting
                    if is_keruing(current_species):
                        size_text = f'{thk}" x {wid}" x {length}ft'
                    else:
                        mm_thk = inch_to_mm.get(thk, int(thk * 25.4))
                        mm_wid = inch_to_mm.get(wid, int(wid * 25.4))
                        size_text = f"{mm_thk}mm x {mm_wid}mm x {length}ft"
                    
                    line_total = round(price * qty, 2)
                    grand_total += line_total
                    
                    internal_view.append(
                        f"""{current_species.upper()} timber
{size_text}

$/ton : ${rate:,.2f}
pcs/ton : {pcs_per_ton}
$/pcs : ${price:,.2f}

Qty : {qty} pcs
Total : ${line_total:,.2f}

------------------------"""
                    )
                    
                    customer_reply.append(
                        f"""📦 {current_species} timber
   {size_text} @ ${price:,.2f}/pcs x {qty} pcs = ${line_total:,.2f}
"""
                    )
                    
                except Exception as e:
                    errors.append(f"Error processing line {line_num}: {str(e)}")
    
    if mode == "Manual Table":
        # Process timber
        for idx, row in timber_table.iterrows():
            if pd.isna(row["Thickness"]) or pd.isna(row["Width"]) or pd.isna(row["Length"]) or pd.isna(row["Qty"]):
                continue
            
            try:
                species = row["Species"]
                t = float(row["Thickness"])
                w = float(row["Width"])
                l = float(row["Length"])
                qty = int(row["Qty"])
                
                # Convert units
                thk = mm_to_inch(t) if row["T Unit"] == "mm" else int(t)
                wid = mm_to_inch(w) if row["W Unit"] == "mm" else int(w)
                length = m_to_ft(l) if row["L Unit"] == "m" else int(l)
                
                if length == 19:
                    length = 20
                
                # Validation
                dimension_errors = validate_dimensions(thk, wid, length)
                if dimension_errors:
                    errors.extend([f"Row {idx+1}: {err}" for err in dimension_errors])
                    continue
                
                rate = timber_prices[species]
                pcs_per_ton, pcs, price = calc(thk, wid, length, rate)
                
                if is_keruing(species):
                    size_text = f'{thk}" x {wid}" x {length}ft'
                else:
                    mm_thk = inch_to_mm.get(thk, int(thk * 25.4))
                    mm_wid = inch_to_mm.get(wid, int(wid * 25.4))
                    size_text = f"{mm_thk}mm x {mm_wid}mm x {length}ft"
                
                line_total = round(price * qty, 2)
                grand_total += line_total
                
                internal_view.append(
                    f"""{species.upper()} timber
{size_text}

$/ton : ${rate:,.2f}
pcs/ton : {pcs_per_ton}
$/pcs : ${price:,.2f}

Qty : {qty} pcs
Total : ${line_total:,.2f}

------------------------"""
                )
                
                customer_reply.append(
                    f"""📦 {species} timber
   {size_text} @ ${price:,.2f}/pcs x {qty} pcs = ${line_total:,.2f}
"""
                )
                
            except Exception as e:
                errors.append(f"Error processing timber row {idx+1}: {str(e)}")
        
        # Process plywood
        for idx, row in plywood_table.iterrows():
            if pd.isna(row["Thickness"]) or pd.isna(row["Qty"]):
                continue
            
            try:
                grade = row["Type"]
                thk = int(row["Thickness"])
                qty = int(row["Qty"])
                
                note = ""
                
                # Apply MOQ rules
                if grade == "MR" and thk == 3 and qty < 10:
                    qty = 10
                    note = "⚠️ Minimum order quantity for MR 3mm is 10pcs (adjusted)"
                
                thk_str = str(thk)
                if thk_str not in plywood_prices.get(grade, {}):
                    errors.append(f"Plywood row {idx+1}: Thickness {thk}mm not available for {grade}")
                    continue
                
                price = plywood_prices[grade][thk_str]
                line_total = round(price * qty, 2)
                grand_total += line_total
                
                internal_view.append(
                    f"""{grade.upper()} PLYWOOD
{thk}mm

$/pcs : ${price:,.2f}

Qty : {qty} pcs
Total : ${line_total:,.2f}

------------------------"""
                )
                
                customer_reply.append(
                    f"""📋 {grade} plywood {thk}mm @ ${price:,.2f}/pcs x {qty} pcs = ${line_total:,.2f}"""
                )
                
                if note:
                    customer_reply.append(note)
                    
            except Exception as e:
                errors.append(f"Error processing plywood row {idx+1}: {str(e)}")
    
    # Display errors if any
    if errors:
        with st.expander("⚠️ Validation Errors", expanded=True):
            for error in errors:
                st.error(error)
    
    # Display results if there are any items
    if internal_view:
        # Summary metrics
        st.subheader("📊 Quote Summary")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Items", len(customer_reply))
        with col_m2:
            st.metric("Grand Total", f"${grand_total:,.2f}")
        with col_m3:
            st.metric("Quote Generated", datetime.now().strftime("%H:%M:%S"))
        
        # Internal View (for staff)
        with st.expander("🔧 Internal View (Staff Only)", expanded=False):
            st.text_area("Detailed Calculations", "\n\n".join(internal_view), height=400)
        
        # Customer Reply
        st.subheader("📄 Customer Quote")
        
        # Add footer
        customer_reply.append(f"\n💰 **TOTAL: ${round(grand_total, 2)}**")
        customer_reply.append("\n---")
        customer_reply.append("📏 **Tolerances:**")
        customer_reply.append("- Thickness/Width: +-1~2mm")
        customer_reply.append("- Length: +-25~50mm")
        customer_reply.append("\n🚚 **Delivery / Collection:**")
        customer_reply.append("30 Krani Loop (Blk A) #04-05")
        customer_reply.append("TimMac @ Kranji S739570")
        customer_reply.append(f"\n📅 Quote Date: {datetime.now().strftime('%Y-%m-%d')}")
        
        st.text_area("Ready to Send", "\n".join(customer_reply), height=400)
        
        # Export option
        col_e1, col_e2 = st.columns(2)
        with col_e1:
            st.download_button(
                label="📥 Download Quote (TXT)",
                data="\n".join(customer_reply),
                file_name=f"timber_quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        with col_e2:
            st.info("💡 Tip: Copy the quote above and paste into email/WhatsApp")
    else:
        st.warning("No valid items to process. Please check your inputs.")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("🪵 DS V25 Timber AI Buddy | Powered by Streamlit | Prices stored in config/prices.json")