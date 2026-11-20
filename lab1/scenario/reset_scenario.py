from system.query_system import age_hash_index, analyze, build_hash_index, stats, users

INITIAL_USERS = [
    [1, 'Anna', 18], [2, 'Ivan', 21], [3, 'Petr', 17],
    [4, 'Maria', 25], [5, 'Alex', 18], [6, 'Olga', 30],
    [7, 'Nikita', 21],
]

def reset_scenario(add_new=False):
    users[:] = [row.copy() for row in INITIAL_USERS]
    stats.clear()
    analyze(users)
    age_hash_index[:] = build_hash_index(users, 'age', bucket_count=5)
    if add_new:
        for i in range(15):
            users.append([8 + i, f'New_{i+1}', 18])

print('Сценарии готовы к запуску.')

