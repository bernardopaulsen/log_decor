from abc import abstractmethod


class WrapCases:

    @abstractmethod
    def execute_test(self,
                     msg: str,
                     level: int,
                     args: tuple,
                     kwargs: dict,
                     logged_msg: str):
        ...

    def test_10(self):
        self.execute_test(msg='test-test',
                          level=10,
                          args=tuple(),
                          kwargs=dict(),
                          logged_msg='test-test')
        
    def test_20(self):
        self.execute_test(msg='test-test',
                          level=20,
                          args=tuple(),
                          kwargs=dict(),
                          logged_msg='test-test')