import os
import random
from bs4 import BeautifulSoup

from selenium import webdriver

driver = webdriver.Chrome("./chromedriver")

meals_list_url = 'https://cookidoo.es/organize/es-ES/my-recipes'
dinners_list_url = 'https://cookidoo.es/organize/es-ES/custom-list/01F4PXQKYQ0W4X0WT6Q8PB0J7M'


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


def get_all_recipes_urls(url):
    driver.get(url)

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    a_tag_dom_elements = driver.find_elements_by_css_selector('core-tile a')
    names = soup.findAll('p', attrs={'class': 'core-tile__description-text'})

    names = [recipe_element.text for recipe_element in names]
    recipes_urls = [recipe_element.get_attribute('href') for recipe_element in a_tag_dom_elements]

    result = []
    for idx, url in enumerate(recipes_urls):
        name = names[idx]
        result.append((url, name))

    return result


ingredients_to_prioritize = input('Ingredients to prioritize: ')
ingredients_to_prioritize = list(map(lambda x: x.strip(), ingredients_to_prioritize.split(',')))
print(ingredients_to_prioritize)


login()
my_meals_urls = get_all_recipes_urls(meals_list_url)
my_dinners_urls = get_all_recipes_urls(dinners_list_url)

selected_recipes = []


for i in range(2):
    meal, dinner = (my_meals_urls.pop(random.randrange(len(my_meals_urls))),
                    my_dinners_urls.pop(random.randrange(len(my_dinners_urls))))
    meal_url, meal_name = meal
    dinner_url, dinner_name = dinner
    add_recipe_to_shopping_list(meal_url)
    add_recipe_to_shopping_list(dinner_url)

    selected_recipes.append((meal_name, dinner_name))


week_days = ['lunes', 'martes']

template_meal = '{:>12} ☀️ {}'
template_dinner = '{:>12}️ 🌚 {}'

for idx, day in enumerate(week_days):
    meal, dinner = selected_recipes[idx]
    print(template_meal.format(day, meal))
    print(template_dinner.format('', dinner))

driver.close()
