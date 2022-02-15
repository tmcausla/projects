import random

#defines class for unit that is capable of taking actions.  constructor initializes stats and conditions
class Unit:
    def __init__(self, name, school, max_health, weapon, attack_dice, armor=0, is_ranged=False, health_regen=0):
        self.name = name
        self.school = school
        self.max_health = max_health
        self.health = max_health
        self.health_regen = health_regen
        self.weapon = weapon
        self.attack_dice = attack_dice
        self.full_armor = armor
        self.armor = armor
        self.is_active = False
        self.is_ranged = is_ranged
        self.advantage = False
        self.disadvantage = False
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

    def roll_status_die(self):
        result = random.randint(1, 20)
        print(f'Status die rolled {result}.')
        return result

    def attack(self, target):
        if isinstance(target, Mage) and not self.is_ranged:
            print(f'{target.name} may select a creature to guard.')
            target = target.choose_guard()
        print(f'{self.name} is attacking {target.name}')
        attack_value = self.roll_dice()
        if self.advantage:
            print('Advantage! Reroll and take the higher result.')
            new_attack_value = self.roll_dice()
            if new_attack_value > attack_value:
                attack_value = new_attack_value
            self.advantage = False
        if self.disadvantage:
            print('Disadvantage! Reroll and take the lower result.')
            new_attack_value = self.roll_dice()
            if new_attack_value < attack_value:
                attack_value = new_attack_value
            self.disadvantage = False
        if target.is_weak:
            print('Target is weak! Roll again and add the result.')
            attack_value += self.roll_dice()
        target.lose_health(attack_value)
        self.is_active = False


class Mage(Unit):
    def __init__(self, name, school, max_health, start_mana, mana_regen, weapon, attack_dice, armor=0, is_ranged=False, health_regen=0):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged, health_regen)
        self.mana = start_mana
        self.mana_regen = mana_regen
        self.spellbook = []
        self.front_line = [self]
        self.graveyard = []
        self.is_active = True

    def __repr__(self):
        return f"{self.name} is a {self.school} Mage.  They have {self.health} health + {self.armor} armor and attack with {self.weapon} using d{self.attack_dice} dice.  They have {self.mana} mana and regain {self.mana_regen} mana at the start of every round."

    def gain_mana(self, value):
        self.mana += value
        print(f'{self.name} now has {self.mana} mana')

    def lose_mana(self, value):
        self.mana -= value
        if self.mana < 0:
            self.mana = 0
        print(f'{self.name} now has {self.mana} mana')

    def list_spellbook(self):
        print('Spells available to be cast:')
        for spell in self.spellbook:
            print(spell)
        print('----------')

    def list_front_line(self):
        print('----------')
        for unit in self.front_line:
            print(unit)
        print('----------')

    def list_graveyard(self):
        print('Spells currently in your graveyard pile:')
        for spell in self.graveyard:
            print(spell)
        print('----------')

    def choose_guard(self):
        active = [unit for unit in self.front_line if unit.is_active]
        for i in range(len(active)):
            print(f'{i + 1} - {active[i]}')
        guard = int(input(f'Your mage {self.name} is being targeted, you may choose a creature to block the attack. Select a number and press Enter.\n'))
        if guard > 1:
            active[guard - 1].is_active = False
            print(f'{self.name} is blocking the attack with {active[guard - 1].name}.')
        return active[guard - 1]

    def cast_spell(self, spell, target=None):
        self.lose_mana(spell.mana_cost)
        if isinstance(spell, Creature):
            self.front_line.append(spell)
            print(f'{self.name} has summoned {spell.name} to the arena.\n')
        else:
            print(f'{self.name} is casting {spell.name} on {target.name}.')
            if 'heal' in spell.action:
                target.gain_health(spell.roll_dice())
            if 'regenerate health' in spell.action:
                target.health_regen += spell.roll_dice()
                print(f'{target.name} will start to regenerate health between rounds.\n')
            if 'take damage' in spell.action:
                target.lose_health(spell.roll_dice())
            if 'lose mana' in spell.action:
                target.lose_mana(spell.roll_dice())
            if 'be poisoned' in spell.action or 'Poison' in spell.school:
                if target.roll_status_die() >= spell.status_roll:
                    target.is_poison = True
                    print(f'{target.name} is poisoned!\n')
            if 'cure poison' in spell.action:
                target.is_poison = False
                print(f'{target.name} is no longer poisoned.\n')
            if 'be burned' in spell.action or 'Fire' in spell.school:
                if target.roll_status_die() >= spell.status_roll:
                    target.is_burn = True
                    print(f'{target.name} is burned!\n')
            if 'cure burn' in spell.action:
                target.is_burn = False
                print(f'{target.name} is no longer burned.\n')
            if 'be weakened' in spell.action:
                if target.roll_status_die() >= spell.status_roll:
                    target.is_weak = True
                    print(f'{target.name} is feeling weak!\n')
            if 'cure weak' in spell.action:
                target.is_weak = False
                print(f'{target.name} is no longer feeling weak.\n')
            if 'gain advantage' in spell.action:
                if target.disadvantage:
                    target.disadvantage = False
                    print(f'{target.name} is no longer at a disadvantage.\n')
                else:
                    target.advantage = True
                    print(f'{target.name} has gained advantage for attack!\n')
            if 'gain disadvantage' in spell.action:
                if target.advantage:
                    target.advantage = False
                    print(f'{target.name} has lost advantage.\n')
                else:
                    target.disadvantage = True
                    print(f'{target.name} is now disadvantaged at attacking!\n')
            if 'become ranged' in spell.action:
                target.is_ranged = True
                print(f'{target.name} can now attack from range!\n')
            if 'lose range' in spell.action:
                target.is_ranged = False
                print(f'{target.name} has lost its distance and can now be blocked.\n')
            self.graveyard.append(spell)
        self.spellbook.remove(spell)
        self.is_active = False

    def end_round_upkeep(self):
        for unit in self.front_line:
            if unit.is_burn:
                unit.lose_health(random.randint(1, 6))
                if self.roll_status_die() > 13:
                    unit.is_burn = False
            if unit.is_poison:
                unit.lose_health(random.randint(1, 3))
            if unit.is_dead:
                self.graveyard.append(unit)
                self.front_line.remove(unit)
            unit.is_active = True
            unit.gain_health(unit.health_regen)
        self.gain_mana(self.mana_regen)

    
