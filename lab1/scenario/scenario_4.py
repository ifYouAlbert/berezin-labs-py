from system.query_system import run_query, users
from reset_scenario import reset_scenario

"""### Обращение № 4
> «После расширения базы планировщик, кажется, неправильно оценивает объём данных для диапазонного запроса. Проверьте расчёт стоимости и аргументы планировщика».
"""

reset_scenario(add_new=True)
print('Реальное количество строк:', len(users))
print('Количество столбцов:', len(users[0]))
run_query('select name from users where age > 18')
