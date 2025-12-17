import streamlit as st
from fpdf import FPDF
import random

# ================= COMPANY VERIFICATION HELPERS =================

VERIFIED_COMPANIES = [
    "TATA CONSULTANCY SERVICES",
    "INFOSYS",
    "WIPRO",
    "HCL TECHNOLOGIES",
    "ACCENTURE",
    "COGNIZANT",
    "CAPGEMINI",
    "TATA MOTORS",
    "RELIANCE INDUSTRIES",
    "ICICI BANK",
    "HDFC BANK"
]

def normalize_company(name):
    return name.strip().upper()

def company_exists(company_name):
    return normalize_company(company_name) in VERIFIED_COMPANIES


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="LoanGenie Agentic AI",
    page_icon="🤖",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
body { background:#f5f7fb; }
.agent-card {
    background:white;
    border-radius:16px;
    padding:22px;
    margin-bottom:22px;
    border-left:6px solid #2563eb;
    box-shadow:0 10px 25px rgba(0,0,0,0.06);
}
.dashboard-card {
    background:white;
    border-radius:18px;
    padding:18px;
    text-align:center;
    box-shadow:0 8px 20px rgba(0,0,0,0.08);
}
.kpi { font-size:22px; font-weight:700; }
.kpi-label { font-size:13px; color:#64748b; }
.log-box {
    background:#020617;
    color:#e5e7eb;
    padding:18px;
    border-radius:14px;
    font-family:monospace;
}
</style>
""", unsafe_allow_html=True)

# ================= SESSION STATE =================
if "stage" not in st.session_state:
    st.session_state.stage = "start"
    st.session_state.data = {}
    st.session_state.logs = []

def log(agent, msg):
    st.session_state.logs.append(f"{agent}: {msg}")

# ================= SIDEBAR DASHBOARD =================
st.sidebar.markdown("## 🏦 LoanGenie AI")
st.sidebar.caption("Agentic Loan Processing Platform")
st.sidebar.markdown("---")

if st.session_state.data:
    d = st.session_state.data

    st.sidebar.markdown(f"""
    <div class="dashboard-card">
        <div class="kpi">₹ {d.get('loan_amount','--')}</div>
        <div class="kpi-label">Loan Amount</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
    <div class="dashboard-card">
        <div class="kpi">{d.get('credit_score','--')}</div>
        <div class="kpi-label">Credit Score</div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown(f"""
    <div class="dashboard-card">
        <div class="kpi">₹ {d.get('emi','--')}</div>
        <div class="kpi-label">EMI</div>
    </div>
    """, unsafe_allow_html=True)

# ================= MAIN HEADER =================
st.title("🤖 LoanGenie – Agentic AI Loan Assistant")
st.caption("With LoanGenie AI, we’re turning every chat into a loan opportunity — making banking faster, smarter, and truly human-like.")
st.divider()

# ================= MASTER AGENT =================
if st.session_state.stage == "start":
    log("Master Agent", "Journey started")
    with st.form("start_form"):
        start = st.form_submit_button("Start Loan Journey")
        if start:
            st.session_state.stage = "sales"
            st.rerun()

# ================= SALES AGENT =================
elif st.session_state.stage == "sales":
    log("Sales Agent", "Collecting loan details")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("## 💬 Sales Agent")
    st.caption("Collects customer intent and loan preferences")

    with st.form("sales_form"):
        loan_amount = st.number_input("Loan Amount (₹)", min_value=50000, step=50000)
        tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48])

        submit = st.form_submit_button("Proceed to Verification")
        if submit:
            st.session_state.data["loan_amount"] = loan_amount
            st.session_state.data["tenure"] = tenure
            st.session_state.stage = "verification"
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= VERIFICATION AGENT =================
elif st.session_state.stage == "verification":
    log("Verification Agent", "KYC in progress")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("## 🪪 Verification Agent")
    st.caption("Identity, KYC & employer verification")

    with st.form("kyc_form"):
        name = st.text_input("Full Name")
        aadhaar = st.text_input("Aadhaar (12 digits)", max_chars=12)
        phone = st.text_input("Mobile Number", max_chars=10)
        city = st.text_input("City")
        employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed"])
        company = st.text_input("Company / Organization Name")

        if company:
            if company_exists(company):
                st.success("✔ Company verified")
            else:
                st.warning("⚠ Company not found")

        verify = st.form_submit_button("Verify KYC")

        if verify:
            if len(aadhaar) != 12 or not aadhaar.isdigit():
                st.error("Invalid Aadhaar")
            elif len(phone) != 10 or not phone.isdigit():
                st.error("Invalid Mobile Number")
            elif not company_exists(company):
                st.error("Company not found in verified database")
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
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= UNDERWRITING AGENT =================
elif st.session_state.stage == "underwriting":
    log("Underwriting Agent", "Risk evaluation")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Underwriting Agent")
    st.caption("Income, credit score & EMI assessment")

    with st.form("underwriting_form"):
        income = st.number_input("Monthly Income (₹)", min_value=10000, step=5000)
        evaluate = st.form_submit_button("Evaluate Loan")

        if evaluate:
            credit_score = random.choice([720, 750, 780])
            loan = st.session_state.data["loan_amount"]
            tenure = st.session_state.data["tenure"]
            emi = int((loan * 1.12) / tenure)

            st.session_state.data.update({
                "income": income,
                "credit_score": credit_score,
                "emi": emi
            })

            if credit_score >= 700 and emi <= 0.5 * income:
                st.session_state.stage = "sanction"
            else:
                st.session_state.stage = "rejected"

            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= SANCTION AGENT =================
elif st.session_state.stage == "sanction":
    log("Sanction Agent", "Loan approved")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.success("🎉 Loan Approved")

    with st.form("sanction_form"):
        gen = st.form_submit_button("Generate Sanction Letter")
        if gen:
            d = st.session_state.data
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"""
TATA CAPITAL – PERSONAL LOAN SANCTION LETTER

Name: {d['name']}
Loan Amount: ₹{d['loan_amount']}
Tenure: {d['tenure']} months
EMI: ₹{d['emi']}
Credit Score: {d['credit_score']}

STATUS: APPROVED
""")
            pdf.output("sanction_letter.pdf")
            st.download_button("Download PDF", open("sanction_letter.pdf", "rb"))

    st.markdown('</div>', unsafe_allow_html=True)

# ================= REJECTION =================
elif st.session_state.stage == "rejected":
    log("Underwriting Agent", "Loan rejected")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.error("❌ Loan Rejected")
    st.caption("Eligibility criteria not met")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= AGENT LOGS =================
st.divider()
st.markdown("### 🧠 Agent Activity Log")
st.markdown('<div class="log-box">', unsafe_allow_html=True)
for l in st.session_state.logs[-10:]:
    st.write("•", l)
st.markdown('</div>', unsafe_allow_html=True)
