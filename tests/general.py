import unittest

from domain import create_menu
from recipes import Recipe, recipe_has_ingredient


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
       self.my_meals = [
           Recipe('', 'Raviolis con salsa de berenjena', ['berenjenas', 'raviolis', 'parmesano']),
           Recipe('', 'Puré de calabaza', ['calabaza', 'nata']),
           Recipe('', 'Arroz a la cubana', ['arroz', 'huevo', 'tomate frito']),
           Recipe('', 'Paella', ['arroz', 'conejo', 'pimientos']),
       ]
       self.my_dinners = [
           Recipe('', 'Ensalada de piña', ['lechuga', 'jamón york', 'piña']),
           Recipe('', 'Sopa de fideos', ['caldo de pollo', 'fideos', '4 huevos']),
           Recipe('', 'Tortilla de patatas', ['huevos', 'patatas', 'cebolla']),
       ]

    def test_creates_menu_plan(self):
        days = ['jueves', 'sábado']
        result = create_menu(week_days=days, my_meals=self.my_meals, my_dinners=self.my_dinners)
        self.assertEqual(len(result), 2)

    def test_do_not_fail_if_not_enough_recipes(self):
        days = ['jueves', 'sábado', 'lunes', 'miércoles']
        result = create_menu(week_days=days, my_meals=self.my_meals, my_dinners=self.my_dinners)
        self.assertEqual(len(result), 3)  # 3 because we have only 3 dinner recipes

    def test_do_not_pick_any_recipe_if_ingredients_requirement_can_not_be_satisfied(self):
        days = ['jueves']
        ingredients_list = ['pollo']

        my_meals = [
            Recipe('', 'Puré de calabaza', ['calabaza', 'nata']),
            Recipe('', 'Arroz a la cubana', ['arroz', 'huevo', 'tomate frito']),
        ]
        my_dinners = [
            Recipe('', 'Ensalada de piña', ['lechuga', 'jamón york', 'piña']),
            Recipe('', 'Tortilla de patatas', ['huevos', 'patatas', 'cebolla']),
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
            recipes_selected.append(meal)
            recipes_selected.append(dinner)

        for ingredient in ingredients_list:
            self.assertTrue(any([recipe for recipe in recipes_selected if recipe_has_ingredient(recipe, ingredient)]))


if __name__ == '__main__':
    unittest.main()
