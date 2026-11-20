"""### Обращение № 1. После массового импорта поиск возвращает не все записи

> «Мы загрузили ещё 15 пользователей, всем указали возраст 18 лет. В общем списке они есть, а поиск по возрасту показывает только часть людей. Можете проверить, откуда расхождение?»

Сценарий моделирует загрузку данных **в обход штатной операции `insert_user()`**. После загрузки статистика явно обновляется. Не редактируйте код сценария — исследуйте состояние таблицы и индекса.
"""

from lab2.scenario.reset_scenario import reset_scenario
from lab2.system import query_system


def run():
    reset_scenario()

    for i in range(15):
        query_system.users.append([8 + i, f'New_{i + 1}', 18])
    query_system.analyze(query_system.users)

    print('Фактических записей с age=18:', sum(row[2] == 18 for row in query_system.users))
    query_system.run_query('select name from users where age = 18')


if __name__ == "__main__":
    run()
