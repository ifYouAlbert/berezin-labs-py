# ЛР 3

## Эксплуатация

Проверить корректность рабочих данных:
```bash
python app.py check
```

Показать пользователей
```bash
python app.py users
```

Текущие обращения
```bash
python app.py list
```

Архивные обращения
```bash
python app.py archive
```

## Запуск плана

Проверить оба плана без изменений файлов
```bash
python plan_runner.py --check
```

Тестировние
```bash
python -m unittest -v test_plan.py
```
