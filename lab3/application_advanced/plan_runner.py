                                                                             

       
                                                                                   
                                                                                     
                                                                     
                                                                                  
   
import argparse
from checks import inspect_system
from run_lab import DATA, cmd_status, cmd_backup, cmd_archive, cmd_restore
from plan import MAINTENANCE_PLAN, RECOVERY_PLAN


class PlanError(ValueError):
    pass


def validate_plan(plan, phase):
                                                                       
    if not isinstance(plan, (tuple, list)):
        raise PlanError('План должен быть списком действий')
    if phase == 'maintenance':
        required = {'CHECK': 2, 'BACKUP_B0': 1, 'ARCHIVE': 1, 'BACKUP_B1': 1}
    elif phase == 'recovery':
        required = {'DIAGNOSE': 1, 'RESTORE_B1': 1, 'CHECK': 1}
    else:
        raise PlanError(f'Неизвестный тип плана: {phase}')
    from collections import Counter
    counts = Counter(plan)
    if counts != required:
        raise PlanError(f'Необходимо использовать действия {dict(required)}; получено {dict(counts)}')
    if phase == 'maintenance':
        b0 = plan.index('BACKUP_B0')
        archive = plan.index('ARCHIVE')
        b1 = plan.index('BACKUP_B1')
        checks = [i for i, action in enumerate(plan) if action == 'CHECK']
        if not (checks[0] < b0 < archive < checks[1] < b1):
            raise PlanError('Сначала проверка, затем B0, архивирование, повторная проверка, затем B1')
    else:
        if not (plan.index('DIAGNOSE') < plan.index('RESTORE_B1') < plan.index('CHECK')):
            raise PlanError('Сначала диагностируйте сбой, затем восстанавливайте B1, затем проверяйте')
    return True


def diagnose_failure():
    result = inspect_system(DATA)
    if result['ok']:
        raise PlanError('Неисправность не обнаружена. Сначала завершите обслуживание и отдельно запустите simulate_failure.py --confirm')
    print('Сбой обнаружен:', '; '.join(result['errors']))
    return 0


def execute_plan(plan, phase):
    validate_plan(plan, phase)                                                     
    operations = {
        'CHECK': cmd_status,
        'BACKUP_B0': lambda: cmd_backup('B0'),
        'ARCHIVE': cmd_archive,
        'BACKUP_B1': lambda: cmd_backup('B1'),
        'DIAGNOSE': diagnose_failure,
        'RESTORE_B1': lambda: cmd_restore('B1'),
    }
    print(f'\n=== Выполняется план: {phase} ===')
    for index, step in enumerate(plan, 1):
        print(f'\nШаг {index}/{len(plan)}: {step}')
        result = operations[step]()
        if result not in (0, None):
            raise RuntimeError(f'Шаг {step} завершился с ошибкой; план остановлен')
    print(f'\nПЛАН {phase}: выполнен успешно')


def main():
    parser=argparse.ArgumentParser(description='ЛР №3: проверка и выполнение последовательности')
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true', help='Проверить оба плана без изменений файлов')
    group.add_argument('--phase', choices=('maintenance','recovery'),help='Выполнить выбранный план')
    args=parser.parse_args()
    try:
        if args.check:
            validate_plan(MAINTENANCE_PLAN, 'maintenance')
            print('[PASS] План обслуживания: верный порядок')
            validate_plan(RECOVERY_PLAN, 'recovery')
            print('[PASS] План восстановления: верный порядок')
            print('Планы проверены. Файлы не изменялись.')
        else:
            execute_plan(MAINTENANCE_PLAN if args.phase=='maintenance' else RECOVERY_PLAN,args.phase)
        return 0
    except (PlanError, OSError, ValueError, RuntimeError, NotImplementedError) as exc:
        print('[FAIL]',exc)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
