import re

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Recipe:
    def __init__(self, url, name, ingredients):
        self.url = url
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        return f'<Recipe> {self.name}'

    def add_to_shopping_list(self, driver):
        recipe_id = self.url.split('/')[-1]
        driver.get(self.url)
        add_button = driver.find_element_by_id(f'add-trigger-{recipe_id}')
        add_button.click()

        add_to_list_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "[data-action='Add to shopping list']"))
        )
        add_to_list_button.click()

    def has_ingredient(self, ingredient):
        return any([recipe_ingredient for recipe_ingredient in self.ingredients if
                    ingredient.lower() in recipe_ingredient.lower()])

    def ingredients_satisfied(self, ingredients):
        ingredients_satisfied = [ingredient for ingredient in ingredients if self.has_ingredient(ingredient)]
        return ingredients_satisfied



def get_all_recipes(driver, url):
    driver.get(url)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    a_tag_dom_elements = driver.find_elements_by_css_selector('core-tile a')
    names = soup.findAll('p', attrs={'class': 'core-tile__description-text'})

    names = [recipe_element.text for recipe_element in names]
    recipes_urls = [recipe_element.get_attribute('href') for recipe_element in a_tag_dom_elements]

    result = []
    for idx, url in enumerate(recipes_urls):
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul[id=ingredients-0]"))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ingredients = soup.select('ul[id^=ingredients] > li')
        ingredients = [cleanup_name(ingr.text) for ingr in ingredients]
        name = names[idx]
        result.append(Recipe(url=url, name=name, ingredients=ingredients))

    return result


def cleanup_name(string):
    return re.sub(r'\s+', ' ', string)
