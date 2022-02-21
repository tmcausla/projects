import random
import copy

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

#allows a unit to gain health, caps healing at max_health value
    def gain_health(self, value):
        print(f'{self.name} is gaining {value} health.')
        self.health += value
        self.is_dead = False
        if self.health > self.max_health:
            self.health = self.max_health
        print(f'{self.name} now has {self.health} health.\n')

#takes health away from a unit taking armor into account, when health reaches zero unit will cure negative status and lose active status
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

#rolls the set of dice unique to each spell and unit
    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your attack dice rolled {sum}.')
        return sum

#rolls a d20
    def roll_status_die(self):
        result = random.randint(1, 20)
        print(f'Status die rolled {result}.')
        return result

#a unit's method for attacking an enemy, player can choose a guard if mage is being targeted, not invoked for spells (melee only)
    def attack(self):
        target = self.choose_target()
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
            print('Target is weak! Roll your smallest die and add the result.')
            attack_value += random.randint(1, self.attack_dice[-1])
        target.lose_health(attack_value)
        self.is_active = False
        print('---------------')

#removes negative status conditions from a unit
    def cure_status(self):
        self.is_burn = False
        self.is_poison = False
        self.is_weak = False
        self.disadvantage = False
        print(f'{self.name} no longer suffers from negative conditions.\n')

#returns a list of available targets in the enemy's front line
    def get_targets(self):
        return [unit for unit in self.enemy.front_line]

#prints a list of available targets in the enemy's front line
    def list_targets(self):
        targets = self.get_targets()
        print('---------------')
        if len(targets) < 1:
            print('There are no available targets.')
        else:
            print('These are your available targets:')
            for i in range(len(targets)):
                print(f'{i + 1} - {targets[i].name} currently has {targets[i].health} health + {targets[i].armor} armor. It attacks with d{targets[i].attack_dice} dice.')
        print('---------------')

#returns input for selecting a target
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

#defines Mage class, constructor initializes spellbook, front_line, graveyard lists
class Mage(Unit):
    def __init__(self, name, school, max_health, start_mana, mana_regen, weapon, attack_dice, armor=0, is_ranged=False, health_regen=0):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged, health_regen)
        self.mana = start_mana
        self.mana_regen = mana_regen
        self.spellbook = []
        self.front_line = [self]
        self.graveyard = []
        self.is_active = True

#return Mage's name and school, health and armor and attack, mana
    def __repr__(self):
        return f"{self.name} is a {self.school} Mage.  They have {self.health} health + {self.armor} armor and attack with {self.weapon} using d{self.attack_dice} dice.  They have {self.mana} mana and regain {self.mana_regen} mana at the start of every round."

#allows a Mage to gain mana, no maximum
    def gain_mana(self, value):
        self.mana += value
        print(f'{self.name} now has {self.mana} mana.')

#takes mana away from a Mage, caps minimum to zero
    def lose_mana(self, value):
        self.mana -= value
        if self.mana < 0:
            self.mana = 0
        print(f'{self.name} now has {self.mana} mana.')

#returns a list of the Mage's spellbook
    def get_spellbook(self):
        return [spell for spell in self.spellbook]

#prints a list of the Mage's spellbook
    def list_spellbook(self):
        print('---------------')
        if len(self.spellbook) < 1:
            print('You have no available spells to cast.')
        else:
            print('Spells available to be cast:')
            for i in range(len(self.spellbook)):
                print(f'{i + 1} - {self.spellbook[i]}')
        print('---------------')

#returns a list of Mage's front line units
    def get_front_line(self):
        return [unit for unit in self.front_line]

#prints a list of Mage's front line units
    def list_front_line(self):
        print('---------------')
        if len(self.front_line) < 1:
            print('You have no allies in the arena!')
        else:
            print('Your allies in the arena are:')
            for i in range(len(self.front_line)):
                print(f'{i + 1} - {self.front_line[i]}')
        print('---------------')

#returns a list of Mage's active units on front line
    def get_active(self):
        return [unit for unit in self.front_line if unit.is_active]

#prints a list of active units on Mage's front line
    def list_active(self):
        print('---------------')
        if len(self.get_active()) < 1:
            print(f'{self.name} has no units that can take an action. They must wait until the next round.')
        else:
            print(f"These are {self.name}'s units that can still take an action:")
            active = self.get_active()
            for i in range(len(active)):
                print(f'{i + 1} - {active[i]}')
        print('---------------')

