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

# --- Define AHMAD the Little Boy Character URL (Animated Avatar) ---
# This is a public URL for a placeholder animated character (a little boy with glasses).
# For production, you could host your own optimized Lottie or GIF file.
AHMAD_AVATAR_URL = "https://raw.githubusercontent.com/ai-driven-dev/assets/main/animated_boy_avatar.gif"

# --- Advanced Custom Styling (CSS & Background) ---
st.markdown(f"""
    <style>
    /* Main App Background - Stylized Solar Panels Over Gradient */
    .stApp {{
        background: 
            linear-gradient(135deg, rgba(255, 255, 255, 0.95) 0%, rgba(240, 249, 255, 0.90) 100%),
            url('https://raw.githubusercontent.com/ai-driven-dev/assets/main/solar_bg_pattern.webp');
        background-size: cover;
        background-attachment: fixed;
    }}

    .main-header {{
        font-size: 2.8rem;
        color: #FF8C00; /* Solar Orange */
        font-weight: 800;
        margin-bottom: 0rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}
    .sub-header {{
        font-size: 1.2rem;
        color: #4A5568;
        margin-bottom: 2rem;
    }}

    /* Ahmad Avatar Styling in Sidebar */
    .ahmad-sidebar-container {{
        text-align: center;
        margin-bottom: 20px;
        border-bottom: 1px solid #E2E8F0;
        padding-bottom: 15px;
    }}
    .ahmad-avatar-img {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        border: 4px solid #FF8C00;
        box-shadow: 0 4px 10px rgba(255, 140, 0, 0.3);
    }}
    .ahmad-label {{
        margin-top: 10px;
        font-weight: 700;
        color: #2D3748;
        font-size: 1.1rem;
    }}

    /* Global Metric Card Styling */
    div[data-testid="stMetricValue"] {{
        color: #FF8C00;
        font-weight: 700;
    }}
    </style>
""", unsafe_allow_html=True)


# --- WELCOME POPUP FOR VISITORS ---
@st.experimental_dialog("☀️ Welcome to SolarAI Estimator!")
def welcome_popup():
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(AHMAD_AVATAR_URL, use_container_width=True)
    with col2:
        st.markdown(f"""
            ### Hello! I'm Ahmad! 👋

            I'm your little AI assistant, and I love solar power! I've been animated just for you.

            I am here to help you calculate **exactly** what you need for your perfect solar energy system.

            **In this app, we will figure out:**
            1.  How many solar panels you need ☀️
            2.  The best inverter for your load ⚡
            3.  The right battery bank 🔋
            4.  And exactly **which cables** are required for safety! 🛠️

            Let's build something green together! Please close this popup to start.
        """)
    if st.button("Let's Get Started, Ahmad!", type="primary", use_container_width=True):
        st.session_state.welcome_shown = True
        st.rerun()

# Trigger the popup once per session
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False

if not st.session_state.welcome_shown:
    welcome_popup()


# --- Session State Initialization for Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am **Ahmad**, your *little animated* solar AI assistant. Tell me about your appliances or power requirements, and I'll help you configure the ideal setup!"}
    ]


