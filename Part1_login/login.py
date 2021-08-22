from selenium import webdriver                      # Browser (Браузер)
from selenium.webdriver.common.keys import Keys     # Keys (Кнопки)
from auth_data import username, password            # Login (Из auth_data берём наши данные для логина и пароля)
import time                                         # Time (Время)
import random                                       # Random (Рандом)


def login(username, password):

    # Browser (Путь к драйверу в зависимости от того, какой браузер мы хотим использовать)
    browser = webdriver.Chrome("../chromedriver/chromedriver")

    try:
        # Main page (Открываем главную страницу)
        browser.get("https://www.instagram.com")

        # Pause (Делаем паузу, чтобы посмотреть что происходит)
        time.sleep(random.randrange(3, 5))

        # Login - insert the field attribute
        # (Смотрим как называется атрибут поля и вставляем в поле для логина наш логин)
        username_input = browser.find_element_by_name("username")
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        # Password - insert the field attribute
        # (Смотрим как называется атрибут поля и вставляем в поле для пароля наш пароль)
        password_input = browser.find_element_by_name("password")
        password_input.clear()
        password_input.send_keys(password)

        # Simulate a button press ENTER (Симулируем нажатие кнопки ENTER)
        password_input.send_keys(Keys.ENTER)

        time.sleep(10)

        # Close browser (Закрываем браузер)
        browser.close()
        browser.quit()

    # If Instagram changes something in the code (Если инстаграм что то поменяет в коде, мы увидим где именно ошибка)
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

login(username, password)
