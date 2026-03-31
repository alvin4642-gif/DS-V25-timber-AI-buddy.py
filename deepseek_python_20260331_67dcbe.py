# DS V25 timber AI buddy.py - FINAL VERSION (FIXED CLEAR BUTTONS)
import streamlit as st
import pandas as pd
import re
import math
from datetime import datetime

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(layout="wide", page_title="Timber AI Assistant V25", page_icon="📄")
st.title("Timber AI Assistant V25")
st.caption("Professional Quoting System (Prices in SGD)")

# ==============================
# CUSTOM CSS
# ==============================
st.markdown("""
<style>
/* Green generate button */
.stButton button[kind="primary"] {
    background-color: #10b981 !important;
    color: white !important;
}
.stButton button[kind="primary"]:hover {
    background-color: #059669 !important;
}
/* Calibri font for text areas */
.stTextArea textarea {
    font-family: 'Calibri', 'Segoe UI', sans-serif !important;
    font-size: 14px !important;
    line-height: 1.6 !important;
}
/* Bigger mode selector */
div[data-testid="stRadio"] > div {
    gap: 20px;
}
div[data-testid="stRadio"] label {
    font-size: 20px !important;
    font-weight: bold !important;
    padding: 10px 20px !important;
    background-color: #f0f2f6;
    border-radius: 10px;
}
div[data-testid="stRadio"] label:hover {
    background-color: #e0e2e6;
}
</style>
""", unsafe_allow_html=True)

# ==============================
# RESET FUNCTION
# ==============================
def reset_all():
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

# ==============================
# MODE SELECTION - TOP
# ==============================
st.markdown("### SELECT QUOTING MODE")
mode = st.radio(
    "",
    ["Customer Enquiry", "Manual Table"],
    horizontal=True,
    label_visibility="collapsed"
)
st.divider()