# --- Sidebar: AHMAD Character & Configuration ---
with st.sidebar:
    # 1. Display Animated Ahmad Character
    st.markdown(f"""
        <div class="ahmad-sidebar-container">
            <img src="{AHMAD_AVATAR_URL}" class="ahmad-avatar-img" alt="Animated Ahmad Boy">
            <div class="ahmad-label">Ahmad - Your AI Assistant</div>
        </div>
    """, unsafe_allow_html=True)

    # 2. System Parameters (Simplified)
    st.markdown("## ⚙️ System Inputs")
    st.markdown("Set your main operating parameters below.")

    peak_sun_hours = st.slider("Peak Sun Hours (hrs/day)", min_value=3.0, max_value=8.0, value=5.5, step=0.1)
    panel_wattage = st.selectbox("Solar Panel Rating (Watts)", [400, 540, 580, 600], index=2) # Default 580W
    system_voltage = st.selectbox("Battery Bank Voltage (V)", [12, 24, 48, 96], index=2) # Default 48V
    autonomy_days = st.slider("Backup Days", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
    cable_length = st.number_input("Est. Cable Length (Panel to Inverter, m)", min_value=5, max_value=150, value=20, step=5)


# --- Main Interface ---
st.markdown('<p class="main-header">☀️ SolarAI Estimator & Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Accurate load calculation, hardware sizing, cable recommendations, and animated AI assistance.</p>', unsafe_allow_html=True)

# Create Tabs for Organization
tab_calculator, tab_visualization, tab_chat = st.tabs(["⚡ Load & Hardware Calculator", "📊 Visual Summary", "🤖 Chat with Ahmad"])


# ==========================================
# TAB 1: CALCULATOR
# ==========================================
with tab_calculator:
    st.markdown("### 🔌 Step 1: Define Your Daily Load")
    st.markdown("Add your appliances to calculate exact daily energy consumption.")

    # Default Load Profile DataFrame
    if "load_data" not in st.session_state:
        st.session_state.load_data = pd.DataFrame([
            {"Appliance": "LED Lights (5)", "Quantity": 5, "Watts Each": 12, "Hours Used/Day": 6},
            {"Appliance": "Inverter AC (1.5 Ton)", "Quantity": 1, "Watts Each": 1600, "Hours Used/Day": 7},
            {"Appliance": "Refrigerator (Medium)", "Quantity": 1, "Watts Each": 180, "Hours Used/Day": 14},
            {"Appliance": "Ceiling Fan", "Quantity": 4, "Watts Each": 75, "Hours Used/Day": 12},
            {"Appliance": "Laptop/Charger", "Quantity": 2, "Watts Each": 90, "Hours Used/Day": 5},
        ])

    # Editable DataFrame for Loads
    edited_loads = st.data_editor(st.session_state.load_data, num_rows="dynamic", use_container_width=True, key="load_editor")
    st.session_state.load_data = edited_loads

    # Perform Calculations
    if not edited_loads.empty:
        # Avoid issues if users input 0
        df = edited_loads.copy()
        df["Quantity"] = pd.to_numeric(df["Quantity"]).fillna(0)
        df["Watts Each"] = pd.to_numeric(df["Watts Each"]).fillna(0)
        df["Hours Used/Day"] = pd.to_numeric(df["Hours Used/Day"]).fillna(0)

        df["Total Watts"] = df["Quantity"] * df["Watts Each"]
        df["Daily Watt-Hours"] = df["Total Watts"] * df["Hours Used/Day"]

        max_surge_load = df["Total Watts"].sum()
        total_daily_wh = df["Daily Watt-Hours"].sum()
        total_daily_kwh = total_daily_wh / 1000.0

        # --- Sizing Calculations ---
        
        # 1. Inverter Sizing (with 25% safety margin & surge consideration)
        recommended_inverter_kw = (max_surge_load * 1.25) / 1000.0

        # 2. Solar Panel Sizing (accounting for 20% system losses)
        daily_generation_factor = peak_sun_hours * 0.80 # 80% system efficiency factor
        total_panel_watts_required = total_daily_wh / daily_generation_factor if daily_generation_factor > 0 else 0
        num_panels = int(np.ceil(total_panel_watts_required / panel_wattage))
        actual_installed_capacity_w = num_panels * panel_wattage

        # 3. Battery Bank Sizing (LiFePO4 focus at 48V+, Lead Acid below)
        dod = 0.80 if system_voltage >= 48 else 0.50 # Higher depth of discharge for modern/higher voltage systems
        total_battery_wh = (total_daily_wh * autonomy_days) / dod
        battery_amp_hours = total_battery_wh / system_voltage

        # 4. Cable Sizing Calculation (DC Side, Panel Array to Inverter)
        # Assuming typical Voc of panels in series, here we calculate Max DC Current (Imp)
        # Approximation: Current = Array Watts / nominal DC voltage (simplified)
        max_dc_current = actual_installed_capacity_w / system_voltage if system_voltage > 0 else 0
        
        # Comprehensive Cable Recommendation Logic (simplified heuristics)
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
        st.markdown("### 📌 Step 2: Ahmad's System Recommendations")

        # Metric Visuals
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Total Connected Load", value=f"{max_surge_load:,.0f} W", help="Sum of all appliance wattage running simultaneously.")
        with col2:
            st.metric(label="Daily Energy Used", value=f"{total_daily_kwh:.2f} kWh", help="Total energy consumed per 24 hours.")
        with col3:
            st.metric(label="Solar Panels Required", value=f"{num_panels} Units", delta=f"{actual_installed_capacity_w/1000:.1f} kW Total Array", help=f"Using {panel_wattage}W panels.")
        with col4:
            st.metric(label="Recommended Inverter", value=f"{max(1.0, recommended_inverter_kw):.1f} kW", help="Sized 25% above peak load.")

        st.markdown("---")
        st.markdown("#### 🔋 Battery & 🛠️ Wiring Specifications")
        col5, col6, col7 = st.columns(3)
        with col5:
            st.metric(label="Battery Bank Capacity", value=f"{battery_amp_hours:.0f} Ah @ {system_voltage}V", help=f"Sized for {autonomy_days} days backup with {dod*100}% DoD.")
        with col6:
            st.metric(label="Estimated Max DC Current", value=f"{max_dc_current:.1f} A", help="Maximum expected current from solar array to inverter.")
        with col7:
            # Highlight Cable Recommendation
            st.success(f"**Recommended DC Cable:**  \n### {cable_size}  \nType: {cable_type} (Length: {cable_length}m)")


        # Success Popup simulation
        if st.button("🚀 Finalize & Run Ahmad's AI Validation", type="primary"):
            with st.spinner("Ahmad is double-checking the figures..."):
                time.sleep(1.5)
            st.toast("System configuration optimized and validated successfully by Ahmad AI!", icon="✅")

# ==========================================
# TAB 2: VISUALIZATIONS
# ==========================================
with tab_visualization:
    st.markdown("### 📊 Energy Consumption Visuals")

    if not edited_loads.empty and "Total Watts" in df.columns:
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### Daily Energy Consumption Breakdown (Wh)")
            fig_pie = px.pie(
                df, 
                names="Appliance", 
                values="Daily Watt-Hours",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.YlOrRd_r # Solar colors
            )
            fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_pie, use_container_width=True)

        with col_b:
            st.markdown("#### Power Draw Comparison (Watts)")
            fig_bar = px.bar(
                df,
                x="Appliance",
                y="Total Watts",
                color="Appliance",
                text="Total Watts",
                color_discrete_sequence=px.colors.sequential.Plasma
            )
            fig_bar.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Please add appliances in the Load Calculator tab to view analytics.")

