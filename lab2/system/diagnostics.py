from collections import Counter
from enum import StrEnum
from pprint import pprint

from lab2.system import query_system

KNOWN_INCIDENTS = {
    'INC-01': 'Индекс охватывает не все строки таблицы',
    'INC-02': 'Индексные ключи не соответствуют данным таблицы',
    'INC-03': 'Некорректное общее число строк в статистике',
    'INC-04': 'Некорректные частоты значений в статистике',
}

# Ваше решение должно заключаться в изменении кода ниже


class RuleIncidents(StrEnum):
    MissingIndexRows = 'missing_index_rows'
    WrongIndexKeys = 'wrong_index_keys'
    RowCountMismatch = 'row_count_mismatch'
    AgeCountsMismatch = 'age_counts_mismatch'


RULE_INCIDENTS = {
    RuleIncidents.MissingIndexRows: 'INC-01',
    RuleIncidents.WrongIndexKeys: 'INC-02',
    RuleIncidents.RowCountMismatch: 'INC-03',
    RuleIncidents.AgeCountsMismatch: 'INC-04',
}


def collect_metrics(table, index, statistics):
    age_column = query_system.column_index('age')
    table_rows = len(table)
    indexed_positions = set()
    wrong_keys = []

    for bucket in index:
        for indexed_age, positions in bucket:
            for position in positions:
                if not 0 <= position < table_rows:
                    continue
                indexed_positions.add(position)
                table_age = table[position][age_column]
                if indexed_age != table_age:
                    wrong_keys.append({
                        'position': position,
                        'indexed_age': indexed_age,
                        'table_age': table_age,
                    })

    missing_positions = sorted(set(range(table_rows)) - indexed_positions)
    actual_age_counts = Counter(row[age_column] for row in table)
    stored_age_counts = statistics.get('age_counts', {})
    age_count_differences = {}

    for age in sorted(actual_age_counts.keys() | stored_age_counts.keys()):
        actual = actual_age_counts[age]
        stored = stored_age_counts.get(age, 0)
        if actual != stored:
            age_count_differences[age] = {'actual': actual, 'stored': stored}

    return {
        'table_rows': table_rows,
        'missing_positions': missing_positions,
        'wrong_keys': wrong_keys,
        'analyzed_rows': statistics.get('analyzed_rows'),
        'age_count_differences': age_count_differences,
    }


def evaluate_rules(metrics):
    conditions = {
        RuleIncidents.MissingIndexRows: bool(metrics['missing_positions']),
        RuleIncidents.WrongIndexKeys: bool(metrics['wrong_keys']),
        RuleIncidents.RowCountMismatch: metrics['analyzed_rows'] != metrics['table_rows'],
        RuleIncidents.AgeCountsMismatch: bool(metrics['age_count_differences']),
    }
    return [rule for rule, triggered in conditions.items() if triggered]


def match_incidents(triggered_rules):
    incident_codes = [RULE_INCIDENTS[rule] for rule in triggered_rules]
    return {code: KNOWN_INCIDENTS[code] for code in incident_codes}


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

    print("\nМетрики:")
    pprint(result['metrics'])
    print()
    print('Сработавшие правила:', result['triggered_rules'])
    print('Возможные инциденты:', result['possible_incidents'] or 'Отклонений не найдено')
    return result
