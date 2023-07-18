from random import random
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import csv

from .top_secret_file import LOGIN, PASSWORD

count_string, count_main_link = 0, 0
ua = UserAgent()
options = webdriver.ChromeOptions()
options.add_argument(ua.random)
options.add_argument('--disable-blink-features=AutomationControlled')

txt_file = open('repeat_list.txt', 'r', encoding='utf-8')
repeat_list = set(txt_file.read().split(', '))
txt_file.close()
with webdriver.Chrome(options=options) as browser:
    browser.get('https://wordstat.yandex.ru/')
    sleep(2 + random()*5)
    login = browser.find_elements(By.CLASS_NAME, 'b-link_pseudo_yes')
    for i in login:
        if i.text == 'Войти':
            i.click()
    sleep(random()*3)
    browser.find_element(By.ID, 'b-domik_popup-username').send_keys(LOGIN)
    browser.find_element(By.ID, 'b-domik_popup-password').send_keys(PASSWORD)
    button = browser.find_elements(By.CLASS_NAME, 'b-form-button__input')
    button[1].click()
    sleep(0.5 + random()*3)
    with open('loyalty.csv', 'a', encoding='utf-8-sig', newline='') as file:
        # цикл для перехода по страницам
        for page in range(31, 42):
            browser.get(f'https://wordstat.yandex.ru/#!/?page={page}&words=%D0%BB%D0%BE%D1%8F%D0%BB%D1%8C%D0%BD%D0%BE%D1%81%D1%82%D1%8C')
            sleep(3 + random()*3)
            # находим все запросы и их количество
            for i in range(len(request_text := browser.find_elements(By.CLASS_NAME, 'b-phrase-link__link'))):
                try:
                    request_text = browser.find_elements(By.CLASS_NAME, 'b-phrase-link__link')
                    # переходим на второй уровень вложенности
                    link, name = request_text[i].get_attribute('href'), request_text[i].text
                    print(f'Текст: {name} ||||| Ссылка: {link}')
                    browser.get(link)
                    sleep(2 + random()*3)
                    text = browser.find_elements(By.CLASS_NAME, 'b-phrase-link__link')
                    number = browser.find_elements(By.CLASS_NAME, 'b-word-statistics__td-number')
                    count_main_link += 1
                except Exception:
                    print('Что-то пошло не так во втором цикле!')
                for j in range(len(text)):
                    try:
                        phrase = text[j].text.lower()
                        requests_amount = number[j].text
                        if 'лояль' not in phrase:
                            print('Нет слова лояльность')
                            continue
                        elif phrase in repeat_list or 'статистика по словам' in phrase:
                            print(f'Повтор {phrase} + {requests_amount}')
                            continue
                        lst_second = [phrase, requests_amount]
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow(lst_second)
                        count_string += 1
                        print(f'Записали в файл фразу: {phrase}, количество запросов: {requests_amount}, номер главной ссылки: {count_main_link}, номер записанной строки: {count_string}, текущая страница {page}')
                        if phrase not in repeat_list:
                            repeat_list.add(phrase)
                        rl = open('repeat_list.txt', 'a', encoding='utf-8')
                        rl.write(', '.join(repeat_list))
                        rl.close()
                    except Exception:
                        print('Что-то пошло не так в третьем цикле!')
                browser.back()
                sleep(2 + random()*3)
