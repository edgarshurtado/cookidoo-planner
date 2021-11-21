import unittest

from domain import create_menu
from recipes import Recipe, recipe_has_ingredient
from constants import Weekdays


class PlannerTests(unittest.TestCase):
    def setUp(self) -> None:
       self.my_meals = [
           Recipe('', 'Raviolis con salsa de berenjena', Recipe.RecipeType.MEAL, ['berenjenas', 'raviolis', 'parmesano']),
           Recipe('', 'Puré de calabaza', Recipe.RecipeType.MEAL, ['calabaza', 'nata']),
           Recipe('', 'Arroz a la cubana', Recipe.RecipeType.MEAL, ['arroz', 'huevo', 'tomate frito']),
           Recipe('', 'Paella', Recipe.RecipeType.MEAL, ['arroz', 'conejo', 'pimientos']),
       ]
       self.my_dinners = [
           Recipe('', 'Ensalada de piña', Recipe.RecipeType.DINNER, ['lechuga', 'jamón york', 'piña']),
           Recipe('', 'Sopa de fideos', Recipe.RecipeType.DINNER, ['caldo de pollo', 'fideos', '4 huevos']),
           Recipe('', 'Tortilla de patatas', Recipe.RecipeType.DINNER, ['huevos', 'patatas', 'cebolla']),
       ]

    def test_picks_1_meal_and_1_dinner_for_each_selected_day(self):
        my_meals = [
            Recipe('', 'A', Recipe.RecipeType.MEAL, []),
            Recipe('', 'B', Recipe.RecipeType.MEAL, []),
            Recipe('', 'C', Recipe.RecipeType.MEAL, [])
        ]

        my_dinners = [
            Recipe('', 'D', Recipe.RecipeType.DINNER, []),
            Recipe('', 'E', Recipe.RecipeType.DINNER, []),
            Recipe('', 'F', Recipe.RecipeType.DINNER, []),
        ]
        days = [Weekdays.SATURDAY, Weekdays.SUNDAY]
        result = create_menu(week_days=days, my_meals=my_meals, my_dinners=my_dinners)
        self.assertEqual(len(result), 2)
        self.assertEqual(len(result[0]), 2)
        self.assertEqual(len(result[1]), 2)

    def test_stops_when_runs_out_of_meals_or_dinners(self):
        my_meals = [
            Recipe('', 'A', Recipe.RecipeType.MEAL, []),
            Recipe('', 'B', Recipe.RecipeType.MEAL, []),
            Recipe('', 'C', Recipe.RecipeType.MEAL, []),
            Recipe('', 'X', Recipe.RecipeType.MEAL, [])
        ]

        my_dinners = [
            Recipe('', 'D', Recipe.RecipeType.DINNER, []),
            Recipe('', 'E', Recipe.RecipeType.DINNER, []),
            Recipe('', 'F', Recipe.RecipeType.DINNER, []),
        ]
        days = [Weekdays.MONDAY, Weekdays.TUESDAY, Weekdays.WEDNESDAY, Weekdays.THURSDAY, Weekdays.FRIDAY]
        result = create_menu(week_days=days, my_meals=my_meals, my_dinners=my_dinners)
        self.assertEqual(len(result), 3)

    def test_do_not_pick_any_recipe_if_ingredients_requirement_can_not_be_satisfied(self):
        days = ['jueves']
        ingredients_list = ['pollo']

        my_meals = [
            Recipe('', 'Puré de calabaza', Recipe.RecipeType.MEAL, ['calabaza', 'nata']),
            Recipe('', 'Arroz a la cubana', Recipe.RecipeType.MEAL, ['arroz', 'huevo', 'tomate frito']),
        ]
        my_dinners = [
            Recipe('', 'Ensalada de piña', Recipe.RecipeType.DINNER, ['lechuga', 'jamón york', 'piña']),
            Recipe('', 'Tortilla de patatas', Recipe.RecipeType.DINNER, ['huevos', 'patatas', 'cebolla']),
        ]
        result = create_menu(week_days=days, my_meals=my_meals, my_dinners=my_dinners,
                             ingredients=ingredients_list)

        self.assertEqual(len(result), 0)

    def test_uses_given_ingredients_at_least_in_one_recipe(self):
        days = ['jueves', 'sábado']
        ingredients_list = ['pollo', 'huevo']
        result = create_menu(week_days=days, my_meals=self.my_meals, my_dinners=self.my_dinners,
                             ingredients=ingredients_list)

        recipes_selected = []
        for meal, dinner in result:
            recipes_selected += [meal, dinner]

        for ingredient in ingredients_list:
            self.assertTrue(any([recipe for recipe in recipes_selected if recipe_has_ingredient(recipe, ingredient)]))


if __name__ == '__main__':
    unittest.main()
