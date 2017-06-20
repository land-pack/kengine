import sys
import time
import copy


class UserManager(list):

    def append(self, item):
        item.realtime()
        super(UserManager, self).append(item)


class User(dict):

    def realtime(self):
        self.update({
            "time": time.time()
        })
        # all real time require value are declare here ~

if __name__ == '__main__':
    um = UserManager()
    user1 = User(name='frank', age=25)
    um.append(user1)
    print um
    time.sleep(0.4)
    
    user2 = User(name='jack', age=27)
    um.append(user2)
    print um
