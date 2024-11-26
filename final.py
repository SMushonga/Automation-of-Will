from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import functions_file, data_check, data_mine


driver = functions_file.open_chrome()
df = pd.read_excel('')
df['Answer'] = None
df = df

functions_file.login("", "", driver)

def final(df , driver, iteration = 0):
    check = 'check ' + str(iteration) + '.csv'
    complete = 'complete ' + str(iteration) + '.csv'
    error_doc = 'errors ' + str(iteration) + '.csv'
    complete_df = data_mine.generate_main(df, complete, driver)
    filter_no_will =  complete_df[complete_df['Answer'] != 'No Will']
    check_df = data_check.check_data(filter_no_will, check, driver)

    undone = check_df[check_df['Answer'] != 'generated']
    errors = functions_file.error_catcher(undone, error_doc, driver)
    
    errors_fake = errors[errors['Answer'] == '"Capital Legacy responded with - API Error: There was an error while trying to process the request, please try again later or contact support."']
    errors_real = errors[errors['Answer'] != '"Capital Legacy responded with - API Error: There was an error while trying to process the request, please try again later or contact support."']
    '''while (not errors_fake.empty) and (iteration < 3):
        iteration += 1
        check = 'check ' + str(iteration) + '.csv'
        complete = 'complete ' + str(iteration) + '.csv'
        error_doc = 'errors ' + str(iteration) + '.csv'
        complete_df = data_mine.generate_main(errors_fake, complete, driver)
        filter_no_will =  complete_df[complete_df['Answer'] != 'No Will']
        check_df = data_check.check_data(filter_no_will, check, driver)

        undone = check_df[check_df['Answer'] != 'generated']
        errors_ = functions_file.error_catcher(undone, error_doc, driver)
        errors_fake = errors_[errors_['Answer'] == '"Capital Legacy responded with - API Error: There was an error while trying to process the request, please try again later or contact support."']
        errors_real = pd.concat([errors_real, errors_[errors_['Answer'] != '"Capital Legacy responded with - API Error: There was an error while trying to process the request, please try again later or contact support."']], ignore_index=True)
    errors_real.to_csv('real_errors.csv', index=False, header=False, mode='a')
    #errors_real.to_excel('final.xlsx')'''
    errors_real.to_csv('real_errors.csv', index=False, header=False, mode='a')
    return 


final(df, driver, 0)
a = pd.read_csv('check 0.csv')
b = pd.read_csv('errors 0.csv')
a = a.set_index(("id_number"))  # Align on 'id'
b = b.set_index(("id_number"))  # Align on 'id'
a.update(b)            # Update matching rows in a with b
a.reset_index(inplace=True)
print(a.head())
a.to_excel('export.xlsx', index=False)
functions_file.close_driver(driver)
