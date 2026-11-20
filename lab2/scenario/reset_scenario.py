from lab2.system import query_system


INITIAL_USERS = [
    [1, 'Anna', 18], [2, 'Ivan', 21], [3, 'Petr', 17],
    [4, 'Maria', 25], [5, 'Alex', 18], [6, 'Olga', 30],
    [7, 'Nikita', 21],
]


def reset_scenario(add_new=False):
    """Восстанавливает исходную таблицу, индекс и статистику."""
    query_system.users = [row.copy() for row in INITIAL_USERS]
    query_system.age_hash_index = query_system.build_hash_index(
        query_system.users, 'age', bucket_count=5
    )

    if add_new:
        for i in range(15):
            query_system.insert_user([8 + i, f'New_{i + 1}', 18])

    query_system.stats.clear()
    query_system.analyze(query_system.users)
