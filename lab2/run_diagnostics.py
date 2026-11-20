from lab2.scenario import scenario_1, scenario_2, scenario_3, scenario_4, scenario_5
from lab2.system.diagnostics import diagnose


SCENARIOS = {
    1: scenario_1.run,
    2: scenario_2.run,
    3: scenario_3.run,
    4: scenario_4.run,
    5: scenario_5.run,
}


def main():
    for number, scenario in SCENARIOS.items():
        print(f'\nОбращение {number}')
        SCENARIOS[number]()
        diagnose()


if __name__ == '__main__':
    main()
