from selenium import webdriver                      # Creates a browser (Создаёт браузер)
from selenium.webdriver.common.keys import Keys     # Keys (Кнопки)
from auth_data import users_settings_dict           # Login (Из data берём наши данные для логина и пароля)
import time                                         # Time (Время)
import random                                       # Random (Рандом)
from selenium.common.exceptions import NoSuchElementException
import requests  # The library allows us to easily and with a minimum amount of code interact with web applications
                 # Библиотека позволяет нам легко и с минимальным количеством кода взаимодействовать с веб-приложениями
import os                                           # Creates a folder for downloaded files
                                                    # (Создаём папку для скачанных файлов)
from selenium.webdriver.chrome.options import Options   # Модуль опции

# Create a class (Создаём класс)
class InstagramBot():

    # Create a constructor (Создаём конструктор)
    def __init__(self, username, password, window_size):

        self.username = username
        self.password = password
        options = Options()
        options.add_argument(f"--window-size={window_size}")
        self.browser = webdriver.Chrome("../chromedriver/chromedriver", options=options)

    # Method to close the browser (Метод для закрытия браузера)
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # Copy the previously written login (Копируем ранее написанный login)
    def login(self):

        browser = self.browser
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

    def like_photo_by_hashtag(self, hashtag):

        browser = self.browser
        browser.get(f"https://www.instagram.com/explore/tags/{hashtag}/")
        time.sleep(5)

        # Scrolling the page for the bot to see more posts and copy more links
        # (Листаем страницу чтобы бот увидел больше постов и скопировал больше ссылок)
        for i in range(1, 3):  # Set the number of scrolls (Устанавливаем количество скроллов)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.randrange(3, 5))

        # Collecting links to all posts from the page (Собираем ссылки на все посты со страницы)
        hrefs = browser.find_elements_by_tag_name("a")

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
                like_button = browser.find_element_by_xpath(
                    "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button").click()
                time.sleep(random.randrange(90, 110))
            except Exception as ex:
                print(ex)
                self.close_browser()

    # Checking by Xpath whether an element exists on the page (Проверяем по Xpath существует ли элемент на странице)
    def xpath_exists(self, url):

        browser = self.browser
        # (The method in the try block tries to find the passed elements on the page. If successful, exist = True,
        # otherwise the variable will be assigned False)
        # (Метод в блоке try пытается найти на странице переданные элементы. В случае успеха exist = True,
        # а если нет, то переменной будет присвоенно значение False)
        try:
            browser.find_element_by_xpath(url)
            exist = True
        except NoSuchElementException:
            exist = False
        return exist

    # Like the direct link (Ставим лайк по прямой ссылке)
    def put_exactly_like(self, userpost):

        browser = self.browser
        browser.get(userpost)
        time.sleep(4)

        # If the link is not correct and the post does not exist (Если ссылка не верна и поста не существует)
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого поста не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пост успешно найден, ставим лайк!")
            time.sleep(3)

            # Put Like (Ставим лайк)
            like_button = "/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[1]/span[1]/button"
            browser.find_element_by_xpath(like_button).click()
            time.sleep(3)

            print(f"Лайк на пост {userpost} поставлен!")
            self.close_browser()

    # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4 # Part4

    # The method collects links to all posts of the user (Метод собирает ссылки на все посты пользователя)
    def get_all_posts_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        # If the link is not correct and the account does not exist (Если ссылка не верна и пользователя не существует)
        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого пользователя не существует, проверьте URL")
            self.close_browser()
        else:
            print("Пользователь успешно найден, ставим лайки!")
            time.sleep(3)

            # Instagram at the first load shows us 24 posts, with each next scrolling it shows 12 new posts.
            # The number of posts is shown at the top of the profile. We take this figure and divide by 12,
            # to find out how many scrolls we need to make. int to get an integer
            # (Инстаграм при первой загрузке показывает нам 24 поста, при каждой следующей прокрутке показывается
            # 12 новых постов. Количество постов показывается вверху профиля. Берём эту цифру и делим на 12,
            # чтобы узнать сколько прокруток нам надо совершить. int чтобы получить целое число)
            posts_count = int(browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span/").text)
            loops_count = int(posts_count / 12)
            print(loops_count)

            post_urls = []
            for i in range(0, loops_count):
                # Collecting links to all posts from the page (Собираем ссылки на все посты со страницы)
                hrefs = browser.find_elements_by_tag_name("a")
                # Get the link from each element (Достаём ссылку из каждого элемента)
                posts_urls = [item.get_attribute("href") for item in hrefs if "/p/" in item.get_attribute("href")]

                # Scrolling the page for the bot to see more posts and copy more links
                # (Листаем страницу чтобы бот увидел больше постов и скопировал больше ссылок)
                for href in hrefs:
                    posts_urls.append(href)
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(random.randrange(3, 5))
                    print(f"Итерация #{i}")

                file_name = userpage.split("/")[-2]

                with open(f"{file_name}.txt", "a") as file:
                    for post_url in post_urls:
                        file.write(post_url + "\n")

                # Due to scrolling, some links are duplicated, apply the set function to the list
                # (Из-за скролла некоторые ссылки дублируются, применим к списку функцию set)
                set_posts_urls = set(post_urls)
                # Let's return it back to the list for more convenient work (Вернём обратно в список для более удобной работы)
                set_posts_urls = list(set_posts_urls)

                # Save the non-repeating list of links to a new file (Сохраним неповторяющийся список ссылок в новый файл)
                with open(f"{file_name}_set.txt", "a") as file:
                    for post_url in set_posts_urls:
                        file.write(post_url + "\n")


    # By clicking on the link to the account, the bot goes through all the posts and likes each one
    # (Переходя по ссылке на аккаунт, бот проходит по всем постам и на каждый ставит лайк)
    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # Opening the file for reading (Открываем файл для чтения)
        with open(f"{file_name}_set.txt") as file:
            urls_list = file.readlines()

            # Create a for loop that sends the bot to the link, finds the like button and clicks
            # (Создаём цикл for который отправляет бота по ссылке, находит кнопку лайка и кликает)
            for post_url in urls_list[0:6]:
                try:
                    browser.get(post_url)
                    time.sleep(3)

                    # Put Like (Ставим лайк)
                    like_button = "/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button"
                    browser.find_element_by_xpath(like_button).click()
                    time.sleep(random.randrange(90, 110))

                    print(f"Лайк на пост {post_url} успешно поставлен!")
                except Exception as ex:
                    print(ex)
                    self.close_browser()

        self.close_browser()

    # The method downloads content from the user's page (Метод скачивает контент со страницы пользователя)
    def download_userpage_content(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        # Create a folder with a username, everything will be downloaded there
        # (Создаём папку с именем пользователя, туда всё будет скачиваться)
        if os.path.exists(f"{file_name}"):
            print("Папка уже существует!")
        else:
            os.mkdir(file_name)    # Next, add the path to the folder when saving pictures and videos
                                   # (Далее, добавить путь к папке при сохранении картинок и видео)

        # Let's save the received links to the list and at the end of the method save it to a file
        # (Сохраним далее полученные ссылки в список и в конце метода сохраним его в файл)
        img_and_video_src_urls = []
        # Opening the file for reading (Открываем файл для чтения)
        with open(f"{file_name}_set.txt") as file:
            urls_list = file.readlines()

            # Create a for loop that sends the bot to the link, finds the like button and clicks
            # (Создаём цикл for который отправляет бота по ссылке, находит кнопку лайка и кликает)
            for post_url in urls_list[0:10]:
                try:
                    browser.get(post_url)
                    time.sleep(5)

                    # Image links (Ссылка на изображения)
                    img_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img"
                    # Video links (Ссылка на видео)
                    video_src = "/html/body/div[1]/section/main/div/div[1]/article/div[2]/div/div/div[1]/div/div/video"
                    post_id = post_url.split("/")[-2]

                    if self.xpath_exists(img_src):
                        # If there is our picture on the page, then we take the link in the attribute src
                        # (Если наша картинка есть на странице, то забираем ссылку лежащую в атрибуте src)
                        img_src_url = browser.find_element_by_xpath(img_src).get_attribute("src")
                        img_and_video_src_urls.append(img_src_url)

                        # Save the image under the post name (Сохраняем изображение под именем поста)
                        get_img = requests.get(img_src_url)
                        with open(f"{file_name}/{file_name}_{post_id}_img.jpg", "wb") as img_file:
                            img_file.write(get_img.content)

                    elif self.xpath_exists(video_src):
                        # If there is our video on the page, then we take the link in the attribute src
                        # (Если наша видео есть на странице, то забираем ссылку лежащую в атрибуте src)
                        video_src_url = browser.find_element_by_xpath(video_src).get_attribute("src")
                        img_and_video_src_urls.append(video_src_url)

                        # Save the video under the post name (Сохраняем видео под именем поста)
                        get_video = requests.get(video_src_url, stream=True)
                        with open(f"{file_name}/{file_name}_{post_id}_video.mp4", "wb") as video_file:
                            for chunk in get_video.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    video_file.write(chunk)

                    else:
                        print("Упс! Что-то пошло не так!")
                        img_and_video_src_urls.append(f"{post_url}, нет ссылки")

                    print(f"Контент из поста {post_url} успешно скачан!")


                except Exception as ex:
                    print(ex)
                    self.close_browser()

            self.close_browser()

        with open(f'{file_name}/{file_name}_img_and_video_src_urls.txt', 'a') as file:
            for i in img_and_video_src_urls:
                file.write(i + "\n")

    # Install the requests library in the terminal and import module
    # (В терминале устанавливаем библиотеку requests и импортируем модуль)

    # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5 # Part 5

    # Subscription method for all subscribers of the transferred account
    # (Метод подписки на всех подписчиков переданного аккаунта)
    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # Create a folder with a username, everything will be downloaded there
        # (Создаём папку с именем пользователя, туда всё будет скачиваться)
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не существует, проверьте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно найден, начинаем скачивать ссылки на подписчиков!")
            time.sleep(2)

            # Find out the number of subscribers (Узнаём количество подписчиков)
            followers_button = browser.find_element_by_xpath(
                "/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
            followers_count = followers_button.get_attribute("title")
            #followers_count = followers_button.text
            #followers_count = int(followers_count.split(' ')[0])
            print(f"Количество подписчиков: {followers_count}")
            time.sleep(2)

            # If the number of subscribers is more than 999, remove the commas from the number
            # (Если количество подписчиков больше 999, убираем из числа запятые)

            if "," in followers_count:
                followers_count = int("".join(followers_count.split(",")))
            else:
                followers_count = int(followers_count)

            # Scroll subscribers (just like we did with posts)
            # (Скролим подписчиков(точно также как делали с постами))
            loops_count = int(followers_count / 12)
            print(f"Число итераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

            try:
                # List for links (Список для ссылок)
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",
                                           followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Итерация #{i}")

                all_urls_div = followers_ul.find_elements_by_tag_name("li")

                # Go through the list in a loop, extracting the href attribute from each "a" and saving it to the list
                # (Проходим по списку циклом извлекая из каждого "a" атрибут href и сохраняя его в список через append)
                for url in all_urls_div:
                    url = url.find_element_by_tag_name("a").get_attribute("href")
                    followers_urls.append(url)

                # Save all user subscribers to a file (Сохраняем всех подписчиков пользователя в файл)
                with open(f"{file_name}/{file_name}.txt", "a") as text_file:
                    for link in followers_urls:
                        text_file.write(link + "\n")

                # Open the file with subscribers, take one link from there for iteration, go to the page and check the conditions
                # (Открываем файл с подписчиками, берём от туда одну ссылку за иттерацию, заходим на страницу и проверяем условия)
                with open(f"{file_name}/{file_name}.txt") as text_file:
                    users_urls = text_file.readlines()

                    for user in users_urls[0:10]:
                        try:
                            try:
                                with open(f'{file_name}/{file_name}_subscribe_list.txt',
                                          'r') as subscribe_list_file:
                                    lines = subscribe_list_file.readlines()
                                    if user in lines:
                                        print(
                                            f'Мы уже подписаны на {user}, переходим к следующему пользователю!')
                                        continue

                            except Exception as ex:
                                print('Файл со ссылками ещё не создан!')
                                print(ex)

                            browser = self.browser
                            browser.get(user)
                            page_owner = user.split("/")[-2]

                            if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div/a"):
                                print("Это наш профиль, уже подписан, пропускаем итерацию!")
                            elif self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/div/span/span[1]/button/div/span"):
                                print(f"Уже подписаны, на {page_owner} пропускаем итерацию!")
                            else:
                                time.sleep(random.randrange(4, 8))

                                # Working with open and closed profile (Работа с открытым и закрытым профилем)
                                if self.xpath_exists("/html/body/div[1]/section/main/div/div/article/div[1]/div/h2"):
                                    try:
                                        follow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                        print(f'Запросили подписку на пользователя {page_owner}. Закрытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)
                                else:
                                    try:
                                        if self.xpath_exists("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button"):
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                        else:
                                            follow_button = browser.find_element_by_xpath(
                                                "/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/span/span[1]/button").click()
                                            print(f'Подписались на пользователя {page_owner}. Открытый аккаунт!')
                                    except Exception as ex:
                                        print(ex)

                                # We write data to a file for links of all subscriptions, if there is no file, we create it, if there is, we add
                                # (Записываем данные в файл для ссылок всех подписок, если файла нет, создаём, если есть - дополняем)
                                with open(f'{file_name}/{file_name}_subscribe_list.txt', 'a') as subscribe_list_file:
                                    subscribe_list_file.write(user)

                                # No more than 25 - 30 people per hour. Up to 360 people per day
                                # (Не более 25 - 30 человек в час. До 360 человек в сутки)
                                time.sleep(random.randrange(120, 180))

                        except Exception as ex:
                            print(ex)
                            self.close_browser()

            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()

    # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6 # Part 6

    # Method for sending messages to direct (Метод для отправки сообщений в директ)
    def send_direct_message(self, usernames="", message="", img_path=''):

        browser = self.browser
        time.sleep(random.randrange(2, 4))

        # Find the direct button (Находим кнопку директа)
        direct_message_button = "/html/body/div[1]/section/nav/div[2]/div/div/div[3]/div/div[2]/a"

        if not self.xpath_exists(direct_message_button):
            print("Кнопка отправки сообщений не найдена!")
            self.close_browser()
        else:
            print("Отправляем сообщение...")
            # Click on it (Нажимаем на её)
            direct_message = browser.find_element_by_xpath(direct_message_button).click()
            time.sleep(random.randrange(2, 4))

        # Disable pop-up window (Отключаем всплывающее окно)
        if self.xpath_exists("/html/body/div[4]/div/div"):
            browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[2]").click()
        time.sleep(random.randrange(2, 4))

        # Press the button "Send message" (Нажимаем кнопку "Отправить сообщение")
        send_message_button = browser.find_element_by_xpath(
            "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # Sending a message to multiple users (Отправляем сообщение нескольким пользователям)
        for user in usernames:
            # Enter the recipient (Вводим получателя)
            to_input = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/div[1]/div/div[2]/input")
            to_input.send_keys(user)
            time.sleep(random.randrange(2, 4))

            # Selecting a recipient from the list (Выбираем получателя из списка)
            users_list = browser.find_element_by_xpath(
                "/html/body/div[4]/div/div/div[2]/div[2]").find_element_by_tag_name("button").click()
            time.sleep(random.randrange(2, 4))

        # Add another user (Добавляем ещё пользователя)
        next_button = browser.find_element_by_xpath(
            "/html/body/div[4]/div/div/div[1]/div/div[2]/div/button").click()
        time.sleep(random.randrange(2, 4))

        # Sending a text message (Отправка текстового сообщения)
        if message:
            text_message_area = browser.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/textarea")
            text_message_area.clear()
            text_message_area.send_keys(message)
            time.sleep(random.randrange(2, 4))
            text_message_area.send_keys(Keys.ENTER)
            print(f"Сообщение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

        # Send image (Отправка изображения)
        if img_path:
            send_img_input = browser.find_element_by_xpath(
                "/html/body/div[1]/section/div/div[2]/div/div/div[2]/div[2]/div/div[2]/div/div/form/input")
            send_img_input.send_keys(img_path)
            print(f"Изображение для {usernames} успешно отправлено!")
            time.sleep(random.randrange(2, 4))

        self.close_browser()

# Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8 # Part 8

# Unsubscribe method from all users (Метод отписки от всех пользователей)
    def unsubscribe_for_all_users(self, userpage):

        # Open our page (Открываем свою страницу)
        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        # Xpath of buttons with number of subscribers (Xpath кнопки с количеством подписчиков)
        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        # If the number of subscribers is more than 999, remove the commas from the number
        # (Если количество подписчиков больше 999, убираем из числа запятые)
        if ',' in following_count:
            following_count = int(''.join(following_count.split(',')))
        else:
            following_count = int(following_count)

        print(f"Количество подписок: {following_count}")

        time.sleep(random.randrange(2, 4))

        loops_count = int(following_count / 10) + 1
        print(f"Количество перезагрузок страницы: {loops_count}")

        following_users_dict = {}

        # After unsubscribing from 10 users (top), reload the page
        # (После отписки от 10 пользователей (верхних), перезагружаем страницу)
        for loop in range(1, loops_count + 1):

            count = 10
            browser.get(f"https://www.instagram.com/{username}/")
            time.sleep(random.randrange(3, 6))

            # Click / call the subscription menu (Кликаем/вызываем меню подписок)
            following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")

            following_button.click()
            time.sleep(random.randrange(3, 6))

            # We take all the li from the ul, they store the unsubscribe button and links to subscriptions
            # (Забираем все li из ul, в них хранится кнопка отписки и ссылки на подписки)
            following_div_block = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]/ul/div")
            following_users = following_div_block.find_elements_by_tag_name("li")
            time.sleep(random.randrange(3, 6))

            for user in following_users:

                if not count:
                    break

                user_url = user.find_element_by_tag_name("a").get_attribute("href")
                user_name = user_url.split("/")[-2]

                # Add a pair of username to the dictionary: link to the account, save the information
                # (Добавляем в словарь пару имя_пользователя: ссылка на аккаунт, сохраним информацию)
                following_users_dict[user_name] = user_url

                following_button = user.find_element_by_tag_name("button").click()
                time.sleep(random.randrange(3, 6))
                unfollow_button = browser.find_element_by_xpath("/html/body/div[5]/div/div/div/div[3]/button[1]").click()

                print(f"Итерация #{count} >>> Отписался от пользователя {user_name}")
                count -= 1

                time.sleep(random.randrange(120, 130))
                time.sleep(random.randrange(2, 4))

        self.close_browser()

    # Unsubscribe method, unsubscribe from everyone who does not follow us.
    # We collect a list of subscribers, then a list of subscriptions, then compare them, find those who are not subscribed to us and unsubscribe from them.
    # (Метод отписки, отписываемся от всех кто не подписан на нас).
    # (Собираем список подписчиков, потом список подписок, затем сравниваем их, находим тех кто не подписан на нас и отписываемся от их).
    def smart_unsubscribe(self, username):

        browser = self.browser
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        followers_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span")
        followers_count = followers_button.get_attribute("title")

        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_count = following_button.find_element_by_tag_name("span").text

        time.sleep(random.randrange(3, 6))

        # If the number of subscribers is more than 999, remove the commas from the number
        # (Если количество подписчиков больше 999, убираем из числа запятые)
        if ',' in followers_count or following_count:
            followers_count, following_count = int(''.join(followers_count.split(','))), int(''.join(following_count.split(',')))
        else:
            followers_count, following_count = int(followers_count), int(following_count)

        # We collect 12 people(Instagram no longer gives back)
        # (Собираем по 12 человек(Инстаграм больше не отдаёт))
        print(f"Количество подписчиков: {followers_count}")
        followers_loops_count = int(followers_count / 12) + 1
        print(f"Число итераций для сбора подписчиков: {followers_loops_count}")

        print(f"Количество подписок: {following_count}")
        following_loops_count = int(following_count / 12) + 1
        print(f"Число итераций для сбора подписок: {following_loops_count}")

        # Collecting a list of subscribers (Собираем список подписчиков)
        followers_button.click()
        time.sleep(4)

        followers_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        try:
            followers_urls = []
            print("Запускаем сбор подписчиков...")
            # Scroll the page by the number of scroll iterations (which we get from the number of subscribers / 12
            # (Скролим страницу на число итераций скрола(которое получим из числа подписчиков / 12))
            for i in range(1, followers_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            # Putting all li tags into a list (Собираем все теги li в список)
            all_urls_div = followers_ul.find_elements_by_tag_name("li")

            # Retrieving links (Извлекаем ссылки)
            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                followers_urls.append(url)

            # Save all user subscribers to a file (Сохраняем всех подписчиков пользователя в файл)
            with open(f"{username}_followers_list.txt", "a") as followers_file:
                for link in followers_urls:
                    followers_file.write(link + "\n")
        except Exception as ex:
            print(ex)
            self.close_browser()

        time.sleep(random.randrange(4, 6))

        # Reload the page (Перезагружаем страницу)
        browser.get(f"https://www.instagram.com/{username}/")
        time.sleep(random.randrange(3, 6))

        # Collecting a list of subscriptions(and doing the same)
        # (Собираем список подписок (и проделываем то же самое))
        following_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a")
        following_button.click()
        time.sleep(random.randrange(3, 5))

        following_ul = browser.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")

        try:
            following_urls = []
            print("Запускаем сбор подписок")

            for i in range(1, following_loops_count + 1):
                browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", following_ul)
                time.sleep(random.randrange(2, 4))
                print(f"Итерация #{i}")

            all_urls_div = following_ul.find_elements_by_tag_name("li")

            for url in all_urls_div:
                url = url.find_element_by_tag_name("a").get_attribute("href")
                following_urls.append(url)

            # Save all user subscriptions to a file (Сохраняем все подписки пользователя в файл)
            with open(f"{username}_following_list.txt", "a") as following_file:
                for link in following_urls:
                    following_file.write(link + "\n")

            # We compare two lists, if the user is in subscriptions, but he is not in subscribers, we add him to a separate list
            # (Сравниваем два списка, если пользователь есть в подписках, но его нет в подписчиках, заносим его в отдельный список)

            count = 0
            unfollow_list = []
            for user in following_urls:
                if user not in followers_urls:
                    count += 1
                    unfollow_list.append(user)
            print(f"Нужно отписаться от {count} пользователей")

            # Save everyone from whom you need to unsubscribe to a file
            # (Cохраняем всех от кого нужно отписаться в файл)
            with open(f"{username}_unfollow_list.txt", "a") as unfollow_file:
                for user in unfollow_list:
                    unfollow_file.write(user + "\n")

            print("Запускаем отписку...")
            time.sleep(2)

            # Go to each user on the page and unsubscribe
            # (Заходим к каждому пользователю на страницу и отписываемся)
            with open(f"{username}_unfollow_list.txt") as unfollow_file:
                unfollow_users_list = unfollow_file.readlines()
                unfollow_users_list = [row.strip() for row in unfollow_users_list]

            try:
                count = len(unfollow_users_list)
                for user_url in unfollow_users_list:
                    browser.get(user_url)
                    time.sleep(random.randrange(4, 6))

                    # Unsubscribe button (Кнопка отписки)
                    unfollow_button = browser.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button")
                    unfollow_button.click()

                    time.sleep(random.randrange(4, 6))

                    # Unsubscribe confirmation (Подтверждение отписки)
                    unfollow_button_confirm = browser.find_element_by_xpath("/html/body/div[4]/div/div/div/div[3]/button[1]")
                    unfollow_button_confirm.click()

                    print(f"Отписались от {user_url}")
                    count -= 1
                    print(f"Осталось отписаться от: {count} пользователей")

                    time.sleep(random.randrange(120, 130))
                    time.sleep(random.randrange(4, 6))

            except Exception as ex:
                print(ex)
                self.close_browser()

        except Exception as ex:
            print(ex)
            self.close_browser()

        time.sleep(random.randrange(4, 6))
        self.close_browser()

# Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7 # Part 7

# Switching between bot accounts (Переключение между аккаунтами ботов)
for user, user_data in users_settings_dict.items():
    username = user_data['login']
    password = user_data['password']
    window_size = user_data['window_size']

    my_bot = InstagramBot(username, password)
    my_bot.login()
    # my_bot.close_browser()
    # my_bot.get_all_followers('username')
    time.sleep(random.randrange(4, 8))
    my_bot.smart_unsubscribe("username")   # Enter the nickname here (Сюда вводим никнейм)

#my_bot = InstagramBot(username, password)
#my_bot.login()

#my_bot.send_direct_message(direct_users_list, "Hey! How's it going?", "E:\PyCharm all projects\Instagram bot\Part6_sending_messages_to_Direct\img2.jpg")
#my_bot.get_all_followers("https://www.instagram.com/evgenii_ponasenkov/")