"""ЛР № 3. В этом файле допишите две функции: create_backup и restore_backup.
"""
from pathlib import Path
from datetime import date
from copy import deepcopy
import shutil

DATA_FILES = ("users.json", "tickets.json")


def create_backup(data_dir, backup_dir):
    """Создать НОВУЮ резервную копию обоих JSON-файлов.

    data_dir: каталог с рабочими файлами.
    backup_dir: НОВЫЙ каталог конкретной копии (например, backups/B0).
    Нельзя перезаписывать существующую резервную копию.
    Возвратить Path созданного каталога.
    Если копирование не удалось, не оставлять неполную копию.
    """
    data_dir = Path(data_dir)
    backup_dir = Path(backup_dir)

    backup_dir.mkdir(parents=True, exist_ok=False)

    try:
        for data_file in DATA_FILES:
            if not data_dir.exists():
                raise Exception(f"data_dir: {data_dir} must exist")

            p_data_file = data_dir / data_file
            p_backup_file = backup_dir / data_file
            shutil.copy2(p_data_file, p_backup_file)

            p_backup_file.write_bytes(p_data_file.read_bytes())
    except:
        shutil.rmtree(backup_dir)
        raise

    return backup_dir


def archive_tickets(data, cutoff_date):
    cutoff = date.fromisoformat(cutoff_date)
    result = {"tickets": [], "archive": deepcopy(data["archive"])}
    for ticket in data["tickets"]:
        item = deepcopy(ticket)
        old_closed = item["status"] == "closed" and date.fromisoformat(item["created_at"]) < cutoff
        if old_closed:
            result["archive"].append(item)
        else:
            result["tickets"].append(item)
    return result


def restore_backup(backup_dir, data_dir):
    """Восстановить оба рабочих файла из проверенной резервной копии.

    До изменения рабочих файлов убедиться, что оба файла в копии
    существуют.
    Вернуть Path каталога data_dir.
    """
    raise NotImplementedError("Реализуйте restore_backup()")