#returns a list of Mage's graveyard
    def get_graveyard(self):
        return [spell for spell in self.graveyard]

#prints a list of Mage's graveyard contents
    def list_graveyard(self):
        print('---------------')
        if len(self.graveyard) < 1:
            print('Your graveyard pile is empty.')
        else:
            print('These are your used spells and defeated creatures:')
            for i in range(len(self.graveyard)):
                print(f'{i + 1} - {self.graveyard[i]}')
        print('---------------')

#returns input for choosing a guard when Mage is target of an attack
    def choose_guard(self):
        active = self.get_active()
        if len(active) < 1:
            return self
        valid_range = [str(i + 1) for i in range(len(active))]
        print(f'Your mage {self.name} is being targeted, you may choose a creature to block the attack. Select a number and press Enter.')
        for i in range(len(active)):
            if i == 0:
                print(f'{i + 1} - No guard, allow {self.name} to take damage. They currently have {self.health} health + {self.armor} armor.')
            else:
                print(f'{i + 1} - {active[i].name} currently has {active[i].health} health + {active[i].armor} armor.')
        guard = input()
        while guard not in valid_range:
            guard = input('That is not a valid choice.  Please select a number from the list above and press Enter.\n')
        if int(guard) > 1:
            active[int(guard) - 1].is_active = False
            print(f'{self.name} is blocking the attack with {active[int(guard) - 1].name}.')
        return active[int(guard) - 1]

#returns input for choosing a spell from Mage's spellbook
    def choose_spell(self):
        self.list_spellbook()
        if len(self.spellbook) < 1:
            return None
        spells = self.get_spellbook()
        valid_range = [str(i + 1) for i in range(len(spells))]
        print(f'You have {self.mana} mana.')
        spell = input('Choose the spell you wish to cast and press Enter.\n')
        while spell not in valid_range:
            spell = input("That is not a valid spell. Please choose a number from the list above and press Enter.\n")
        target_spell = spells[int(spell) - 1]
        if target_spell.mana_cost > self.mana:
            print('You do not have enough mana to cast that spell. Please try again.')
            return self.choose_spell()
        return target_spell

#returns input for choosing an active unit from the Mage's front line
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

#handles effects of spells based on keywords found in school and action properties of spell
    def cast_spell(self):
        spell = self.choose_spell()
        self.lose_mana(spell.mana_cost)
        if isinstance(spell, Creature):
            self.front_line.append(spell)
            print(f'{self.name} has summoned {spell.name} to the arena.\n')
        else:
            if 'area' in spell.school:
                print(f'{self.name} is casting {spell.name}.')
            else:
                target = self.choose_target()
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
            if 'take damage' in spell.action or 'trap' in spell.school:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        unit.lose_health(spell.roll_dice())
                else:
                    target.lose_health(spell.roll_dice())
            if 'lose mana' in spell.action:
                target.lose_mana(spell.roll_dice())
            if 'gain mana' in spell.action:
                self.gain_mana(spell.roll_dice())
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
            if 'be weakened' in spell.action or 'trap' in spell.school:
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
            if 'gain disadvantage' in spell.action or 'trap' in spell.school:
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
            if 'be dazed' in spell.action or 'trap' in spell.school:
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
            if 'be cursed' in spell.action or 'Curse' in spell.school:
                if 'area' in spell.school:
                    for unit in self.enemy.front_line:
                        if unit.roll_status_die() > spell.status_roll:
                            unit.is_poison = True
                            unit.is_burn = True
                            unit.is_weak = True
                            unit.disadvantage = True
                            print(f'{unit.name} has been cursed!')
                    print('')
                else:
                    if target.roll_status_die() > spell.status_roll:
                        target.is_poison = True
                        target.is_burn = True
                        target.is_weak = True
                        target.disadvantage = True
                        print(f'{target.name} has been cursed!\n')
            if 'be resurrected' in spell.action:
                graveyard = self.get_graveyard() + self.enemy.get_graveyard()
                targets = [unit for unit in graveyard if isinstance(unit, Creature)]
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

