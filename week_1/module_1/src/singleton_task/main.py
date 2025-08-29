from week_1.module_1.src.singleton_task import singleton_for_import

singleton1 = singleton_for_import.Singleton()
singleton2 = singleton_for_import.Singleton()

print(singleton1 is singleton2)
