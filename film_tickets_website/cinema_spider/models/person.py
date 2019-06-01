class Person:
    def __init__(self, **kwargs):
        self.name = kwargs.get('nameCn')
        self.person_url = kwargs.get('personUrl')


class Actor(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Director(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
