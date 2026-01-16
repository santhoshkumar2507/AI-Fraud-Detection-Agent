import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

st.set_page_config(page_title="AI Fraud Detection Agent", layout="wide")

st.title("💳 AI Fraud Detection Agent")
st.caption("Agentic AI system for real-time fraud, suspicious and normal transaction detection")


MAX_TRANSACTION_LIMIT = 80000
DAILY_TRANSACTION_LIMIT = 150000
KNOWN_LOCATIONS = ["chennai", "coimbatore", "bangalore", "hyderabad"]
SAFE_TIME_START = 6
SAFE_TIME_END = 22


if "agent_log" not in st.session_state:
    st.session_state.agent_log = []


uploaded_file = st.file_uploader("📂 Upload Transaction CSV", type=["csv"])

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("CSV Loaded Successfully. System Activated.")

 
    user_memory = data.groupby("user_id")["amount"].mean().to_dict()

 
    def detect_fraud(row):
        reasons = []
        risk = 0

        user_avg = user_memory[row["user_id"]]
        amount = row["amount"]
        location = row["location"].lower()
        hour = int(row["time"].split(":")[0])

       
        if amount >= MAX_TRANSACTION_LIMIT:
            return "FRAUD", ["Transaction exceeds ₹80,000 limit"], 100

        
        user_day_total = data[data["user_id"] == row["user_id"]]["amount"].sum()
        if user_day_total > DAILY_TRANSACTION_LIMIT:
            return "FRAUD", ["Daily transaction limit exceeded"], 100

        if amount > 3 * user_avg:
            risk += 35
            reasons.append("Unusual amount for this user")

        if hour < SAFE_TIME_START or hour > SAFE_TIME_END:
            risk += 25
            reasons.append("Transaction at unusual time")

        if location not in KNOWN_LOCATIONS:
            risk += 30
            reasons.append("Transaction from unknown location")

        if risk >= 70:
            status = "FRAUD"
        elif risk >= 40:
            status = "SUSPICIOUS"
        else:
            status = "NORMAL"

        if not reasons:
            reasons.append("No suspicious activity")

        return status, reasons, risk

  
    results = []
    for _, row in data.iterrows():
        status, reasons, risk = detect_fraud(row)

        st.session_state.agent_log.append({
            "Time": datetime.now().strftime("%H:%M:%S"),
            "User": row["user_id"],
            "Status": status,
            "Action": "Blocked & Alerted" if status == "FRAUD" else "Verification" if status == "SUSPICIOUS" else "No Action"
        })

        results.append({
            "User ID": row["user_id"],
            "Amount": row["amount"],
            "Time": row["time"],
            "Location": row["location"],
            "Merchant": row["merchant"],
            "Category": row["category"],
            "Status": status,
            "Risk Score": risk,
            "Reasons": ", ".join(reasons)
        })

    df = pd.DataFrame(results)

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 Live Detection",
        "📊 Analytics",
        "🧠 Agent Memory",
        "📥 Data & Report",
        "🚨 Agent Log",
        "🧪 Simulation"
    ])

   
    with tab1:
        st.subheader("Live Fraud Detection")
        for _, row in df.iterrows():
            st.write(f"User {row['User ID']} | ₹{row['Amount']} | {row['Location']}")
            st.progress(min(row["Risk Score"] / 100, 1.0))

            if row["Status"] == "FRAUD":
                st.error("🚨 FRAUD")
                st.warning("📩 SMS Sent | 🚫 Card Blocked")
            elif row["Status"] == "SUSPICIOUS":
                st.warning("⚠ SUSPICIOUS – OTP Verification Sent")
            else:
                st.success("✅ NORMAL")

            st.write("Reason:", row["Reasons"])
            st.divider()

   
    with tab2:
        st.subheader("Analytics")
        counts = df["Status"].value_counts()
        fig, ax = plt.subplots()
        ax.bar(counts.index, counts.values)
        st.pyplot(fig)

   
    with tab3:
        st.subheader("Agent Memory")
        mem_df = pd.DataFrame({
            "User ID": user_memory.keys(),
            "Average Spend": user_memory.values()
        })
        st.dataframe(mem_df)

 
    with tab4:
        st.subheader("Download Report")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download Fraud Report", csv, "fraud_report.csv", "text/csv")


    with tab5:
        st.subheader("Agent Activity Log")
        log_df = pd.DataFrame(st.session_state.agent_log)
        st.dataframe(log_df)


    with tab6:
        st.subheader("Transaction Simulation")

        uid = st.number_input("User ID", min_value=1, step=1)
        amt = st.number_input("Amount", min_value=1)
        tme = st.text_input("Time (HH:MM)", "12:00")
        loc = st.text_input("Location", "chennai")

        if st.button("Simulate Transaction"):
            fake = {
                "user_id": uid,
                "amount": amt,
                "time": tme,
                "location": loc,
                "merchant": "SIMULATED",
                "category": "SIMULATED"
            }
            status, reasons, risk = detect_fraud(fake)

            st.write("Status:", status)
            st.write("Risk Score:", risk)
            st.write("Reasons:", reasons)

else:
    st.info("Upload CSV to activate the system.")


