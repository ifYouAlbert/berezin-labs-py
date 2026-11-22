# ЛР 2


Цель работы:
реализовать диагностику таблицы, хеш-индекса и сохранённой статистики.

Все пять обращений проверены.

| № | Отличающиеся метрики                                                                        | Какие значения не в норме?                                            | Сработавшее правило |
|---|---------------------------------------------------------------------------------------------|-----------------------------------------------------------------------|---------------------|
| 1 | missing_positions = [7, ..., 21]                                                            | В индексе отсутствуют 15 позиций.                                     | INC-01              |
| 2 | wrong_keys = [{'position': 3, 'indexed_age': 25, 'table_age': 26}]                          | У строки на позиции 3 остался старый ключ 25.                         | INC-02              |
| 3 | analyzed_rows': 17                                                                          | Число строк в статистике занижено на 5.                               | INC-03              |
| 4 | age_count_differences = {18: {'actual': 17, 'stored': 13}, 21: {'actual': 2, 'stored': 6}}` | Частота возраста 18 занижена на 4, частота возраста 21 завышена на 4. | INC-04              |
| 5 | -                                                                                           | Отклонений не найдено.                                                | -                   |

Вывод обращения 1

```
Статистика обновлена: {'age_counts': {18: 2, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 7}
Статистика обновлена: {'age_counts': {18: 17, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 22}
Фактических записей с age=18: 17
Запрос: select name from users where age = 18
План: HashTable, стоимость: 9.000, X=17, N=22
Результат: ['Anna', 'Alex']

Метрики:
{'age_count_differences': {},
 'analyzed_rows': 22,
 'missing_positions': [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
 'table_rows': 22,
 'wrong_keys': []}

Сработавшие правила: [<RuleIncidents.MissingIndexRows: 'missing_index_rows'>]
Возможные инциденты: {'INC-01': 'Индекс охватывает не все строки таблицы'}
```

Вывод обращения 2

```
Статистика обновлена: {'age_counts': {18: 17, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 22}
Статистика обновлена: {'age_counts': {18: 17, 21: 2, 17: 1, 26: 1, 30: 1}, 'analyzed_rows': 22}
Карточка Maria: [4, 'Maria', 26] 


Запрос: select name from users where age = 25
План: HashTable, стоимость: 9.000, X=0, N=22
Результат: ['Maria']



Запрос: select name from users where age = 26
План: HashTable, стоимость: 9.000, X=1, N=22
Результат: []

Метрики:
{'age_count_differences': {},
 'analyzed_rows': 22,
 'missing_positions': [],
 'table_rows': 22,
 'wrong_keys': [{'indexed_age': 25, 'position': 3, 'table_age': 26}]}

Сработавшие правила: [<RuleIncidents.WrongIndexKeys: 'wrong_index_keys'>]
Возможные инциденты: {'INC-02': 'Индексные ключи не соответствуют данным таблицы'}
```

Вывод обращения 3

```
Статистика обновлена: {'age_counts': {18: 17, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 22}
Строк в таблице: 22
Количество строк по статистике: 17
Сумма частот по возрастам: 22
Запрос: select name from users where age = 18
План: HashTable, стоимость: 9.000, X=17, N=22
Результат: ['Anna', 'Alex', 'New_1', 'New_2', 'New_3', 'New_4', 'New_5', 'New_6', 'New_7', 'New_8', 'New_9', 'New_10', 'New_11', 'New_12', 'New_13', 'New_14', 'New_15']

Метрики:
{'age_count_differences': {},
 'analyzed_rows': 17,
 'missing_positions': [],
 'table_rows': 22,
 'wrong_keys': []}

Сработавшие правила: [<RuleIncidents.RowCountMismatch: 'row_count_mismatch'>]
Возможные инциденты: {'INC-03': 'Некорректное общее число строк в статистике'}
```

Вывод обращения 4

```
Статистика обновлена: {'age_counts': {18: 17, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 22}
Строк в таблице: 22
По статистике всего строк: 22
По статистике возраст 18: 13
В таблице возраст 18: 17
По статистике возраст 21: 6
В таблице возраст 21: 2

Метрики:
{'age_count_differences': {18: {'actual': 17, 'stored': 13},
                           21: {'actual': 2, 'stored': 6}},
 'analyzed_rows': 22,
 'missing_positions': [],
 'table_rows': 22,
 'wrong_keys': []}

Сработавшие правила: [<RuleIncidents.AgeCountsMismatch: 'age_counts_mismatch'>]
Возможные инциденты: {'INC-04': 'Некорректные частоты значений в статистике'}
```

Вывод обращения 5

```
Статистика обновлена: {'age_counts': {18: 17, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 22}
Число строк: 22
Запрос: select name from users where age = 18
План: HashTable, стоимость: 9.000, X=17, N=22
Результат: ['Anna', 'Alex', 'New_1', 'New_2', 'New_3', 'New_4', 'New_5', 'New_6', 'New_7', 'New_8', 'New_9', 'New_10', 'New_11', 'New_12', 'New_13', 'New_14', 'New_15']
Статистика: {'age_counts': {18: 17, 21: 2, 17: 1, 25: 1, 30: 1}, 'analyzed_rows': 22}

Метрики:
{'age_count_differences': {},
 'analyzed_rows': 22,
 'missing_positions': [],
 'table_rows': 22,
 'wrong_keys': []}

Сработавшие правила: []
Возможные инциденты: Отклонений не найдено
```

