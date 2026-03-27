from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from tornado.gen import sleep
import time
import streamlit as st
from LoadData import data
from selenium.webdriver.support.ui import Select
from ENV_FULL_BOUNCE import jenkinsBounce


def nextFlow():
    st.markdown("""
        <style>
        .cool-title {
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            font-family: 'Trebuchet MS', sans-serif;
            color: #4A90E2;
            text-shadow: 2px 2px 4px #aaa;
            margin-top: 30px;
        }
        </style>
        <div class="cool-title">Operational Flow</div>
        """, unsafe_allow_html=True)

    if st.button("**Press To Execute Flow**", use_container_width=True, type="primary"):

        driver = webdriver.Edge()
        driver.get("http://ilcechr084:8080/job/ANM_CONFIGURATION/")

        wait = WebDriverWait(driver, 10)

        # 2. Click on "Login" link
        login_link = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "log in"))
        )
        login_link.click()

        # 3. Enter Username and Password
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "j_username"))  # Jenkins default field
        )
        password_field = wait.until(
            EC.presence_of_element_located((By.NAME, "j_password"))  # Jenkins default field
        )

        username_field.send_keys(f"{data['User_Name']}")
        password_field.send_keys(f"{data['Password']}")


        sign_in_button = wait.until(
            EC.element_to_be_clickable((By.NAME, "Submit"))  # Jenkins login button
        )
        sign_in_button.click()


        build_with_params = wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Build with Parameters"))
        )
        build_with_params.click()


        env_textbox = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "setting-input")))
        env_textbox.clear()
        env_textbox.send_keys(f"{data['Env_No']}")



        # Step 1: Find all select elements named "value"
        select_elements = wait.until(
            EC.presence_of_all_elements_located((By.NAME, "value"))
        )

        # Step 2: Loop through and find the one with hidden input "ANM_URL"
        for select_element in select_elements:
            parent = select_element.find_element(By.XPATH, "./preceding-sibling::input[@name='name']")
            if parent.get_attribute("value") == "ANM_URL":
                select_anm = Select(select_element)
                select_anm.select_by_visible_text(f"{data['ANM_IP']}")
                break


        # # 8. Click Build
        # build_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Build']")))
        # build_button.click()

        driver.quit()

        print("Build triggered successfully!")

        print("-------------------------------------------------------------------------------------------------------------------------------------\n")
        print("Starting Jenkins Full Bounce")
        username = data['User_Name']
        password = data['Password']
        vapp_num = data['VAPP_No']


        jenkinsBounce(username, password, vapp_num, webdriver)

        print("-------------------------------------------------------------------------------------------------------------------------------------\n")

        # After jenkinsBounce completes


        driver = webdriver.Edge()
        driver.get(f"http://illnqw{data['Env_No']}:1234/plugins/vmmonitor/")

        wait = WebDriverWait(driver, 120)

        # Locate the MAESTRO status cell
        status_element = wait.until(
            EC.presence_of_element_located((By.XPATH, "//td[contains(text(),'MAESTRO')]/following-sibling::td"))
        )
        status_text = status_element.text.strip().upper()
        st.markdown("<br>", unsafe_allow_html=True)
        if "UP" in status_text:
            st.markdown(f"""
                <div style="background-color:#d4edda; padding:15px; border-radius:10px; 
                            color:#155724; font-weight:900; text-align:center;">
                            ✅ Maestro Is Up
                </div>
            """, unsafe_allow_html=True)
        elif "DOWN" in status_text:

            st.markdown(f"""
                <div style="background-color:#f8d7da; padding:15px; border-radius:10px; 
                            color:#721c24; font-weight:900; text-align:center;">
                            ❌ Maestro Is Down
                </div>
            """, unsafe_allow_html=True)


        elif "NOT INSTALLED" in status_text:

            st.markdown(f"""
                <div style="background-color:#fff3cd; padding:15px; border-radius:10px; 
                            color:#856404; font-weight:900; text-align:center;">
                            ⚠️ Maestro Is Not Installed
                </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown(f"""
                <div style="background-color:#fff3cd; padding:15px; border-radius:10px; 
                            color:#856404; font-weight:900; text-align:center;">
                            ⚠️ Status Unknown
                </div>
            """, unsafe_allow_html=True)

        driver.quit()
