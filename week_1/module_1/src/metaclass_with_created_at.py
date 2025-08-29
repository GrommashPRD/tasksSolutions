from datetime import datetime


class CreatedAtMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class MyNewClass(metaclass=CreatedAtMetaClass):
    pass


example = MyNewClass

print(example.created_at)
