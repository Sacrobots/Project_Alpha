import streamlit as st
from anmEnv import envList
from LoadData import data
from sendMail import sendOutlookMail

st.set_page_config(page_title="Amdocs Notification Manager", page_icon="🔐", layout="centered")

@st.cache_data
def get_active_env_list():
    return envList()

def first():
    st.markdown("<h2 style='text-align: center;'>Amdocs Notification Manager</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    env_no   = st.text_input("ENV No")
    vapp     = st.text_input("VAPP No")

    active_env_list = get_active_env_list()

    anm_active_env = st.selectbox("Select ANM IP", active_env_list)

    if st.button("Proceed", use_container_width=True, type="primary"):

        data["User_Name"] = username
        data["Password"] = password
        data["Env_No"] = env_no
        data["VAPP_No"] = vapp
        data["ANM_IP"] = anm_active_env

        print("Stored Data: ", data)

        sendOutlookMail()

        st.success('**✅ Mail Sent Successfully**')


