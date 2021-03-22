import urllib.request
from bs4 import BeautifulSoup

page_url = 'https://cookidoo.es/recipes/recipe/es-ES/r55683'

html = ''

with urllib.request.urlopen(page_url) as response:
    html = response.read()

soup = BeautifulSoup(html, 'html.parser')
title = soup.find('h1', attrs={'class': 'recipe-card__title'}).text

ingredients = [ingredient.text for ingredient in soup.find(attrs={'id': 'ingredients'}).find_all('li')]
ingredients = list(map(lambda x: ' '.join(x.split()), ingredients))

print(title, ingredients)
