import streamlit as st
from google import genai

st.set_page_config(page_title="AI Proofreader", page_icon="📝")
st.title("📝 My AI Proofreader & Editor")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")
    st.markdown("[Get an API key here](https://aistudio.google.com/app/apikey)")

draft_text = st.text_area("Paste your assignment draft here:", height=250)

if st.button("Proofread & Improve"):
    if not api_key:
        st.warning("Please enter your API key in the sidebar.")
    elif not draft_text:
        st.warning("Please paste some text to proofread.")
    else:
        with st.spinner("Analyzing your text..."):
            try:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Act as an expert academic editor. Review the following text for grammar, punctuation, and clarity.
                1. Provide a polished, academic version of the text.
                2. Provide a bulleted list of the specific vocabulary replacements you made and explain why they improve the flow.

                Draft:
                {draft_text}
                """
                
                response = client.models.generate_content(
                    model="gemini-3.7-flash",
                    contents=prompt
                )
                
                st.subheader("Results")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
