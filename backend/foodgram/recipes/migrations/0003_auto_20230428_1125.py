# Generated by Django 2.2.16 on 2023-04-28 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_auto_20230428_0819'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredienttorecipe',
            options={'verbose_name': 'Количество ингредиента в рецепте', 'verbose_name_plural': 'Количество ингредиентов в рецепте'},
        ),
        migrations.RemoveConstraint(
            model_name='ingredienttorecipe',
            name='recipe_ingredient_exists',
        ),
        migrations.RemoveConstraint(
            model_name='ingredienttorecipe',
            name='amount_gte_1',
        ),
        migrations.AddConstraint(
            model_name='ingredienttorecipe',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique ingredient recipe'),
        ),
    ]