from django.db import models
from django.forms import ModelForm
from  django.forms.widgets import TextInput

import src.impl.htmlproc as htmlproc

class Recipe(models.Model):
    cusine = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=50, null=True)
    original_url = models.CharField(max_length=200, null = True)
    prep_time = models.CharField(max_length=50, null=True)
    cooking_time = models.CharField(max_length=50, null=True)
    servings = models.CharField(max_length=50, null=True)
    author = models.CharField(max_length=50, null = True)
    approved = models.BooleanField(default=False)
    steps = models.CharField(max_length=10000,null = True)

    @staticmethod
    def getRecipe(index):
        result = htmlproc.get_next_recipe()
        counter = 1
        for recipe in result:
            if(counter == int(index)):
                parsedRecipe =  parseResult(recipe)
                return parsedRecipe
        counter +=1

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    part = models.CharField(max_length=100) 
    quantity = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    measurement_unit = models.CharField(max_length=200, null=True)
    pre_comment = models.CharField(max_length=50, null=True)
    post_comment = models.CharField(max_length=50, null=True)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

def parseResult(result):
    recipe = Recipe()
    recipe.title = result[0][0]
    recipe.original_url = result[0][1]
    recipe.steps = result[0][3]
    recipe.prep_time = result[0][4]
    recipe.cooking_time = result[0][5]
    recipe.servings = result[0][6]
    recipe.author = result[0][7]
    recipe.save()
    for part in result[0][2]:
        for member in result[0][2][part]:
            ingredient = Ingredient() 
            ingredient.name=member[3]
            ingredient.part=part
            ingredient.measurement_unit = member[1]
            ingredient.quantity = member[0]
            ingredient.pre_comment = member[2]
            ingredient.post_comment = member[4]
            ingredient.recipe = recipe
            ingredient.save()
            ingredient.recipe = recipe 
    return recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cusine', 'approved']

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['part','quantity','measurement_unit','pre_comment', 'name','post_comment']
        #widgets = { 'part': TextInput(attrs={'class':'form-control form-control-lg'})}
class Step(models.Model):
    position = models.IntegerField(default=0)
    text = models.CharField(max_length=10000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ['position', 'text','recipe'] 

