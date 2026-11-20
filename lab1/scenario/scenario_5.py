from system.query_system import analyze, stats, users
from reset_scenario import reset_scenario

"""### Обращение № 5
> «После добавления пользователей статистика по возрасту осталась прежней. Наверное, система работает неправильно».

Проверьте утверждение с учётом правил обновления статистики в задании. Не считайте каждое отличие статистики от текущих данных дефектом автоматически.

"""

reset_scenario()
print('До загрузки:')
print('Статистика для age=18:', stats['age_counts'].get(18, 0))
for i in range(15):
    users.append([8 + i, f'New_{i+1}', 18])
print('После загрузки без обновления статистики:')
print('Статистика для age=18:', stats['age_counts'].get(18, 0))
print('Фактическое число строк с age=18:', sum(r[2] == 18 for r in users))
print('После явного обновления:')
analyze(users)
print('Статистика для age=18:', stats['age_counts'].get(18, 0))
