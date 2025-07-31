

# import streamlit as st
# import pdfplumber
# import google.generativeai as genai

# # ✅ Set your Gemini API key here
# genai.configure(api_key="AIzaSyADGV44iVUAvaX7uJgrEqG9qnx-QL25VtM")  # Replace with your actual key

# # ✅ Load the Gemini model correctly
# model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")  # Use this or 'models/gemini-1.5-pro'

# # ✅ Extract text from PDF using pdfplumber
# def extract_text_from_pdf(file):
#     text = ""
#     with pdfplumber.open(file) as pdf:
#         for page in pdf.pages:
#             page_text = page.extract_text()
#             if page_text:
#                 text += page_text
#     return text

# # ✅ Function to query Gemini
# def ask_gemini(text):
#     prompt = f"""
#     Extract structured data from the following resume in JSON format.
#     Include fields: Name, Email, Phone, Skills, Education, Experience.
    
#     Resume:
#     {text}
#     """

#     response = model.generate_content(prompt)
#     return response.text

# # ✅ Streamlit App
# st.title("🤖 Gemini Resume Parser")
# uploaded_file = st.file_uploader("📄 Upload a PDF Resume", type=["pdf"])

# if uploaded_file:
#     resume_text = extract_text_from_pdf(uploaded_file)
#     st.subheader("📄 Extracted Resume Text")
#     st.text_area("Text", resume_text, height=200)

#     if st.button("🔍 Parse Resume"):
#         with st.spinner("Parsing with Gemini..."):
#             output = ask_gemini(resume_text)

#         st.subheader("📊 Parsed Resume Data")
#         st.code(output)


import streamlit as st
import pdfplumber
import google.generativeai as genai
import json

# ✅ Configure your Gemini API key
genai.configure(api_key="AIzaSyADGV44iVUAvaX7uJgrEqG9qnx-QL25VtM")  # 🔁 Replace with your actual key

# ✅ Load the Gemini model
model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

# ✅ Extract text from PDF using pdfplumber
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

# ✅ Function to generate content using Gemini
def ask_gemini(text):
    prompt = f"""
    Extract structured data from the following resume in JSON format.
    Include fields: Name, Email, Phone, Skills, Education, Experience.
    
    Resume:
    {text}
    """
    response = model.generate_content(prompt)
    return response.text

# ✅ Clean Gemini output to extract JSON from markdown-like formatting
def extract_json_from_response(response_text):
    if response_text.strip().startswith("```"):
        return response_text.strip().split("```")[1].replace("json", "", 1).strip()
    return response_text.strip()

# ✅ Streamlit App UI
st.set_page_config(page_title="Gemini Resume Parser", layout="centered")
st.title("🤖 Gemini Resume Parser")
uploaded_file = st.file_uploader("📄 Upload a PDF Resume", type=["pdf"])

if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)
    st.subheader("📄 Extracted Resume Text")
    st.text_area("Raw Resume Text", resume_text, height=200)

    if st.button("🔍 Parse Resume"):
        with st.spinner("Parsing with Gemini..."):
            output = ask_gemini(resume_text)
            cleaned_output = extract_json_from_response(output)

            try:
                parsed_data = json.loads(cleaned_output)
                st.subheader("📊 Parsed Resume Data")
                st.json(parsed_data)
            except json.JSONDecodeError:
                st.error("❌ Gemini output is not valid JSON. Please review or try again.")
                st.subheader("⚠️ Raw Gemini Output:")
                st.code(output)