#activates negative conditions and rolls to remove them, dead units cleared from arena, health and mana regen occurs
    def end_round_upkeep(self):
        for unit in self.front_line:
            if unit.is_burn:
                print(f"{unit.name} takes damage from a burn.")
                unit.lose_health(random.randint(2, 6))
                if self.roll_status_die() > 13:
                    unit.is_burn = False
                    print(f'{unit.name} has treated their burn.')
            if unit.is_poison:
                print(f'{unit.name} takes damage from poison.')
                unit.lose_health(random.randint(1, 3))
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


#defines Creature class, constructor takes mana_cost as parameter
class Creature(Unit):
    def __init__(self, name, school, max_health, mana_cost, weapon, attack_dice, armor=0, is_ranged=False, health_regen=0):
        super().__init__(name, school, max_health, weapon, attack_dice, armor, is_ranged, health_regen)
        self.mana_cost = mana_cost

#returns Creature's name and school and mana cost, health and armor and attack
    def __repr__(self):
        return f"{self.name} is a {' '.join(self.school)} creature that costs {self.mana_cost} mana to summon.  It has {self.health} health + {self.armor} armor and attacks with {self.weapon} using d{self.attack_dice} dice."


#defines Spell class, keywords for spell effects found in school and action properties
class Spell:
    def __init__(self, name, school, action, attack_dice, mana_cost, status_roll=None):
        self.name = name
        self.school = school
        self.action = action
        self.attack_dice = attack_dice
        self.mana_cost = mana_cost
        self.status_roll = status_roll

#returns Spell's name and school and mana cost, effect and attack dice
    def __repr__(self):
        return f"{self.name} is a {' '.join(self.school)} spell that costs {self.mana_cost} mana.  Its target(s) will {' and '.join(self.action)} using d{self.attack_dice} dice."

#rolls set of dice unique to spell
    def roll_dice(self):
        sum = 0
        for die in self.attack_dice:
            sum += random.randint(1, die)
        print(f'Your spell dice rolled {sum}.')
        return sum


###DECLARING VARIABLES####
#creatures and spells for Priestess Mage spellbook
dragon1 = Creature("Alfiya", ['Holy', 'Dragon'], 21, 24, 'holy dragon breath', [10, 8, 4], 6)
cleric1 = Creature('Artemis', ['Holy', 'Cleric'], 14, 14, 'a spear', [8, 4], 2, True)
angel1 = Creature('Guardian Angel', ['Holy', 'Angel'], 14, 12, 'a shortsword', [6, 4], 2)
angel2 = Creature('Cassiel', ['Holy', 'Angel', 'Cleric'], 10, 9, 'divine magic', [4, 4], 1, False, 10)
angel3 = Creature('Valshalla', ['Holy', 'Angel'], 16, 21, 'a lightning sword', [8, 6, 4], 3, False, 4)
angel4 = Creature('Selesius', ['Holy', 'Angel'], 15, 21, 'a halberd', [8, 6, 4], 4, False, 4)
angel5 = Creature('Samandriel', ['Holy', 'Hero', 'Angel'], 17, 21, "the greatsword 'Starfire'", [10, 6, 4], 4, False, 4)
dispel1 = Spell('Dispel', ['Metamagic', 'Cure'], ['cure status'], [0], 4)
heal1 = Spell('Lay Hands', ['Holy', 'Healing'], ['heal', 'cure status'], [12, 6], 9)
heal2 = Spell('Minor Heal', ['Holy', 'Healing'], ['heal'], [6, 4], 5)
regen1 = Spell('Sacred Ground', ['Holy', 'area', 'Regeneration'], ['regenerate health'], [6, 4], 8)
divine_protect = Spell('Divine Protection', ['Holy', 'Protection'], ['gain armor', 'cure status'], [6, 6], 8)
holy1 = Spell('Pillar of Righteous Flame', ['Holy', 'Fire', 'attack'], ['take damage', 'be burned', 'be dazed', 'be weakened'], [10, 6, 4], 14, 15)
holy2 = Spell('Sunfire Burst', ['Holy', 'attack'], ['take damage', 'gain disadvantage'], [6, 4], 7)
holy3 = Spell('Luminous Blast', ['Holy', 'attack'], ['take damage', 'be dazed'], [10, 4], 5, 18)
priestess_spellbook = [cleric1, angel1, angel2, angel3, angel4, angel5, dragon1, heal1, heal2, dispel1, regen1, divine_protect, holy1, holy2, holy3]
priestess = Mage('Priestess of Asyra', 'Holy', 44, 15, 12, 'the Staff of Asyra', [8, 4], 4, True, 10)
priestess.spellbook = priestess_spellbook

