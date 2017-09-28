class Recipe:
    def __init__(self, title=None, original_url=None, author=None, prep_time=None, cooking_time=None, servings=None):
        self.title = title
        self.ingredientEntrySets = []
        self.original_url = original_url
        self.author = author
        self.prep_time = prep_time
        self.cooking_time = cooking_time
        self.serving = servings

    def reprJSON(self):
        return dict(title=self.title, ingredientEntrySets=self.ingredientEntrySets)


class IngredientEntrySet:
    def __init__(self, title):
        self.title = title
        self.ingredientEntries = []

    def reprJSON(self):
        return dict(title=self.title, ingredientEntries=self.ingredientEntries)


class IngredientEntry:
    def __init__(self, quantity, measurement_unit, pre_comment, name, post_comment):
        self.quantity = quantity
        self.measurementUnit = measurement_unit
        self.preComment = pre_comment
        self.name = name
        self.postComment = post_comment

    def reprJSON(self):
        return dict(quantity=self.quantity, measurementUnit=self.measurementUnit, preComment=self.preComment,
                    name=self.name, postComment=self.postComment)
