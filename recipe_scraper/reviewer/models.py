from django.db import models
from django.forms import ModelForm

import src.impl.htmlproc as htmlproc

class Recipe(models.Model):
    cusine = models.CharField(max_length=50)
    title = models.CharField(max_length=200, default="N/A")
    author = models.CharField(max_length=50)
    original_url = models.CharField(max_length=200)
    pub_date =models.DateTimeField('date published')
    approved = models.IntegerField(default=0)
    
    @staticmethod
    def parseResult(result):
        recipe = Recipe()
        recipe.title = result[0][0]
        recipe.original_url = result[0][1]
        recipe.ingredients = result[0][2]
        return recipe

    @staticmethod
    def getRecipe(index):
        result = htmlproc.get_next_recipe()
        counter = 1
        for recipe in result:
            if(counter == int(index)):
                parsedRecipe =  Recipe.parseResult(recipe)
                return parsedRecipe
            counter +=1
    
class Ingredient(models.Model):
    name = models.CharField(max_length=50)

class IngredientEntry(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    measurement_unit = models.CharField(max_length=200)

class Step(models.Model):
    position = models.IntegerField(default=0)
    text = models.CharField(max_length=10000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cusine', 'approved']

class IngredientEntryForm(ModelForm):
    class Meta:
        model = IngredientEntry
        fields = ['ingredient', 'quantity','measurement_unit','recipe']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']
        
class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ['position', 'text','recipe'] 


