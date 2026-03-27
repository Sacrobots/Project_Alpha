import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import streamlit as st
from selenium import webdriver



def jenkinsBounce(username, password, vapp_num, webdriver):


    driver = webdriver.Edge()
    driver.maximize_window()

    vapp = vapp_num
    user_name = username
    pwd = password

    try:
        driver.get('http://ilcechr042:8080/job/J-Boot-PMX/build?delay=0sec')


        driver.find_element(By.CLASS_NAME, "login").click()
        driver.find_element(By.NAME, "j_username").send_keys(user_name)
        driver.find_element(By.NAME, "j_password").send_keys(pwd)
        driver.find_element(By.NAME, "Submit").click()

        time.sleep(5)

        Str = f"//option[@value='VAPP_{vapp}']"

        driver.find_element(By.XPATH, Str).click()

        checkbox = driver.find_element(By.XPATH, '//input[@name="value" and @value="FULL"]')
        if not checkbox.is_selected():
            checkbox.click()

        # Submit Button
        driver.find_element(By.ID, 'yui-gen1-button').click()

        time.sleep(5)
        driver.quit()

        Jenkins = "http://ilcechr042:8080/job/J-Boot-PMX/"

        st.markdown(f"""
            <div style="background-color:#d4edda; padding:15px; border-radius:10px; 
                        color:#155724; font-weight:900; text-align:center;">
                ✅ Build & Full Bounce Initiated: <a href="{Jenkins}" target="_blank" style="color:#155724; text-decoration:underline;">Check Status</a>
            </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        print(f"Error: {e}")




