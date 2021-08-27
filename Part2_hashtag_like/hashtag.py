from selenium import webdriver                      # Browser (Браузер)
from selenium.webdriver.common.keys import Keys     # Keys (Кнопки)
from auth_data import username, password            # Login (Из auth_data берём наши данные для логина и пароля)
import time                                         # Time (Время)
import random                                       # Random (Рандом)

def hashtag_search(username, password, hashtag):
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

        time.sleep(5)

        # Part2
        # Search by hashtag and like the user (Выполняем поиск по хэштегу и ставим пользьвотелю лайк)
        try:
            # Search by hashtag  (Поиск по хэштегу)
            browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
            time.sleep(5)

            # Scrolling the page for the bot to see more posts and copy more links
            # (Листаем страницу чтобы бот увидел больше постов и скопировал больше ссылок)
            for i in range(1, 3):    # Set the number of scrolls (Устанавливаем количество скроллов)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(3, 5))

            # Collecting links to all posts from the page (Собираем ссылки на все посты со страницы)
            hrefs = browser.find_elements_by_tag_name("a")

            # Get the link from each element (Достаём ссылку из каждого элемента)
            # posts_urls = []
            # for item in hrefs:
            #     href = item.get_attribute("href")
            # #
            # #     # In all the link to the posts occurs /p/, and we will make a selection by it
            # #     # (Во всех ссылка на посты встречается /p/, по нему и сделаем отбор)
            #     if "/p/" in href:
            #         posts_urls.append(href)
            #         print(posts_urls)

            # This is the same loop, only one line (Это тот же цикл, только в одну строку)
            posts_urls = [item.get_attribute("href") for item in hrefs if "/p/" in item.get_attribute("href")]
            print(posts_urls)

            # On selected links set Like. By Xpath code. (На отобранные ссылки ставим лайк. По Xpath коду)
            # (Limiting Instagram on the number of likes:
            # for new accounts - no more than 30 actions per hour, no more than 720 per day;
            # for accounts older than 6 months - no more than 60 actions per hour, no more than 1440 per day)
            # (Ограничение Инстаграма на количество лайков:
            # для новых аккаунтов - не более 30 действий в час, не более 720 в день;
            # для аккаунтов старше 6 месяцев - не более 60 действий в час, не более 1440 в день)
            for url in posts_urls:
                try:
                    browser.get(url)
                    like_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button/").click()
                    time.sleep(random.randrange(90, 110))
                except Exception as ex:
                    print(ex)

            # Close browser (Закрываем браузер)
            browser.close()
            browser.quit()

        except Exception as ex:

            print(ex)
            browser.close()
            browser.quit()

    # If Instagram changes something in the code (Если инстаграм что то поменяет в коде, мы увидим где именно ошибка)
    except Exception as ex:
        print(ex)
        browser.close()
        browser.quit()

hashtag_search(username, password, "surfing")
