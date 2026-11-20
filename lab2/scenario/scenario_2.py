"""### Обращение № 2. После изменения возраста выдача противоречит карточке пользователя

> «Пользователю Maria недавно исправили возраст с 25 на 26. В карточке теперь 26, но поиск по возрасту 25 всё ещё показывает Maria, а по возрасту 26 — нет. Проверьте, пожалуйста».

Сценарий моделирует изменение поля `age` напрямую в данных, без штатной операции `change_user_age()`. Статистика после изменения корректно пересчитывается.
"""

from lab2.scenario.reset_scenario import reset_scenario
from lab2.system import query_system


def run():
    reset_scenario(add_new=True)

    query_system.users[3][query_system.column_index('age')] = 26
    query_system.analyze(query_system.users)

    print('Карточка Maria:', query_system.users[3], '\n\n')
    query_system.run_query('select name from users where age = 25')
    print('\n\n')
    query_system.run_query('select name from users where age = 26')


if __name__ == "__main__":
    run()
