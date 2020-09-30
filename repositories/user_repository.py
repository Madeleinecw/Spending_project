from db.run_sql import run_sql
from models.user import User
from models.transaction import Transaction
from models.merchant import Merchant
from models.tag import Tag
import repositories.user_repository as user_repository
import repositories.tag_repository as tag_repository



def save(user):
    sql = "INSERT INTO users (name, budget) VALUES (%s, %s) RETURNING id"
    values = [user.name, user.budget]
    results = run_sql(sql, values)
    id = results[0]['id']
    user.id = id


def select_all():
    users = []
    sql = "SELECT * FROM users"
    results = run_sql(sql)
    for result in results:
        user = User(result["name"], result["budget"],  result["id"])
        users.append(user)
    return users


def select(id):
    sql = "SELECT * FROM users WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]
    user = User(result["name"], result["budget"], result["id"])
    return user


def delete_all():
    sql = 'DELETE FROM users'
    run_sql(sql)


def delete(id):
    sql = "DELETE FROM users WHERE id = %s"
    values = [id]
    run_sql(sql, values)


def update(user):
    sql = "UPDATE users SET (name, budget) = (%s, %s) WHERE id = %s"
    values = [user.name, user.budget, user.id,]
    run_sql(sql, values)


def select_transactions(user):
    transactions = []

    sql = "SELECT T.id, T.amount, T.tag_id, T.merchant_id, T.user_id, TA.name, M.name FROM transactions as T LEFT JOIN tags as TA on T.tag_id = TA.id LEFT JOIN merchants as M on T.merchant_id = M.id WHERE T.user_id = %s;"
    values = [user.id]
    results = run_sql(sql, values)

    for row in results:
        merchant = Merchant(row['name'], row['merchant_id'])
        tag = tag_repository.select(row['tag_id'])
        user = user_repository.select(row['user_id'])
        transaction = Transaction(row['amount'], user, merchant, tag, row['id'])
        transactions.append(transaction)
    return transactions
