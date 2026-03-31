# DS V25 timber AI buddy.py - PROFESSIONAL CLEAN VERSION
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
st.caption("Professional Quoting System")

# ==============================
# CUSTOM CSS FOR COMPACT LAYOUT
# ==============================
st.markdown("""
<style>
/* Compact spacing */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}
.stMetric {
    background-color: #f8f9fa;
    padding: 10px;
    border-radius: 5px;
}
/* Professional quote box */
.quote-box {
    background-color: #ffffff;
    border: 1px solid #d1d5db;
    border-radius: 8px;
    padding: 15px;
    margin: 10px 0;
    font-family: 'Courier New', monospace;
    font-size: 13px;
}
.quote-line {
    border-bottom: 1px solid #e5e7eb;
    padding: 5px 0;
}
.total-line {
    border-top: 2px solid #000000;
    padding-top: 8px;
    margin-top: 8px;
    font-weight: bold;
}
/* Hide default streamlit decorations */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
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
# RATES SECTION
# ==============================
st.subheader("Current Rates (USD/ton)")

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
# PLYWOOD PRICES SECTION
# ==============================
with st.expander("Plywood Prices (USD/sheet)", expanded=False):
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
# MODE SELECTION
# ==============================
mode = st.radio(
    "Select Mode",
    ["Customer Enquiry", "Manual Table"],
    horizontal=True
)

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
# MAIN FORM
# ==============================
with st.form(key="main_form"):
    
    if mode == "Customer Enquiry":
        enquiry = st.text_area("Customer Enquiry", height=120, 
                               placeholder="Example: Kapur 20mm x 100mm x 2.4m 50pcs")
        
        if st.form_submit_button("Load Sample"):
            enquiry = """Kapur 20mm x 100mm x 2.4m 50pcs
Balau 1" x 3" x 8ft 100pcs
Chengal 25mm x 150mm x 3.0m 25pcs"""
    
    if mode == "Manual Table":
        st.subheader("Timber Order Table")
        
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
        
        timber_df = pd.DataFrame(default_rows)
        
        timber_table = st.data_editor(
            timber_df,
            num_rows="dynamic",
            use_container_width=True,
            key="timber",
            column_config={
                "Species": st.column_config.SelectboxColumn(
                    options=["Kapur", "Balau", "Chengal", "Mixed Keruing", "Pure Keruing"]
                ),
                "T Unit": st.column_config.SelectboxColumn(options=["mm", "inch"], default="mm"),
                "W Unit": st.column_config.SelectboxColumn(options=["mm", "inch"], default="mm"),
                "L Unit": st.column_config.SelectboxColumn(options=["m", "ft"], default="m")
            }
        )
        
        st.subheader("Plywood Order Table")
        plywood_df = pd.DataFrame([{"Type": "Marine", "Thickness": None, "Qty": None}])
        
        plywood_table = st.data_editor(
            plywood_df,
            num_rows="dynamic",
            use_container_width=True,
            key="plywood",
            column_config={
                "Type": st.column_config.SelectboxColumn(options=["Marine", "Furniture", "MR"])
            }
        )
    
    colA, colB = st.columns(2)
    generate = colA.form_submit_button("GENERATE QUOTE", type="primary", use_container_width=True)
    reset = colB.form_submit_button("RESET", use_container_width=True)

if reset:
    reset_all()

# ==============================
# GENERATE QUOTE
# ==============================
if generate:
    quote_items = []
    calculation_log = []
    grand_total = 0.0
    
    if mode == "Customer Enquiry":
        if not enquiry.strip():
            st.error("Please enter customer enquiry")
            st.stop()
        
        lines = enquiry.lower().split("\n")
        current_species = None
        
        for line_num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            
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
                    
                    quote_items.append({
                        "type": "timber",
                        "name": f"{current_species} Timber",
                        "size": size_text,
                        "price": price,
                        "qty": qty,
                        "total": line_total
                    })
                    
                    calculation_log.append(f"{current_species} | {size_text} | Rate: ${rate}/ton | {pcs_per_ton} pcs/ton | ${price}/pcs | Qty: {qty} | Total: ${line_total}")
                    
                except Exception as e:
                    st.error(f"Line {line_num}: {str(e)}")
    
    if mode == "Manual Table":
        for idx, row in timber_table.iterrows():
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
                
                quote_items.append({
                    "type": "timber",
                    "name": f"{species} Timber",
                    "size": size_text,
                    "price": price,
                    "qty": qty,
                    "total": line_total
                })
                
                calculation_log.append(f"{species} | {size_text} | Rate: ${rate}/ton | {pcs_per_ton} pcs/ton | ${price}/pcs | Qty: {qty} | Total: ${line_total}")
                
            except Exception as e:
                st.error(f"Row {idx+1}: {str(e)}")
        
        for idx, row in plywood_table.iterrows():
            if pd.isna(row["Thickness"]) or pd.isna(row["Qty"]):
                continue
            
            try:
                grade = row["Type"]
                thk = int(row["Thickness"])
                qty = int(row["Qty"])
                
                note = ""
                if grade == "MR" and thk == 3 and qty < 10:
                    qty = 10
                    note = "(MOQ adjusted to 10pcs)"
                
                if thk not in plywood_prices[grade]:
                    st.error(f"Plywood row {idx+1}: {thk}mm not available for {grade}")
                    continue
                
                price = plywood_prices[grade][thk]
                line_total = round(price * qty, 2)
                grand_total += line_total
                
                quote_items.append({
                    "type": "plywood",
                    "name": f"{grade} Plywood {thk}mm",
                    "size": f"{thk}mm",
                    "price": price,
                    "qty": qty,
                    "total": line_total,
                    "note": note
                })
                
                calculation_log.append(f"{grade} Plywood {thk}mm | ${price}/pcs | Qty: {qty} | Total: ${line_total} {note}")
                
            except Exception as e:
                st.error(f"Plywood row {idx+1}: {str(e)}")
    
    # ==============================
    # DISPLAY RESULTS - PROFESSIONAL LAYOUT
    # ==============================
    if quote_items:
        st.divider()
        
        # Summary Row
        st.subheader("Quote Summary")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Total Items", len(quote_items))
        with col_s2:
            st.metric("Grand Total", f"${grand_total:,.2f}")
        with col_s3:
            st.metric("Quote Date", datetime.now().strftime("%Y-%m-%d"))
        
        st.divider()
        
        # Two Column Layout: Left = Quote Items, Right = Summary Info
        col_left, col_right = st.columns([2, 1])
        
        with col_left:
            st.markdown("### Quoted Items")
            st.markdown("---")
            
            for i, item in enumerate(quote_items, 1):
                st.markdown(f"**{i}. {item['name']}**")
                st.markdown(f"   Size: {item['size']}")
                st.markdown(f"   Unit Price: ${item['price']:,.2f}/pcs")
                st.markdown(f"   Quantity: {item['qty']} pcs")
                st.markdown(f"   **Total: ${item['total']:,.2f}**")
                if item.get('note'):
                    st.caption(f"   Note: {item['note']}")
                st.markdown("---")
        
        with col_right:
            st.markdown("### Summary")
            st.markdown("---")
            st.markdown(f"**Subtotal:** ${grand_total:,.2f}")
            st.markdown("---")
            st.markdown("**Delivery / Collection:**")
            st.markdown("30 Krani Loop (Blk A) #04-05")
            st.markdown("TimMac @ Kranji S739570")
            st.markdown("---")
            st.markdown("**Tolerances:**")
            st.markdown("• Thickness/Width: +-1~2mm")
            st.markdown("• Length: +-25~50mm")
            st.markdown("---")
            st.caption(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        st.divider()
        
        # Staff Calculation Log (Collapsible)
        with st.expander("Staff Calculation Log"):
            st.text("\n".join(calculation_log))
        
        # Export Button
        export_text = "TIMBER AI ASSISTANT V25 - QUOTE\n"
        export_text += "=" * 50 + "\n\n"
        for i, item in enumerate(quote_items, 1):
            export_text += f"{i}. {item['name']}\n"
            export_text += f"   Size: {item['size']}\n"
            export_text += f"   ${item['price']:,.2f}/pcs x {item['qty']} pcs = ${item['total']:,.2f}\n\n"
        export_text += "=" * 50 + "\n"
        export_text += f"TOTAL: ${grand_total:,.2f}\n\n"
        export_text += "Delivery: 30 Krani Loop (Blk A) #04-05, TimMac @ Kranji S739570\n"
        export_text += f"Quote Date: {datetime.now().strftime('%Y-%m-%d')}\n"
        
        st.download_button(
            label="Export Quote (TXT)",
            data=export_text,
            file_name=f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )
        
    else:
        st.warning("No valid items to process. Please add items to quote.")

# ==============================
# FOOTER
# ==============================
st.markdown("---")
st.caption("Timber AI Assistant V25 | Professional Quoting System")