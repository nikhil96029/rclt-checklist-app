import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from fpdf import FPDF
import tempfile
import os

# Define test packages
packages = {
    "RCLT Pre-employment Package 12": [
        "Complete Hemogram",
        "URINE ROUTINE & MICROSCOPIC",
        "Fasting Blood Sugar",
        "Kidney (2 Tests)",
        "Liver (1 Tests)",
        "ECG",
        "X-ray Chest",
        "Fitness Summary By Medical Officer"
    ],
    "RCLT Pre-employment Package 13": [
        "Complete Hemogram",
        "URINE ROUTINE & MICROSCOPIC",
        "Fasting Blood Sugar",
        "Hba1c",
        "Kidney (2 Tests)",
        "Liver (1 Tests)",
        "Lipid Profile (9 Tests)",
        "ECG",
        "X-ray Chest",
        "Fitness Summary By Medical Officer"
    ],
    "RCLT Pre-employment Package 14": [
        "Complete Hemogram",
        "URINE ROUTINE & MICROSCOPIC",
        "Fasting Blood Sugar",
        "Hba1c",
        "Kidney (6 Tests)",
        "Liver (1 Tests)",
        "Lipid Profile (9 Tests)",
        "ECG",
        "X-ray Chest",
        "Fitness Summary By Medical Officer"
    ]
}

# Streamlit UI setup
st.set_page_config(page_title="PDF Checklist Tool", layout="centered")
st.title("🧪 PDF + Test Checklist Merger")
st.markdown("📄 Please upload a test report PDF to begin.")

# Upload the original PDF
uploaded_pdf = st.file_uploader("Upload Test Report PDF", type="pdf")

if uploaded_pdf:
    selected_package = st.selectbox("Choose a Package", list(packages.keys()))
    selected_tests = st.multiselect("Select Tests", packages[selected_package])

    if st.button("Generate Final PDF"):
        # Save uploaded PDF temporarily
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        temp_input.write(uploaded_pdf.read())
        temp_input.close()

        # Create checklist page
        checklist = FPDF()
        checklist.add_page()
        checklist.set_font("Arial", "B", 14)
        checklist.cell(0, 10, f"Package Name - {selected_package}", ln=True)

        # Table headers
        checklist.set_fill_color(173, 216, 230)  # Light blue
        checklist.set_font("Arial", "B", 12)
        checklist.cell(95, 10, selected_package, border=1, fill=True)
        checklist.cell(95, 10, "Status", border=1, fill=True)
        checklist.ln()

        # Table content
        checklist.set_font("Arial", "", 12)
        for test in packages[selected_package]:
            checklist.cell(95, 10, test, border=1)
            checkbox = "Done" if test in selected_tests else "Pending"
            checklist.cell(95, 10, checkbox, border=1)
            checklist.ln()

        # Save checklist PDF
        checklist_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        checklist.output(checklist_path)

        # Merge original PDF with checklist
        pdf_writer = PdfWriter()
        pdf_reader = PdfReader(temp_input.name)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        checklist_reader = PdfReader(checklist_path)
        for page in checklist_reader.pages:
            pdf_writer.add_page(page)

        # Save final merged PDF
        final_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
        with open(final_path, "wb") as f:
            pdf_writer.write(f)

        # Show download button
        with open(final_path, "rb") as f:
            st.download_button("📥 Download Final PDF", f, file_name="final_report_with_checklist.pdf")

else:
    st.info("👈 Please upload a PDF to get started.")
