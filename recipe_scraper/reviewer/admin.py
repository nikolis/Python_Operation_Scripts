from django.contrib import admin

from .models import Ingredient
from .models import IngredientEntry
from .models import Step
from .models import Recipe

admin.site.register(Ingredient)
admin.site.register(IngredientEntry)
admin.site.register(Step)
admin.site.register(Recipe)
