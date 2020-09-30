from flask import Blueprint, Flask, redirect, render_template, request

from models.transaction import Transaction
import repositories.transaction_repository as transaction_repository
import repositories.user_repository as user_repository
import repositories.merchant_repository as merchant_repository
import repositories.tag_repository as tag_repository

transactions_blueprint = Blueprint("transactions", __name__)

@transactions_blueprint.route("/transactions")
def transactions():
    transactions = transaction_repository.select_all()
    total = 0
    for transaction in transactions:
        total += transaction.amount
    return render_template("transactions/index.html", transactions=transactions, total = total)

@transactions_blueprint.route("/transactions/new")
def new_transaction():
    merchants = merchant_repository.select_all()
    users = user_repository.select_all()
    tags = tag_repository.select_all()
    return render_template("/transactions/new.html", merchants = merchants, users = users, tags = tags)

@transactions_blueprint.route("/transactions/create", methods=["POST"])
def create_transaction():
    amount = request.form["amount"]
    user = user_repository.select(request.form["user"])
    merchant = merchant_repository.select(request.form["merchant"])
    tag = tag_repository.select(request.form["tag"])
    new_transaction = Transaction(amount, user, merchant, tag)
    transaction_repository.save(new_transaction)
    tags = tag_repository.select_all()
    transactions = user_repository.select_transactions(user)
    total = 0
    for transaction in transactions:
        total += transaction.amount
    return render_template("/users/dashboard.html", user = user, transactions = transactions, total = total, tags = tags)

@transactions_blueprint.route("/transactions/<id>/delete", methods= ["POST"])
def delete(id):
    transaction_repository.delete(id)
    return redirect("/transactions")

@transactions_blueprint.route("/transactions/<id>")
def edit(id):
    transaction = transaction_repository.select(id)
    merchants = merchant_repository.select_all()
    tags = tag_repository.select_all()
    return render_template("/transactions/edit.html", transaction = transaction, user_id = transaction.user, merchants = merchants, tags = tags)

@transactions_blueprint.route("/transactions/<id>/edit", methods = ["POST"])
def update_transaction(id):
    transaction = transaction_repository.select(id)
    user = user_repository.select(transaction.user.id)
    amount = request.form['amount']
    merchant = merchant_repository.select(request.form['merchant'])
    tag = tag_repository.select(request.form['tag'])
    updated_transaction = Transaction(amount, user, merchant, tag, transaction.id)
    transaction_repository.update(updated_transaction)
    transactions = user_repository.select_transactions(user)
    tags = tag_repository.select_all()
    total = 0
    for transaction in transactions:
        total += transaction.amount
    return render_template("/users/dashboard.html", user = user, transactions = transactions, total = total, tags = tags)

