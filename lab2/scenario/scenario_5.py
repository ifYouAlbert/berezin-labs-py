"""### Обращение № 5. Контрольная проверка после корректного обслуживания

> «Пользователей загрузили обычным способом, статистику обновили. Жалоб на поисковую выдачу нет, но хотелось бы убедиться, что индекс и статистика согласованы».

В этом сценарии **не предусмотрено неисправностей**. Диагностический движок должен сообщить, что отклонения по заданным проверкам не обнаружены.
"""

from lab2.scenario.reset_scenario import reset_scenario
from lab2.system import query_system


def run():
    reset_scenario(add_new=True)
    print('Число строк:', len(query_system.users))
    query_system.run_query('select name from users where age = 18')
    print('Статистика:', query_system.stats)


if __name__ == "__main__":
    run()
