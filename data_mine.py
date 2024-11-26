from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import functions_file

def generate_main(dataframe, doc, driver):
    click_counter = 0
    for index, id_ in dataframe.iloc[:].iterrows():
        functions_file.get_to_profile(id_['id_number'], driver)
        if (index % 5) == 0:
            dataframe.to_csv(doc, index=False)
        if (click_counter % 15) == 0 and click_counter != 0:
            time.sleep(60)
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
        if functions_file.check(dataframe, index, driver):
            functions_file.go_home(driver)
            continue

        try: 
            functions_file.generate(dataframe, index, driver)
            click_counter += 1
            functions_file.go_home(driver)
            continue
        except:
            dataframe.loc[index, 'Answer'] = 'Did Not Generate'
            functions_file.go_home(driver)
            continue
    else:
        dataframe.to_csv(doc, index=False)
    return dataframe
