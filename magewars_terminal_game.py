import random

class Unit:
    def __init__(self, name, max_health, armor=0):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.full_armor = armor
        self.armor = armor
        self.is_active = True
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

    def roll_d4(self):
        return random.randint(1, 4)

    def roll_d6(self):
        return random.randint(1, 6)

    def roll_d8(self):
        return random.randint(1, 8)

    def roll_d10(self):
        return random.randint(1, 10)

    def roll_d12(self):
        return random.randint(1, 12)

    def roll_d20(self):
        return random.randint(1, 20)

class Mage(Unit):
    def __init__(self, name, max_health, start_mana, mana_regen, armor=0):
        super().__init__(name, max_health, armor)
        self.mana = start_mana
        self.mana_regen = mana_regen
        self.spellbook = []
        self.front_line = []
        self.graveyard = []

    def gain_mana(self, value):
        self.mana += value

    def lose_mana(self, value):
        self.mana -= value
        if self.mana < 0:
            self.mana = 0
    