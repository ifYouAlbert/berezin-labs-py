                                                                
import argparse
from collections import Counter
from pathlib import Path
from checks import inspect_system, load_state, validate_state, save_json_atomic
from maintenance import create_backup, archive_tickets, restore_backup

ROOT=Path(__file__).resolve().parent
DATA=ROOT/"data"
BACKUPS=ROOT/"backups"
CUTOFF="2026-01-01"


def require_ok(path, name):
    info=inspect_system(path)
    if not info["ok"]:
        raise ValueError(f"{name} не прошла проверку: " + "; ".join(info["errors"]))
    return info


def cmd_status():
    r=inspect_system(DATA)
    print("Статус:","OK" if r["ok"] else "ERROR")
    if r["ok"]: print("Сводка:",r["summary"])
    else:
        for e in r["errors"]: print(" -",e)
    return 0 if r["ok"] else 1


def cmd_backup(label):
    require_ok(DATA,"Рабочая система")
    target=BACKUPS/label
    path=create_backup(DATA,target)
    require_ok(path, f"Резервная копия {label}")
    for name in ("users.json","tickets.json"):
        if (DATA/name).read_bytes()!=(path/name).read_bytes():
            raise ValueError("Скопированный файл не совпадает с оригиналом: "+name)
    print(f"Создана и проверена копия {label}: {path}")
    return 0


def cmd_archive():
    require_ok(DATA,"Рабочая система")
    require_ok(BACKUPS/"B0","Резервная копия B0")
    users,old=load_state(DATA)
    before={t["id"]:t for t in old["tickets"]+old["archive"]}
    new=archive_tickets(old,CUTOFF)
    errors=validate_state(users,new)
    if errors: raise ValueError("Неправильный результат: "+"; ".join(errors))
    after={t["id"]:t for t in new["tickets"]+new["archive"]}
    if after!=before:
        raise ValueError("После архивирования изменились или потерялись обращения")
    from datetime import date
    cutoff=date.fromisoformat(CUTOFF)
    expected={t["id"] for t in old["tickets"] if t["status"]=="closed" and date.fromisoformat(t["created_at"])<cutoff}
    actual={t["id"] for t in new["archive"]}-{t["id"] for t in old["archive"]}
    if expected!=actual or len(new["tickets"]) != len(old["tickets"])-len(expected):
        raise ValueError(f"Неправильный отбор обращений: ожидались {sorted(expected)}, получены {sorted(actual)}")
    save_json_atomic(DATA/"tickets.json",new)
    print(f"Архивирование успешно. Перенесены ID: {sorted(actual)}")
    print("После обслуживания:",require_ok(DATA,"Рабочая система")["summary"])
    return 0


def cmd_restore(label):
    require_ok(BACKUPS/label, f"Резервная копия {label}")
    restore_backup(BACKUPS/label, DATA)
    require_ok(DATA,"Восстановленная система")
    for name in ("users.json","tickets.json"):
        if (DATA/name).read_bytes() != (BACKUPS/label/name).read_bytes():
            raise ValueError("Восстановленные данные не совпадают с выбранной копией: "+name)
    print(f"Восстановление из {label} прошло успешно")
    return 0


def main():
    parser=argparse.ArgumentParser(description="ЛР № 3: команды обслуживания")
    sub=parser.add_subparsers(dest="command",required=True)
    sub.add_parser("status",help="Проверка текущих файлов")
    p=sub.add_parser("backup",help="Создание резервной копии")
    p.add_argument("label",choices=("B0","B1"))
    sub.add_parser("archive",help="Архивирование согласно регламенту")
    p=sub.add_parser("restore",help="Восстановление из выбранной копии")
    p.add_argument("label",choices=("B0","B1"))
    args=parser.parse_args()
    try:
        if args.command=="status":return cmd_status()
        if args.command=="backup":return cmd_backup(args.label)
        if args.command=="archive":return cmd_archive()
        if args.command=="restore":return cmd_restore(args.label)
    except (OSError,ValueError,NotImplementedError,RuntimeError) as exc:
        print("ОШИБКА:",exc)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
