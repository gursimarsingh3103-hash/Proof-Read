from google import genai
import streamlit as st
import time
import traceback

st.set_page_config(page_title="AI Proofreader & Editor", page_icon="📝")
st.sidebar.header("Settings")
api_key = st.sidebar.text_input(
    "Enter Google Gemini API Key:", type="password"
)
st.title("📝 My AI Proofreader & Editor")
draft_text = st.text_area("Paste your assignment draft here:", height=250)

def generate_with_retry(client, model, contents, max_retries=3):
    last_error = None
    for attempt in range(max_retries):
        try:
            return client.models.generate_content(model=model, contents=contents)
        except Exception as e:
            last_error = e
            if "503" in str(e) or "UNAVAILABLE" in str(e):
                time.sleep(2 * (attempt + 1))  # wait a bit longer each retry
                continue
            raise  # not a 503 - don't retry, raise immediately
    raise last_error

if st.button("Proofread & Improve"):
    if not api_key:
        st.error("Please enter your API key in the sidebar.")
    elif not draft_text.strip():
        st.error("Please paste some text.")
    else:
        with st.spinner("Proofreading..."):
            try:
                client = genai.Client(api_key=api_key)
                response = generate_with_retry(
                    client,
                    model="gemini-2.5-flash",
                    contents="Proofread and improve this text:\n\n" + draft_text,
                )
                st.subheader("Polished Output")
                st.write(response.text)
            except Exception as e:
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    st.error("Gemini's servers are overloaded right now. Please wait a moment and try again.")
                else:
                    st.error(f"{type(e).__name__}: {e}")
                with st.expander("Full error details"):
                    st.code(traceback.format_exc())
