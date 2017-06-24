def run_for(method):
    def _wrapper(*args, **kwargs):
        print 'method==>',method.func_name, method, args, kwargs
        resp = method(*args, **kwargs)
        return resp
    return _wrapper


@run_for
def hello(p):
    print 'happy ',p

if __name__ == '__main__':
    hello('hack')

