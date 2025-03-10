import timeit
from functools import lru_cache
import matplotlib.pyplot as plt
from typing import Optional, List


@lru_cache(maxsize=None)

# Обчислює n-е число Фібоначчі, використовуючи кешування
def fibonacci_lru(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_lru(n - 1) + fibonacci_lru(n - 2)

# Вузол Splay Tree, що зберігає номер та значення числа Фібоначчі
class SplayTreeNode:
    def __init__(self, key: int, value: int):
        self.key: int = key
        self.value: int = value
        self.left: Optional['SplayTreeNode'] = None
        self.right: Optional['SplayTreeNode'] = None

# Splay Tree для збереження обчислених значень чисел Фібоначчі
class SplayTree:

    def __init__(self):
        self.root: Optional[SplayTreeNode] = None

    def _splay(self, root: Optional[SplayTreeNode], key: int) -> Optional[SplayTreeNode]:
        """Переміщує вузол з ключем `key` до кореня"""
        if root is None or root.key == key:
            return root

        # Ліве піддерево
        if key < root.key:
            if root.left is None:
                return root

            if key < root.left.key:  
                root.left.left = self._splay(root.left.left, key)
                root = self._rotate_right(root)

            elif key > root.left.key:  
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._rotate_left(root.left)

            return self._rotate_right(root) if root.left else root

        # Праве піддерево
        else:
            if root.right is None:
                return root

            if key > root.right.key:  
                root.right.right = self._splay(root.right.right, key)
                root = self._rotate_left(root)

            elif key < root.right.key:  
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._rotate_right(root.right)

            return self._rotate_left(root) if root.right else root

    def _rotate_left(self, x: SplayTreeNode) -> SplayTreeNode:
        """Виконує ліву ротацію"""
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _rotate_right(self, x: SplayTreeNode) -> SplayTreeNode:
        """Виконує праву ротацію"""
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def insert(self, key: int, value: int) -> None:
        """Вставляє значення у Splay Tree, якщо його немає"""
        if self.root is None:
            self.root = SplayTreeNode(key, value)
            return

        self.root = self._splay(self.root, key)
        if self.root.key == key:
            return  

        new_node = SplayTreeNode(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def find(self, key: int) -> Optional[int]:
        """Шукає значення у дереві, повертає його, якщо знайдено"""
        self.root = self._splay(self.root, key)
        return self.root.value if self.root and self.root.key == key else None

# Обчислює n-е число Фібоначчі з використанням Splay Tree
def fibonacci_splay(n: int, tree: SplayTree) -> int:
    if n <= 1:
        return n
    if (result := tree.find(n)) is not None:
        return result
    result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result

# Вимірює середній час виконання функції
def measure_time(func, *args) -> float:
    return timeit.timeit(lambda: func(*args), number=10) / 10


# Тестування продуктивності
n_values = range(0, 950, 50)
lru_times: List[float] = []
splay_times: List[float] = []

for n in n_values:
    # Час для LRU Cache
    lru_time = measure_time(fibonacci_lru, n)
    lru_times.append(lru_time)

    # Час для Splay Tree
    tree = SplayTree()
    splay_time = measure_time(fibonacci_splay, n, tree)
    splay_times.append(splay_time)


# Побудова графіка
plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label="LRU Cache", marker="o")
plt.plot(n_values, splay_times, label="Splay Tree", marker="x")
plt.xlabel("Число Фібоначчі (n)")
plt.ylabel("Середній час виконання (сек)")
plt.title("Порівняння продуктивності обчислення чисел Фібоначчі для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)
plt.show()


# Виведення результатів у вигляді таблиці
print(f"{'n':<10}{'LRU Cache час (с)':<20}{'Splay Tree час (с)'}")
print("-" * 50)
for n, lru_time, splay_time in zip(n_values, lru_times, splay_times):
    print(f"{n:<10}{lru_time:<20.10f}{splay_time:<20.10f}")
