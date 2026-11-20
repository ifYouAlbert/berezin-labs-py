from system.query_system import run_query, users
from reset_scenario import reset_scenario

"""### Обращение № 3
> «Я выбираю пользователей в возрасте 18 лет и старше, но некоторых совершеннолетних в выдаче нет».

"""

reset_scenario()
run_query('select name from users where age >= 18')


print()
print('Что реально есть в таблице:')
print(users)
