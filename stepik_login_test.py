import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import math


# Фикстура для браузера
@pytest.fixture(scope="class")  # Изменили на function для изолированных тестов
def browser():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


# Фикстура для ожиданий (WebDriverWait)
@pytest.fixture()
def wait(browser):
    return WebDriverWait(browser, 10)


@pytest.fixture(scope="session")
def load_config():
    with open('info.json') as f:
        return json.load(f)


def get_answer():
    return str(math.log(int(time.time())))


class TestLogin:
    def test_authorization(self, browser, wait, load_config):
        login = load_config['a']
        password = load_config['b']

        browser.get('https://stepik.org/lesson/236895/step/1')

        login_link = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href*="login"]'))
        )
        login_link.click()

        input_login = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="login"]'))
        )
        input_login.send_keys(login)

        input_password = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '[name="password"]'))
        )
        input_password.send_keys(password)

        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[type="submit"]'))
        )
        submit_button.click()

        wait.until(EC.url_contains("lesson"))

    @pytest.mark.parametrize('link', [
        "https://stepik.org/lesson/236895/step/1",
        "https://stepik.org/lesson/236896/step/1",
        "https://stepik.org/lesson/236897/step/1",
        "https://stepik.org/lesson/236898/step/1",
        "https://stepik.org/lesson/236899/step/1",
        "https://stepik.org/lesson/236903/step/1",
        "https://stepik.org/lesson/236904/step/1",
        "https://stepik.org/lesson/236905/step/1"
    ])
    def test_complete(self, browser, wait, link):
        answer = get_answer()  # Новое вычисление для каждого теста

        browser.get(link)

        # Ожидание и ввод ответа
        input_field = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[placeholder="Напишите ваш ответ здесь..."]'))
        )
        input_field.send_keys(answer)

        # Отправка ответа
        submit_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.submit-submission'))
        )
        submit_button.click()

        # Проверка результата
        feedback = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'p.smart-hints__hint'))
        )
        assert feedback.text == "Correct!", f"Expected 'Correct!', but got '{feedback.text}'"