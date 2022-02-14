import random

#defines class for unit that is capable of taking actions.  constructor initializes stats and conditions
class Unit:
    def __init__(self, name, school, max_health, weapon, attack_dice, armor=0, is_ranged=False):
        self.name = name
        self.school = school
        self.max_health = max_health
        self.health = max_health
        self.weapon = weapon
        self.attack_dice = attack_dice
        self.full_armor = armor
        self.armor = armor
        self.is_active = False
        self.is_ranged = is_ranged
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
        print(f'{self.name} is attacking {target.name}')
        target.lose_health(self.roll_dice())


class Mage(Unit):
    def __init__(self, name, school, max_health, start_mana, mana_regen, weapon, attack_dice, armor=0, is_ranged=False):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged)
        self.mana = start_mana
        self.mana_regen = mana_regen
        self.spellbook = []
        self.front_line = [self]
        self.graveyard = []
        self.is_active = True

    def __repr__(self):
        return f"{self.name} is a {self.school} Mage.  They have {self.health} health and attack with {self.weapon} using d{self.attack_dice} dice.  They have {self.mana} mana and regain {self.mana_regen} at the start of every round."

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
    def __init__(self, name, school, max_health, mana_cost, weapon, attack_dice, armor=0, is_ranged=False):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged)
        self.mana_cost = mana_cost

    def __repr__(self):
        return f"{self.name} is a {self.school} creature.  It has {self.health} health and attacks with {self.weapon} using d{self.attack_dice} dice."


class Spell:
    def __init__(self, name, school, action, attack_dice, mana_cost):
        self.name = name
        self.school = school
        self.action = action
        self.attack_dice = attack_dice
        self.mana_cost = mana_cost

    def __repr__(self):
        return f"{self.name} is a {self.school} spell that costs {self.mana_cost} mana.  Its target will {str(self.action)} using d{self.attack_dice} dice."
    
    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your spell dice rolled {sum}')
        return sum




########TEST AREA#########
dragon1 = Creature("Alfiya", "Holy", 19, 24, "holy dragon breath", [8, 8, 6], 3)
cleric1 = Creature("Artemis", "Holy", 10, 14, "a spear", [6, 6], 1, True)
angel1 = Creature("Cassiel", "Holy", 8, 9, 'holy magic', [4, 4])
angel2 = Creature("Guardian Angel", "Holy", 12, 12, 'a shortsword', [8, 8], 1)


#angel2.attack(dragon1)
#angel1.attack(dragon1)
#dragon1.gain_health(dragon1.roll_dice())

player1 = Mage("Asyra", "Holy", 34, 9, 9, "the Staff of Asyra", [6, 6])
player1.spellbook = [dragon1, cleric1, angel1, angel2]
#player1.list_spellbook()
#player1.list_front_line()

player1.list_spellbook()
print('-------')
player1.list_graveyard()
print('\n-------\n-------\n')
player1.spellbook.remove(dragon1)
player1.graveyard.append(dragon1)
player1.list_graveyard()
print('----------')
player1.list_spellbook()