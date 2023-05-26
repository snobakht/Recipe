from django.shortcuts import render
from .models import Recipe
from .config import CHATGPT_API_KEY, DALLE_API_KEY
import openai
import requests
from .forms import RecipeForm

openai.api_key = CHATGPT_API_KEY
headers = {'Authorization': f'Token {DALLE_API_KEY}', 'Content_Type': 'application/json'}

def home(request):
    return render(request, 'home.html')
# Create your views here.
def generate_recipe_and_image(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']

            recipe = generate_recipe(ingredients)
            image = generate_image(ingredients)
            recipe_obj = Recipe.objects.create(name=recipe, ingredients=ingredients, image=image)
            return render(request, 'recipes/generate.html', {'recipe': recipe_obj, 'image': image})
    else:
        form = RecipeForm()
    return render(request, 'recipes/generate.html', {'form': form})


def generate_recipe(items ):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        prompt= "in one line describe food containing these items:"+ items,
        max_tokens=100
    )
    recipe = response['choices'][0]['message']['content']

    return recipe


def generate_image(items):
    data = {'prompt': items, 'n': 1}
    response = requests.post('https://api.openai.com/v1/images/generations', json=data, headers=headers)
    image_url = response.json()['output'][0]['image']
    return image_url
