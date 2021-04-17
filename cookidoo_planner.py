import os
import random

from selenium import webdriver

driver = webdriver.Chrome("./chromedriver")
paella_url = 'https://cookidoo.es/recipes/recipe/es-ES/r121101'


def login():
    page_url = 'https://cookidoo.es/profile/es-ES/login?redirectAfterLogin=https://cookidoo.es/foundation/es-ES'

    driver.get(page_url)

    email_input = driver.find_element_by_id('email')
    email_input.send_keys(os.environ.get('user'))

    password_input = driver.find_element_by_id('password')
    password_input.send_keys(os.environ.get('pass'))

    driver.find_element_by_id('j_submit_id').click()

    print('login as {}'.format(os.environ.get('user')))


def add_recipe_to_shopping_list(recipe_url):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    recipe_id = recipe_url.split('/')[-1]
    driver.get(recipe_url)
    add_button = driver.find_element_by_id(f'add-trigger-{recipe_id}')
    add_button.click()

    add_to_list_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-action='Add to shopping list']"))
    )
    add_to_list_button.click()


def get_all_recipes_urls():
    driver.get('https://cookidoo.es/organize/es-ES/my-recipes')
    recipes_dom_elements = driver.find_elements_by_css_selector('core-tile a')
    recipes_urls = [recipe_element.get_attribute('href') for recipe_element in recipes_dom_elements]

    return recipes_urls


login()
my_recipes_urls = get_all_recipes_urls()

for i in range(3):
    recipe_url = my_recipes_urls.pop(random.randrange(len(my_recipes_urls)))
    add_recipe_to_shopping_list(recipe_url)

driver.close()
