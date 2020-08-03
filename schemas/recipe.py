from ma import ma
from models.user import User


class RecipeSchema(ma.ModdelSchema):
    class Meta:
        fields = ('recipe_id', 'recipe_name', 'recipe_description', 'meal', 'time', 'ingredients', 'instructions')