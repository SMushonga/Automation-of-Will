from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def open_chrome():
    driver = webdriver.Chrome()
    return driver

def login(username, password_, driver):


    driver.get("https://empower.unity-fe.co.za/login")
    email = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "email")))
    email.send_keys(username)

    password = driver.find_element(by=By.NAME, value="password")
    password.send_keys(password_)

    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign in')]")
    button.click()

def go_home(driver):
    home = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.fa.fa-home")))
    home.click()

def get_to_profile(id_number, driver):

    search = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "search")))
    search.clear()
    search.send_keys(id_number)
    button_2 =  driver.find_element(By.XPATH, "//button[contains(text(), 'Search')]")
    button_2.click()

    button_3 = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'View')]")))
    button_3.click()

    Insurance = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT,  "Insurance")))
    Insurance.click()

    Will_Plans = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.LINK_TEXT,  "Will Plans")))
    Will_Plans.click()


def go_to_pending(driver):
    button_4 = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, "//li[text()='No policies for selected status']")))
    button_4 = driver.find_element(By.XPATH, "//button[text()='Pending']")
    button_4.click()



def go_to_docs(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//td[contains(text(), 'KeyPlanTM Diamond')]")))
    #element = driver.find_element(By.XPATH, "//td[contains(text(), 'KeyPlanTM Diamond')]")
    element.click()
    
    Documents = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Documents")))
    Documents.click()

def check(outputs, index, driver):
    try:
        button_4 = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//a[@role='button' and contains(@class, 'btn-danger') and text()='Re-Generate']")))
        outputs.loc[index, 'Answer'] = 'generated'
        return True
    except:
        outputs.loc[index, 'Answer'] = 'not_generated'
        return False


def generate(outputs, index, driver):
    button_4 = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[@role='button' and contains(@class, 'btn-danger') and text()='Generate']")))
    if button_4.text == 'Generate':
        button_4.click()
        outputs.loc[index, 'Answer'] = 'generated_attempt'
    return
    '''try:
        confirm = WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH,"//a[@role='button' and contains(@class, 'btn-danger') and text()='Re-Generate']")))
        if confirm.text == 'Re-Generate':
            outputs.loc[id_number, 'Answer'] = 'generated'
        else:
            outputs.loc[id_number, 'Answer'] = 'Clicked_Generate_Not_Generated'  
    except:
        outputs.loc[id_number, 'Answer'] = 'Timed_out'''
def error_catcher_attempt(outputs, index, driver):
    button_4 = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//a[@role='button' and contains(@class, 'btn-danger') and text()='Generate']")))
    if button_4.text == 'Generate':
        button_4.click()
    error = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.vue-toast_container._error div.vue-toast_message span")))

    outputs.loc[index, 'Answer'] = error.text
    time.sleep(5)
    return


def error_catcher(dataframe, doc, driver):
    click_counter = 0
    for index, id_ in dataframe.iloc[:].iterrows():
        get_to_profile(id_['id_number'], driver)
        if (index % 5) == 0:
            dataframe.to_csv(doc, index=False)
        if (click_counter % 15) == 0 and click_counter != 0:
            time.sleep(60)
        try:
            go_to_pending(driver)
            try:
                go_to_docs(driver)
            except:
                dataframe.loc[index, 'Answer'] = 'No Will'
                go_home(driver)
                continue
        except:
            go_to_docs(driver)  
        if check(dataframe, index, driver):
            go_home(driver)
            continue
        try: 
            error_catcher_attempt(dataframe, index, driver)
            go_home(driver)
            continue
        except Exception as e:
            dataframe.loc[index, 'Answer'] = 'Failed to error'
            go_home(driver)
            continue
    else:
        dataframe.to_csv(doc, index=False)
    return dataframe

def close_driver(driver):
    driver.quit()

