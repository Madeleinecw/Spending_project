from flask import Blueprint, Flask, redirect, render_template, request

from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository
import repositories.transaction_repository as transaction_repository

merchants_blueprint = Blueprint("merchants", __name__)

@merchants_blueprint.route("/merchants")
def merchants():
    merchants = merchant_repository.select_all()
    return render_template("merchants/index.html", merchants=merchants)

@merchants_blueprint.route("/merchants/new")
def new_merchant():
    return render_template("merchants/new.html")

@merchants_blueprint.route("/merchants", methods=["POST"])
def create_merchant():
    name = request.form["name"]
    new_merchant = Merchant(name)
    merchant_repository.save(new_merchant)
    return redirect("/merchants")

@merchants_blueprint.route("/merchants/<id>/edit")
def edit(id):
    merchant = merchant_repository.select(id)
    transactions = transaction_repository.select_all()
    total = 0
    for transaction in transactions:
        if transaction.merchant.id == merchant.id:
            total += transaction.amount
    return render_template("merchants/edit.html", merchant = merchant, transactions = transactions, total = total)

@merchants_blueprint.route("/merchants/<id>", methods=['post'])
def update(id):
    name = request.form['name']
    updated_merchant = Merchant(name, id)
    merchant_repository.update(updated_merchant)
    return redirect("/merchants")

@merchants_blueprint.route("/merchants/<id>/delete")
def delete(id):
    merchant_repository.delete(id)
    return redirect("/merchants")