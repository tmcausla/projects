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
        self.enemy = None

    def gain_health(self, value):
        print(f'{self.name} is gaining {value} health.')
        self.health += value
        self.is_dead = False
        if self.health > self.max_health:
            self.health = self.max_health
        print(f'{self.name} now has {self.health} health.\n')
    
    def lose_health(self, value):
        print(f'{self.name} is taking {value} damage.')
        if self.armor > 0:
            print(f'{self.name} has {self.armor} armor.')
            if value >= self.armor:
                value -= self.armor
                self.armor = 0    
            else:
                self.armor -= value
                print(f'{self.name} now has {self.health} health and {self.armor} armor.')
                return
        self.health -= value
        if self.health <= 0:
            self.health = 0
            self.is_dead = True
            self.is_active = False
            self.cure_status()
        print(f'{self.name} now has {self.health} health and {self.armor} armor.')
        if self.health == 0:
            print(f'{self.name} is dead!')

    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your attack dice rolled {sum}.')
        return sum

    def roll_status_die(self):
        result = random.randint(1, 20)
        print(f'Status die rolled {result}.')
        return result

    def attack(self, target):
        if isinstance(target, Mage) and not self.is_ranged:
            target = target.choose_guard()
        print(f'{self.name} is attacking {target.name}.')
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
        print('---------------')

    def cure_status(self):
        self.is_burn = False
        self.is_poison = False
        self.is_weak = False
        self.disadvantage = False
        print(f'{self.name} no longer suffers from negative conditions.\n')

    def get_targets(self):
        return [unit for unit in self.enemy.front_line]

    def list_targets(self):
        targets = self.get_targets()
        print('---------------')
        if len(targets) < 1:
            print('There are no available targets.')
        else:
            print('These are your available targets:')
            for i in range(len(targets)):
                print(f'{i + 1} - {targets[i]}')
        print('---------------')

    def choose_target(self):
        self.list_targets()
        valid_targets = self.get_targets()
        if len(valid_targets) < 1:
            return None
        valid_range = [str(i + 1) for i in range(len(valid_targets))]
        target = input('Pick your target from the list above and press Enter.\n')
        while target not in valid_range:
            target = input('That is not a valid target. Please choose a number from the list above and press Enter.\n')
        return valid_targets[int(target) - 1]


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
        print(f'{self.name} now has {self.mana} mana.')

    def lose_mana(self, value):
        self.mana -= value
        if self.mana < 0:
            self.mana = 0
        print(f'{self.name} now has {self.mana} mana.')

    def get_spellbook(self):
        return [spell for spell in self.spellbook]

    def list_spellbook(self):
        print('---------------')
        if len(self.spellbook) < 1:
            print('You have no available spells to cast.')
        else:
            print('Spells available to be cast:')
            for i in range(len(self.spellbook)):
                print(f'{i + 1} - {self.spellbook[i]}')
        print('---------------')

    def get_front_line(self):
        return [unit for unit in self.front_line]

    def list_front_line(self):
        print('---------------')
        if len(self.front_line) < 1:
            print('You have no allies in the arena!')
        else:
            print('Your allies in the arena are:')
            for i in range(len(self.front_line)):
                print(f'{i + 1} - {self.front_line[i]}')
        print('---------------')

    def get_active(self):
        return [unit for unit in self.front_line if unit.is_active]

    def list_active(self):
        print('---------------')
        if len(self.get_active()) < 1:
            print('You have no units that can take an action. You must wait until the next round.')
        else:
            print('These units can still take an action:')
            active = self.get_active()
            for i in range(len(active)):
                print(f'{i + 1} - {active[i]}')
        print('---------------')

    def get_graveyard(self):
        return [spell for spell in self.graveyard]

    def list_graveyard(self):
        print('---------------')
        if len(self.graveyard) < 1:
            print('Your graveyard pile is empty.')
        else:
            print('These are your used spells and defeated creatures:')
            for i in range(len(self.graveyard)):
                print(f'{i + 1} - {self.graveyard[i]}')
        print('---------------')

    def choose_guard(self):
        active = self.get_active()
        if len(active) < 1:
            return self
        valid_range = [str(i + 1) for i in range(len(active))]
        print(f'Your mage {self.name} is being targeted, you may choose a creature to block the attack. Select a number and press Enter.')
        for i in range(len(active)):
            if i == 0:
                print(f'{i + 1} - No guard, allow {self.name} to take damage.')
            else:
                print(f'{i + 1} - {active[i]}')
        guard = input()
        while guard not in valid_range:
            guard = input('That is not a valid choice.  Please select a number from the list above and press Enter.\n')
        if int(guard) > 1:
            active[int(guard) - 1].is_active = False
            print(f'{self.name} is blocking the attack with {active[int(guard) - 1].name}.')
        return active[int(guard) - 1]

    def choose_spell(self):
        self.list_spellbook()
        if len(self.spellbook) < 1:
            return None
        spells = self.get_spellbook()
        valid_range = [str(i + 1) for i in range(len(spells))]
        spell = input('Choose the spell you wish to cast and press Enter.\n')
        while spell not in valid_range:
            spell = input('That is not a valid spell. Please choose a number from the list above and press Enter.\n')
        return spells[int(spell) - 1]

    def choose_active_unit(self):
        self.list_active()
        active = self.get_active()
        if len(active) < 1:
            return None
        valid_range = [str(i + 1) for i in range(len(active))]
        active_unit = input('Choose a unit to take an action and press Enter.\n')
        while active_unit not in valid_range:
            active_unit = input('That is not a valid unit. Please choose a number from the list above and press Enter.\n')
        return active[int(active_unit) - 1]

    def cast_spell(self, spell, target=None):
        self.lose_mana(spell.mana_cost)
        if isinstance(spell, Creature):
            self.front_line.append(spell)
            print(f'{self.name} has summoned {spell.name} to the arena.\n')
        else:
            if target is None:
                print(f'{self.name} is casting {spell.name}.')
            else:
                print(f'{self.name} is casting {spell.name} on {target.name}.')
            if 'heal' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        unit.gain_health(spell.roll_dice())
                else:
                    target.gain_health(spell.roll_dice())
            if 'gain armor' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        unit.armor += spell.roll_dice()
                        print(f'{unit.name} has gained armor.')
                    print('')
                else:
                    target.armor += spell.roll_dice()
                    print(f'{target.name} has gained armor.\n')
            if 'melt armor' in spell.action or 'Acid' in spell.school:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.roll_status_die() > spell.status_roll:
                            unit.full_armor = 0
                            unit.armor = 0
                            print(f"{unit.name}'s armor melted away!")
                    print('')
                else:
                    if target.roll_status_die() > spell.status_roll:
                        target.full_armor = 0
                        target.armor = 0
                        print(f"{target.name}'s armor melted away!\n")
            if 'regenerate health' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        unit.health_regen += spell.roll_dice()
                        print(f'{unit.name} will start to regenerate health between rounds.')
                    print('')
                else:
                    target.health_regen += spell.roll_dice()
                    print(f'{target.name} will start to regenerate health between rounds.\n')
            if 'take damage' in spell.action:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        unit.lose_health(spell.roll_dice())
                else:
                    target.lose_health(spell.roll_dice())
            if 'lose mana' in spell.action:
                target.lose_mana(spell.roll_dice())
            if 'be poisoned' in spell.action or 'Poison' in spell.school:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.roll_status_die() > spell.status_roll:
                            unit.is_poison = True
                            print(f'{unit.name} is poisoned!')
                    print('')
                else:
                    if target.roll_status_die() >= spell.status_roll:
                        target.is_poison = True
                        print(f'{target.name} is poisoned!\n')
            if 'cure status' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        unit.cure_status()
                    print('')
                else:
                    target.cure_status()
            if 'be burned' in spell.action or 'Fire' in spell.school:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.roll_status_die() > spell.status_roll:
                            unit.is_burn = True
                            print(f'{unit.name} is burned!')
                    print('')
                else:
                    if target.roll_status_die() >= spell.status_roll:
                        target.is_burn = True
                        print(f'{target.name} is burned!\n')
            if 'be weakened' in spell.action:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.roll_status_die() > spell.status_roll:
                            unit.is_weak = True
                            print(f'{unit.name} is feeling weak!')
                    print('')
                else:
                    if target.roll_status_die() >= spell.status_roll:
                        target.is_weak = True
                        print(f'{target.name} is feeling weak!\n')
            if 'gain advantage' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        if unit.disadvantage:
                            unit.disadvantage = False
                            print(f'{unit.name} is no longer at a disadvantage.')
                        else:
                            unit.advantage = True
                            print(f'{unit.name} has gained advantage for attack!')
                    print('')
                else:
                    if target.disadvantage:
                        target.disadvantage = False
                        print(f'{target.name} is no longer at a disadvantage.\n')
                    else:
                        target.advantage = True
                        print(f'{target.name} has gained advantage for attack!\n')
            if 'gain disadvantage' in spell.action:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.advantage:
                            unit.advantage = False
                            print(f'{unit.name} has lost advantage.\n')
                        else:
                            unit.disadvantage = True
                            print(f'{unit.name} is now disadvantaged at attacking!\n')
                else:
                    if target.advantage:
                        target.advantage = False
                        print(f'{target.name} has lost advantage.\n')
                    else:
                        target.disadvantage = True
                        print(f'{target.name} is now disadvantaged at attacking!\n')
            if 'become ranged' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        unit.is_ranged = True
                        print(f'{unit.name} can now avoid guards!')
                    print('')
                else:
                    target.is_ranged = True
                    print(f'{target.name} can now avoid guards!\n')
            if 'lose range' in spell.action:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        unit.is_ranged = False
                        print(f'{unit.name} can now be blocked.')
                    print('')
                else:
                    target.is_ranged = False
                    print(f'{target.name} can now be blocked.\n')
            if 'be dazed' in spell.action:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.roll_status_die() > spell.status_roll:
                            unit.is_active = False
                            print(f'{unit.name} will not be able to act this round.')
                    print('')
                else:
                    if target.roll_status_die() > spell.status_roll:
                        target.is_active = False
                        print(f'{target.name} will not be able to act this round.\n')
            if 'be inspired' in spell.action:
                if 'area' in spell.school:
                    for unit in self.front_line:
                        unit.is_active = True
                        print(f'{unit.name} is ready to act again!')
                    print('')
                else:
                    target.is_active = True
                    print(f'{target.name} is ready to act again!\n')
            if 'be resurrected' in spell.action:
                targets = self.get_graveyard() + self.enemy.get_graveyard()
                valid_target = [str(i + 1) for i in range(len(targets))]
                for i in range(len(targets)):
                    print(f'{i + 1} - {targets[i]}')
                resurrect = input('Who would you like to resurrect? Select a target and press Enter.\n')
                while (resurrect) not in valid_target:
                    resurrect = input('That is not a valid target. Please select a number from the list above and press Enter.\n')
                resurrect = int(resurrect) - 1
                targets[resurrect].gain_health(spell.roll_dice() * 2)
                targets[resurrect].is_poison = True
                targets[resurrect].is_weak = True
                targets[resurrect].attack_dice.pop(-1)
                print(f'{targets[resurrect].name} is back from the dead!\n')
                self.front_line.append(targets[resurrect])
            self.graveyard.append(spell)
        self.spellbook.remove(spell)
        self.is_active = False
        print('---------------')

    def end_round_upkeep(self):
        for unit in self.front_line:
            if unit.is_burn:
                print(f"{unit.name} takes damage from a burn.")
                unit.lose_health(random.randint(1, 6))
                if self.roll_status_die() > 13:
                    unit.is_burn = False
                    print(f'{unit.name} has treated their burn.')
            if unit.is_poison:
                print(f'{unit.name} takes damage from poison.')
                unit.lose_health(random.randint(0, 3))
                if self.roll_status_die() > 17:
                    unit.is_poison = False
                    print(f'{unit.name} has neutralized their poison wound.')
            if unit.is_weak:
                if self.roll_status_die() > 15:
                    unit.is_weak = False
                    print(f'{unit.name} has regained their strength.')
            if unit.is_dead:
                print(f'{unit.name} has been cleared from the arena.\n')
                self.graveyard.append(unit)
                self.front_line.remove(unit)
            else:
                unit.is_active = True
                if unit.armor < unit.full_armor:
                    unit.armor = unit.full_armor
                if unit.health_regen > 0:
                    unit.gain_health(unit.health_regen)
                    unit.health_regen -= 1
        self.gain_mana(self.mana_regen)
        print('---------------')

    
