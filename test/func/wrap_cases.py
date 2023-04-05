from abc import abstractmethod


def none_func(*args, **kwargs):
    return str()


def arg_func(*args, **kwargs):
    return str(args[0]) + ' ' + str(list(kwargs.values()))


def res_func(result):
    args, kwargs = result
    return str(args[0]) + ' ' + str(list(kwargs.values()))


class WrapCases:

    @abstractmethod
    def execute_test(self,
                     msg: str,
                     level: int,
                     arg_func,
                     res_func,
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        ...

    def test_none_func(self):
        self.execute_test(msg='abc',
                          level=10,
                          args=(1, 2),
                          kwargs=dict(b=3, c=4),
                          arg_func=none_func,
                          res_func=none_func,
                          logged_msg='abc() -> '
                          )
        
    def test_some_func(self):
        self.execute_test(msg='abc',
                          level=10,
                          args=(1, 2),
                          kwargs=dict(b=3, c=4),
                          arg_func=arg_func,
                          res_func=res_func,
                          logged_msg='abc(1 [3, 4]) -> 1 [3, 4]'
                          )
