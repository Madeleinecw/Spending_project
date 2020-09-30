from flask import Blueprint, Flask, redirect, render_template, request

from models.tag import Tag
import repositories.tag_repository as tag_repository
import repositories.transaction_repository as transaction_repository

tags_blueprint = Blueprint("tags", __name__)


@tags_blueprint.route("/tags")
def tags():
    tags = tag_repository.select_all()
    return render_template("tags/index.html", tags = tags)

@tags_blueprint.route("/tags/new")
def new_tag():
    return render_template("tags/new.html")

@tags_blueprint.route("/tags", methods=["POST"])
def create_tag():
    name = request.form["name"]
    new_tag = Tag(name)
    tag_repository.save(new_tag)
    return redirect("/tags")

@tags_blueprint.route("/tags/<id>/edit")
def edit(id):
    tag = tag_repository.select(id)
    transactions = transaction_repository.select_all()
    total = 0
    for transaction in transactions:
        if transaction.tag.id == tag.id:
            total += transaction.amount
    return render_template("tags/edit.html", tag = tag, transactions = transactions, total = total)

@tags_blueprint.route("/tags/<id>", methods=['post'])
def update(id):
    name = request.form['name']
    updated_tag = Tag(name, id)
    tag_repository.update(updated_tag)
    return redirect("/tags")