class Creature(Unit):
    def __init__(self, name, school, max_health, mana_cost, weapon, attack_dice, armor=0, is_ranged=False, health_regen=0):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged, health_regen)
        self.mana_cost = mana_cost

    def __repr__(self):
        return f"{self.name} is a {' '.join(self.school)} creature that costs {self.mana_cost} mana to summon.  It has {self.health} health + {self.armor} armor and attacks with {self.weapon} using d{self.attack_dice} dice."


class Spell:
    def __init__(self, name, school, action, attack_dice, mana_cost):
        self.name = name
        self.school = school
        self.action = action
        self.attack_dice = attack_dice
        self.mana_cost = mana_cost

    def __repr__(self):
        return f"{self.name} is a {' '.join(self.school)} spell that costs {self.mana_cost} mana.  Its target will {' and '.join(self.action)} using d{self.attack_dice} dice."
    
    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your spell dice rolled {sum}')
        return sum




########TEST AREA#########
dragon1 = Creature("Alfiya", ['Holy', 'dragon'], 19, 24, "holy dragon breath", [8, 8, 6], 3)
cleric1 = Creature("Artemis", ['Holy', 'cleric'], 10, 14, "a spear", [6, 6], 1, True)
angel1 = Creature("Cassiel", ['Holy', 'angel'], 8, 9, 'holy magic', [4, 4])
angel2 = Creature("Guardian Angel", ['Holy', 'angel'], 12, 12, 'a shortsword', [8, 8], 1)
heal1 = Spell("Minor Restoration", ['Holy', 'healing'], ["heal"], [4, 4], 6)
fireball1 = Spell("Fireball", ['Fire', 'attack'], ["take damage"], [10, 4, 4], 12)
sludge_bomb = Spell("Sludge Bomb", ['Poison', 'attack'], ['take damage', 'be poisoned'], [6, 6], 5)


#angel2.attack(dragon1)
#angel1.attack(dragon1)
#dragon1.gain_health(dragon1.roll_dice())

priestess = Mage("Asyra", "Holy", 34, 9, 9, "the Staff of Asyra", [6, 6])
priestess.spellbook = [dragon1, cleric1, angel1, angel2, heal1, fireball1, sludge_bomb]
warlock = Mage('Taylor', 'Demon', 38, 11, 9, 'a fire whip', [8, 10], 3)

priestess.cast_spell(dragon1)
priestess.cast_spell(cleric1)
before = [unit.name for unit in priestess.front_line if unit.is_active]
priestess.end_round_upkeep()
warlock.attack(priestess)
active = [unit.name for unit in priestess.front_line if unit.is_active]
print(before)
print(active)