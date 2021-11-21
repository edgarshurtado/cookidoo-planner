import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Recipe:
    class RecipeType:
        MEAL = 'meal',
        DINNER = 'DINNER'

    def __init__(self, url, name, list, ingredients):
        self.url = url
        self.name = name
        self.ingredients = ingredients
        self.list = list

    def __str__(self):
        return f'<Recipe> {self.name}'

    def has_ingredient(self, ingredient):
        return any([recipe_ingredient for recipe_ingredient in self.ingredients if
                    ingredient.lower() in recipe_ingredient.lower()])

    def ingredients_satisfied(self, ingredients):
        ingredients_satisfied = [ingredient for ingredient in ingredients if self.has_ingredient(ingredient)]
        return ingredients_satisfied


def recipe_has_ingredient(recipe, ingredient):
    return any([recipe_ingredient for recipe_ingredient in recipe.ingredients if
                ingredient.lower() in recipe_ingredient.lower()])
