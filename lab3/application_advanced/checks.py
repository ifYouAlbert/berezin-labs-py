                                                                                 
import json
import os
import tempfile
from datetime import date
from pathlib import Path

FILES = ("users.json", "tickets.json")


def read_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)


def load_state(data_dir):
    data_dir = Path(data_dir)
    return read_json(data_dir / "users.json"), read_json(data_dir / "tickets.json")


def validate_state(users, data):
                                                                               
    errors = []
    if not isinstance(users, list):
        return ["users.json: ожидается список пользователей"]
    if not isinstance(data, dict) or not isinstance(data.get("tickets"), list) or not isinstance(data.get("archive"), list):
        return ["tickets.json: необходим объект с двумя списками tickets и archive"]

    user_ids = set()
    for i, user in enumerate(users):
        if not isinstance(user, dict) or type(user.get("id")) is not int or not isinstance(user.get("name"), str) or not user["name"].strip():
            errors.append(f"Некорректный пользователь, позиция {i}")
            continue
        if user["id"] in user_ids:
            errors.append(f"Повторяющийся ID пользователя: {user['id']}")
        user_ids.add(user["id"])

    ticket_ids = set()
    for section in ("tickets", "archive"):
        for i, item in enumerate(data[section]):
            if not isinstance(item, dict):
                errors.append(f"{section}[{i}]: обращение не является объектом")
                continue
            tid = item.get("id")
            if type(tid) is not int:
                errors.append(f"{section}[{i}]: ID должен быть целым числом")
            elif tid in ticket_ids:
                errors.append(f"Обращение ID={tid} встречается несколько раз")
            else:
                ticket_ids.add(tid)
            if type(item.get("user_id")) is not int or item["user_id"] not in user_ids:
                errors.append(f"Обращение {tid}: неизвестный пользователь")
            if not isinstance(item.get("title"), str) or not item["title"].strip():
                errors.append(f"Обращение {tid}: отсутствует заголовок")
            if item.get("status") not in ("open", "closed"):
                errors.append(f"Обращение {tid}: недопустимый статус")
            if section == "archive" and item.get("status") != "closed":
                errors.append(f"Обращение {tid}: в архиве не может быть открытого обращения")
            created = item.get("created_at")
            try:
                if not isinstance(created, str) or date.fromisoformat(created).isoformat() != created:
                    raise ValueError
            except ValueError:
                errors.append(f"Обращение {tid}: дата должна быть в формате YYYY-MM-DD")
    return errors


def inspect_system(data_dir):
                                                                        
    try:
        users, data = load_state(data_dir)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"ok": False, "errors": [f"Ошибка чтения: {type(exc).__name__}: {exc}"], "summary": None}
    errors = validate_state(users, data)
    summary = None
    if not errors:
        summary = {"users": len(users), "tickets": len(data["tickets"]), "archive": len(data["archive"]), "total": len(data["tickets"])+len(data["archive"])}
    return {"ok": not errors, "errors": errors, "summary": summary}


def save_json_atomic(path, data):
                                                                                        
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".tmp_", suffix=".json", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)
