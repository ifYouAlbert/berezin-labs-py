                                                                              
import argparse
from pathlib import Path
from checks import load_state, validate_state, inspect_system, save_json_atomic

DATA = Path(__file__).resolve().parent / "data"


def display_tickets(archived=False):
    users, data = load_state(DATA)
    errors = validate_state(users, data)
    if errors:
        raise ValueError("Данные повреждены: " + "; ".join(errors))
    names = {u["id"]: u["name"] for u in users}
    key = "archive" if archived else "tickets"
    print(f"Список: {key}")
    for t in data[key]:
        print(f"#{t['id']:3} | {names[t['user_id']]:8} | {t['status']:6} | {t['created_at']} | {t['title']}")
    print(f"Всего: {len(data[key])}")


def add_ticket(user_id, title):
    users, data = load_state(DATA)
    errors = validate_state(users, data)
    if errors:
        raise ValueError("Состояние некорректно: " + "; ".join(errors))
    if user_id not in {u["id"] for u in users}:
        raise ValueError("Такого пользователя не существует")
    from datetime import date
    all_ids = [t["id"] for t in data["tickets"] + data["archive"]]
    new_id = max(all_ids, default=100) + 1
    data["tickets"].append({"id":new_id,"user_id":user_id,"title":title,"status":"open","created_at":date.today().isoformat()})
    save_json_atomic(DATA / "tickets.json",data)
    print(f"Обращение #{new_id} создано")


def close_ticket(ticket_id):
    users,data=load_state(DATA)
    errors=validate_state(users,data)
    if errors:
        raise ValueError("Состояние некорректно: " + "; ".join(errors))
    for t in data["tickets"]:
        if t["id"]==ticket_id:
            t["status"]="closed"
            save_json_atomic(DATA / "tickets.json",data)
            print(f"Обращение #{ticket_id} закрыто")
            return
    raise ValueError("Обращение не найдено в текущем списке")


def main():
    parser=argparse.ArgumentParser(description="Application")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("check",help="Проверить состояние")
    sub.add_parser("users",help="Показать пользователей")
    sub.add_parser("list",help="Показать текущие обращения")
    sub.add_parser("archive",help="Показать архив")
    add=sub.add_parser("add",help="Создать обращение")
    add.add_argument("user_id",type=int);add.add_argument("title")
    close=sub.add_parser("close",help="Закрыть обращение")
    close.add_argument("ticket_id",type=int)
    args=parser.parse_args()
    try:
        if args.command=="check":
            r=inspect_system(DATA)
            print("OK" if r["ok"] else "ERROR",r["summary"] if r["ok"] else r["errors"])
            return 0 if r["ok"] else 1
        if args.command=="users":
            users,data=load_state(DATA)
            errors=validate_state(users,data)
            if errors: raise ValueError("; ".join(errors))
            for u in users: print(f"{u['id']}: {u['name']}")
        elif args.command in ("list","archive"):
            display_tickets(archived=args.command=="archive")
        elif args.command=="add": add_ticket(args.user_id,args.title)
        elif args.command=="close": close_ticket(args.ticket_id)
        return 0
    except (OSError, ValueError) as exc:
        print(f"Ошибка: {exc}")
        return 1

if __name__=="__main__":
    raise SystemExit(main())
