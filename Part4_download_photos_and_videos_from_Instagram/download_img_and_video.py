from selenium import webdriver                      # Creates a browser (Создаёт браузер)
from selenium.webdriver.common.keys import Keys     # Keys (Кнопки)
from auth_data import username, password            # Login (Из auth_data берём наши данные для логина и пароля)
import time                                         # Time (Время)
import random                                       # Random (Рандом)
from selenium.common.exceptions import NoSuchElementException
import requests  # The library allows us to easily and with a minimum amount of code interact with web applications
                 # Библиотека позволяет нам легко и с минимальным количеством кода взаимодействовать с веб-приложениями
import os                                           # Creates a folder for downloaded files
                                                    # (Создаём папку для скачанных файлов)

# Create a class (Создаём класс)
class InstagramBot():

    # Create a constructor (Создаём конструктор)
    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("../chromedriver/chromedriver")

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

my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.download_userpage_content("https://www.instagram.com/evgenii_ponasenkov/")













