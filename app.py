import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import io
from docx import Document
from fpdf import FPDF

# --- Page Configuration ---
st.set_page_config(
    page_title="SolarAI Estimator | Engr. Bilal Mehmood",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern High-Contrast & Aligned Styling ---
st.markdown("""
    <style>
    /* Global Background & Typography */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFDF0 !important; /* Soft Cream Yellow */
        color: #1A1A1A !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    /* Force Clean High-Contrast Text Color */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #111827 !important;
    }

    /* Top Premium Banner Header */
    .app-header-banner {
        background: linear-gradient(135deg, #FFB703 0%, #FB8500 100%);
        padding: 30px 35px;
        border-radius: 18px;
        color: #000000 !important;
        text-align: center;
        margin-bottom: 25px;
        border: 2px solid #E07A00;
        box-shadow: 0 10px 25px -5px rgba(251, 133, 0, 0.25);
    }
    .app-header-banner h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #000000 !important;
    }
    .app-header-banner p {
        margin: 10px 0 0 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #1A1A1A !important;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #FEF3C7 !important; /* Light Amber/Yellow */
        border-right: 2px solid #FCD34D;
    }

    /* Ahmad Animated Character Avatar Container */
    .ahmad-sidebar-container {
        text-align: center;
        margin-bottom: 20px;
        background: #FFFFFF;
        border: 2px solid #F59E0B;
        border-radius: 16px;
        padding: 20px 15px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
    }
    .animated-avatar-box {
        width: 90px;
        height: 90px;
        margin: 0 auto;
        background: #FEF3C7;
        border: 3px solid #F59E0B;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.8rem;
        animation: floatAvatar 3s ease-in-out infinite;
    }
    @keyframes floatAvatar {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }
    .ahmad-label {
        margin-top: 10px;
        font-weight: 800;
        color: #111827 !important;
        font-size: 1.25rem;
    }
    .ahmad-sublabel {
        font-size: 0.85rem;
        color: #4B5563 !important;
        font-weight: 600;
    }

    /* Streamlit Metric Boxes Alignment & Styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF !important;
        border: 1px solid #FCD34D !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.03);
    }
    div[data-testid="stMetricValue"] {
        color: #D97706 !important;
        font-weight: 800 !important;
        font-size: 1.8rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #374151 !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
    }

    /* Table & Tabs Alignment */
    .stDataFrame {
        background-color: #FFFFFF !important;
        border-radius: 10px;
        border: 1px solid #E5E7EB;
    }
    button[data-baseweb="tab"] {
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    </style>
""", unsafe_allow_html=True)


# --- REPORT GENERATION FUNCTIONS ---
def generate_docx_report(df, total_daily_kwh, num_panels, panel_wattage, recommended_inverter_kw, battery_amp_hours, system_voltage, cable_size, cable_length):
    doc = Document()
    doc.add_heading('SolarAI Power Systems Estimator Report', 0)
    doc.add_paragraph('Designed by Engr. Bilal Mehmood | Ahmad AI Assistant')
    
    doc.add_heading('1. Executive Summary & Hardware Sizing', level=1)
    doc.add_paragraph(f'• Total Daily Energy Consumption: {total_daily_kwh:.2f} kWh')
    doc.add_paragraph(f'• Solar Panels Required: {num_panels} Units ({panel_wattage}W each)')
    doc.add_paragraph(f'• Recommended Inverter Capacity: {max(1.0, recommended_inverter_kw):.1f} kW')
    doc.add_paragraph(f'• Battery Bank Capacity: {battery_amp_hours:.0f} Ah @ {system_voltage}V')
    doc.add_paragraph(f'• Recommended DC Cable: {cable_size} (Length: {cable_length}m)')

    doc.add_heading('2. Appliance Load Inventory', level=1)
    table = doc.add_table(rows=1, cols=4)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Appliance'
    hdr_cells[1].text = 'Quantity'
    hdr_cells[2].text = 'Watts Each'
    hdr_cells[3].text = 'Hours/Day'
    
    for _, row in df.iterrows():
        row_cells = table.add_row().cells
        row_cells[0].text = str(row['Appliance'])
        row_cells[1].text = str(row['Quantity'])
        row_cells[2].text = str(row['Watts Each'])
        row_cells[3].text = str(row['Hours Used/Day'])
        
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio


class PDFReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 14)
        self.cell(0, 10, 'SolarAI Power Systems Estimator Report', 0, 1, 'C')
        self.set_font('helvetica', '', 9)
        self.cell(0, 5, 'Designed by Engr. Bilal Mehmood | Ahmad AI Assistant', 0, 1, 'C')
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def generate_pdf_report(df, total_daily_kwh, num_panels, panel_wattage, recommended_inverter_kw, battery_amp_hours, system_voltage, cable_size, cable_length):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, '1. Executive Summary & Hardware Sizing', 0, 1)
    
    pdf.set_font('helvetica', '', 10)
    pdf.cell(0, 6, f'Total Daily Energy Consumption: {total_daily_kwh:.2f} kWh', 0, 1)
    pdf.cell(0, 6, f'Solar Panels Required: {num_panels} Units ({panel_wattage}W each)', 0, 1)
    pdf.cell(0, 6, f'Recommended Inverter Capacity: {max(1.0, recommended_inverter_kw):.1f} kW', 0, 1)
    pdf.cell(0, 6, f'Battery Bank Capacity: {battery_amp_hours:.0f} Ah @ {system_voltage}V', 0, 1)
    pdf.cell(0, 6, f'Recommended DC Cable: {cable_size} (Length: {cable_length}m)', 0, 1)
    pdf.ln(5)

    pdf.set_font('helvetica', 'B', 12)
    pdf.cell(0, 8, '2. Appliance Load Inventory', 0, 1)
    
    pdf.set_font('helvetica', 'B', 9)
    pdf.cell(70, 7, 'Appliance', 1)
    pdf.cell(30, 7, 'Qty', 1)
    pdf.cell(45, 7, 'Watts Each', 1)
    pdf.cell(45, 7, 'Hours/Day', 1)
    pdf.ln()

    pdf.set_font('helvetica', '', 9)
    for _, row in df.iterrows():
        pdf.cell(70, 6, str(row['Appliance']), 1)
        pdf.cell(30, 6, str(row['Quantity']), 1)
        pdf.cell(45, 6, str(row['Watts Each']), 1)
        pdf.cell(45, 6, str(row['Hours Used/Day']), 1)
        pdf.ln()

    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        pdf_output = pdf_output.encode('latin-1')
    return io.BytesIO(pdf_output)


