                                                                                 
import argparse
from pathlib import Path
from checks import inspect_system

ROOT=Path(__file__).resolve().parent


def damage_working_file():
    working=ROOT/"data"/"tickets.json"
    backup=ROOT/"backups"/"B1"
    result=inspect_system(backup)
    if not result["ok"]:
        raise RuntimeError("B1 отсутствует или неисправна. Повреждение отменено: " + "; ".join(result["errors"]))
    if not inspect_system(ROOT/"data")["ok"]:
        raise RuntimeError("Рабочие данные уже повреждены. Сначала восстановите их")
    working.write_text('{"tickets": [\n',encoding='utf-8')
    print("ИСКУССТВЕННЫЙ СБОЙ: повреждён только data/tickets.json")
    print("Проверьте состояние и восстановите данные из B1")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--confirm",action="store_true",help="Я понимаю, что будет изменён рабочий tickets.json")
    args=p.parse_args()
    if not args.confirm:
        print("Безопасный режим: файл не изменён. Для выполнения используйте --confirm")
    else:
        try: damage_working_file()
        except (OSError,RuntimeError) as e:
            print("Ошибка:",e)
            raise SystemExit(1)
