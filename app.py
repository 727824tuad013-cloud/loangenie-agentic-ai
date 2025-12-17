import streamlit as st
from fpdf import FPDF
import random

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="LoanGenie Agentic AI",
    page_icon="🤖",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
body { background-color: #f4f6fa; }
.agent-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}
.dashboard-card {
    background: white;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.08);
    text-align: center;
}
.log-box {
    background: #0f172a;
    color: #e5e7eb;
    padding: 15px;
    border-radius: 10px;
    font-family: monospace;
}
.stButton>button {
    background: linear-gradient(135deg, #0052cc, #007bff);
    color: white;
    border-radius: 8px;
    height: 45px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.data = {}
    st.session_state.logs = []
    st.session_state.evaluate_clicked = False

def log(agent, msg):
    st.session_state.logs.append(f"{agent}: {msg}")

# ================= DASHBOARD =================
st.sidebar.title("📊 Loan Dashboard")

if st.session_state.data:
    d = st.session_state.data

    col1, col2 = st.sidebar.columns(2)
    col1.metric("Loan Amount", f"Rs. {d.get('loan_amount','--')}")
    col2.metric("EMI", f"Rs. {d.get('emi','--')}")

    col3, col4 = st.sidebar.columns(2)
    col3.metric("Credit Score", d.get("credit_score", "--"))
    col4.metric("Income", f"Rs. {d.get('income','--')}")

    status = "IN PROGRESS"
    if st.session_state.stage == "sanction":
        status = "APPROVED"
    elif st.session_state.stage == "rejected":
        status = "REJECTED"

    st.sidebar.markdown("---")
    st.sidebar.metric("Loan Status", status)

    if d.get("credit_score", 0) >= 750:
        st.sidebar.success("🟢 Low Risk Customer")
    elif d.get("credit_score", 0) >= 700:
        st.sidebar.warning("🟡 Medium Risk Customer")
    else:
        st.sidebar.error("🔴 High Risk Customer")

else:
    st.sidebar.info("No active loan journey")

# ================= MAIN UI =================
st.title("🤖 LoanGenie – Agentic AI Loan Assistant")
st.caption("Master Agent orchestrating Sales, Verification, Underwriting & Sanction")
st.divider()

# ================= MASTER AGENT =================
if st.session_state.stage == "start":
    log("Master Agent", "Conversation started")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.write("### Welcome! Get your personal loan approved in minutes.")
    if st.button("Start Loan Journey"):
        st.session_state.stage = "sales"
    st.markdown('</div>', unsafe_allow_html=True)

# ================= SALES AGENT =================
elif st.session_state.stage == "sales":
    log("Sales Agent", "Collecting loan details")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.write("### 💬 Sales Agent")

    loan_amount = st.number_input("Loan Amount (Rs.)", min_value=50000, step=50000)
    tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48])

    if st.button("Proceed to Verification"):
        st.session_state.data["loan_amount"] = loan_amount
        st.session_state.data["tenure"] = tenure
        st.session_state.stage = "verification"
    st.markdown('</div>', unsafe_allow_html=True)

# ================= VERIFICATION AGENT =================
elif st.session_state.stage == "verification":
    log("Verification Agent", "Collecting KYC")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.write("### 🪪 Verification Agent")

    name = st.text_input("Full Name (as per Aadhaar)")
    aadhaar = st.text_input("Aadhaar Number (12 digits)", max_chars=12)
    phone = st.text_input("Mobile Number", max_chars=10)
    city = st.text_input("City")
    employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed"])
    company = st.text_input("Company / Business Name")

    if st.button("Verify KYC"):
        if len(aadhaar) != 12 or not aadhaar.isdigit():
            st.error("Invalid Aadhaar number")
        elif len(phone) != 10 or not phone.isdigit():
            st.error("Invalid mobile number")
        else:
            st.session_state.data.update({
                "name": name,
                "aadhaar": aadhaar,
                "phone": phone,
                "city": city,
                "employment": employment,
                "company": company
            })
            st.session_state.stage = "underwriting"
    st.markdown('</div>', unsafe_allow_html=True)

# ================= UNDERWRITING AGENT =================
elif st.session_state.stage == "underwriting":
    log("Underwriting Agent", "Evaluating eligibility")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.write("### 📊 Underwriting Agent")

    income = st.number_input("Monthly Income (Rs.)", min_value=10000, step=5000)

    credit_score = random.choice([720, 750, 780])
    preapproved_limit = 400000

    loan = st.session_state.data["loan_amount"]
    tenure = st.session_state.data["tenure"]
    emi = int(loan / tenure)

    st.write(f"Credit Score: {credit_score}")
    st.write(f"Pre-approved Limit: Rs. {preapproved_limit}")
    st.write(f"Estimated EMI: Rs. {emi}")

    if st.button("Evaluate Loan"):
        st.session_state.evaluate_clicked = True

    if st.session_state.evaluate_clicked:
        st.session_state.evaluate_clicked = False

        st.session_state.data.update({
            "income": income,
            "credit_score": credit_score,
            "emi": emi
        })

        if credit_score >= 700 and emi <= 0.5 * income:
            st.session_state.stage = "sanction"
        else:
            st.session_state.stage = "rejected"

    st.markdown('</div>', unsafe_allow_html=True)

# ================= SANCTION AGENT =================
elif st.session_state.stage == "sanction":
    log("Sanction Agent", "Loan approved")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.success("🎉 Loan Approved!")

    if st.button("Generate Sanction Letter"):
        d = st.session_state.data

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, f"""
TATA CAPITAL - PERSONAL LOAN SANCTION LETTER

Name: {d['name']}
Aadhaar: {d['aadhaar']}
City: {d['city']}
Employment: {d['employment']}

Loan Amount: Rs. {d['loan_amount']}
Tenure: {d['tenure']} months
EMI: Rs. {d['emi']}
Credit Score: {d['credit_score']}

Status: APPROVED
        """)

        pdf.output("sanction_letter.pdf")

        st.download_button(
            "Download Sanction Letter (PDF)",
            open("sanction_letter.pdf", "rb"),
            file_name="sanction_letter.pdf"
        )
    st.markdown('</div>', unsafe_allow_html=True)

# ================= REJECTION =================
elif st.session_state.stage == "rejected":
    log("Underwriting Agent", "Loan rejected")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.error("❌ Loan Rejected")
    st.write("Reason: Eligibility or EMI criteria not met")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= AGENT LOGS =================
st.divider()
st.write("### 🧠 Agent Activity Log")
st.markdown('<div class="log-box">', unsafe_allow_html=True)
for l in st.session_state.logs:
    st.write(l)
st.markdown('</div>', unsafe_allow_html=True)

