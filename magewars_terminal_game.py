import random

#defines class for unit that is capable of taking actions.  constructor initializes stats and conditions
class Unit:
    def __init__(self, name, max_health, weapon, attack_dice, armor=0):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.weapon = weapon
        self.attack_dice = attack_dice
        self.full_armor = armor
        self.armor = armor
        self.is_active = False
        self.is_dead = False
        self.is_poison = False
        self.is_burn = False
        self.is_weak = False

    def gain_health(self, value):
        print(f'{self.name} is gaining {value} health')
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health
        print(f'{self.name} now has {self.health} health\n')
    
    def lose_health(self, value):
        print(f'{self.name} is taking {value} damage')
        if self.armor > 0:
            print(f'{self.name} has {self.armor} armor')
            if value >= self.armor:
                value -= self.armor
                self.armor = 0    
            else:
                self.armor -= value
                print(f'{self.name} now has {self.health} health and {self.armor} armor\n')
                return
        self.health -= value
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.is_active = False
        print(f'{self.name} now has {self.health} health and {self.armor} armor\n')

    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your attack dice rolled {sum}')
        return sum

    def attack(self, target):
        target.lose_health(self.roll_dice())


class Mage(Unit):
    def __init__(self, name, max_health, start_mana, mana_regen, weapon, attack_dice, armor=0):
        super().__init__(name, max_health, weapon, attack_dice, armor)
        self.mana = start_mana
        self.mana_regen = mana_regen
        self.spellbook = []
        self.front_line = [self]
        self.graveyard = []
        self.is_active = True

    def gain_mana(self, value):
        self.mana += value
        print(f'{self.name} now has {self.mana} mana')

    def lose_mana(self, value):
        self.mana -= value
        if self.mana < 0:
            self.mana = 0
        print(f'{self.name} now has {self.mana} mana')

    def list_spellbook(self):
        for spell in self.spellbook:
            print(spell)

    def list_front_line(self):
        for unit in self.front_line:
            print(unit)

    def list_graveyard(self):
        for spell in self.graveyard:
            print(spell)

    
class Creature(Unit):
    def __init__(self, name, max_health, mana_cost, weapon, attack_dice, armor=0):
        super().__init__(name, max_health, weapon, attack_dice, armor)
        self.mana_cost = mana_cost


class Spell:
    def __init__(self, name, action, attack_dice, mana_cost):
        self.name = name
        self.action = action
        self.attack_dice = attack_dice
        self.mana_cost = mana_cost
    
    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your spell dice rolled {sum}')
        return sum