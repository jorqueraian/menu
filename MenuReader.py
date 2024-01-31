import csv
import re
from enum import Enum
import random
import pandas as pd
import numpy as np

class RecipeInd_text_unused(Enum):
    """
    0: name of meal, 1: Recipe Type (Main, Side), 2: Number of servings, 
    3: list of ingredient pairs for example (1tsp, chicken), 4: list of instructions, 
    5: original recipe link if applicable, 6: allowed sides, 7: number of sides to include, 
    8: tags (spicy:medium, veggie, favorite)
    """
    NAME = "Recipe Name"
    TYPE = "Dish Type"
    NUM_SERVINGS = "Number of Servings"
    INGREDIENTS = "Ingredients"
    INSTRUCTIONS = "Instructions"
    LINK = "Original Recipe"
    ALLOWED_SIDES = "Allowed Sides"
    NUM_SIDES = "Number of sides"
    TAGS = "Flags"

class RecipeInd(Enum):
    """
    0: name of meal, 1: Recipe Type (Main, Side), 2: Number of servings, 
    3: list of ingredient pairs for example (1tsp, chicken), 4: list of instructions, 
    5: original recipe link if applicable, 6: allowed sides, 7: number of sides to include, 
    8: tags (spicy:medium, veggie, favorite)
    """
    NAME = 0
    TYPE = 1
    NUM_SERVINGS = 2
    INGREDIENTS = 3
    INSTRUCTIONS = 4
    LINK = 5
    ALLOWED_SIDES = 6
    NUM_SIDES = 7
    TAGS = 8


def read_menu(menu_csv, dish_type="main"):
    """
    This function takes in a string with the location of the recipe csv file and 
    returns a list of the recipes. Where each recipe is a list indexed based on the RecipeInd
    
    """
    with open(menu_csv, newline='') as csvfile:
        # reads in file and gives and iterator object of the rows of the file, ie the recipes
        recipes = csv.reader(csvfile, delimiter=',', quotechar='"')
        # Skip first line which is just the column header
        next(recipes)
        # Turning the iterator into a list
        
        recipe_arr = [row for row in recipes]  #[row for row in recipes if row[RecipeInd.TYPE.value].lower().strip() == dish_type]

        # TODO: Split by main meal, dinner/lunch, side and so on
        # Loop over recipes in the list 

        for j, row in enumerate(recipe_arr):
            # Parse ingredient list by commas and remove whitespaces
            ingredients = re.split(R",\s*", row[RecipeInd.INGREDIENTS.value])
            # Initialize list for parsed ingredients where each element will look like ("1tsp", "chicken") when applicable
            ing_pairs = [("","")]*len(ingredients)
            # initialize dictionary for tags, example "spicy:mild"
            tags = {}

            # loop through ingredient list to parse into quantity and ingredient pairs
            for i, ing in enumerate(ingredients):
                # in the text ingredients will have the first word being the quantity example: "1tsp chicken" if it exists. we may also have just "chicken" with no quantity
                # so we will split each ingredient into words
                ing_by_word = re.split(R"\s+", ing)
                #  then we will determine if the first word is a quantity or if no quantity is given
                ing_pairs[i]=(ing_by_word[0], ' '.join(ing_by_word[1:])) if re.match(R"[0-9]+[0-9-./]*\w*", ing_by_word[0]) else ("", ing)
            
            # from the tags text we want to parse the tags and put them in a dictionary such that the text "spicy:hot, salty" will be
            # encoded as {"spicy":"hot", "salty":"salty"}. first we split by , and then split by : if it exists
            for tag in re.split(R", *", row[RecipeInd.TAGS.value]):
                dic_pair = re.split(R":", tag)
                tags[dic_pair[0]] = dic_pair[1] if len(dic_pair) > 1 else dic_pair[0]

            # Parse instructions list
            instructions = re.split(R"\s*\(\d\)\s*", row[RecipeInd.INSTRUCTIONS.value])
            inst_arr = instructions

            for i, instruc in enumerate(inst_arr):
                inst_arr[i] = instruc

            inst_arr = list(filter(None, instructions))


            # Once text is parsed we will put the parsed info back into the original array. might be smart to generate a new list for better memory management but what ever
            recipe_arr[j][RecipeInd.INGREDIENTS.value]=ing_pairs
            recipe_arr[j][RecipeInd.INSTRUCTIONS.value]=inst_arr  # this is only so front end doesn't break but should de removed when parsing of instructions is done
            recipe_arr[j][RecipeInd.TAGS.value] = tags
        return [row for row in recipe_arr if row[RecipeInd.TYPE.value].lower().strip() == dish_type]


def generate_meal_plan(num_recipes, meals_per_day=1):
    # TODO: This might be tricky. we need to a way to take into account how many servings (maybe. i think we can ignore this)
    # a meal has and how many people will be eating. Maybe adding a way to remove items from the meal plan
    # this should also save the meal plan as a file and reload checking how old the file is. If its at least a day old and its monday
    # then a new meal plan will be created. Or if no file exists it will generate. For simplicity i think the meal plan should be saved as: [[4,3],[5],[1,12,6],....] where each element is a list
    # of that days and meals given by their index in the recipe array. But the function should return a list with more information. or maybe the flask should just generate the info for its self.
    
    meal_plan = [ [] for _ in range(7)]
    recipe_indices = [i for i in range(num_recipes)]

    for day in range(len(meal_plan)):
        meal_plan[day] = random.sample(recipe_indices, meals_per_day)
    return meal_plan
 

def save_meal_plan(meal_plan):
    # TODO: Can probably just save directly to a file. google this. But we probably want to save as csv 
    # file(or honestly just a txt file) with days as the rows and each row being the meals
    pass


def remove_from_meal_plan(meal_plan, day, meal):
    meal_plan[day].remove(meal)
    save_meal_plan(meal_plan)



def generate_shopping_list(meal_plan):
    # TODO: also may be trick to add up ingredients and what not. do last
    pass


print(read_menu("menu.csv"))
#print(RecipeInd.INGREDIENTS.value)