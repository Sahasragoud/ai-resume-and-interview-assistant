import streamlit as st

st.set_page_config(
    page_title="AI Resume & Interview Assistant",
    layout="wide"
)

st.title("🤖 AI Resume & Interview Assistant")

st.markdown(
    """
    ### Welcome 👋  
    Use the **sidebar** to navigate between:
    - 📄 Resume Agent (upload resume + JD, view ATS)
    - 🎤 Interview Agent (take AI-powered interview)

    👉 **Important:**  
    First complete **Resume Agent**, then switch to **Interview Agent**.
    """
)