from django.db import models
from django.forms import ModelForm

import src.impl.htmlproc as htmlproc

class Recipe(models.Model):
    cusine = models.CharField(max_length=50, default="N/A")
    title = models.CharField(max_length=200, default="N/A")
    author = models.CharField(max_length=50, default = "N/A")
    original_url = models.CharField(max_length=200, default= "N/A")
    pub_date =models.DateTimeField('date published', null=True)
    approved = models.IntegerField(default=0)

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
    name = models.CharField(max_length=50, default="N/A")
    part = models.CharField(max_length=100, default="N/A") 
    quantity = models.DecimalField(max_digits=15, decimal_places=4, null=True)
    measurement_unit = models.CharField(max_length=200, null=True)
    pre_comment = models.CharField(max_length=50,default='N/A')
    post_comment = models.CharField(max_length=50, default='N/A')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

def parseResult(result):
    recipe = Recipe()
    recipe.title = result[0][0]
    recipe.original_url = result[0][1]
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
            recipe.ingredients.add(ingredient)
    return recipe



class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cusine', 'approved']

class IngredientEntryForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ['quantity','measurement_unit','pre_comment', 'name','post_comment']

class Step(models.Model):
    position = models.IntegerField(default=0)
    text = models.CharField(max_length=10000)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ['position', 'text','recipe'] 


