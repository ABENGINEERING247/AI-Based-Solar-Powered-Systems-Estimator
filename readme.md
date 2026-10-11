Here is the updated **`README.md`** featuring **Engr. Bilal Mehmood** credited as the Certified Generative and Agentic AI Application Developer.

---

# ☀️ SolarAI Estimator & Ahmad AI Assistant

An end-to-end, load-based **AI Solar Power System Sizing & Optimization Application** built using **Streamlit**.

This application allows homeowners, installers, and engineers to calculate precise solar hardware requirements—including solar panel arrays, hybrid inverters, battery bank capacity, and DC cable gauge selection—based on custom load profiles. It also includes an interactive AI assistant named **Ahmad** to answer questions and validate system configurations.

---

## 👨‍💻 Developer & Author

* **Developer:** **Engr. Bilal Mehmood**
* **Certification:** Certified Generative & Agentic AI Application Developer
* **Role:** Lead AI Architect & Application Developer

---

## 🌟 Key Features

* **⚡ Interactive Load Inventory:** Add, edit, or delete household appliances, surge power, and operating hours dynamically.
* **📐 Automated Hardware Sizing:**
* **Solar Panels:** Calculates required panel wattage and exact count based on location-specific Peak Sun Hours (PSH).
* **Inverter Sizing:** Recommends inverter capacity ($\text{kW}$) with safety margins and surge protection considerations.
* **Battery Bank Sizing:** Recommends battery capacity ($\text{Ah}$) based on system voltage and Depth of Discharge (DoD).
* **Cable Sizing & Gauge Selection:** Calculates maximum DC current and recommends suitable cable cross-sectional area ($\text{mm}^2$ / AWG) for given cable runs.


* **📊 Visual Analytics:** Interactive breakdown charts (powered by Plotly) displaying energy consumption and peak wattage per appliance.
* **🤖 Ahmad Chatbot Assistant:** Context-aware assistant to guide users through solar chemistry (LiFePO4 vs. Lead-Acid), wiring standards, and cost optimization.
* **🚀 Live Notifications & Validation:** Real-time popups (`st.toast`) upon running system optimization checks.

---

## 🚀 Quick Start Guide

### 1. Prerequisites

Ensure you have **Python 3.8+** installed on your system.

### 2. Installation

Clone or download the repository, then navigate to your project folder:

```bash
cd solar-ai-estimator

```

Install the required Python dependencies:

```bash
pip install streamlit pandas numpy plotly

```

### 3. Running the App

Launch the Streamlit web application:

```bash
streamlit run app.py

```

The application will automatically open in your default browser at `http://localhost:8501`.

---

## 🛠 Project Structure

```text
solar-ai-estimator/
│
├── app.py              # Main Streamlit Application (UI, Logic, Charts & Chatbot)
├── README.md           # Project Documentation
└── requirements.txt    # Python Dependencies

```

---

## 📦 `requirements.txt`

If you are deploying this app (e.g., to Streamlit Community Cloud or Heroku), include a `requirements.txt` file with:

```text
streamlit>=1.30.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0

```

---

## ⚙️ How It Works (Calculation Logic)

1. **Daily Energy Consumption:**

$$\text{Daily Energy (Wh)} = \sum (\text{Quantity} \times \text{Wattage} \times \text{Hours Used})$$


2. **Solar Array Sizing:**

$$\text{Panel Capacity Needed (W)} = \frac{\text{Daily Energy (Wh)}}{\text{Peak Sun Hours} \times 0.80 \text{ (System Efficiency)}}$$


3. **Inverter Capacity:**

$$\text{Inverter Size (kW)} = \frac{\text{Total Connected Peak Load (W)} \times 1.25 \text{ (Safety Margin)}}{1000}$$


4. **Battery Capacity:**

$$\text{Battery Capacity (Ah)} = \frac{\text{Daily Energy (Wh)} \times \text{Autonomy Days}}{\text{System Voltage (V)} \times \text{DoD (Depth of Discharge)}}$$



---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to fork the repository and submit a pull request.
