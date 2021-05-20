import os
import random

from selenium import webdriver

from recipes import get_all_recipes

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


key_ingredients = input('Ingredients to prioritize: ')
key_ingredients = list(map(lambda x: x.strip(), key_ingredients.split(',')))
print(key_ingredients)


driver = webdriver.Chrome("./chromedriver")
login()

my_meals = get_all_recipes(driver, meals_list_url)
my_dinners = get_all_recipes(driver, dinners_list_url)

selected_recipes = []


week_days = ['martes', 'jueves', 'sábado']

while len(selected_recipes) < len(week_days):
    meal_candidate_idx, dinner_candidate_idx = (random.randrange(len(my_meals)), random.randrange(len(my_dinners)))

    meal_candidate = my_meals[meal_candidate_idx]
    dinner_candidate = my_dinners[dinner_candidate_idx]

    if len(key_ingredients) > 0:
        meal_key_ingredients = meal_candidate.ingredients_satisfied(key_ingredients)
        dinner_key_ingredients = dinner_candidate.ingredients_satisfied(key_ingredients)

        key_ingredients_satisfied = meal_key_ingredients + dinner_key_ingredients
        print(key_ingredients_satisfied)

        if len(key_ingredients_satisfied) > 0:
            key_ingredients = [ki for ki in key_ingredients if ki not in key_ingredients_satisfied]
        else:
            continue
    else:
        # Recover discarded recipes
        pass

    meal, dinner = (my_meals.pop(meal_candidate_idx), my_dinners.pop(dinner_candidate_idx))

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
