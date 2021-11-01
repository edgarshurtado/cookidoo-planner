import os
import time
import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from bs4 import BeautifulSoup
from selenium import webdriver

from recipes import Recipe


class CookidooScrapper:
    def __init__(self):
        self.driver = webdriver.Chrome("./chromedriver")

    def login(self):
        page_url = 'https://cookidoo.es/profile/es-ES/login?redirectAfterLogin=https://cookidoo.es/foundation/es-ES'

        self.driver.get(page_url)

        email_input = self.driver.find_element_by_id('email')
        email_input.send_keys(os.environ.get('user'))

        password_input = self.driver.find_element_by_id('password')
        password_input.send_keys(os.environ.get('pass'))

        self.driver.find_element_by_id('j_submit_id').click()

        print('login as {}'.format(os.environ.get('user')))

    def get_all_recipes(self, url, list_name):
        self.driver.get(url)

        self.scroll_to_the_end()

        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        a_tag_dom_elements = self.driver.find_elements_by_css_selector('core-tile a')
        names = soup.findAll('p', attrs={'class': 'core-tile__description-text'})

        names = [recipe_element.text for recipe_element in names]
        recipes_urls = [recipe_element.get_attribute('href') for recipe_element in a_tag_dom_elements]

        result = []
        for idx, url in enumerate(recipes_urls):
            self.driver.get(url)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul[id=ingredients-0]"))
            )
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            ingredients = soup.select('ul[id^=ingredients] > li')
            ingredients = [cleanup_name(ingr.text) for ingr in ingredients]
            name = names[idx]
            result.append(Recipe(url=url, name=name, list=list_name, ingredients=ingredients))

        return result

    def scroll_to_the_end(self):
        def get_scroll_height():
            return self.driver.execute_script("return document.body.scrollHeight")

        SCROLL_PAUSE_TIME = 0.5

        # Get scroll height
        last_height = get_scroll_height()

        while True:
            # Scroll down to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = get_scroll_height()
            if new_height == last_height:
                break
            last_height = new_height

    def add_recipe_to_shopping_list(self, recipe: Recipe):
        recipe_id = self.url.split('/')[-1]
        self.driver.get(self.url)
        add_button = self.driver.find_element_by_id(f'add-trigger-{recipe_id}')
        add_button.click()

        add_to_list_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-action='Add to shopping list']"))
        )
        add_to_list_button.click()


def cleanup_name(string):
    return re.sub(r'\s+', ' ', string)
