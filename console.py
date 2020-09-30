import pdb

from models.transaction import Transaction
import repositories.transaction_repository as transaction_repository

from models.user import User
import repositories.user_repository as user_repository

from models.merchant import Merchant
import repositories.merchant_repository as merchant_repository
from models.tag import Tag
import repositories.tag_repository as tag_repository

transaction_repository.delete_all()
tag_repository.delete_all()
merchant_repository.delete_all()
user_repository.delete_all()

user_1 = User('Mary Berry', 0)
user_repository.save(user_1)

user_2 = User('Paul Hollywood', 0)
user_repository.save(user_2)

merchant_1 = Merchant('Tesco')
merchant_repository.save(merchant_1)

merchant_2 = Merchant('ASDA')
merchant_repository.save(merchant_2)

tag_1 = Tag('Groceries')
tag_repository.save(tag_1)

tag_2 = Tag('Transport')
tag_repository.save(tag_2)

transaction_1 = Transaction(15, user_1, merchant_1, tag_1)
transaction_repository.save(transaction_1)

transaction_2 = Transaction(10, user_2, merchant_2, tag_2)
transaction_3 = Transaction(25, user_2, merchant_1, tag_1)
transaction_repository.save(transaction_2)
transaction_repository.save(transaction_3)

pdb.set_trace()