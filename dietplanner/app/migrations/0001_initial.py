# Generated by Django 4.2.7 on 2023-11-04 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'ingredient',
            },
        ),
        migrations.CreateModel(
            name='Recipes',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('steps', models.TextField()),
                ('number_of_ingredients', models.IntegerField(null=True)),
            ],
            options={
                'db_table': 'recipes',
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.ingredients')),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.recipes')),
            ],
            options={
                'db_table': 'recipeingredient',
            },
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('recipe_id', 'ingredient_id'), name='unique_recipe_ingredient'),
        ),
    ]