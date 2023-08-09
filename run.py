#My refusal to add anything to PATH is causing problems so run this to run C:\Users\jorqu\Documents\git_projects\menu\.conda\Scripts\flask --app run run
# I have not idea what im doing. im just following this: https://blog.appseed.us/flask-templates-curated-list-18vq/

#templates came from here:: https://github.com/doersino/nyum/tree/main

from flask import Flask, render_template
from MenuReader import read_menu, generate_meal_plan

app = Flask(__name__)

app.__RECIPES = None
app.__MEAL_PLAN = [["Monday", [[1,"food name 1", {"spicy":True, "favorite":True}], [2,"food name 2", {"favorite":True}]]], ["Tuesday", [[3,"food name 3", {"veggie":True}]]],["Wednesday", [[1,"food name 1", {"veggie":True}]]],["Thursday", [[3,"food name 3", {"veggie":True}]]]]

@app.route('/')
def calendar():
    if app.__RECIPES is None:
        app.__RECIPES = read_menu("menu.csv")
    if app.__MEAL_PLAN is None:
        app.__MEAL_PLAN = generate_meal_plan(app.__RECIPES)
    return render_template(R'index.template.html', mealplan=app.__MEAL_PLAN)


@app.route('/recipe/<id>')
def recipe(id):
    recipe_in_question = app.__RECIPES[int(id)]
    return render_template(R'recipe.template.html', title=recipe_in_question[0], ingredients=recipe_in_question[3], instructions=["do the thing", "then the second thing", "and so on"])
