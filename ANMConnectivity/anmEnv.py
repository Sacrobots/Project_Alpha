import numpy
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def envList():
    pd.set_option('display.max_columns', None)
    driver = webdriver.Edge()
    driver.maximize_window()
    driver.get("https://amdocs.sharepoint.com/sites/Charter_Spectrum/Lists/ANM%20Environments/AllItems.aspx?sortField=Active%5Fx0020%5FConnection&isAscending=false&viewid=c3f7f056%2D7ab4%2D465f%2D8a31%2Dd95619f5f2df")


    table = WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.ID, "listTabPanel"))
    )

    # Find rows (adjust selector depending on SharePoint’s markup)
    rows = table.find_elements(By.CSS_SELECTOR, "div[role='row']")

    data = []
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "div[role='gridcell']")
        cell_texts = [cell.text.strip() for cell in cells]
        if cell_texts:
            data.append(cell_texts)

    header_cells = table.find_elements(By.CSS_SELECTOR, "div[role='columnheader']")
    column_names = [cell.text.strip() for cell in header_cells if cell.text.strip()]


    df = pd.DataFrame(data, columns=column_names).reset_index(drop=True)


    lst = list(df['CES Env'].head(6))
    lst = lst[1:]

    print("\nList Of ANM IP: ",lst)

    return lst