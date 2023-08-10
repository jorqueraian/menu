import csv
import re





def read_menu(menu_csv): # Im lazy so this will be poorly written 
    """
    This will give you a list of recipes each an array indexed as follow
    0: name, 1: Recipe Type (Main, Side), 2: Number of servings, 3: list of ingredient pairs, 4: string of instructions, 5: notes and links, 6: allowed sides, 7: number of sides to include, 8: flags (spicy, veggie, favorite)
    """
    with open(menu_csv, newline='') as csvfile:
        recipes = csv.reader(csvfile, delimiter=',', quotechar='"')
        recipe_arr = [row for row in recipes][1:]
        # TODO: Split by main meal, dinner/lunch, side and so on
        for j, row in enumerate(recipe_arr):
            ingredients = re.split(R", *", row[3])
            ing_pairs = [("","")]*len(ingredients)
            for i, ing in enumerate(ingredients):
                ing_by_word = re.split(R" +", ing)
                ing_pairs[i]=(ing_by_word[0], ' '.join(ing_by_word[1:])) if re.match(R"[0-9]+[0-9-./]*\w*", ing_by_word[0]) else ("", ing)
            # TODO: also need to do same thing but for instructions probably splitting on something of the form (\d)
            # TODO: Parse tags string and put in dictionary: example: {"spicy":True, "favorite":True}
            recipe_arr[j][3]=ing_pairs
            recipe_arr[j][4]=[recipe_arr[j][4]]  # this is only so front end doesn't break but should de removed when parsing of instructions is done
        return recipe_arr
    

def generate_meal_plan(recipes):
    # This might be tricky. we need to a way to take into account how many servings 
    # a meal has and how many people will be eating. Maybe adding a way to remove items from the meal plan
    # this should also save the meal plan as a file and reload checking how old the file is. If its at least a day old and its monday
    # then a new meal plan will be created. Or if no file exists it will generate. For simplicity i think the meal plan should be saved as: [[4,3],[5],[1,12,6],....] where each element is a list
    # of that days and meals given by their index in the recipe array. But the function should return a list with more information. or maybe the flask should just generate the info for its self.
    pass


def save_meal_plan(meal_plan):
    # TODO: Can probably just save directly to a file.
    pass


def remove_from_meal_plan(meal_plan, day, meal):
    meal_plan[day].remove(meal)
    save_meal_plan(meal_plan)


def generate_shopping_list(meal_plan):
    #also may be trick to add up ingredients and what not. do last
    pass



#print(read_menu("menu.csv")[0])