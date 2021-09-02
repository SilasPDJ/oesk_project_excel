# Testando a execução do super

class A:
    def __init__(self):
        print("Eu vou viajar de aviaaaaaaaaaaaaaaao")


class B:
    def __init__(self) -> None:
        print(self.teste)
        print("Por que o SENHOR vai me levaaaaaaar")


class C(A, B):
    teste = True

    def __init__(self):
        # Sempre quem tiver primeiro vai ser o super

        # B() assim chama, o super é chamado porque é super...
        # Se eu não for usar super() eu não vou usar ()
        # ClassSemSuper.init(self, *args)
        # super().init()
        # A.__init__(self) == super().__init__()
        B.__init__(self)
        # super().__init__()
        super(B, self).__init__()

        # Super pode receber o argumento da classe que eu quero iniciar...


# C()


class A:
    def __init__(self):
        print(self.atributo_de_b)


class B(A):

    def __init__(self):
        self.atributo_de_b = True
        super().__init__()
        # self.atributo_de_b = True


B()
