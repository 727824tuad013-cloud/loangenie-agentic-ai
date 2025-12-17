import streamlit as st
from fpdf import FPDF
import random

st.set_page_config(page_title="LoanGenie AI", page_icon="🤖")

st.title("🤖 LoanGenie AI")
st.subheader("Turning every chat into a loan opportunity")
st.divider()

if "stage" not in st.session_state:
    st.session_state.stage = 1
    st.session_state.data = {}

# ---------------- STAGE 1 ----------------
if st.session_state.stage == 1:
    with st.form("loan_form"):
        loan = st.selectbox("Loan Type", ["Personal Loan", "Home Loan", "Vehicle Loan"])
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.data["loan"] = loan
            st.session_state.stage = 2

# ---------------- STAGE 2 ----------------
elif st.session_state.stage == 2:
    with st.form("income_form"):
        income = st.number_input("Monthly Income (₹)", min_value=0)
        submitted = st.form_submit_button("Next")
        if submitted:
            st.session_state.data["income"] = income
            st.session_state.stage = 3

# ---------------- STAGE 3 ----------------
elif st.session_state.stage == 3:
    with st.form("city_form"):
        city = st.text_input("City")
        submitted = st.form_submit_button("Check Eligibility")
        if submitted:
            st.session_state.data["city"] = city
            st.session_state.stage = 4

# ---------------- STAGE 4 ----------------
elif st.session_state.stage == 4:
    credit_score = random.randint(600, 800)
    st.write(f"### Credit Score: **{credit_score}**")

    if credit_score >= 700 and st.session_state.data["income"] >= 25000:
        st.success("🎉 Loan Approved!")

        if st.button("Generate Sanction Letter"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, f"""
LOAN SANCTION LETTER

Loan Type: {st.session_state.data['loan']}
City: {st.session_state.data['city']}
Monthly Income: ₹{st.session_state.data['income']}
Credit Score: {credit_score}

Status: APPROVED
            """)
            pdf.output("sanction_letter.pdf")
            st.download_button("Download PDF", open("sanction_letter.pdf", "rb"))

    else:
        st.error("❌ Not Eligible")
        st.write("### Tips to Improve Eligibility")
        st.write("- Increase income")
        st.write("- Improve credit score")
        st.write("- Reduce existing EMIs")

