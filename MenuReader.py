import csv
import re





def read_menu(menu_csv): # Im lazy so this will be poorly written 
    """
    This will give you a list of recipes each an array indexed as follow
    0: name, 1: Recipe Type (Main, Side), 2: Number of servings, 3: list of ingredient pairs, 4: string of instructions, 5: notes and links, 6: allowed sides as cs string, 7: number of sides to include
    """
    with open(menu_csv, newline='') as csvfile:
        recipes = csv.reader(csvfile, delimiter=',', quotechar='"')
        recipe_arr = [row for row in recipes][1:]
        for j, row in enumerate(recipe_arr):
            ingredients = re.split(R", *", row[3])
            ing_pairs = [("","")]*len(ingredients)
            for i, ing in enumerate(ingredients):
                ing_by_word = re.split(R" +", ing)
                ing_pairs[i]=(ing_by_word[0], ' '.join(ing_by_word[1:])) if re.match(R"[0-9]+[0-9-./]*\w*", ing_by_word[0]) else ("", ing)
            recipe_arr[j][3]=ing_pairs
        return recipe_arr


print(read_menu("menu.csv")[4])