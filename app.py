import time
from google import genai
import streamlit as st

st.set_page_config(page_title="AI Proofreader & Editor", page_icon="📝")

st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

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
                
                # Built-in retry mechanism to handle temporary 503 traffic spikes smoothly
                response = None
                for attempt in range(4):
                    try:
                        response = client.models.generate_content(
                            model="gemini-3.7-flash",
                            contents="Proofread and improve this text:\n\n" + draft_text
                        )
                        break
                    except Exception as api_err:
                        if "503" in str(api_err) and attempt < 3:
                            time.sleep(2)
                            continue
                        else:
                            raise api_err

                st.subheader("Polished Output")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")
