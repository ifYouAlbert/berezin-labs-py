from lab2.system import query_system


# Известные категории инцидентов — НЕ готовые правила
KNOWN_INCIDENTS = {
    'INC-01': 'Индекс охватывает не все строки таблицы',
    'INC-02': 'Индексные ключи не соответствуют данным таблицы',
    'INC-03': 'Неправильное общее количество строк в статистике',
    'INC-04': 'Неправильное распределение значений в статистике',
}

# Ваше решение должно заключаться в изменении кода ниже

def collect_metrics(table, index, statistics):
    # Здесь вам предстоит организовать сбор нужных метрик
    raise NotImplementedError('Реализуйте сбор метрик')


def evaluate_rules(metrics):
    # Здесь вам предстоит определить границы метрик(правила), после которых мы можем считать, что значения вышли из нормы
    raise NotImplementedError('Реализуйте проверку правил')


def match_incidents(triggered_rules):
    #Здесь нужно сопоставить правила и значения статистики, после чего определить, какие из предложенных инцедентов могут сработать
    raise NotImplementedError('Реализуйте распознавание инцидентов')


def diagnose():
    metrics = collect_metrics(
        query_system.users, query_system.age_hash_index, query_system.stats
    )
    fired = evaluate_rules(metrics)
    matches = match_incidents(fired)
    result = {
        'metrics': metrics,
        'triggered_rules': fired,
        'possible_incidents': matches,
    }
    print('Метрики:', result['metrics'])
    print('Сработавшие правила:', result['triggered_rules'])
    print('Возможные инциденты:', result['possible_incidents'] or 'Отклонений не найдено')
    return result
