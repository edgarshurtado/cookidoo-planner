import os
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome("./chromedriver")


def login():
    page_url = 'https://cookidoo.es/profile/es-ES/login?redirectAfterLogin=https://cookidoo.es/foundation/es-ES'

    driver.get(page_url)

    email_input = driver.find_element_by_id('email')
    email_input.send_keys(os.environ.get('user'))

    password_input = driver.find_element_by_id('password')
    password_input.send_keys(os.environ.get('pass'))

    driver.find_element_by_id('j_submit_id').click()

    print('login as {}'.format(os.environ.get('user')))


login(driver)
driver.close()

html = driver.page_source
# soup = BeautifulSoup(html, 'html.parser')
# title = soup.find('h1', attrs={'class': 'recipe-card__title'}).text
#
# ingredients = [ingredient.text for ingredient in soup.find(attrs={'id': 'ingredients'}).find_all('li')]
# ingredients = list(map(lambda x: ' '.join(x.split()), ingredients))
#
# print(title, ingredients)
