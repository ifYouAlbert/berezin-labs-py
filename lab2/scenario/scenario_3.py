"""### Обращение № 3. Статистика показывает неправильный размер таблицы

> «Мы выполнили обновление статистики. В таблице 22 записи, но в сведениях о последнем анализе указано меньше строк. При этом пользователи в таблице никуда не исчезали».

Сценарий моделирует повреждение **одного служебного показателя** после успешного `analyze()`. Проверяйте статистику и реальные данные независимо.
"""

from lab2.scenario.reset_scenario import reset_scenario
from lab2.system import query_system


def run():
    reset_scenario(add_new=True)

    query_system.stats['analyzed_rows'] -= 5

    print('Строк в таблице:', len(query_system.users))
    print('Количество строк по статистике:', query_system.stats['analyzed_rows'])
    print('Сумма частот по возрастам:', sum(query_system.stats['age_counts'].values()))
    query_system.run_query('select name from users where age = 18')


if __name__ == "__main__":
    run()