# --- WELCOME POPUP FOR VISITORS (st.dialog) ---
@st.dialog("☀️ Welcome to SolarAI Power Systems Estimator!")
def welcome_popup():
    col1, col2 = st.columns([1, 2], vertical_alignment="center")
    with col1:
        st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="font-size: 4.5rem; background: #FEF3C7; border-radius: 50%; width: 100px; height: 100px; line-height: 100px; margin: 0 auto; border: 2px solid #F59E0B;">👦</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            ### Hello! I'm Ahmad 👋
            
            I'm your **AI Solar Assistant**, here to help you size and design your complete solar power system!

            **Here's what we will calculate together:**
            * ☀️ **Solar Panels:** Total wattage & required quantity
            * ⚡ **Inverter Sizing:** Peak capacity with safety margin
            * 🔋 **Battery Bank:** Capacity ($\text{Ah}$) & backup duration
            * 🛠️ **DC Cable Sizing:** Maximum current & gauge ($\text{mm}^2$ / AWG)
        """)
    st.markdown("---")
    if st.button("🚀 Start Solar Calculation", type="primary", use_container_width=True):
        st.session_state.welcome_shown = True
        st.rerun()

if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    welcome_popup()


# --- Session State Initialization for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am **Ahmad**, your solar AI assistant. Tell me about your appliances or power requirements, and I'll help you configure the ideal setup!"}
    ]


# --- Sidebar: Ahmad & Inputs ---
with st.sidebar:
    st.markdown("""
        <div class="ahmad-sidebar-container">
            <div class="animated-avatar-box">👦</div>
            <div class="ahmad-label">Ahmad</div>
            <div class="ahmad-sublabel">Animated AI Solar Assistant</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### ⚙️ System Parameters")
    st.markdown("Adjust parameters for your location & hardware setup:")

    peak_sun_hours = st.slider("Peak Sun Hours (hrs/day)", min_value=3.0, max_value=8.0, value=5.5, step=0.1)
    panel_wattage = st.selectbox("Solar Panel Rating (Watts)", [400, 540, 580, 600], index=2)
    system_voltage = st.selectbox("Battery Bank Voltage (V)", [12, 24, 48, 96], index=2)
    autonomy_days = st.slider("Backup Days (Autonomy)", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
    cable_length = st.number_input("Cable Length (Panel to Inverter, m)", min_value=5, max_value=150, value=20, step=5)


# --- TOP HEADER BANNER ---
st.markdown("""
    <div class="app-header-banner">
        <h1>☀️ SolarAI Power Systems Estimator</h1>
        <p>AI-Driven Load Calculation, Equipment Sizing & Cable Selection | Designed by <b>Engr. Bilal Mehmood</b></p>
    </div>
""", unsafe_allow_html=True)

# Create Tabs for Clean Navigation
tab_calculator, tab_visualization, tab_chat = st.tabs(["⚡ Load & Hardware Calculator", "📊 Visual Analytics", "🤖 Chat with Ahmad"])


# ==========================================
# TAB 1: CALCULATOR
# ==========================================
with tab_calculator:
    st.markdown("### 🔌 Step 1: Define Your Connected Load Profile")
    st.markdown("Add, edit, or adjust appliances below to compute exact daily energy consumption.")

    if "load_data" not in st.session_state:
        st.session_state.load_data = pd.DataFrame([
            {"Appliance": "LED Lights (5)", "Quantity": 5, "Watts Each": 12, "Hours Used/Day": 6},
            {"Appliance": "Inverter AC (1.5 Ton)", "Quantity": 1, "Watts Each": 1600, "Hours Used/Day": 7},
            {"Appliance": "Refrigerator (Medium)", "Quantity": 1, "Watts Each": 180, "Hours Used/Day": 14},
            {"Appliance": "Ceiling Fan", "Quantity": 4, "Watts Each": 75, "Hours Used/Day": 12},
            {"Appliance": "Laptop / Charger", "Quantity": 2, "Watts Each": 90, "Hours Used/Day": 5},
        ])

    edited_loads = st.data_editor(
        st.session_state.load_data, 
        num_rows="dynamic", 
        use_container_width=True, 
        key="load_editor"
    )
    st.session_state.load_data = edited_loads

    if not edited_loads.empty:
        df = edited_loads.copy()
        df["Quantity"] = pd.to_numeric(df["Quantity"]).fillna(0)
        df["Watts Each"] = pd.to_numeric(df["Watts Each"]).fillna(0)
        df["Hours Used/Day"] = pd.to_numeric(df["Hours Used/Day"]).fillna(0)

        df["Total Watts"] = df["Quantity"] * df["Watts Each"]
        df["Daily Watt-Hours"] = df["Total Watts"] * df["Hours Used/Day"]

        max_surge_load = df["Total Watts"].sum()
        total_daily_wh = df["Daily Watt-Hours"].sum()
        total_daily_kwh = total_daily_wh / 1000.0

        recommended_inverter_kw = (max_surge_load * 1.25) / 1000.0
        daily_generation_factor = peak_sun_hours * 0.80
        total_panel_watts_required = total_daily_wh / daily_generation_factor if daily_generation_factor > 0 else 0
        num_panels = int(np.ceil(total_panel_watts_required / panel_wattage))
        actual_installed_capacity_w = num_panels * panel_wattage

        dod = 0.80 if system_voltage >= 48 else 0.50
        total_battery_wh = (total_daily_wh * autonomy_days) / dod
        battery_amp_hours = total_battery_wh / system_voltage

        max_dc_current = actual_installed_capacity_w / system_voltage if system_voltage > 0 else 0
        
        if max_dc_current <= 12:
            cable_size = "4 mm² (AWG 12)"
            cable_type = "Standard PV Solar Cable"
        elif max_dc_current <= 25:
            cable_size = "6 mm² (AWG 10)"
            cable_type = "Standard PV Solar Cable"
        elif max_dc_current <= 45:
            cable_size = "10 mm² (AWG 8)"
            cable_type = "Heavy Duty PV Solar Cable"
        elif max_dc_current <= 70:
            cable_size = "16 mm² (AWG 6)"
            cable_type = "Extra Heavy Duty DC Cable"
        else:
            cable_size = "25 mm² or Twin-Core 16mm²"
            cable_type = "Specialized High-Current DC Cable"

        st.markdown("---")
        st.markdown("### 📌 Step 2: System Sizing & Hardware Output")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Connected Load", value=f"{max_surge_load:,.0f} W")
        with col2:
            st.metric(label="Daily Energy Used", value=f"{total_daily_kwh:.2f} kWh")
        with col3:
            st.metric(label="Solar Panels Required", value=f"{num_panels} Units", delta=f"{actual_installed_capacity_w/1000:.1f} kW Array")
        with col4:
            st.metric(label="Recommended Inverter", value=f"{max(1.0, recommended_inverter_kw):.1f} kW")

        st.markdown("### 🔋 Battery Bank & 🛠️ DC Wiring Recommendations")
        
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric(label="Battery Bank Capacity", value=f"{battery_amp_hours:.0f} Ah @ {system_voltage}V")
        with col6:
            st.metric(label="Estimated Max DC Current", value=f"{max_dc_current:.1f} A")
        with col7:
            st.success(f"**Recommended Cable Size:**  \n### {cable_size}  \nType: {cable_type} (Run: {cable_length}m)")

        st.markdown("---")
        
        # --- REPORT DOWNLOAD BUTTONS SECTION ---
        st.markdown("### 📥 Download Calculation Reports")
        rep_col1, rep_col2 = st.columns(2)

        docx_data = generate_docx_report(df, total_daily_kwh, num_panels, panel_wattage, recommended_inverter_kw, battery_amp_hours, system_voltage, cable_size, cable_length)
        pdf_data = generate_pdf_report(df, total_daily_kwh, num_panels, panel_wattage, recommended_inverter_kw, battery_amp_hours, system_voltage, cable_size, cable_length)

        with rep_col1:
            st.download_button(
                label="📄 Download Word Report (.docx)",
                data=docx_data,
                file_name="SolarAI_Calculation_Report.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )

        with rep_col2:
            st.download_button(
                label="📑 Download PDF Report (.pdf)",
                data=pdf_data,
                file_name="SolarAI_Calculation_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

# ==========================================
# TAB 2: VISUALIZATIONS
# ==========================================
with tab_visualization:
    st.markdown("### 📊 Energy Consumption & Load Breakdown")

    if not edited_loads.empty and "Total Watts" in df.columns:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### Daily Energy Consumption Breakdown (Wh)")
            fig_pie = px.pie(
                df, 
                names="Appliance", 
                values="Daily Watt-Hours",
                hole=0.45,
                color_discrete_sequence=px.colors.sequential.YlOrRd_r
            )
            fig_pie.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#111827", size=13),
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            st.markdown("#### Appliance Peak Power Draw (Watts)")
            fig_bar = px.bar(
                df,
                x="Appliance",
                y="Total Watts",
                color="Appliance",
                text="Total Watts",
                color_discrete_sequence=px.colors.sequential.Oranges_r
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#111827", size=13),
                showlegend=False, 
                margin=dict(t=20, b=20, l=20, r=20)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Please add appliances in the Load Calculator tab to view visual analytics.")

# ==========================================
# TAB 3: AHMAD CHATBOT ASSISTANT
# ==========================================
with tab_chat:
    st.markdown("### 🤖 Ask Ahmad — Your AI Solar Assistant")
    st.markdown(f"Inquire about your system requirements, panel configurations, battery chemistries, or why **{cable_size if 'cable_size' in locals() else 'certain cables'}** were recommended.")

    for message in st.session_state.messages:
        avatar = "👦" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Ahmad anything about solar power systems..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="👦"):
            with st.spinner("Ahmad is formulating recommendations..."):
                time.sleep(1)
                
                lower_prompt = prompt.lower()
                if "battery" in lower_prompt:
                    response = "For modern 48V solar configurations, **LiFePO4 (Lithium Iron Phosphate)** batteries are ideal. They offer up to 80% Depth of Discharge (DoD) and over 4,000 charge cycles compared to traditional lead-acid units!"
                elif "cable" in lower_prompt or "wire" in lower_prompt:
                    if 'cable_size' in locals():
                        response = f"I calculated **{cable_size}** for your system because your maximum array DC current is approximately **{max_dc_current:.1f} Amps**. Using stranded UV-resistant PV cable prevents excessive voltage drop and heat buildup over your {cable_length}m run."
                    else:
                        response = "Proper cable selection depends on maximum continuous DC current (Amps) and total cable length. Thicker copper conductors reduce losses and ensure electrical safety."
                elif "panel" in lower_prompt:
                    response = f"Using {panel_wattage}W high-efficiency panels, your load of {total_daily_kwh:.1f} kWh/day requires roughly **{num_panels} solar panels** to ensure stable daily generation."
                elif "cost" in lower_prompt or "price" in lower_prompt:
                    response = "System costs vary by brand and market conditions. Investing in Tier-1 solar panels, a reliable pure sine wave hybrid inverter, and lithium storage delivers the best long-term return on investment (ROI)."
                elif "hello" in lower_prompt or "hi" in lower_prompt:
                    response = "Hello! I am Ahmad! How can I assist you with your solar energy planning today?"
                else:
                    response = f"Regarding *'{prompt}'*, always ensure your inverter installation includes proper grounding/earthing and surge protection devices (SPD) on both AC and DC sides for optimal safety!"

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
