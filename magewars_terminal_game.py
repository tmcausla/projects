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
        self.health += value
        if self.health > self.max_health:
            self.health = self.max_health
    
    def lose_health(self, value):
        if self.armor > 0:
            if value >= self.armor:
                value -= self.armor
                self.armor = 0    
            else:
                self.armor -= value
                return
        self.health -= value
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.is_active = False

    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
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

    def lose_mana(self, value):
        self.mana -= value
        if self.mana < 0:
            self.mana = 0

    
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
        return sum