class A:
    def __init__(self) -> None:
        for i in range(1, 10):
            if i == 1:
                self.test = True
            elif self.test:
                print('pass')
            else:
                print(hasattr(self, 'test'))


a = A()

# pp = hasattr(a, 'teste')
# p = print
# p(pp)
