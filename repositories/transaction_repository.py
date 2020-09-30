from db.run_sql import run_sql
from models.transaction import Transaction
from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository
from models.user import User
import repositories.user_repository as user_repository
from models.tag import Tag
import repositories.tag_repository as tag_repository

def save(transaction):
    sql = "INSERT INTO transactions (amount, user_id, merchant_id, tag_id) VALUES (%s, %s, %s, %s) RETURNING id"
    values = [transaction.amount, transaction.user.id, transaction.merchant.id, transaction.tag.id]
    results = run_sql(sql, values)
    id = results[0]['id']
    transaction.id = id

def select_all():
    transactions = []

    sql = "SELECT * FROM transactions"
    results = run_sql(sql)

    for result in results:
        user = user_repository.select(result["user_id"])
        merchant = merchant_repository.select(result["merchant_id"])
        tag = tag_repository.select(result["tag_id"])
        transaction = Transaction(result["amount"], user, merchant, tag, result["id"])
        transactions.append(transaction)

    return transactions


def select(id):
    sql = "SELECT * FROM transactions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    user = user_repository.select(result["user_id"])
    tag = tag_repository.select(result["tag_id"])
    merchant = merchant_repository.select(result["merchant_id"])
    transaction = Transaction(result["amount"], user, merchant, tag, result["id"])
    return transaction


def update(transaction):
    sql = "UPDATE transactions SET (amount, user_id, merchant_id, tag_id) = (%s, %s, %s, %s) WHERE id = %s"
    values = [transaction.amount, transaction.user.id, transaction.merchant.id, transaction.tag.id, transaction.id]
    run_sql(sql, values)
    return transaction

def delete_all():
    sql = 'DELETE FROM transactions'
    run_sql(sql)

def delete(id):
    sql = "DELETE FROM transactions WHERE id = %s"
    values = [id]
    run_sql(sql, values)