#creatures and spells for Dwarven Warlord Mage spellbook
dwarf1 = Creature('Dwarf Kriegshammer', ['Dwarven', 'Soldier'], 11, 11, 'a kriegshammer', [12, 6], 4)
dwarf2 = Creature('Dwarf Panzergarde', ['Dwarven', 'Soldier'], 14, 11, 'a war hammer', [6, 6], 6)
dwarf3 = Creature('Dwarf Kriegsbiel', ['Dwarven', 'Soldier'], 11, 11, 'a war axe', [8, 6, 4], 2)
dwarf4 = Creature('Anvil Throne Crossbowman', ['Dwarven', 'Soldier'], 10, 11, 'a crossbow', [6, 6], 2, True)
dwarf5 = Creature('Ludwig Bolstorm', ['Dwarven', 'Hero', 'Soldier'], 11, 13, 'a repeating crossbow', [8, 4, 4], 4, True)
machine1 = Creature('Ballista', ['Soldier', 'War Machine'], 10, 8, 'a giant bolt', [20], 4, True)
elephant1 = Creature('Titanodon', ['Soldier', 'Animal', 'Monstrosity'], 20, 19, 'tusks', [12, 8], 4)
golem1 = Creature('Iron Golem', ['Earth', 'Golem'], 15, 13, 'iron fists', [12, 4], 10)
heal4 = copy.deepcopy(heal2)
dispel2 = copy.deepcopy(dispel1)
war1 = Spell('Whirling Strike', ['Soldier', 'area','attack'], ['take damage'], [6, 6], 9)
war2 = Spell('Spiked Pit', ['Soldier', 'Earth', 'trap'], ['spring a trap'], [8, 4], 10, 12)
war3 = Spell('Fortified Position', ['Soldier', 'area','Command'], ['gain armor', 'gain advantage'], [8, 8], 6)
earth1 = Spell('Hail of Stones', ['Earth', 'area', 'attack'], ['take damage', 'gain disadvantage'], [8, 4, 4], 8, 8)
earth2 = Spell('Hurl Boulder', ['Earth', 'attack'], ['take damage', 'be dazed'], [12, 8], 8, 15)
warlord_spellbook = [dwarf1, dwarf2, dwarf3, dwarf4, dwarf5, machine1, elephant1, golem1, heal4, dispel2, war1, war2, war3, earth1, earth2]
warlord = Mage('Anvil Throne Warlord', 'Soldier', 44, 12, 9, "Eisenach's Forge Hammer", [8, 8, 4], 14)
warlord.spellbook = warlord_spellbook

#creatures and spells for Siren Mage spellbook
shark1 = Creature('Deptonne Berserker', ['Aquatic', 'Deptonne'], 14, 12, 'razor claws and teeth', [6, 6], 2)
shark2 = Creature('Deptonne Bloodshaman', ['Aquatic', 'Deptonne', 'Cleric'], 10, 8, 'a coral staff', [6, 4], 2, False, 5)
shark3 = Creature('Shoalsdeep Thrasher', ['Aquatic', 'Deptonne', 'Pirate'], 8, 5, 'a serrated sword', [4, 4, 4], 2)
pirate1 = Creature('Merren Harpooner', ['Aquatic', 'Merren', 'Pirate'], 12, 12, 'a harpoon', [8, 4], 2, True)
crocodile1 = Creature('Shoalsdeep Crocodile', ['Nature', 'Reptile'], 15, 15, 'death roll', [10, 8], 6)
kraken1 = Creature('Kraken', ['Aquatic', 'Octopus', 'Monstrosity'], 21, 21, 'tentacles', [12, 6, 4], 4)
kraken2 = Creature('Sherean Leviathan', ['Aquatic', 'Fish','Monstrosity'], 26, 22, 'an endless maw', [12, 8, 4], 4)
song1 = Spell('Chant of Rage', ['Psychic', 'area', 'Song'], ['be weakened', 'lose range', 'gain advantage'], [0], 6, 8)
song2 = Spell('Song of Love', ['Psychic', 'area', 'Song'], ['cure status', 'regenerate health', 'gain armor'], [6, 4], 6)
song3 = Spell('Lullaby', ['Psychic', 'area', 'Song'], ['be dazed', 'be weakened', 'gain disadvantage'], [0], 8, 12)
song4 = Spell('Ballad of Courage', ['Soldier', 'area', 'Song'], ['be inspired', 'gain advantage'], [0], 7)
heal_rain1 = Spell('Renewing Rain', ['Aquatic', 'area', 'healing'], ['heal', 'cure status', 'regenerate health'], [6, 4], 9)
water1 = Spell('Hydrothermal Vent', ['Aquatic', 'trap'], ['spring a trap'], [10, 4], 8, 12)
water2 = Spell('Tsunami', ['Aquatic', 'area', 'attack'], ['take damage'], [6, 6, 6], 14)
water3 = Spell('Geyser', ['Aquatic', 'attack'], ['take damage', 'be burned'], [6, 4], 4, 10)
siren_spellbook = [shark1, shark2, shark3, pirate1, crocodile1, kraken1, kraken2, song1, song2, song3, song4, heal_rain1, water1, water2, water3]
siren = Mage('Siren of Shoalsdeep', 'Aquatic', 40, 13, 12, 'Shoalsdeep Trident', [8, 6, 4], 6, False, 16)
siren.spellbook = siren_spellbook

