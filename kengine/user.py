import time


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
    first_manager = UserManager()
    user1 = User(name='frank', age=25)
    first_manager.append(user1)
    print first_manager

    time.sleep(0.4)
    # the second user come in, he/she want the all member user information ~
    # but do no need query all information about the member , just require real
    # time field ~
    second_manager = UserManager()
    user2 = User(name='jack', age=27)
    second_manager.append(user1)
    second_manager.append(user2)
    print second_manager
