import time
from google import genai
import streamlit as st

st.set_page_config(page_title="AI Proofreader & Editor", page_icon="📝")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "Enter Google Gemini API Key:", type="password"
)
st.sidebar.markdown(
    "[Get an API key here](https://aistudio.google.com/app/apikey)"
)

st.title("📝 My AI Proofreader & Editor")

st.markdown("Paste your assignment draft here:")
draft_text = st.text_area("", height=250)

if st.button("Proofread & Improve"):
  if not api_key:
    st.error("Please enter your Google Gemini API key in the sidebar.")
  elif not draft_text.strip():
    st.error("Please paste some text to proofread.")
  else:
    with st.spinner("AI is proofreading your text..."):
      try:
        client = genai.Client(api_key=api_key)

        prompt = (
            "You are an expert academic editor and proofreader. Carefully"
            " review the following text for grammar, spelling, clarity,"
            " punctuation, and professional flow. Provide a polished version"
            " followed by a brief summary of key improvements made:\n\n"
            f"{draft_text}"
        )

        response = None
        for attempt in range(3):
          try:
            response = client.models.generate_content(
                model="gemini-3.7-flash", contents=prompt
            )
            break
          except Exception as api_err:
            if "503" in str(api_err) and attempt < 2:
              time.sleep(2)
              continue
            else:
              raise api_err

        st.subheader("Polished Output")
        st.write(response.text)

      except Exception as e:
        st.error(f"An error occurred: {e}")
        