#creatures and spells for Necromancer Mage spellbook
skeleton1 = Creature('Skeletal Minion', ['Skeleton', 'Undead', 'Soldier'], 8, 5, 'a femur', [6, 4], 2)
skeleton2 = Creature('Deathfang', ['Skeleton', 'Undead', 'Animal'], 11, 8, 'fangs', [6, 4], 3)
skeleton3 = Creature('Skeletal Archer', ['Skeleton', 'Undead', 'Soldier'], 11, 11, 'a bow', [8, 4], 2, True)
zombie1 = Creature('Zombie Minion', ['Undead', 'Zombie'], 9, 7, 'biting', [6, 6])
zombie2 = Creature('Zombie Brute', ['Undead', 'Zombie'], 12, 11, 'mangling claws', [8, 8], 2)
zombie3 = Creature('Ravenous Ghoul', ['Undead'], 11, 13, 'biting', [8, 8], 4)
zombie4 = Creature('Plague Zombie', ['Undead', 'Zombie'], 6, 9, 'diseased strikes', [4, 4, 4], 8)
demon1 = Creature('Malacoda', ['Poison', 'Demon', 'Monstrosity'], 15, 16, 'talons', [8, 8], 6, False, 6)
dispel3 = copy.deepcopy(dispel1)
dispel4 = copy.deepcopy(dispel1)
curse1 = Spell('Arcane Corruption', ['Necro', 'Curse'], ['take damage', 'be cursed'], [6, 4], 7, 11)
necro1 = Spell('Zombie Frenzy', ['Necro', 'area'], ['be inspired', 'gain advantage', 'lose range', 'gain disadvantage'], [0], 9)
necro2 = Spell('Drain Soul', ['Necro', 'Vampiric'], ['gain mana', 'lose mana'], [6, 4], 0)
necro3 = Spell('Animate Dead', ['Necro', 'Resurrection'], ['be resurrected'], [10, 6], 12)
necro4 = copy.deepcopy(necro3)
necromancer_spellbook = [skeleton1, skeleton2, skeleton3, zombie1, zombie2, zombie3, zombie4, demon1, dispel3, dispel4, curse1, necro1, necro2, necro3, necro4]
necromancer = Mage('Darkfenne Necromancer', 'Necro', 42, 13, 11, 'the Libro Mortuos tome', [8, 4], 8, True)
necromancer.spellbook = necromancer_spellbook

