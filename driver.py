

def initilize_driver():

    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import Select
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless")
    import re
    import datetime

    # The place we will direct our WebDriver to
    url = 'https://www.portfolio123.com/app/auth'

    # Creating the WebDriver object using the ChromeDriver
    #chrome_options=options
    driver = webdriver.Chrome(chrome_options=options)

    # Directing the driver to the defined url
    driver.get(url)



    # Select the id box
    id_box = driver.find_element_by_xpath('//*[@id="user"]')
    # Send id information
    id_box.send_keys('semanuel')

    # Find password box
    pass_box = driver.find_element_by_xpath('//*[@id="passwd"]')
    # Send password
    pass_box.send_keys('mike')

    # Find login button
    login_button = driver.find_element_by_xpath('//*[@id="auth"]/div/div/div/div/div/div/form/button')
    # Click login
    login_button.click()
    driver.find_element_by_xpath('//*[@id="auth"]/div/div/div/div/div/div/form/div[3]/div/label/input').click()

    return driver
    