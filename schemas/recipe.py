from ma import ma
from models.recipe import Recipe


class RecipeSchema(ma.Schema):
    class Meta:
        fields = ('recipe_id', 'recipe_name', 'recipe_description', 'meal', 'time', 'ingredients', 'instructions')


recipe_schema = RecipeSchema()
recipes_schema = RecipeSchema(many=True)