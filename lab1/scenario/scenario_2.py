from system.query_system import run_query
from reset_scenario import reset_scenario


"""### Обращение № 2
> «В системе точно есть пользователь Olga, возраст 30. После расширения базы поиск по этому возрасту ничего не показывает».

"""

reset_scenario(add_new=True)
run_query('select name from users where age = 30')
