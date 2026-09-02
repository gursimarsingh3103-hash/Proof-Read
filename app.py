from google import genai
import streamlit as st
import traceback

st.set_page_config(page_title="AI Proofreader & Editor", page_icon="📝")
st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "Enter Google Gemini API Key:", type="password"
)
st.title("📝 My AI Proofreader & Editor")
draft_text = st.text_area("Paste your assignment draft here:", height=250)

if st.button("Proofread & Improve"):
  if not api_key:
    st.error("Please enter your API key in the sidebar.")
  elif not draft_text.strip():
    st.error("Please paste some text.")
  else:
    with st.spinner("Proofreading..."):
      try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Proofread and improve this text:\n\n" + draft_text,
        )
        st.subheader("Polished Output")
        st.write(response.text)
      except Exception as e:
        st.error(f"{type(e).__name__}: {e}")
        with st.expander("Full error details"):
          st.code(traceback.format_exc())
