import sys
sys.path.append("..")

import unittest
from kengine.user import UserManager, User

class TestUserManager(unittest.TestCase):


	def test_01_user(self):
		user_frank = User(name='frank', age=25, job='python dev')
		
		


if __name__ == '__main__':
	unittest.main()