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
            image = generate_image(recipe)
            recipe_obj = Recipe.objects.create(name=recipe.split("THE_DISH_NAME_IS:")[1], ingredients=ingredients,
                                               order=recipe, image=image)
            return render(request, 'recipes/generate.html', {'recipe': recipe_obj, 'image': image})
    else:
        form = RecipeForm()
    return render(request, 'recipes/generate.html', {'form': form})


def generate_recipe(items):
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        # prompt= "in one line describe food containing these items:"+ items,
        max_tokens=100,
        messages=[
            {"role": "system", "content": "you are a good prompt engineer for dalle 2 image generator!"},
            {"role": "user", "content": "write one sentence about these ingredients: "+ items+" "+ "That is a certain "
                                                                                                   "cuisine and has "
                                                                                                   "these "
                                                                                                   "ingredients, "
                                                                                                   "also provide a "
                                                                                                   "name for that "
                                                                                                   "dish. make sure that you provide the name of the dish in your final sentence, exactly as, THE_DISH_NAME_IS: name_of_dish"},
            {"role": "assistant",
             "content": ""},
            {"role": "user", "content": ""}
        ]
    )
    recipe = response['choices'][0]['message']['content']

    return recipe


def generate_image(recipe):
    response = openai.Image.create(
        prompt=recipe,
        n=1,
        size="512x512"
    )
    image_url = response['data'][0]['url']
    return image_url
