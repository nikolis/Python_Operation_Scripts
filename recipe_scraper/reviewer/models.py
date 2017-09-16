from django.db import models

class Recipe(models.Model):
    cusine = models.CharField(max_length=50)
    title = models.CharField(max_length=200, default="N/A")
    author = models.CharField(max_length=50)
    original_url = models.CharField(max_length=200)
    pub_date =models.DateTimeField('date published')
    approved = models.IntegerField(default=0)

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

class IngredientEntry(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    measurement_unit = models.CharField(max_length=200)

class Step(models.Model):
    position = models.IntegerField(default=0)
    test = models.CharField(max_length=10000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

