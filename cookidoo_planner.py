import os
import random
from recipes import get_all_recipes

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


# ingredients_to_prioritize = input('Ingredients to prioritize: ')
# ingredients_to_prioritize = list(map(lambda x: x.strip(), ingredients_to_prioritize.split(',')))
# print(ingredients_to_prioritize)


login()
my_meals = get_all_recipes(driver, meals_list_url)
my_dinners = get_all_recipes(driver, dinners_list_url)

selected_recipes = []


week_days = ['jueves', 'sábado', 'lunes']

for i in range(len(week_days)):
    meal, dinner = (my_meals.pop(random.randrange(len(my_meals))),
                    my_dinners.pop(random.randrange(len(my_dinners))))

    meal.add_to_shopping_list(driver)
    dinner.add_to_shopping_list(driver)

    selected_recipes.append((meal, dinner))


template_meal = '{:>12} ☀️ {}'
template_dinner = '{:>12}️ 🌚 {}'

for idx, day in enumerate(week_days):
    meal, dinner = selected_recipes[idx]
    print(template_meal.format(day, meal))
    print(template_dinner.format('', dinner))

driver.close()