#creatures and spells for Druid Mage spellbook
plant1 = Creature('Togorah', ['Nature', 'Tree'], 20, 21, 'massive branches', [12, 6, 4], 4, health_regen=15)
plant2 = Creature('Vine Snapper', ['Nature', 'Vine'], 12, 7, 'biting thorns', [8, 4], health_regen=9)
plant3 = Creature('Thornlasher', ['Nature', 'Vine'], 13, 7, 'ensnaring vines', [6, 4], health_regen=10)
plant4 = Creature('Raptor Vine', ['Nature', 'Vine'], 12, 9, 'voracious bites', [10, 4], health_regen=9)
plant5 = Creature('Corrosive Orchid', ['Nature', 'Flower'], 9, 7, 'corrosive mist', [4, 4, 4], 0, True, health_regen=6)
plant6 = Creature('Kralathor', ['Nature', 'Vine', 'Monstrosity'], 15, 16, 'a great maw', [8, 8], 2, False, 10)
spider1 = Creature('Giant Wolf Spider', ['Nature', 'Spider'], 15, 15, 'poison fangs', [8, 8], 4)
plant7 = Spell('Barkskin', ['Nature', 'Healing', 'Protection'], ['gain armor', 'cure status', 'regenerate health'], [6, 6], 4)
heal_rain2 = copy.deepcopy(heal_rain1)
heal5 = copy.deepcopy(heal1)
acid1 = Spell('Acid Ball', ['Acid', 'attack'], ['take damage', 'melt armor'], [4, 4], 5, 4)
plant8 = Spell('Burst of Thorns', ['Nature', 'attack'], ['take damage'], [8, 4], 5)
plant9 = copy.deepcopy(plant8)
plant10 = Spell('Tanglevine', ['Nature', 'area', 'attack'], ['take damage', 'be dazed', 'be weakened'], [4, 4], 5, 13)
plant11 = Spell('Stranglevine', ['Nature', 'attack'], ['take damage', 'gain disadvantage', 'be poisoned'], [8, 4], 7, 10)
druid_spellbook = [plant1, plant2, plant3, plant4, plant5, plant6, spider1, plant7, heal_rain2, heal5, acid1, plant8, plant9, plant10, plant11]
druid = Mage('Wychwood Druid', 'Plant Nature', 45, 12, 13, 'a Vinewhip Staff', [8, 4, 4], 6, True, 14)
druid.spellbook = druid_spellbook

#creatures and spells for Beastmaster Mage spellbook
animal1 = Creature('Galador', ['Nature', 'Protector'], 16, 16, 'lightning antlers', [8, 8], 6)
animal2 = Creature('Dire Wolf', ['Nature', 'Canine'], 13, 12, 'savage bites', [6, 6], 4)
animal3 = Creature('Cervere', ['Nature', 'Feline'], 13, 15, 'claws and biting', [8, 8], 4, True)
animal4 = Creature('Kumanjaran Leopard', ['Nature', 'Feline'], 12, 13, 'wild slashing', [6, 6], 4, True)
animal5 = Creature('Mountain Ram', ['Nature', 'Goat'], 9, 8, 'battering horns', [6, 4], 2)
animal6 = Creature('Redclaw', ['Nature', 'Canine'], 14, 16, 'claws and biting', [10, 6], 6)
animal7 = Creature('Tarok', ['Nature', 'Bird'], 11, 13, 'beak and talons', [6, 6], 5)
animal8 = Creature('Woolly Rhinoceros', ['Nature', 'Rhinoceros'], 14, 16, 'a great horn', [8, 8], 6)
enchant1 = Spell('Lion Savagery', ['Nature', 'area', 'Enchantment'], ['be weakened'], [0], 9, 8)
enchant2 = Spell('Rhino Hide', ['Nature', 'area', 'Enchantment'], ['gain armor', 'regenerate health'], [6, 4], 4)
enchant3 = Spell('Bear Strength', ['Nature', 'area', 'Enchantment'], ['melt armor'], [0], 5, 6)
enchant4 = Spell('Bull Endurance', ['Nature', 'area', 'Enchantment'], ['be inspired'], [0], 5)
enchant5 = Spell('Cheetah Speed', ['Nature', 'area', 'Enchantment'], ['become ranged'], [0], 5)
heal6 = Spell('Mending Wave', ['Holy', 'area', 'Healing'], ['heal', 'cure status'], [4, 4], 5)
dispel5 = copy.deepcopy(dispel1)
beastmaster_spellbook = [animal1, animal2, animal3, animal4, animal5, animal6, animal7, animal8, enchant1, enchant2, enchant3, enchant4, enchant5, heal6, dispel5]
beastmaster = Mage('Johktari Beastmaster', 'Animal Nature', 49, 14, 10, 'a Hunting Bow', [8, 4, 4], 8, True)
beastmaster.spellbook = beastmaster_spellbook

