users = [[1, 'Anna', 18],
         [2, 'Ivan', 21],
         [3, 'Petr', 17],
         [4, 'Maria', 25],
         [5, 'Alex', 18],
         [6, 'Olga', 30],
         [7, 'Nikita', 21]]

columns = ['id', 'name', 'age']


def column_index(column):
    return columns.index(column)


def compare(a, op, b):
    if op == '=':
        return a == b
    if op == '>':
        return a > b
    if op == '<':
        return a < b
    if op == '>=':
        return a >= b
    if op == '<=':
        return a <= b
    raise ValueError(f'Неизвестный оператор: {op}')


#
# Блок с реализацией последовательного поиска
#

def seq_search(table, column, op, value):
    c = column_index(column)
    result = []

    for row in table:
        if compare(row[c], op, value):
            result.append(row)

    return result


#
#  Блок с реализацией хэширования
#
def build_hash_index(table, column, bucket_count=10):
    c = column_index(column)
    buckets = [[] for _ in range(bucket_count)]

    for row_id, row in enumerate(table):
        key = row[c]
        bucket_id = hash(key) % bucket_count
        bucket = buckets[bucket_id]

        found = False
        for item in bucket:
            if item[0] == key:
                item[1].append(row_id)
                found = True
                break

        if not found:
            bucket.append([key, [row_id]])

    return buckets


def hash_search(table, index, value):
    bucket_count = len(index)
    bucket_id = hash(value) % bucket_count
    bucket = index[bucket_id]

    for key, row_ids in bucket:
        if key == value:
            return [table[row_id] for row_id in row_ids]

    return []



#
# Блок с реализацией BST
#

class BSTNode:
    def __init__(self, key, row_id):
        self.key = key
        self.row_ids = [row_id]
        self.left = None
        self.right = None


def _bst_insert(node, key, row_id):
    if node is None:
        return BSTNode(key, row_id)

    if key < node.key:
        node.left = _bst_insert(node.left, key, row_id)
    elif key > node.key:
        node.right = _bst_insert(node.right, key, row_id)
    else:
        node.row_ids.append(row_id)

    return node


def build_bst_index(table, column):
    c = column_index(column)
    root = None

    for row_id, row in enumerate(table):
        root = _bst_insert(root, row[c], row_id)

    return root


def bst_search(table, root, op, value):
    row_ids = []

    def walk(node):
        if node is None:
            return

        if op == '=':
            if value < node.key:
                walk(node.left)
            elif value > node.key:
                walk(node.right)
            else:
                row_ids.extend(node.row_ids)
            return

        if op == '>':
            if node.key > value:
                walk(node.left)
                row_ids.extend(node.row_ids)
                walk(node.right)
            else:
                walk(node.right)
            return

        if op == '>=':
            if node.key >= value:
                walk(node.left)
                row_ids.extend(node.row_ids)
                walk(node.right)
            else:
                walk(node.right)
            return

        if op == '<':
            if node.key < value:
                walk(node.left)
                row_ids.extend(node.row_ids)
                walk(node.right)
            else:
                walk(node.left)
            return

        if op == '<=':
            if node.key <= value:
                walk(node.left)
                row_ids.extend(node.row_ids)
                walk(node.right)
            else:
                walk(node.left)
            return

        raise ValueError(f'Неизвестный оператор: {op}')

    walk(root)
    row_ids.sort()
    return [table[row_id] for row_id in row_ids]


#
# Блок с планировщиком и анализом
#
import math

stats = {}

def analyze(table):
    counts = {}
    for row in table:
        age = row[column_index('age')]
        counts[age] = counts.get(age, 0) + 1
    stats['age_counts'] = counts
    stats['analyzed_rows'] = len(table)
    print('Статистика обновлена:', stats)


def planner(N, op, value):
    if N <= 0:
        return [0, 'SeqScan']
    x = stats.get('age_counts', {}).get(value, 0)
    cost_SeqScan = N
    cost_Hash = 1 + 4 * 2
    cost_BST = math.log2(max(N, 1)) * x * 4
    if op != '=':
        if cost_BST <= cost_SeqScan:
            return [cost_BST, 'BST']
        return [cost_SeqScan, 'SeqScan']
    if cost_Hash <= cost_SeqScan:
        return [cost_Hash, 'HashTable']
    return [cost_SeqScan, 'SeqScan']
#
#
#


age_hash_index = build_hash_index(users, 'age', bucket_count=5)

def run_query(query_string):
    query = query_string.lower().strip().split()

    if (len(query) != 8 or query[:4] != ['select', 'name', 'from', 'users']) or (query[4] != 'where') or (query[5] != 'age') or (query[6] not in ('=', '>', '<', '>=', '<=')):
        raise ValueError('Ожидается: select name from users where age = 18')

    value = int(query[7])
    op = query[6]
    plan = planner(len(users[0]) if op != '=' else len(users), op, value)

    if plan[1] == 'SeqScan':
        rows = seq_search(users, 'age', op, value)
    elif plan[1] == 'HashTable':
        _index = build_hash_index(users, 'age', bucket_count=len(age_hash_index))
        rows = hash_search(users, _index, value)
    else:
        idx = build_bst_index(users, 'age')
        rows = bst_search(users, idx, op, value)

    names = [r[column_index('name')] for r in rows]
    print(f'Запрос: {query_string}')
    print(f'План: {plan[1]}, стоимость: {plan[0]:.3f}, X={stats.get("age_counts", {}).get(value, 0)}, N={len(users)}')
    print('Результат:', names)
    return names


if __name__ == "__main__":
    query_string = 'select name from users where age = 18'
    print('ЭТАП 1. Исходная таблица')
    analyze(users)
    run_query(query_string)

    print('\nЭТАП 2. Добавляем 15 строк; статистику НЕ обновляем')
    for i in range(15):
        users.append([8+i, f'New_{i+1}', 18])
    run_query(query_string)

    print('\nЭТАП 3. Обновляем статистику')
    analyze(users)
    run_query(query_string)
