class Person:
    def __init__(self, **kwargs):
        self.name = kwargs.get('nameCn')
        self.person_url = kwargs.get('personUrl')
        self.belong_movie_id = kwargs.get('id')


class Actor(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.img = kwargs.get('img')
        self.name_en = kwargs.get('name_en')
        self.play_role = kwargs.get('play_role')


class Director(Person):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
