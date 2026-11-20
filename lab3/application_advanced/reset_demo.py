                                                                                                  
import argparse
from pathlib import Path
import shutil

ROOT=Path(__file__).resolve().parent

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--confirm",action="store_true",help="Перезаписать рабочие файлы из эталона")
    p.add_argument("--clear-backups",action="store_true",help="Также удалить каталоги B0/B1")
    args=p.parse_args()
    if not args.confirm:
        print("Рабочие данные не изменены. Добавьте --confirm")
    else:
        for name in ("users.json","tickets.json"):
            shutil.copy2(ROOT/"fixtures"/name,ROOT/"data"/name)
        if args.clear_backups:
            for label in ("B0","B1"):
                pth=ROOT/"backups"/label
                if pth.exists(): shutil.rmtree(pth)
        print("Учебные исходные данные восстановлены. Копии очищены:",args.clear_backups)
