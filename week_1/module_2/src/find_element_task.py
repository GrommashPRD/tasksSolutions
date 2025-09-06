from typing import Optional, List

# TODO: \
# Дан отсортированный список чисел, например: [1, 2, 3, 45, 356, 569, 600, 705, 923]\
# Список может содержать миллионы элементов.\
# Необходимо написать функцию search(number: id) -> bool которая принимает число number и \
# возвращает True если это число находится в этом списке.\
# Требуемая сложность алгоритма O(log n).


def search(numbers: Optional[List], number:Optional[int]) -> bool:
    left = 0
    right = len(numbers) - 1

    while left <= right:
        middle = left + (right - left) // 2

        if numbers[middle] == number:
            return True
        if numbers[middle] > number:
            right = middle - 1
        else:
            left = middle + 1

    return False


numbers = [1, 2, 3, 45, 356, 569, 600, 705, 923]
print(search(numbers, 45))
