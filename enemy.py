from random import randint


class Enemy:
    def __init__(self, name: str, health: int, ac: int, stats: list):
        self.name = name
        self.health = health
        self.ac = ac
        self.stats_bonus = stats
        self.available_attacks = list()
        self.available_spells = list()

    def attack(self, armor_class, attack_number):
        current_attack = self.available_attacks[attack_number]
        hit_chance = randint(1, 20) + current_attack.armor_bonus
        damage = sum([randint(1, current_attack.damage) for _ in range(0, current_attack.multiplicator)]) + \
            sum([randint(1, current_attack.add_damage) for _ in range(0, current_attack.add_multiplicator)]) + \
            current_attack.damage_bonus
        if hit_chance - current_attack.armor_bonus == 20:
            damage = damage*2
        if hit_chance < armor_class:
            return 'Промах'
        else:
            return f'Поподание на {damage}'

    def make_spell(self, spell_number):
        current_spell = self.available_spells[spell_number]
        damage = sum([randint(1, current_spell.damage) for _ in range(0, current_spell.multiplicator)])\
            + current_spell.damage_bonus
        return f'Сложность спас броска - {current_spell.save_through}\n' \
               f'Урон при провале - {damage}\n' \
               f'Урон при успехе - {int(damage/2)}\n', damage

    def check_stats(self):
        stats = ['Сила', 'Ловкость', 'Телосложение', 'Интелект', 'Мудрость', 'Харизма']
        for ind, stat in enumerate(stats):
            print(f'{stat} - {randint(1, 20) + self.stats_bonus[ind]}')
        print('\n', end='')

    def __str__(self):
        return f'{self.name}, {self.health}, {self.stats_bonus}'


class Attack:
    def __init__(self, name, armor_bonus, damage, multiplicator, damage_bonus,
                 addition_damage=0, addition_multiplicator=0):
        self.name = name
        self.damage = damage
        self.multiplicator = multiplicator
        self.armor_bonus = armor_bonus
        self.damage_bonus = damage_bonus
        self.add_damage = addition_damage
        self.add_multiplicator = addition_multiplicator

    def __str__(self):
        return f'{self.name}, {self.damage}, {self.multiplicator}, {self.armor_bonus}, {self.damage_bonus}, ' \
               f'{self.add_damage}, {self.add_multiplicator}'


class Spell:
    def __init__(self, name, difficulty, damage, multiplicator, damage_bonus):
        self.name = name
        self.damage = damage
        self.multiplicator = multiplicator
        self.save_through = difficulty
        self.damage_bonus = damage_bonus

    def __str__(self):
        return f'{self.name}, {self.damage}, {self.multiplicator}, {self.save_through}, {self.damage_bonus}'
