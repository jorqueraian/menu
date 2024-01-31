#My refusal to add anything to PATH is causing problems so run this to run C:\Users\jorqu\Documents\git_projects\menu\.conda\Scripts\flask --app run run
# I have not idea what im doing. im just following this: https://blog.appseed.us/flask-templates-curated-list-18vq/

# for future use on progressive web apps: https://www.reddit.com/r/flask/comments/euolxj/how_can_i_turn_my_flask_app_most_efficiently_into/ and https://web.dev/progressive-web-apps/

#templates came from here:: https://github.com/doersino/nyum/tree/main

from flask import Flask, render_template, redirect, url_for
from MenuReader import read_menu, generate_meal_plan, remove_from_meal_plan

app = Flask(__name__)

# These are basically our cookies
app.__RECIPES = None

#Running into problems here with pulling multiple meals 
app.__MEAL_PLAN = None
app.__DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]  # this is sloppy but i dont care


@app.route('/')
def calendar():
    """
    Homepage. first reads in menu file and then generates/loads meal plan
    """
    if app.__RECIPES is None:
        app.__RECIPES = read_menu("menu.csv")
    if app.__MEAL_PLAN is None:
        app.__MEAL_PLAN = generate_meal_plan(len(app.__RECIPES), 1)
    return render_template(R'index.template.html', mealplan=zip(range(len(app.__MEAL_PLAN)), app.__MEAL_PLAN), recipes=app.__RECIPES, days=app.__DAYS)
#Problem: Recipes aren't randomized, each time site is called (even after quitting), the same recipes are propoagated. 

@app.route('/all')
@app.route('/all/<tag>')
def all_recipes(tag=None):
    """
    List of all recipes
    """
    # todo have a way to get all tags, ex main, side drink and then populate the buttons that way. do abstractly
    if tag == None:
        menu_of_interest = app.__RECIPES
    else:
        menu_of_interest = read_menu("menu.csv", tag)
    return render_template(R'all-recipes.template.html', meals=[i for i in range(len(menu_of_interest))], recipes=menu_of_interest)

@app.route('/recipe/<id>')
def recipe(id):
    recipe_in_question = app.__RECIPES[int(id)]
    # title=recipe_in_question[0], ingredients=recipe_in_question[3], instructions=["do the thing", "then the second thing", "and so on"]
    return render_template(R'recipe.template.html', recipe=app.__RECIPES[int(id)])


@app.route('/remove/<day>/<id>')
def remove(day, id):
    remove_from_meal_plan(app.__MEAL_PLAN, app.__DAYS.index(day), int(id))
    return redirect(url_for('calendar'))

"""
#Should have some way to repopulate a recipe if one is trashed for the day
@app.route('/newrecipe/<day>/<id>') 
def newrecipe(day, id):

    Should have some way to pull a new recipe in just for the day needed. On button click. 

    return redirect(url_for('calendar'))
"""
"""
Not sure how to do this yet but
def load_meal_plan(shared_key):
    pass

def share_meal_plan(meal_plan):
    # generates some sharable thing
    pass

    Want to make a separate page that pull up shopping list for meal plan   
@app.route('/shopping/')
def shopping_list():
    generate_shopping_list()
"""

app.run()