# ==============================
# RATES SECTION (SGD)
# ==============================
st.subheader("Current Rates (SGD/ton)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    kapur_rate = st.number_input("Kapur", value=3800, step=50, key="kapur_rate")
with col2:
    balau_rate = st.number_input("Balau", value=5500, step=50, key="balau_rate")
with col3:
    chengal_rate = st.number_input("Chengal", value=6000, step=50, key="chengal_rate")
with col4:
    mixed_keruing_rate = st.number_input("Mixed Keruing", value=650, step=50, key="mixed_rate")
with col5:
    pure_keruing_rate = st.number_input("Pure Keruing", value=1000, step=50, key="pure_rate")

species_rate = {
    "Kapur": kapur_rate,
    "Balau": balau_rate,
    "Chengal": chengal_rate,
    "Mixed Keruing": mixed_keruing_rate,
    "Pure Keruing": pure_keruing_rate
}

# ==============================
# PLYWOOD PRICES SECTION (SGD)
# ==============================
with st.expander("Plywood Prices (SGD/sheet)", expanded=False):
    plywood_tab1, plywood_tab2, plywood_tab3 = st.tabs(["Marine", "Furniture", "MR"])
    
    with plywood_tab1:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            marine_6mm = st.number_input("Marine 6mm", value=25.5, step=0.5, key="marine_6", format="%.1f")
            marine_9mm = st.number_input("Marine 9mm", value=37.0, step=0.5, key="marine_9", format="%.1f")
            marine_12mm = st.number_input("Marine 12mm", value=45.0, step=0.5, key="marine_12", format="%.1f")
        with col_b:
            marine_15mm = st.number_input("Marine 15mm", value=56.0, step=0.5, key="marine_15", format="%.1f")
            marine_18mm = st.number_input("Marine 18mm", value=68.5, step=0.5, key="marine_18", format="%.1f")
            marine_25mm = st.number_input("Marine 25mm", value=95.0, step=0.5, key="marine_25", format="%.1f")
    
    with plywood_tab2:
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            furn_3mm = st.number_input("Furniture 3mm", value=15.0, step=0.5, key="furn_3", format="%.1f")
            furn_6mm = st.number_input("Furniture 6mm", value=17.5, step=0.5, key="furn_6", format="%.1f")
            furn_9mm = st.number_input("Furniture 9mm", value=19.5, step=0.5, key="furn_9", format="%.1f")
        with col_b:
            furn_12mm = st.number_input("Furniture 12mm", value=23.8, step=0.5, key="furn_12", format="%.1f")
            furn_15mm = st.number_input("Furniture 15mm", value=26.8, step=0.5, key="furn_15", format="%.1f")
            furn_18mm = st.number_input("Furniture 18mm", value=31.5, step=0.5, key="furn_18", format="%.1f")
        with col_c:
            furn_25mm = st.number_input("Furniture 25mm", value=45.0, step=0.5, key="furn_25", format="%.1f")
    
    with plywood_tab3:
        col_a, col_b = st.columns(2)
        with col_a:
            mr_3mm = st.number_input("MR 3mm", value=4.1, step=0.5, key="mr_3", format="%.1f")
            mr_6mm = st.number_input("MR 6mm", value=6.8, step=0.5, key="mr_6", format="%.1f")
            mr_9mm = st.number_input("MR 9mm", value=10.5, step=0.5, key="mr_9", format="%.1f")
        with col_b:
            mr_12mm = st.number_input("MR 12mm", value=15.0, step=0.5, key="mr_12", format="%.1f")
            mr_15mm = st.number_input("MR 15mm", value=19.5, step=0.5, key="mr_15", format="%.1f")
            mr_18mm = st.number_input("MR 18mm", value=21.7, step=0.5, key="mr_18", format="%.1f")

plywood_prices = {
    "Marine": {6: marine_6mm, 9: marine_9mm, 12: marine_12mm, 15: marine_15mm, 18: marine_18mm, 25: marine_25mm},
    "Furniture": {3: furn_3mm, 6: furn_6mm, 9: furn_9mm, 12: furn_12mm, 15: furn_15mm, 18: furn_18mm, 25: furn_25mm},
    "MR": {3: mr_3mm, 6: mr_6mm, 9: mr_9mm, 12: mr_12mm, 15: mr_15mm, 18: mr_18mm}
}

st.divider()

# ==============================
# CONSTANTS & FUNCTIONS
# ==============================
inch_to_mm = {1: 20, 2: 43, 3: 70, 4: 93, 6: 143, 8: 193}

def mm_to_inch(mm):
    for inch, val in inch_to_mm.items():
        if abs(mm - val) <= 5:
            return inch
    return max(round(mm / 25.4), 1)

def m_to_ft(m):
    if m <= 2.4: return 8
    elif m <= 3.0: return 10
    elif m <= 3.6: return 12
    elif m <= 4.2: return 14
    else: return round(m * 3.28084)

def calc(thk, wid, length, rate):
    raw = 7200 / (thk * wid * length)
    pcs_per_ton = round(raw, 3)
    pcs = max(math.floor(raw), 1)
    price = round(rate / pcs, 2)
    return pcs_per_ton, pcs, price

def is_keruing(species):
    return species in ["Mixed Keruing", "Pure Keruing"]

# ==============================
# INITIALIZE SESSION STATE FOR TABLES
# ==============================
if "timber_df" not in st.session_state:
    default_rows = []
    for i in range(5):
        default_rows.append({
            "Species": "Kapur",
            "Thickness": None,
            "T Unit": "mm",
            "Width": None,
            "W Unit": "mm",
            "Length": None,
            "L Unit": "m",
            "Qty": None
        })
    st.session_state.timber_df = pd.DataFrame(default_rows)

if "plywood_df" not in st.session_state:
    st.session_state.plywood_df = pd.DataFrame([{
        "Type": "Marine",
        "Thickness": None,
        "Qty": None
    }])

# ==============================
# MAIN FORM
# ==============================
with st.form(key="main_form"):
    
    if mode == "Customer Enquiry":
        enquiry = st.text_area("Customer Enquiry", height=120, 
                               placeholder="Example: Kapur 20mm x 100mm x 2.4m 50pcs")
        
        sample_col = st.columns([1, 4])
        with sample_col[0]:
            if st.form_submit_button("Load Sample"):
                enquiry = """Kapur 20mm x 100mm x 2.4m 50pcs
Balau 1" x 3" x 8ft 100pcs
Chengal 25mm x 150mm x 3.0m 25pcs
MR 3mm 3pcs"""
    
    if mode == "Manual Table":
        st.subheader("Timber Order Table")
        
        timber_col1, timber_col2 = st.columns([6, 1])
        with timber_col2:
            if st.form_submit_button("Clear Timber"):
                # Reset timber dataframe
                default_rows = []
                for i in range(5):
                    default_rows.append({
                        "Species": "Kapur",
                        "Thickness": None,
                        "T Unit": "mm",
                        "Width": None,
                        "W Unit": "mm",
                        "Length": None,
                        "L Unit": "m",
                        "Qty": None
                    })
                st.session_state.timber_df = pd.DataFrame(default_rows)
                st.rerun()
        
        timber_table = st.data_editor(
            st.session_state.timber_df,
            num_rows="dynamic",
            use_container_width=True,
            key="timber_editor",
            column_config={
                "Species": st.column_config.SelectboxColumn(
                    options=["Kapur", "Balau", "Chengal", "Mixed Keruing", "Pure Keruing"]
                ),
                "T Unit": st.column_config.SelectboxColumn(options=["mm", "inch"], default="mm"),
                "W Unit": st.column_config.SelectboxColumn(options=["mm", "inch"], default="mm"),
                "L Unit": st.column_config.SelectboxColumn(options=["m", "ft"], default="m")
            }
        )
        # Save edited data back to session state
        st.session_state.timber_df = timber_table
        
        st.subheader("Plywood Order Table")
        
        plywood_col1, plywood_col2 = st.columns([6, 1])
        with plywood_col2:
            if st.form_submit_button("Clear Plywood"):
                # Reset plywood dataframe
                st.session_state.plywood_df = pd.DataFrame([{
                    "Type": "Marine",
                    "Thickness": None,
                    "Qty": None
                }])
                st.rerun()
        
        plywood_table = st.data_editor(
            st.session_state.plywood_df,
            num_rows="dynamic",
            use_container_width=True,
            key="plywood_editor",
            column_config={
                "Type": st.column_config.SelectboxColumn(options=["Marine", "Furniture", "MR"])
            }
        )
        # Save edited data back to session state
        st.session_state.plywood_df = plywood_table
    
    colA, colB = st.columns([2, 1])
    with colA:
        generate = st.form_submit_button("GENERATE QUOTE", type="primary", use_container_width=True)
    with colB:
        reset = st.form_submit_button("RESET ALL", use_container_width=True)

if reset:
    reset_all()

# ==============================
# GENERATE QUOTE
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
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
            # Check for MR plywood (with or without the word "plywood")
            mr_match = re.search(r'mr\s*(\d+)\s*mm\s*(\d+)\s*pcs', line)
            if mr_match:
                thk = int(mr_match.group(1))
                original_qty = int(mr_match.group(2))
                
                grade = "MR"
                actual_qty = original_qty
                moq_message = ""
                
                # Apply MOQ rule for MR 3mm
                if thk == 3 and original_qty < 10:
                    actual_qty = 10
                    moq_message = "Note: MR 3mm plywood minimum order quantity is 10pcs"
                
                if thk in plywood_prices[grade]:
                    price = plywood_prices[grade][thk]
                    line_total = round(price * actual_qty, 2)
                    grand_total += line_total
                    
                    internal_view.append(
                        f"""{grade.upper()} PLYWOOD
{thk}mm

Price per sheet: S${price}
Customer requested: {original_qty} pcs
Adjusted quantity: {actual_qty} pcs
Total: S${line_total}
{moq_message}
------------------------"""
                    )
                    
                    customer_line = f"{grade} plywood {thk}mm @ S${price}/pcs x {actual_qty} = S${line_total}"
                    if moq_message:
                        customer_line += f"\n({moq_message})"
                    customer_reply.append(customer_line)
                else:
                    errors.append(f"Line {line_num}: Thickness {thk}mm not available for {grade}")
                continue
            
            # Also check for "MR plywood" format
            if "mr" in line and "plywood" in line:
                thickness_match = re.search(r'(\d+)\s*mm', line)
                qty_match = re.search(r'(\d+)\s*pcs', line)
                
                if thickness_match and qty_match:
                    thk = int(thickness_match.group(1))
                    original_qty = int(qty_match.group(1))
                    
                    grade = "MR"
                    actual_qty = original_qty
                    moq_message = ""
                    
                    if thk == 3 and original_qty < 10:
                        actual_qty = 10
                        moq_message = "Note: MR 3mm plywood minimum order quantity is 10pcs"
                    
                    if thk in plywood_prices[grade]:
                        price = plywood_prices[grade][thk]
                        line_total = round(price * actual_qty, 2)
                        grand_total += line_total
                        
                        internal_view.append(
                            f"""{grade.upper()} PLYWOOD
{thk}mm

Price per sheet: S${price}
Customer requested: {original_qty} pcs
Adjusted quantity: {actual_qty} pcs
Total: S${line_total}
{moq_message}
------------------------"""
                        )
                        
                        customer_line = f"{grade} plywood {thk}mm @ S${price}/pcs x {actual_qty} = S${line_total}"
                        if moq_message:
                            customer_line += f"\n({moq_message})"
                        customer_reply.append(customer_line)
                    else:
                        errors.append(f"Line {line_num}: Thickness {thk}mm not available for {grade}")
                continue
            
            # Process timber
            current_species = None
            if "kapur" in line:
                current_species = "Kapur"
            elif "balau" in line:
                current_species = "Balau"
            elif "chengal" in line:
                current_species = "Chengal"
            elif "mixed keruing" in line:
                current_species = "Mixed Keruing"
            elif "pure keruing" in line:
                current_species = "Pure Keruing"
            
            if not current_species:
                continue
            
            qty_match = re.findall(r'(\d+)\s*(pcs|nos|pieces|pc)', line)
            qty = int(qty_match[0][0]) if qty_match else 1
            
            size_match = re.findall(
                r'(\d+(?:\.\d+)?)\s*(mm|inch|")\s*[x*]\s*(\d+(?:\.\d+)?)\s*(mm|inch|")\s*[x*]\s*(\d+(?:\.\d+)?)\s*(m|ft|\')',
                line, re.IGNORECASE
            )
            
            for s in size_match:
                try:
                    v1, u1, v2, u2, v3, u3 = s
                    v1, v2, v3 = float(v1), float(v2), float(v3)
                    
                    thk = mm_to_inch(v1) if u1 in ["mm", "milimeter"] else int(v1)
                    wid = mm_to_inch(v2) if u2 in ["mm", "milimeter"] else int(v2)
                    length = m_to_ft(v3) if u3 in ["m", "meter"] else int(v3)
                    
                    if length == 19: length = 20
                    
                    rate = species_rate[current_species]
                    pcs_per_ton, pcs, price = calc(thk, wid, length, rate)
                    
                    if is_keruing(current_species):
                        size_text = f'{thk}" x {wid}" x {length}ft'
                    else:
                        mm_thk = inch_to_mm.get(thk, int(thk * 25.4))
                        mm_wid = inch_to_mm.get(wid, int(wid * 25.4))
                        size_text = f"{mm_thk}mm x {mm_wid}mm x {length}ft"
                    
                    line_total = round(price * qty, 2)
                    grand_total += line_total
                    
                    internal_view.append(
                        f"""{current_species.upper()} TIMBER
{size_text}

Rate: S${rate}/ton
Pieces per ton: {pcs_per_ton}
Price per piece: S${price}
Quantity: {qty} pcs
Total: S${line_total}
------------------------"""
                    )
                    
                    customer_reply.append(
                        f"{current_species} timber\n{size_text} @ S${price}/pcs x {qty} = S${line_total}"
                    )
                    
                except Exception as e:
                    errors.append(f"Error processing line {line_num}: {str(e)}")
    
    if mode == "Manual Table":
        # Process timber from session state
        timber_data = st.session_state.timber_df
        for idx, row in timber_data.iterrows():
            if pd.isna(row["Thickness"]) or pd.isna(row["Width"]) or pd.isna(row["Length"]) or pd.isna(row["Qty"]):
                continue
            
            try:
                species = row["Species"]
                t = float(row["Thickness"])
                w = float(row["Width"])
                l = float(row["Length"])
                qty = int(row["Qty"])
                
                thk = mm_to_inch(t) if row["T Unit"] == "mm" else int(t)
                wid = mm_to_inch(w) if row["W Unit"] == "mm" else int(w)
                length = m_to_ft(l) if row["L Unit"] == "m" else int(l)
                
                if length == 19: length = 20
                
                rate = species_rate[species]
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
                    f"""{species.upper()} TIMBER
{size_text}

Rate: S${rate}/ton
Pieces per ton: {pcs_per_ton}
Price per piece: S${price}
Quantity: {qty} pcs
Total: S${line_total}
------------------------"""
                )
                
                customer_reply.append(
                    f"{species} timber\n{size_text} @ S${price}/pcs x {qty} = S${line_total}"
                )
                
            except Exception as e:
                errors.append(f"Error processing timber row {idx+1}: {str(e)}")
        
        # Process plywood from session state
        plywood_data = st.session_state.plywood_df
        for idx, row in plywood_data.iterrows():
            if pd.isna(row["Thickness"]) or pd.isna(row["Qty"]):
                continue
            
            try:
                grade = row["Type"]
                thk = int(row["Thickness"])
                original_qty = int(row["Qty"])
                
                actual_qty = original_qty
                moq_message = ""
                
                if grade == "MR" and thk == 3 and original_qty < 10:
                    actual_qty = 10
                    moq_message = "Note: MR 3mm plywood minimum order quantity is 10pcs"
                
                if thk not in plywood_prices[grade]:
                    errors.append(f"Plywood row {idx+1}: Thickness {thk}mm not available for {grade}")
                    continue
                
                price = plywood_prices[grade][thk]
                line_total = round(price * actual_qty, 2)
                grand_total += line_total
                
                internal_view.append(
                    f"""{grade.upper()} PLYWOOD
{thk}mm

Price per sheet: S${price}
Customer requested: {original_qty} pcs
Adjusted quantity: {actual_qty} pcs
Total: S${line_total}
{moq_message}
------------------------"""
                )
                
                customer_line = f"{grade} plywood {thk}mm @ S${price}/pcs x {actual_qty} = S${line_total}"
                if moq_message:
                    customer_line += f"\n({moq_message})"
                customer_reply.append(customer_line)
                    
            except Exception as e:
                errors.append(f"Error processing plywood row {idx+1}: {str(e)}")
    
    # ==============================
    # DISPLAY RESULTS
    # ==============================
    if internal_view:
        # Summary metrics
        st.subheader("Quote Summary")
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Total Items", len(customer_reply))
        with col_m2:
            st.metric("Grand Total", f"S${grand_total:,.2f}")
        with col_m3:
            st.metric("Quote Generated", datetime.now().strftime("%H:%M:%S"))
        
        # Staff Calculation Log
        st.subheader("Staff Calculation Log")
        st.text_area("", "\n".join(internal_view), height=300)
        
        st.divider()
        
        # Customer Reply
        st.subheader("Customer Reply")
        
        # Build the final customer reply text
        final_reply = []
        for item in customer_reply:
            final_reply.append(item)
        
        final_reply.append(f"\nTotal : S${round(grand_total,2)}")
        final_reply.append("\nTolerances:")
        final_reply.append("- Thickness/Width: +-1~2mm")
        final_reply.append("- Length: +-25~50mm")
        final_reply.append("\nDelivery / Self Collection:")
        final_reply.append("30 Krani Loop (Blk A) #04-05")
        final_reply.append("TimMac @ Kranji S739570")
        
        customer_reply_text = "\n".join(final_reply)
        
        # Display the customer reply
        st.text_area("", customer_reply_text, height=350)
        
        # Export button
        st.download_button(
            label="Export Quote (TXT)",
            data=customer_reply_text,
            file_name=f"timber_quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
    else:
        st.warning("No valid items to process. Please check your inputs.")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Timber AI Assistant V25 | Professional Quoting System | Prices in SGD")