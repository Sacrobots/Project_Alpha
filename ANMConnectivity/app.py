import streamlit as st
from home import first
from ANMConfig import nextFlow



st.set_page_config(
    page_title="ANM",
    layout="wide",
    page_icon="🤖"
)


if "page" not in st.session_state:
    st.session_state.page = "📧 Initial Page"

if "config_complete" not in st.session_state:
    st.session_state.config_complete = False

# Sidebar with buttons
with st.sidebar:

    if st.session_state.get("config_complete", False):
        selected = st.selectbox("**Select Options**", ["📧 Initial Page", "▶️ Execute Flow"])
    else:
        selected = st.selectbox("**Select Options**",
                                ["📧 Initial Page", "▶️ Execute Flow"])
    st.session_state.page = selected
    st.markdown("""---""")

    st.markdown("""\n""")

if st.session_state.page == "📧 Initial Page":
    first()



elif st.session_state.page == "▶️ Execute Flow":
    nextFlow()