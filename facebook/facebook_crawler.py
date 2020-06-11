import json
import random
import re
import time
from queue import Queue

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from create_csv import create_csv


class FacebookCrawler:
    LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'  # login page

    def __init__(self, login, password):
        chrome_options = webdriver.ChromeOptions()

        prefs = {"profile.default_content_setting_values.notifications": 2}  # chrome settings
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-blink-features")  # попытка избежать блока
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(chrome_options=chrome_options,
                                       executable_path=r'C:\Users\Zver\Downloads\chromedriver_win32\chromedriver.exe')
        self.wait = WebDriverWait(self.driver, 10)  # дает драйверу подождать несколько секунд, перед следующим действием

        self.page_link = ''

        self.links = None

        self.links_items = None

        self.str = ''

        self.storage = {}

        self.id = ''

        self.counter = 0

        self.friends_names = Queue()
        self.arr_fr_pages = Queue()  # links of fr-s pages

        self.login(login, password)

    def login(self, login, password):
        self.driver.get(self.LOGIN_URL)

        # wait for the login page to load
        self.wait.until(EC.visibility_of_element_located((By.ID, "email")))

        self.driver.find_element_by_id('email').send_keys(login)
        self.driver.find_element_by_id('pass').send_keys(password)
        self.driver.find_element_by_id('loginbutton').click()

        # wait for the main page to load
        time.sleep(random.randrange(1, 5, 1))

        self.driver.find_element_by_class_name('_1vp5').click()  # open my homepage

        self.page_link = self.driver.current_url  # get link of initial page

        self.driver.get(self.page_link)  # open initial page
        time.sleep(random.randrange(1, 5, 1))

    def write_in_json(self):
        f = open('friends.json', 'w', encoding="utf-8")
        f.write(json.dumps(self.storage, indent=4, ensure_ascii=False, sort_keys=False))
        f.close()

        create_csv()  # создаю DataFrame

        self.driver.close()

    def get_id(self, link) -> str:
        try:
            self.driver.get(link)  # open profile page
            time.sleep(random.randrange(1, 5, 1))
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.links = soup.find_all(class_='_1nv3 _11kg _1nv5 profilePicThumb')  # get link including id
            for link in self.links:
                str_link = str(link['href'])
                _id = re.search(r'_id=[0-9]*', str_link)  # parse link to get id
                str_id = _id.group()
                id_num = str_id.strip('_id=')
                return id_num
        except:
            self.write_in_json()

    def get_init_name(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        name = soup.find_all(class_='_2nlw _2nlv')
        for n in name:
            main_user_name = n.get_text()
            return main_user_name

    def get_links_info_friends(self):  # return links (info & friends)
        try:
            arr_links = []
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.links = soup.find(class_='_70k')  # this class stores info,friends,photo,arch
            self.links_items = self.links.find_all('a')
            for link in self.links_items:  # get info,friends,photo,arch active links from my page
                my_str = link.get_text()

                if my_str.find('Друзья') != -1:
                    self.str = link.get('href', None)
                    arr_links.append(self.str)
                elif my_str.find('Информация') != -1:
                    self.str = link.get('href', None)
                    arr_links.append(self.str)
            return arr_links
        except:
            self.write_in_json()

    def get_info(self, link) -> dict:
        try:
            d_info = dict()

            self.driver.get(link)  # open page with info
            time.sleep(random.randrange(1, 5, 1))

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            self.links = soup.find_all(class_='_c24 _50f4')  # get job, education, city,
            if self.links is None:  # ЕСЛИ НЕТ ИНФЫ О job, education, city
                d_info['NO_info'] = '-'
            else:
                for word in self.links:
                    soup_2 = BeautifulSoup(str(word), 'html.parser')
                    text = soup_2.get_text('\t')
                    sep_text = text.strip().split('\t')
                    if len(sep_text) == 1:
                        d_info['some_info'] = sep_text[0]
                    else:
                        _study = re.search(r'Учи[а-я]*', sep_text[0])  # parse
                        _study_2 = re.search(r'Изуча[а-я]*', sep_text[0])  # parse

                        if (_study_2 is not None) or (_study is not None):
                            d_info['study'] = sep_text[1]
                        elif sep_text[0].find('Живет') != -1:
                            d_info['live_in'] = sep_text[1]

            self.links = soup.find_all(class_='_c24 _2ieq')  # get num, vk (or other social net), b-day
            if self.links is None:  # ЕСЛИ НЕТ ИНФЫ О job, education, city
                d_info['NO_info'] = '-'
            else:
                for link in self.links:
                    soup_3 = BeautifulSoup(str(link), 'html.parser')
                    text = soup_3.get_text('\t')
                    sep_text = text.strip().split('\t')

                    if sep_text[0].find('Телефоны') != -1:
                        d_info['phone'] = sep_text[1]
                    elif sep_text[0].find('Дата рождения') != -1:
                        d_info['b-day'] = sep_text[1]
                    elif sep_text[0].find('Ссылки на профили в Сети') != -1:
                        d_info['links'] = sep_text[1]
                    elif sep_text[0].find('Электронный адрес') != -1:
                        d_info['email'] = sep_text[1]

            return d_info
        except:
            self.write_in_json()

    def get_friends(self, link) -> list:
        try:
            self.driver.get(link)  # open page with my friends
            time.sleep(random.randrange(1, 5, 1))

            # scroll
            elems = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_698"))) # all fr users
            length = len(elems) # смотрю сколько чел загрузилось
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(random.randrange(6, 10))  # to load all elems

            elem1 = WebDriverWait(self.driver, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "_698")))
            second_length = len(elem1)

            while second_length > length:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                time.sleep(random.randrange(6, 10))  # to load all elems

                elem1 = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "_698")))
                length = second_length
                second_length = len(elem1)

            time.sleep(random.randrange(1, 5, 1))

            arr_of_friends = []  # names of user's friends

            soup = BeautifulSoup(self.driver.page_source, "html.parser")

            for i in soup.find_all('div', {'class': 'fsl fwb fcb'}):  # имена друзей
                names = i.find_all('a', href=True)
                for name in names:
                    if name is None:
                        continue
                    page_link = name['href']
                    self.arr_fr_pages.put(page_link)  # put in queue
                    self.friends_names.put(name.get_text())  # put a friend name in queue
                    arr_of_friends.append(name.get_text())  # add a friend name
            return arr_of_friends
        except:
            self.write_in_json()


