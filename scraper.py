import time
import sqlite3
from better_profanity import profanity
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, ElementNotVisibleException
ignored_exceptions = (NoSuchElementException,StaleElementReferenceException, TimeoutException, ElementNotVisibleException)

def scrape_messages(driver, friends):
    global block_list
    block_list = []

    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '*//div[contains(text(),"Not now")]')))
        driver.execute_script("arguments[0].click();", element)
    except:
                # assert False, "Failed"
        driver.refresh()
        pass
            # print("56789098765")
            # driver.close()
    time.sleep(3)
    try:
        print("TRY 1")
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '*//button[contains(text(),"Not Now")]' )))
        print("1. ",element)
        driver.execute_script("arguments[0].click();", element)
        print("CLICKED")
    except:
        # assert False, "Failed"
        driver.refresh()
        pass


    print(2)
    count = -1
    while True:
        time.sleep(5)
        ele = driver.find_elements("xpath", "*//div[@role='listitem']//*//div[2]/div")
        count+=1
        if count==len(ele)-1:
            break
        
        print("COunt1 -", count)
        time.sleep(1)
        try:
            WebDriverWait(driver, 50,ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable(ele[count]) or EC.element_to_be_selected(ele[count]))
            print(ele[count].text)
            entire_text = ele[count].text
            lines = entire_text.split('\n')
            # Strip leading and trailing spaces from the first line
            first_line = lines[0].strip()
            print(first_line)
        except:
            pass
        print("COunt2 -", count)

        print("name ---->"+ first_line)
        if first_line in friends:
            print(f"This user is a friend {first_line}")
            continue

        time.sleep(1)
        if ele[count].is_enabled and count < 5:
            ele[count].click()
        else:
            break

# Might be already blocked contact
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '*//div[text()="Unblock"]')))
            print("-----------> already blocked")
            continue
        except:
            pass

        time.sleep(10)

        ele_mess = driver.find_elements("xpath","*//div[@role='presentation']/span/div")
        data = " "
        for j in range(len(ele_mess)):
            ele_mess = driver.find_elements("xpath", "*//div[@role='presentation']/span/div")
            time.sleep(0.5)

            if ele_mess[j].is_displayed:
                WebDriverWait(driver, 30,ignored_exceptions=ignored_exceptions).until(EC.element_to_be_clickable(ele_mess[j]))
                data+= f" {ele_mess[j].text} " 
            # print(data)
            time.sleep(0.5)
            print("data: -", data)
            x = profanity.contains_profanity(data)
            if x:
                try:
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '*//div//*[@aria-label="Conversation information"]'))).click()
                    time.sleep(2)
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "*//div/span[text()='Block']" ))).click()
                    time.sleep(2)
                    WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "*//div/button[text()='Block']" ))).click()
                    block_list.append(ele[count].text)
                    print(block_list)
                except:
                    pass
            print(block_list)
    return block_list
    # driver.close()
    # return render(request, "home.html", context={"block_list": block_list}) 