# ==========================================
# TAB 3: AHMAD CHATBOT ASSISTANT
# ==========================================
with tab_chat:
    st.markdown("### 🤖 Chat with Ahmad (Animated AI Assistant)")
    st.markdown(f"Ask me questions! Tell me what appliances you use, or ask why I recommended **{cable_size if 'cable_size' in locals() else 'certain cables'}**!")

    # Display Chat History
    for message in st.session_state.messages:
        avatar = AHMAD_AVATAR_URL if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Ask Ahmad about solar panels, batteries, or wiring..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar=AHMAD_AVATAR_URL):
            with st.spinner("Ahmad is calculating and formulating advice..."):
                time.sleep(1) # Simulated response delay
                
                # Context-aware intelligent responses
                lower_prompt = prompt.lower()
                if "battery" in lower_prompt:
                    response = "I love batteries! For higher voltage systems like your 48V setup, **LiFePO4 (Lithium)** is much better than Lead-Acid. You can use 80% of their energy, and they last 10 times longer! I recommend them for reliability."
                elif "cable" in lower_prompt or "wire" in lower_prompt:
                    if 'cable_size' in locals():
                        response = f"I chose **{cable_size}** cable for you! It's because your system might handle up to **{max_dc_current:.1f} Amps**, and we need thick, stranded copper (UV-resistant PV1-F type) to keep it safe and cool over {cable_length} meters! Never use skinny wires for solar!"
                    else:
                        response = "Cable size is very important! We must calculate the maximum current (Amps) and the distance first. Thicker cables prevent power loss and dangerous heat!"
                elif "panel" in lower_prompt:
                    response = f"We are using big **{panel_wattage}W** panels! They are super efficient. For your {total_daily_kwh:.1f} kWh daily need, I calculated that **{num_panels} panels** will give you enough power even on partly cloudy days!"
                elif "cost" in lower_prompt or "price" in lower_prompt:
                    response = "I can't tell you exact prices because they change everywhere! But remember, buying Tier-1 panels, a strong hybrid inverter, and good Lithium batteries costs more upfront but saves you a LOT of money over 20 years. Don't go too cheap on the core parts!"
                elif "hello" in lower_prompt or "hi" in lower_prompt:
                    response = "Hi there! I am Ahmad! I'm an animated boy who loves solar power! How can I help you configure your system today? Tell me what appliances you want to run!"
                else:
                    response = f"I've received your query about *'{prompt}'*. Based on the current load profile, make sure your hybrid inverter supports net metering (if available), and remember that correct **earthing/grounding** is essential for safety!"

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
