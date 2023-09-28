import json
import argparse
import os

from enemy import *
from player import *
from datetime import datetime
import functools

available_enemies = list()
available_players = list()
already_in_game = list()

control_dict = {
    "command": 0,
    "cur_page": 1,
    "cur_enemy": 1,
    "cur_player": 1,
}


def log_action(func):
    @functools.wraps(func)
    def wrapper(*arg, **kwargs):
        action_res = func(*arg, **kwargs)
        log_file_name = f'{args.company_set_path.split(".")[0]}_logs.txt'
        if action_res == 1 or action_res is None:
            return
        with open(log_file_name, 'a', encoding='utf-8') as log_file:
            if action_res[0] == 0:
                log_file.write('[{}]: {}{}{}{}'.format(str(datetime.now()).split(".")[0], *action_res[1]))
            else:
                pass
    return wrapper


def page_1():
    print('Выберите кто бьет')
    for ind, current_enemy_1 in enumerate(available_enemies):
        print(f'{ind + 1}. {current_enemy_1.name} {current_enemy_1.health} хитов {current_enemy_1.ac} КЗ')
    print('-2. Обновить данные')
    print('0. Назад')
    try:
        control_dict['command'] = int(input())
    except ValueError:
        print('Ошибка ввода')
        return 1
    if all([control_dict['command'] <= len(available_enemies)]):
        if control_dict['command'] == 0:
            return 2
        elif control_dict['command'] == -2:
            update_data()
        else:
            control_dict['cur_enemy'] = control_dict['command']
            control_dict['cur_page'] += 1
    else:
        print('Ошибка ввода')


def page_2():
    print('Выберите кого бьем')
    for ind, current_player in enumerate(available_players):
        print(f'{ind + 1}. {current_player.player_name} - {current_player.player_health} хитов')
    print('-2. Обновить данные')
    print('0. Назад')
    try:
        control_dict['command'] = int(input())
    except ValueError:
        print('Ошибка ввода')
        return 1
    if all([control_dict['command'] <= len(available_players)]):
        if control_dict['command'] == 0:
            control_dict['cur_page'] -= 1
        elif control_dict['command'] == -2:
            update_data()
        else:
            control_dict['cur_player'] = control_dict['command']
            control_dict['cur_page'] += 1
    else:
        print('Ошибка ввода')


def page_3():
    print('Выберите действие')
    print('1. Атака')
    print('2. Заклинание')
    print('3. Проверка характеристик')
    print('0. Назад')
    try:
        control_dict['command'] = int(input())
    except ValueError:
        print('Ошибка ввода')
        return 1
    if all([control_dict['command'] < 4]):
        if control_dict['command'] == 0:
            control_dict['cur_page'] -= 1
        else:
            control_dict['cur_page'] += control_dict['command']
    else:
        print('Ошибка ввода')


@log_action
def page_4():
    print('Выберите Атаку')
    for ind, cur_attack in enumerate(available_enemies[control_dict['cur_enemy'] - 1].available_attacks):
        print(f'{ind + 1}. {cur_attack.name}')
    print('0. Назад')
    try:
        control_dict['command'] = int(input())
    except ValueError:
        print('Ошибка ввода')
        return 1
    if control_dict['command'] <= len(available_enemies[control_dict['cur_enemy'] - 1].available_attacks):
        if control_dict['command'] == 0:
            control_dict['cur_page'] -= 1
        else:
            damage = available_enemies[control_dict['cur_enemy'] - 1].attack(
                available_players[control_dict['cur_player'] - 1].player_armor_class,
                control_dict['command'] - 1
            )
            current_player = available_players[control_dict['cur_player'] - 1]
            print(damage)
            if current_player.player_health > 0:
                try:
                    current_player.player_health -= int(damage.split()[2])
                    print(f'Здоровье {current_player.player_name} - {current_player.player_health}\n')
                except IndexError:
                    pass
            else:
                print(f'{current_player.player_name} уже мертв\n')
            return 0, [available_enemies[control_dict['cur_enemy'] - 1].name,
                       ' совершил(а) атаку по ',
                       current_player.player_name,
                       f' {damage.lower()}\n']
    else:
        print('Ошибка ввода')


@log_action
def page_5():
    print('Выберите Заклинание')
    for ind, cur_spell in enumerate(available_enemies[control_dict['cur_enemy'] - 1].available_spells):
        print(f'{ind + 1}. {cur_spell.name}')
    print('0. Назад')
    try:
        control_dict['command'] = int(input())
    except ValueError:
        print('Ошибка ввода')
        return 1
    if all([control_dict['command'] <= len(available_enemies[control_dict['cur_enemy'] - 1].available_spells)]):
        if control_dict['command'] == 0:
            control_dict['cur_page'] -= 2
        else:
            spell_res = available_enemies[control_dict['cur_enemy'] - 1].make_spell(
                control_dict['command'] - 1)
            print(spell_res[0])
            return 0, [available_enemies[control_dict['cur_enemy'] - 1].name,
                       ' использовал(а) заклинание на ',
                       available_players[control_dict['cur_player'] - 1].player_name,
                       f', урон - {spell_res[1]}\n']
    else:
        print('Ошибка ввода')


def page_6():
    available_enemies[control_dict['cur_enemy'] - 1].check_stats()
    control_dict['cur_page'] -= 3


page_dict = {
    1: page_1,
    2: page_2,
    3: page_3,
    4: page_4,
    5: page_5,
    6: page_6,
}


def main():
    while control_dict['command'] != -3:
        try:
            res = page_dict[control_dict['cur_page']]()
            if res == 1:
                continue
            if res == 2:
                break
        except KeyError:
            pass


def update_data():
    global available_enemies, available_players
    with open('library.json', 'r', encoding='utf-8') as library:
        data = json.load(library)
        with open(args.company_set_path, 'r', encoding='utf-8') as company_set_file:
            company_set = json.load(company_set_file)
            for current_enemy in data.keys():
                if current_enemy in company_set['Враги'] and current_enemy not in already_in_game:
                    already_in_game.append(current_enemy)
                    val = data[current_enemy]
                    available_enemies.append(Enemy(current_enemy, val['Здоровье'], val['КЗ'], val['Бонусы']))
                    available_enemies[len(available_enemies) - 1].available_attacks = \
                        [Attack(name, *val) for name, val in data[current_enemy]['Атаки'].items()]
                    available_enemies[len(available_enemies) - 1].available_spells = \
                        [Spell(name, *val) for name, val in data[current_enemy]['Заклинания'].items()]

            available_players = [Player(name, *val) for name, val in company_set['Игроки'].items()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("company_set_path", help="Путь до настроек компании")
    args = parser.parse_args()
    update_data()
    main()
