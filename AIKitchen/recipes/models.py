from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    image = models.ImageField(upload_to='recipe_images/')

    def __str__(self):
        return self.name
