from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import functions_file

def check_data(dataframe, doc, driver):
    for index, id_ in dataframe.iloc[:].iterrows():     
        functions_file.get_to_profile(id_['id_number'], driver)
        try:
            functions_file.go_to_pending(driver)
            try:
                functions_file.go_to_docs(driver)
            except:
                dataframe.loc[index, 'Answer'] = 'No Will'
                functions_file.go_home(driver)
                continue
        except:
            functions_file.go_to_docs(driver)
        
        try:
            functions_file.check(dataframe, index, driver)
        except Exception as e:
            dataframe.loc[index, 'Answer'] = 'No Employer'

        functions_file.go_home(driver)
        if (index % 5) == 0:
            dataframe.to_csv(doc, index=False)
    else:
        dataframe.to_csv(doc, index=False)
    return dataframe
