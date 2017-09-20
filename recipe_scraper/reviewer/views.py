from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Recipe,Ingredient
from .models import RecipeForm, IngredientForm, ScrapeForm
from django.forms import Form,modelformset_factory, inlineformset_factory
from django.urls import reverse
from django.shortcuts import get_list_or_404, get_object_or_404



def detail(request, recipe_id):
   recipe = get_object_or_404(Recipe, pk=recipe_id)
   return render(request, 'reviewer/detail.html', {'recipe' : recipe})

def result(request, recipe_id):
    response = "You're loking at the results of question %s"
    return HttpResponse(response % question_id)

def parse(request):
    if request.method =="GET":
        form = ScrapeForm()
        return render(request, 'reviewer/scrape.html', {'scrape_form':form})
    if request.method =="POST":
        form = ScrapeForm(request.POST)
        if form.is_valid():      
            url = form.cleaned_data['scrape_url']
            print(url)
            recipe=Recipe.getRecipe(url)
            RecipeFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=0)
            formSet = RecipeFormSet(instance = recipe)
    return render(request, 'reviewer/parse.html', {'formSet': formSet,'recipe':recipe})

def validate(request, recipe_id):
    RecipeFormSet = inlineformset_factory(Recipe, Ingredient, form=IngredientForm, extra=0)
    formset = RecipeFormSet(
        request.POST, request.FILES,
        queryset = Recipe.objects.filter(pk=recipe_id))
    if formset.is_valid():
        formset.save()
        print("asdfdsadf")
        recipe = Recipe.objects.filter(pk=recipe_id)
        return HttpResponseRedirect(reverse('reviewer:detail', args=(recipe_id,))) 
    return HttpResponse("failedTo approve approved"+recipe_id)

def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
    context= {
        'latest_recipe_list': latest_recipe_list, 
    }
    return render(request, 'polls/index.html', context)
     
