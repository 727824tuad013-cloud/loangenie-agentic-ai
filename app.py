import streamlit as st
from fpdf import FPDF
import random

# ================= MOCK VERIFIED COMPANY DATABASE =================
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


# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="LoanGenie Agentic AI",
    page_icon="🤖",
    layout="wide"
)

# ================= CSS =================
st.markdown("""
<style>
body {
    background: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.agent-card {
    background: linear-gradient(180deg, #ffffff, #f9fafc);
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 22px;
    border-left: 6px solid #2563eb;
    box-shadow: 0 10px 25px rgba(0,0,0,0.06);
}

.dashboard-card {
    background: white;
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
    text-align: center;
}

.kpi {
    font-size: 22px;
    font-weight: 700;
    color: #0f172a;
}

.kpi-label {
    font-size: 13px;
    color: #64748b;
}

.log-box {
    background: #020617;
    color: #e5e7eb;
    padding: 18px;
    border-radius: 14px;
    font-family: Consolas, monospace;
    font-size: 13px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
}

.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8);
    color: white;
    border-radius: 10px;
    height: 48px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(135deg, #1e40af, #1d4ed8);
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
st.sidebar.markdown("## 🏦 LoanGenie AI")
st.sidebar.caption("Agentic Loan Processing Platform")

st.sidebar.markdown("---")

if st.session_state.data:
    d = st.session_state.data

    st.sidebar.markdown("### 📊 Live Loan Metrics")

    st.sidebar.markdown(
        f"""
        <div class="dashboard-card">
            <div class="kpi">₹ {d.get('loan_amount','--')}</div>
            <div class="kpi-label">Loan Amount</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"""
        <div class="dashboard-card">
            <div class="kpi">{d.get('credit_score','--')}</div>
            <div class="kpi-label">Credit Score</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown(
        f"""
        <div class="dashboard-card">
            <div class="kpi">₹ {d.get('emi','--')}</div>
            <div class="kpi-label">Estimated EMI</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    status = "IN PROGRESS"
    if st.session_state.stage == "sanction":
        status = "APPROVED"
    elif st.session_state.stage == "rejected":
        status = "REJECTED"

    st.sidebar.success(f"Loan Status: {status}")

else:
    st.sidebar.info("No active loan journey")

# ================= MAIN UI =================
st.title("🤖 LoanGenie – Agentic AI Loan Assistant")
st.caption("“With LoanGenie AI, we’re turning every chat into a loan opportunity — making banking faster, smarter, and truly human-like.”")
st.divider()

# ================= MASTER AGENT =================
with st.form("start_form"):
    start = st.form_submit_button("Start Loan Journey")
    if start:
        st.session_state.stage = "sales"
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= SALES AGENT =================
elif st.session_state.stage == "sales":
    log("Sales Agent", "Collecting loan details")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("## 💬 Sales Agent")
    st.caption("Collects customer intent and loan preferences")

    loan_amount = st.number_input("Loan Amount (Rs.)", min_value=50000, step=50000)
    tenure = st.selectbox("Tenure (months)", [12, 24, 36, 48])

    with st.form("sales_form"):
    loan_amount = st.number_input("Loan Amount (Rs.)", min_value=50000, step=50000)
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
    log("Verification Agent", "Collecting KYC")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("## 🪪 Verification Agent")
    st.caption("Performs identity validation, KYC checks, and basic customer verification")

    with st.form("kyc_form"):
    name = st.text_input("Full Name (as per Aadhaar)")
    aadhaar = st.text_input("Aadhaar Number (12 digits)", max_chars=12)
    phone = st.text_input("Mobile Number", max_chars=10)
    city = st.text_input("City")
    employment = st.selectbox("Employment Type", ["Salaried", "Self-Employed"])
    company = st.text_input("Company / Business Name")

    verify = st.form_submit_button("Verify KYC")

    if verify:
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
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ================= UNDERWRITING AGENT =================
elif st.session_state.stage == "underwriting":
    log("Underwriting Agent", "Evaluating eligibility")
    st.markdown('<div class="agent-card">', unsafe_allow_html=True)
    st.markdown("## 📊 Underwriting Agent")
    st.caption("Evaluates eligibility using income, credit risk, and EMI affordability analysis")

    income = st.number_input("Monthly Income (Rs.)", min_value=10000, step=5000)

    credit_score = random.choice([720, 750, 780])
    preapproved_limit = 400000

    loan = st.session_state.data["loan_amount"]
    tenure = st.session_state.data["tenure"]
    emi = int(loan / tenure)

    st.write(f"Credit Score: {credit_score}")
    st.write(f"Pre-approved Limit: Rs. {preapproved_limit}")
    st.write(f"Estimated EMI: Rs. {emi}")

    with st.form("underwriting_form"):
    income = st.number_input("Monthly Income (Rs.)", min_value=10000, step=5000)
    evaluate = st.form_submit_button("Evaluate Loan")

    if evaluate:
        st.session_state.data["income"] = income

        if "credit_score" not in st.session_state.data:
            st.session_state.data["credit_score"] = random.choice([720, 750, 780])

        credit_score = st.session_state.data["credit_score"]
        loan = st.session_state.data["loan_amount"]
        tenure = st.session_state.data["tenure"]
        emi = int((loan * 1.12) / tenure)

        st.session_state.data["emi"] = emi

        if credit_score >= 700 and emi <= 0.5 * income:
            st.session_state.stage = "sanction"
        else:
            st.session_state.stage = "rejected"

        st.rerun()



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
    ...
    st.rerun()

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
    st.markdown("## 🚦 Advisory Agent")
    st.caption("Provides transparent rejection reasons and personalized eligibility improvement guidance")
    st.markdown('</div>', unsafe_allow_html=True)

# ================= AGENT LOGS =================
# ================= AGENT LOGS =================
st.divider()
st.write("### 🧠 Agent Activity Log")
st.markdown('<div class="log-box">', unsafe_allow_html=True)
for l in st.session_state.logs:
    st.write(l)
st.markdown('</div>', unsafe_allow_html=True)
