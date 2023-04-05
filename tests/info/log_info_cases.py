from abc import abstractmethod


class LogInfoCases:

    @abstractmethod
    def execute_test(self,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     msg: str):
        ...

    def test_null_args(self):
        self.execute_test(level=0,
                          args=tuple(),
                          kwargs=dict(),
                          msg='func() [0.0s] -> ((), {})')
        
    def test_args(self):
        self.execute_test(level=0,
                          args=(1, 2),
                          kwargs=dict(a=3, b=4),
                          msg="func(1, 2, a=3, b=4) [0.0s] -> ((1, 2), {'a': 3, 'b': 4})")
        
    def test_level_10(self):
        self.execute_test(level=10,
                          args=tuple(),
                          kwargs=dict(),
                          msg='func() [0.0s] -> ((), {})')
        
    def test_level_20(self):
        self.execute_test(level=20,
                          args=tuple(),
                          kwargs=dict(),
                          msg='func() [0.0s] -> ((), {})')