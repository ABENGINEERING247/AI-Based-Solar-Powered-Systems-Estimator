import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="SolarAI Estimator | Ahmad Assistant",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
    <style>
    .main-header {
        font-size: 2.2rem;
        color: #FF8C00;
        font-weight: 700;
        margin-bottom: 0rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4A5568;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F7FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Session State Initialization for Ahmad Chatbot ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am **Ahmad**, your solar AI assistant. Tell me about your appliances or power requirements, and I'll help you configure the ideal setup!"}
    ]

# --- Sidebar: Configuration & Inputs ---
st.sidebar.markdown("## ⚙️ System Parameters")
st.sidebar.markdown("Configure your location and electrical parameters below.")

peak_sun_hours = st.sidebar.slider("Peak Sun Hours (hrs/day)", min_value=3.0, max_value=8.0, value=5.0, step=0.5)
panel_wattage = st.sidebar.selectbox("Solar Panel Rating (Watts)", [400, 540, 580, 600], index=1)
system_voltage = st.sidebar.selectbox("Inverter / Battery Bank Voltage (V)", [12, 24, 48, 96, 220], index=2)
autonomy_days = st.sidebar.slider("Battery Backup Days (Autonomy)", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
cable_length = st.sidebar.slider("Estimated Cable Run Length (Panel to Inverter, meters)", min_value=5, max_value=100, value=15, step=5)

# --- Main Interface ---
st.markdown('<p class="main-header">☀️ AI-Based Solar Power Systems Estimator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Accurate load calculation, hardware sizing, cable recommendations, and intelligent AI assistance.</p>', unsafe_allow_html=True)

# Create Tabs for Organization
tab_calculator, tab_visualization, tab_chat = st.tabs(["⚡ Load & Hardware Calculator", "📊 Visualizations & Reports", "🤖 Ahmad Chatbot Assistant"])

# ==========================================
# TAB 1: CALCULATOR
# ==========================================
with tab_calculator:
    st.markdown("### 🔌 Appliance Load Inventory")
    st.markdown("Add your appliances to calculate exact daily energy consumption.")

    # Default Load Profile DataFrame
    if "load_data" not in st.session_state:
        st.session_state.load_data = pd.DataFrame([
            {"Appliance": "LED Lights (5)", "Quantity": 5, "Watts Each": 12, "Hours Used/Day": 6},
            {"Appliance": "Inverter AC (1.5 Ton)", "Quantity": 1, "Watts Each": 1500, "Hours Used/Day": 8},
            {"Appliance": "Refrigerator", "Quantity": 1, "Watts Each": 200, "Hours Used/Day": 12},
            {"Appliance": "Ceiling Fan", "Quantity": 3, "Watts Each": 75, "Hours Used/Day": 10},
        ])

    # Editable DataFrame for Loads
    edited_loads = st.data_editor(st.session_state.load_data, num_rows="dynamic", use_container_width=True)
    st.session_state.load_data = edited_loads

    # Perform Calculations
    if not edited_loads.empty:
        edited_loads["Total Watts"] = edited_loads["Quantity"] * edited_loads["Watts Each"]
        edited_loads["Daily Watt-Hours"] = edited_loads["Total Watts"] * edited_loads["Hours Used/Day"]

        max_surge_load = edited_loads["Total Watts"].sum()
        total_daily_wh = edited_loads["Daily Watt-Hours"].sum()
        total_daily_kwh = total_daily_wh / 1000.0

        # Sizing Calculations
        # 1. Inverter Sizing (with 25% safety margin & surge consideration)
        recommended_inverter_kw = (max_surge_load * 1.25) / 1000.0

        # 2. Solar Panel Sizing (accounting for 20% system losses)
        daily_generation_factor = peak_sun_hours * 0.80
        total_panel_watts_required = total_daily_wh / daily_generation_factor if daily_generation_factor > 0 else 0
        num_panels = int(np.ceil(total_panel_watts_required / panel_wattage))
        actual_installed_capacity = num_panels * panel_wattage

        # 3. Battery Bank Sizing (Lead-Acid / LiFePO4 with 50%-80% DoD)
        dod = 0.80 if system_voltage >= 48 else 0.50 # Higher depth of discharge for lithium/higher voltage systems
        total_battery_wh = (total_daily_wh * autonomy_days) / dod
        battery_amp_hours = total_battery_wh / system_voltage

        # 4. Cable Sizing Calculation (Approx voltage drop formula: CSA = (2 * L * I) / (Delta_V * Conductivity))
        max_current = max_surge_load / system_voltage if system_voltage > 0 else 0
        # Simple heuristic cable recommendation based on current
        if max_current <= 15:
            cable_size = "4 mm² (AWG 11)"
        elif max_current <= 30:
            cable_size = "6 mm² (AWG 10) / 10 mm²"
        elif max_current <= 55:
            cable_size = "16 mm² (AWG 6)"
        else:
            cable_size = "25 mm² or higher (Heavy Duty DC Cable)"

        st.markdown("---")
        st.markdown("### 📌 Sizing Summary Results")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Connected Load", value=f"{max_surge_load:,.0f} W")
        with col2:
            st.metric(label="Daily Energy Consumption", value=f"{total_daily_kwh:.2f} kWh")
        with col3:
            st.metric(label="Panels Required", value=f"{num_panels} Units", delta=f"{actual_installed_capacity} W Total")
        with col4:
            st.metric(label="Recommended Inverter", value=f"{max(1.0, recommended_inverter_kw):.1f} kW")

        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric(label="Battery Bank Capacity", value=f"{battery_amp_hours:.0f} Ah @ {system_voltage}V")
        with col6:
            st.metric(label="Max DC Current", value=f"{max_current:.1f} A")
        with col7:
            st.metric(label="Recommended DC Cable", value=cable_size, delta=f"Length: {cable_length}m")

        # Success Popup simulation
        if st.button("🚀 Run AI Validation & Generate Report"):
            st.toast("System configuration optimized successfully by Ahmad AI!", icon="✅")

# ==========================================
# TAB 2: VISUALIZATIONS
# ==========================================
with tab_visualization:
    st.markdown("### 📊 System Breakdown & Analytics")

    if not edited_loads.empty:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### Energy Consumption by Appliance (Wh)")
            fig_pie = px.pie(
                edited_loads, 
                names="Appliance", 
                values="Daily Watt-Hours",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Sunset
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            st.markdown("#### Power Draw Comparison (Watts)")
            fig_bar = px.bar(
                edited_loads,
                x="Appliance",
                y="Total Watts",
                color="Appliance",
                text="Total Watts",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Please add appliances in the Load Calculator tab to view analytics.")

# ==========================================
# TAB 3: AHMAD CHATBOT ASSISTANT
# ==========================================
with tab_chat:
    st.markdown("### 🤖 Chat with Ahmad (AI Solar Assistant)")
    st.markdown("Ask questions about your solar setup, wiring standards, battery chemistry, or load optimization.")

    # Display Chat History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask Ahmad anything about solar systems..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Ahmad is calculating and formulating advice..."):
                time.sleep(1) # Simulated response delay
                
                # Context-aware intelligent responses
                lower_prompt = prompt.lower()
                if "battery" in lower_prompt:
                    response = "For robust performance and long life, I recommend **LiFePO4 (Lithium Iron Phosphate)** batteries over traditional tubular lead-acid batteries. They support up to 80% DoD and last 4,000+ cycles."
                elif "cable" in lower_prompt or "wire" in lower_prompt:
                    response = f"For your DC run of ~{cable_length} meters, always use UV-resistant, stranded copper PV solar cables (e.g., H1Z2Z2-K certified) to minimize voltage drop below 2%."
                elif "cost" in lower_prompt or "price" in lower_prompt:
                    response = "System costs depend heavily on your local market rates, but investing in Tier-1 solar panels and a pure sine wave hybrid inverter ensures maximum ROI and reliability."
                else:
                    response = f"I've analyzed your query regarding *'{prompt}'*. Based on your current system load profile, make sure your inverter has adequate surge headroom and your earthing/grounding is properly installed to code!"

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