#creatures and spells for Wizard Mage spellbook
magic1 = Creature('Gargoyle Sentry', ['Metamagic', 'Animated'], 16, 11, 'stone fists', [6, 6], 2)
magic2 = Creature('Wind Elemental', ['Wind'], 15, 12, 'wind storms', [8, 4], 0, True)
magic3 = Creature('Water Elemental', ['Aquatic'], 18, 22, 'crashing waves', [10, 8, 4])
magic4 = Creature('Earth Elemental', ['Earth'], 35, 20, 'quake punches', [12, 4, 4])
magic5 = Creature('Fire Elemental', ['Fire'], 17, 20, 'scorching claws', [10, 6, 4])
magic6 = Creature('Darkfenne Hydra', ['Metamagic', 'Serpent'], 17, 16, 'snapping bites', [8, 8], 2, False, 12)
heal7 = copy.deepcopy(heal1)
heal8 = copy.deepcopy(heal6)
dispel6 = copy.deepcopy(dispel1)
electric1 = Spell('Lightning Bolt', ['Lightning', 'attack'], ['take damage', 'be dazed', 'gain disadvantage'], [10, 4], 8, 12)
electric2 = Spell('Chain Lightning', ['Lightning', 'area', 'attack'], ['take damage', 'gain disadvantage'], [10, 4], 12, 10)
earth3 = copy.deepcopy(earth1)
fire1 = Spell('Fireball', ['Fire', 'attack'], ['take damage', 'be burned'], [12, 6], 8, 13)
fire2 = Spell('Fire Storm', ['Fire', 'area', 'attack'], ['take damage', 'be burned'], [10, 6], 11, 15)
water4 = copy.deepcopy(water2)
wizard_spellbook = [magic1, magic2, magic3, magic4, magic5, magic6, heal7, heal8, dispel6, electric1, electric2, earth3, fire1, fire2, water4]
wizard = Mage('Wizard in Sortilege Manor', 'Metamagic and Elements', 42, 14, 14, 'a Staff of the Arcanum', [8, 6], 6, True)
wizard.spellbook = wizard_spellbook

#creatures and spells for Warlock Mage spellbook
demon2 = Creature('Infernian Scourger', ['Demon'], 10, 9, 'claws', [6, 4], 2)
demon3 = Creature('Drokarr', ['Demon'], 13, 14, 'a tail spike', [8, 6], 4)
demon4 = Creature('Flaming Hellion', ['Fire', 'Demon'], 11, 13, 'a hell trident', [8, 4], 4, True)
demon5 = Creature('Blood Demon', ['Demon', 'Vampire'], 13, 12, 'gorging bites', [6, 6], 3, False, 9)
demon6 = Creature('Cerberus', ['Demon', 'Canine'], 15, 17, 'biting', [6, 6, 6], 6)
demon7 = Creature('Adramalech', ['Demon', 'Lord'], 16, 24, 'a Hellfire Scythe', [12, 8, 4], 6, False, 12)
curse2 = copy.deepcopy(curse1)
curse3 = Spell('Ghoul Rot', ['Necro', 'area', 'Curse'], ['take damage', 'be cursed'], [4, 4], 11, 11)
curse4 = Spell('Demonic Bloodlust', ['Necro', 'area', 'Enchantment'], ['be inspired', 'gain advantage', 'be weakened'], [0], 13, 13)
dispel7 = copy.deepcopy(dispel1)
fire3 = Spell('Ignite', ['Fire', 'area'], ['be burned'], [0], 2, 4)
fire4 = copy.deepcopy(fire1)
fire5 = copy.deepcopy(fire1)
fire6 = Spell("Devil's Trident", ['Necro', 'Fire', 'attack'], ['take damage', 'be cursed'], [8, 4], 7, 14)
fire7 = copy.deepcopy(fire6)
warlock_spellbook = [demon2, demon3, demon4, demon5, demon6, demon7, curse2, curse3, curse4, dispel7, fire3, fire4, fire5, fire6, fire7]
warlock = Mage('Warlock of the Arraxian Crown', 'Demon Fire', 48, 13, 11, 'a Lash of Hellfire', [8, 6, 4], 10)
warlock.spellbook = warlock_spellbook

#declaring a list of Mages to be selected by players
arena_mages = [priestess, warlock, beastmaster, wizard, druid, warlord, siren, necromancer]

########TEST AREA#########
