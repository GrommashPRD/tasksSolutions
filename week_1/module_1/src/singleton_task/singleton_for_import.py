# TODO:\
# Реализуйте паттерн синглтон тремя способами: \
# через механизм импортов


class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.value = None
