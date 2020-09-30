import unittest
from models.user import User
from models.tag import Tag
from models.merchant import Merchant

class TestUser(unittest.TestCase):

    def setUp(self):
        self.user = User("Sue Perkins", 50, 6)
    
    
    def test_user_has_name(self):
        self.assertEqual("Sue Perkins", self.user.name)
        
        
    def test_user_has_budget(self):
        self.assertEqual(50, self.user.budget)
       
        
    def test_user_has_id(self):
        self.assertEqual(6, self.user.id)