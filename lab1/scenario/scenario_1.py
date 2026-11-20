from system.query_system import run_query, users
from reset_scenario import reset_scenario

"""### Обращение № 1
> «Мы загрузили ещё 15 пользователей, всем указали возраст 18 лет. Но поиск по возрасту 18, похоже, не показывает всех пользователей. Проверьте, пожалуйста».

"""

reset_scenario(add_new=True)
print('Число записей в таблице:', len(users))
run_query('select name from users where age = 18')

print()
print('Что реально есть в таблице:')
print(users)