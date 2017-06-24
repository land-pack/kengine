import time
import abc


class User(dict):
    realtime_require = {}

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.realtime()

    def realtime(self):
        for func_name, func in self.realtime_require.items():
            self.update({
                func_name: func(self)
            })

    @classmethod
    def current(cls, f):
        """
        @user.latest
        def account():
                query from mysql ~~
                latest_account = ~~
                return lastest_account
        """
        cls.realtime_require[f.func_name] = f

        def _wrapper(*args, **kwargs):
            return

        return _wrapper


class UserManager(list):
    def append(self, item):
        item.realtime()
        super(UserManager, self).append(item)



@User.current
def idfa(self):
    """
    all real time require value are declare here ~
    """
    return 'idfa:{}'.format(self.get("username"))


if __name__ == '__main__':
    first_manager = UserManager()
    user1 = User(name='frank', age=25)
    print user1
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