class Creature(Unit):
    def __init__(self, name, school, max_health, mana_cost, weapon, attack_dice, armor=0, is_ranged=False, health_regen=0):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged, health_regen)
        self.mana_cost = mana_cost

    def __repr__(self):
        return f"{self.name} is a {' '.join(self.school)} creature that costs {self.mana_cost} mana to summon.  It has {self.health} health + {self.armor} armor and attacks with {self.weapon} using d{self.attack_dice} dice."


class Spell:
    def __init__(self, name, school, action, attack_dice, mana_cost, status_roll=None):
        self.name = name
        self.school = school
        self.action = action
        self.attack_dice = attack_dice
        self.mana_cost = mana_cost
        self.status_roll = status_roll

    def __repr__(self):
        return f"{self.name} is a {' '.join(self.school)} spell that costs {self.mana_cost} mana.  Its target(s) will {' and '.join(self.action)} using d{self.attack_dice} dice."
    
    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your spell dice rolled {sum}.')
        return sum




########TEST AREA#########
dragon1 = Creature("Alfiya", ['Holy', 'dragon'], 19, 24, "holy dragon breath", [10, 8, 6], 3)
cleric1 = Creature("Artemis", ['Holy', 'cleric'], 10, 14, "a spear", [6, 6], 1, True)
angel1 = Creature("Cassiel", ['Holy', 'angel'], 8, 9, 'holy magic', [4, 4])
angel2 = Creature("Guardian Angel", ['Holy', 'angel'], 12, 12, 'a shortsword', [8, 8], 1)
heal1 = Spell("Renewing Rain", ['Water', 'area', 'healing'], ["heal"], [4, 4], 6)
fireball1 = Spell("Firestorm", ['Fire', 'area', 'attack'], ["take damage"], [10, 4, 4], 12, 12)
sludge_bomb = Spell("Sludge Bomb", ['Poison', 'attack'], ['take damage', 'be poisoned'], [6, 6], 5, 14)
revive1 = Spell('Resurrect test', ['Holy', 'resurrection'], ['be resurrected'], [6, 6], 4)



priestess = Mage("Asyra", "Holy", 34, 9, 9, "the Staff of Asyra", [6, 6])
priestess.spellbook = [dragon1, cleric1, angel1, angel2, heal1, fireball1, sludge_bomb]
warlock = Mage('Taykor', 'Demon', 38, 11, 9, 'a fire whip', [8, 10], 3)
warlock.spellbook = [fireball1, sludge_bomb]
priestess.enemy, warlock.enemy = warlock, priestess
for spell in priestess.spellbook:
    spell.enemy = warlock
for spell in warlock.spellbook:
    spell.enemy = priestess

