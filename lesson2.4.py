from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import math
import time
def calc(x):
    return str(math.log(abs(12 * math.sin(int(x)))))
try:
    browser = webdriver.Chrome()

    browser.get("http://suninjuly.github.io/explicit_wait2.html")

    # говорим Selenium проверять в течение 5 секунд, пока кнопка не станет кликабельной
    button = WebDriverWait(browser, 12).until(
            EC.text_to_be_present_in_element((By.ID, "price"), "100"))
    message = browser.find_element(By.TAG_NAME, "button").click()
    x_element = browser.find_element(By.CSS_SELECTOR, '#input_value')
    x = x_element.text
    y = calc(x)
    input1 = browser.find_element(By.ID, 'answer')
    input1.send_keys(y)
    final_btn = browser.find_element(By.CSS_SELECTOR, '[type="submit"]')
    final_btn.click()

finally:
    time.sleep(5)
    browser.quit()