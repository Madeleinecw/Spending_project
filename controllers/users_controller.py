from flask import Blueprint, Flask, redirect, render_template, request
from models.tag import Tag
import repositories.tag_repository as tag_repository
from models.user import User
import repositories.user_repository as user_repository
import repositories.merchant_repository as merchant_repository
import repositories.transaction_repository as transaction_repository

users_blueprint = Blueprint("users", __name__)

# index
@users_blueprint.route("/users")
def users():
    users = user_repository.select_all()
    return render_template("users/index.html", users=users)

# create new user
@users_blueprint.route("/users/new")
def new_user():
    return render_template("users/new.html")

# input page
@users_blueprint.route("/users", methods=["POST"])
def create_user():
    name = request.form["name"]
    budget = request.form["budget"]
    new_user = User(name, budget)
    user_repository.save(new_user)
    return render_template("/users/<id>/dashboard.html", user = new_user)

@users_blueprint.route("/users/<id>/dashboard", methods=["POST", "GET"])
def user_dashboard(id):
    user = user_repository.select(id)
    transactions = user_repository.select_transactions(user)
    total = 0
    for transaction in transactions:
        total += transaction.amount
    return render_template("/users/dashboard.html", user = user, total = total, transactions = transactions)

@users_blueprint.route("/users/welcome", methods = ["POST"])
def welcome():
    id = request.form["user.id"]
    user = user_repository.select(id)
    transactions = user_repository.select_transactions(user)
    total = 0
    tags = tag_repository.select_all()
    for transaction in transactions:
        total += transaction.amount
    return render_template("/users/dashboard.html", user = user, transactions = transactions, tags = tags, total = total)

@users_blueprint.route("/users/<id>", methods=["POST"])
def update_user(id):
    name = request.form["name"]
    budget = request.form["budget"]
    user = User(name, budget, id)
    user_repository.update(user)
    return redirect("/users/dashboard.html")

@users_blueprint.route("/users/dashboard", methods = ["POST"])
def signed_up():
    name = request.form["name"]
    budget = request.form["budget"]
    user = User(name, budget, id)
    user_repository.save(user)
    transactions = user_repository.select_transactions(user)
    return render_template("/users/first_visit.html", user = user, transactions = transactions)

@users_blueprint.route("/budgets/index")
def all_budgets():
    users = user_repository.select_all()
    budget_total = 0
    for user in users:
        budget_total += user.budget
    return render_template("/budgets/index.html", users = users, budget_total = budget_total)

@users_blueprint.route("/budgets/<id>/edit")
def edit(id):
    user = user_repository.select(id)
    return render_template("budgets/edit.html", user = user)


@users_blueprint.route("/budgets/<id>", methods=["POST"])
def update_budget(id):
    user = user_repository.select(id)
    name = user.name
    budget = request.form["budget"]
    updated_user = User(name, budget, id)
    user_repository.update(updated_user)
    users = user_repository.select_all()
    budget_total = 0
    for user in users:
        budget_total += user.budget
    return render_template("/budgets/index.html", users= users, budget_total = budget_total)

@users_blueprint.route("/users/<id>/delete", methods = ["POST"])
def delete_user(id):
    transactions = transaction_repository.select_all()
    user = user_repository.select(id)
    for transaction in transactions:
        if transaction.user.id == user.id:
            transaction_repository.delete(transaction.id)
    user_repository.delete(user.id)
    return redirect("/users")