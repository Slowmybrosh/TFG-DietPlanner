from sqlalchemy import Table, Column, Integer, String, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()
class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)

class Recipes(Base):
    __tablename__ = "recipes"
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String)
    steps = Column(String)
    numberofingredients = Column(Integer)

class RecipeIngredient(Base):
    __tablename__ = "recipeingredient"
    __table_args__ = (
        PrimaryKeyConstraint('recipe_id', 'ingredient_id'),
    )

    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    ingredient_id = Column(Integer, ForeignKey('ingredients.id'))