import sys
sys.path.append("..")

import unittest
from kengine.user import UserManager, User

class TestUserManager(unittest.TestCase):


	def test_01_user(self):
		self.assertRaises(User(), NotImplemented)
		


if __name__ == '__main__':
	unittest.main()