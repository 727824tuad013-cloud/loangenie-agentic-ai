import streamlit as st
from fpdf import FPDF
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="LoanGenie Agentic AI",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 LoanGenie – Agentic AI Loan Assistant")
st.caption("Master Agent orchestrating Sales, Verification, Underwriting & Sanction")

st.divider()

# ---------------- SESSION STATE ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.data = {}
    st.session_state.logs = []

def log(agent, msg):
    st.session_state.logs.append(f"**{agent}:** {msg}")

# ---------------- MASTER AGENT ----------------
if st.session_state.stage == "start":
    log("Master Agent", "Conversation started")
    st.write("### Welcome! I’ll help you get a personal loan in minutes.")
    if st.button("Start Loan Journey"):
        st.session_state.stage = "sales"

# ---------------- SALES AGENT ----------------
elif st.session_state.stage == "sales":
    log("Sales Agent", "Collecting loan requirements")
    st.write("### 💬 Sales Agent")

    loan_amount = st.number_input("Desired Loan Amount (₹)", min_value=50000, step=50000)
    tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48])

    if st.button("Proceed"):
        st.session_state.data["loan_amount"] = loan_amount
        st.session_state.data["tenure"] = tenure
        st.session_state.stage = "verification"

# ---------------- VERIFICATION AGENT ----------------
elif st.session_state.stage == "verification":
    log("Verification Agent", "Verifying KYC details")
    st.write("### 🪪 Verification Agent")

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    city = st.text_input("City")

    if st.button("Verify"):
        st.session_state.data.update({
            "name": name,
            "phone": phone,
            "city": city
        })
        st.session_state.stage = "underwriting"

# ---------------- UNDERWRITING AGENT ----------------
elif st.session_state.stage == "underwriting":
    log("Underwriting Agent", "Fetching credit score & evaluating eligibility")
    st.write("### 📊 Underwriting Agent")

    income = st.number_input("Monthly Income (₹)", min_value=0)
    credit_score = random.randint(650, 850)
    preapproved_limit = random.choice([200000, 300000, 400000])

    st.write(f"**Credit Score:** {credit_score}")
    st.write(f"**Pre-approved Limit:** ₹{preapproved_limit}")

    if st.button("Evaluate Loan"):
        st.session_state.data.update({
            "income": income,
            "credit_score": credit_score,
            "limit": preapproved_limit
        })

        loan = st.session_state.data["loan_amount"]

        if credit_score < 700:
            st.session_state.stage = "rejected"
        elif loan <= preapproved_limit:
            st.session_state.stage = "sanction"
        elif loan <= 2 * preapproved_limit and (loan / 24) <= 0.5 * income:
            st.session_state.stage = "sanction"
        else:
            st.session_state.stage = "rejected"

# ---------------- SANCTION LETTER AGENT ----------------
elif st.session_state.stage == "sanction":
    log("Sanction Agent", "Generating sanction letter")
    st.success("🎉 Loan Approved!")

    if st.button("Generate Sanction Letter"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, f"""
        TATA CAPITAL – PERSONAL LOAN SANCTION LETTER

        Name: {st.session_state.data['name']}
        City: {st.session_state.data['city']}
        Loan Amount: ₹{st.session_state.data['loan_amount']}
        Tenure: {st.session_state.data['tenure']} months
        Credit Score: {st.session_state.data['credit_score']}

        Status: APPROVED
        """)

        pdf.output("sanction_letter.pdf")

        st.download_button(
            "📄 Download Sanction Letter",
            open("sanction_letter.pdf", "rb"),
            file_name="sanction_letter.pdf"
        )

# ---------------- REJECTION ----------------
elif st.session_state.stage == "rejected":
    log("Underwriting Agent", "Loan rejected based on rules")
    st.error("❌ Loan Rejected")
    st.write("### Reason:")
    st.write("- Credit score too low OR")
    st.write("- Loan exceeds eligibility OR")
    st.write("- EMI exceeds 50% of income")

# ---------------- AGENT LOGS ----------------
st.divider()
st.write("### 🧠 Agent Activity Log")
for l in st.session_state.logs:
    st.markdown(l)
