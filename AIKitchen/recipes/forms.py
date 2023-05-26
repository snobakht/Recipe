from django import forms


class RecipeForm(forms.Form):
    ingredients = forms.CharField \
        (widget=forms.Textarea, label='Enter Ingredients', max_length=1000)
