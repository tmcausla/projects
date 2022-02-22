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
            print('Target is weak! Roll your smallest attack die and add the result.')
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
            print(f'{self.name} has no allies in the arena!')
        else:
            print(f"{self.name}'s allies in the arena are:")
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
            print('The graveyard pile is empty.')
        else:
            print(f"These are {self.name}'s used spells and defeated creatures:")
            for i in range(len(self.graveyard)):
                print(f'{i + 1} - {self.graveyard[i]}')
        print('---------------')

#returns input for choosing a guard when Mage is target of an attack
    def choose_guard(self):
        active = self.get_active()
        if self in active:
            active.remove(self)
        if len(active) < 1:
            return self
        valid_range = [str(i + 1) for i in range(len(active))]
        print(f'Your mage {self.name} is being targeted, you may choose a creature to block the attack. Select a number and press Enter.\n')
        print(f'0 - No guard, allow {self.name} to take damage. They currently have {self.health} health + {self.armor} armor.')
        for i in range(len(active)):
            print(f"{i+1} - {active[i].name}, they currently have {active[i].health} health + {active[i].armor} armor.")
        guard_input = input()
        while guard_input not in valid_range:
            guard_input = input('That is not a valid choice.  Please select a number from the list above and press Enter.\n')
        if guard_input == '0':
            print(f'{self.name} has chosen not to use a guard.')
            return self
        guard = int(guard_input) - 1
        active[guard].is_active = False
        print(f'{self.name} is blocking the attack with {active[guard].name}.')
        return active[guard]

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

#returns a friendly target when casting beneficial spell effects
    def choose_friendly(self):
        self.list_front_line()
        valid_targets = self.get_front_line()
        if len(valid_targets) < 1:
            return None
        valid_range = [str(i + 1) for i in range(len(valid_targets))]
        target = input('Pick your target from the list above and press Enter.\n')
        while target not in valid_range:
            target = input('That is not a valid target. Please choose a number from the list above and press Enter.\n')
        return valid_targets[int(target) - 1]


#handles effects of spells based on keywords found in school and action properties of spell
    def cast_spell(self):
        spell = self.choose_spell()
        self.lose_mana(spell.mana_cost)
        if isinstance(spell, Creature):
            self.front_line.append(spell)
            print(f'{self.name} has summoned {spell.name} to the arena.\n')
        else:
            if 'area' in spell.school or 'be resurrected' in spell.action:
                print(f'{self.name} is casting {spell.name}.')
            elif spell.friendly:
                target = self.choose_friendly()
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
    def __init__(self, name, school, action, attack_dice, mana_cost, status_roll=None, friendly=False):
        self.name = name
        self.school = school
        self.action = action
        self.attack_dice = attack_dice
        self.mana_cost = mana_cost
        self.status_roll = status_roll
        self.friendly = friendly

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