from datetime import datetime

# TODO:\
# Напишите метакласс, который автоматически добавляет атрибут created_at\
# с текущей датой и временем к любому классу, который его использует.


class CreatedAtMetaClass(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.now()
        return super().__new__(cls, name, bases, attrs)


class MyNewClass(metaclass=CreatedAtMetaClass):
    pass


example = MyNewClass

print(example.created_at)
