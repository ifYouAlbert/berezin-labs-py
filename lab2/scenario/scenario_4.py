"""### Обращение № 4. Распределение возрастов в статистике выглядит неверным

> «После обновления статистики общее число пользователей совпало с таблицей, но распределение по возрастам вызывает вопросы. В отчёте пользователей 18 лет стало меньше, а 21 года — больше, хотя карточки пользователей не менялись».

Сценарий моделирует повреждение **распределения значений** после успешного `analyze()`. Число строк `analyzed_rows` остаётся правильным.
"""

from lab2.scenario.reset_scenario import reset_scenario
from lab2.system import query_system


def run():
    reset_scenario(add_new=True)

    query_system.stats['age_counts'][18] -= 4
    query_system.stats['age_counts'][21] += 4

    print('Строк в таблице:', len(query_system.users))
    print('По статистике всего строк:', query_system.stats['analyzed_rows'])
    print('По статистике возраст 18:', query_system.stats['age_counts'][18])
    print('В таблице возраст 18:', sum(row[2] == 18 for row in query_system.users))
    print('По статистике возраст 21:', query_system.stats['age_counts'][21])
    print('В таблице возраст 21:', sum(row[2] == 21 for row in query_system.users))


if __name__ == "__main__":
    run()
