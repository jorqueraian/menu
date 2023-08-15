#My refusal to add anything to PATH is causing problems so run this to run C:\Users\jorqu\Documents\git_projects\menu\.conda\Scripts\flask --app run run
# I have not idea what im doing. im just following this: https://blog.appseed.us/flask-templates-curated-list-18vq/

# for future use on progressive web apps: https://www.reddit.com/r/flask/comments/euolxj/how_can_i_turn_my_flask_app_most_efficiently_into/ and https://web.dev/progressive-web-apps/

#templates came from here:: https://github.com/doersino/nyum/tree/main

from flask import Flask, render_template, redirect, url_for
from MenuReader import read_menu, generate_meal_plan, remove_from_meal_plan

app = Flask(__name__)

app.__RECIPES = None
app.__MEAL_PLAN = [[1, 2], [3], [4, 3], [5,6], [7,8]]
#[["Monday", [[1,"food name 1", {"spicy":True, "favorite":True}], [2,"food name 2", {"favorite":True}]]], ["Tuesday", [[3,"food name 3", {"veggie":True}]]],["Wednesday", [[1,"food name 1", {"veggie":True}]]],["Thursday", [[3,"food name 3", {"veggie":True}]]]]
app.__DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]  # this is sloppy but i dont care


@app.route('/')
def calendar():
    if app.__RECIPES is None:
        app.__RECIPES = read_menu("menu.csv")
    if app.__MEAL_PLAN is None:
        app.__MEAL_PLAN = generate_meal_plan(app.__RECIPES)
    return render_template(R'index.template.html', mealplan=zip(range(len(app.__MEAL_PLAN)), app.__MEAL_PLAN), recipes=app.__RECIPES, days=app.__DAYS)


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
Not sure how to do this yet but
def load_meal_plan(shared_key):
    pass

def share_meal_plan(meal_plan):
    # generates some sharable thing
    pass
"""


app.run()