def bfs(crawler_instance):
    visited = set()  # names of visited people

    while not crawler_instance.friends_names.empty():
        name = crawler_instance.friends_names.get()
        if name not in visited:
            visited.add(name)  # add name in visited
            try:
                page_link = crawler_instance.arr_fr_pages.get()  # взяла из очереди ссылку на стр человека

                user_id = crawler_instance.get_id(page_link)
                user_name = name

                arr_links_inf_fr = crawler_instance.get_links_info_friends()  # return 2 links to open inf and fr pages

                user_information = crawler_instance.get_info(arr_links_inf_fr[0])
                user_friends = crawler_instance.get_friends(arr_links_inf_fr[1])

                fill_storage(crawler_instance, user_id, user_name, user_information,
                             user_friends)  # add new person in stor

            except TimeoutException:
                crawler_instance.write_in_json()
        else:
            crawler_instance.arr_fr_pages.get()  # удаляю ссыдку на стр, если уже смотрели такого Пользователя


def fill_storage(crawler_instance, user_id: str, user_name: str, d_information: dict, friends: list):
    crawler_instance.counter += 1

    if crawler_instance.counter < 150:  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        d_information['name'] = user_name

        d_friends_list = dict()
        d_friends_list['friends'] = friends

        d_user = dict()
        d_user['general_info'] = d_information
        d_user['friends_list'] = d_friends_list
        crawler_instance.storage[user_id] = d_user

    else:
        return '150 FRIENDS'  # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def main():
    # crawler = FacebookCrawler(login='79037332943', password='мщшц38епцщг')
    crawler = FacebookCrawler(login='irkaxortiza@mail.ru', password='17YouWannaBeOnTop1995')

    # INITIAL ADDING
    id = crawler.get_id(crawler.page_link)  # only main user id

    user_name = crawler.get_init_name()

    arr_links_inf_fr = crawler.get_links_info_friends()  # return 2 links to open inf and fr pages
    arr_info = crawler.get_info(arr_links_inf_fr[0])  # call method to get info from page
    arr_friends = crawler.get_friends(arr_links_inf_fr[1])  # call method to get list of friends from page

    fill_storage(crawler, id, user_name, arr_info, arr_friends)

    bfs(crawler)  # call bfs from my friends


if __name__ == '__main__':
    main()
