from flask import Flask, request, jsonify, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from scraper import scrape_messages
# from sqlalchemy import create_engine, Column, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import uuid

app = Flask(__name__)

global block_list

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    friends = data.get('friends', [])

    # Initialize WebDriver
    service = ChromeService(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start Chrome maximized
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))

        # Attempt to log in
        user_input = driver.find_element(By.NAME, "username")
        pass_input = driver.find_element(By.NAME, "password")
        user_input.send_keys(username)
        pass_input.send_keys(password)

        # Click the login button
        login_button = driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')
        login_button.click()

        # Wait for the login process to complete
        WebDriverWait(driver, 10).until(EC.url_contains("instagram.com"))

        time.sleep(10)

        driver.get("https://www.instagram.com/direct/inbox/?hl=en")
        WebDriverWait(driver, 10).until(EC.url_contains("instagram.com"))
        # Scrape messages 
        # messages_data = scrape_messages(driver, password)
        # conn = setup_database()
        print('successfully connection created')
        block_list = scrape_messages(driver, friends)
        # Store messages in SQLite 
        # session.bulk_save_objects([Message(
        #     id=str(uuid.uuid4()),
        #     sender=msg['sender'], 
        #     text=msg['text'], 
        #     timestamp=msg['timestamp']
        # ) for msg in messages_data])
        # session.commit() 
        
        driver.quit() 
        return render_template('block_list.html', block_list=block_list)
    
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit()
        return jsonify(success=False)
    
# @app.route('/block-list') 
# def display_block_list(): 
#     return render_template('block_list.html', block_list = block_list)

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify, render_template
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from scraper import scrape_messages
# from sqlalchemy import create_engine, Column, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import uuid

# app = Flask(__name__)

# # Setup Database 
# # engine = create_engine('sqlite:///messages.db') 
# # Base = declarative_base() 

# # class Message(Base): 
# #     __tablename__ = 'messages' 
    
# #     id = Column(String, primary_key=True) 
# #     sender = Column(String) 
# #     text = Column(String) 
# #     timestamp = Column(DateTime) 

# # Base.metadata.create_all(engine) 
# # Session = sessionmaker(bind=engine) 
# # session = Session()

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     username = data.get('username')
#     password = data.get('password')

#     # Initialize WebDriver
#     service = ChromeService(ChromeDriverManager().install())
#     options = webdriver.ChromeOptions()
#     driver = webdriver.Chrome(service=service, options=options) 
#     driver.get("https://www.instagram.com/accounts/login/") 
#     time.sleep(5)
#     driver.maximize_window()

#     try:
#         # Attempt to log in
#         print(password, username)
#         username_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
#         username_field.send_keys(username)
#         time.sleep(2)

#         password_field = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
#         password_field.send_keys(password)
#         time.sleep(2)

#         # Click the login button
#         login_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button')))
#         login_button.click()
#         time.sleep(5)  # Increased sleep time to allow login process

#         # Check if login was successful
#         if "Save Your Login Info?" in driver.page_source or "home" in driver.current_url:
#             # Navigate to DMs 
#             driver.get("https://www.instagram.com/direct/inbox/")
#             # time.sleep(5) 
#             # Scrape messages 
#             # messages_data = scrape_messages(driver) 
#             # # Store messages in SQLite 
#             # for msg in messages_data: 
#             #     message = Message(
#             #         id=str(uuid.uuid4()),
#             #         sender=msg['sender'], 
#             #         text=msg['text'], 
#             #         timestamp=msg['timestamp']
#             #     ) 
#             #     session.add(message) 
#             # session.commit() 
#             # driver.quit() 
#             # return jsonify(success=True, messages=messages_data)
#         else:
#             print("Failed to log in. Current URL:", driver.current_url)
#             driver.quit()
#             return jsonify(success=False)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         driver.quit()
#         return jsonify(success=False)

# if __name__ == '__main__':
#     app.run(debug=True)
                         