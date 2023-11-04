from django.db import models

class Ingredients(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'ingredient'

class Recipes(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    steps = models.TextField()
    number_of_ingredients = models.IntegerField(null=True)

    class Meta:
        db_table = 'recipes'

class RecipeIngredient(models.Model):
    recipe_id = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient_id = models.ForeignKey(Ingredients, on_delete=models.CASCADE)

    class Meta:
        db_table = 'recipeingredient'
        constraints = [
            models.UniqueConstraint(fields=['recipe_id', 'ingredient_id'], name='unique_recipe_ingredient'),
        ]

