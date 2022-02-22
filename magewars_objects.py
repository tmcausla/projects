from magewars_terminal_game import *
import copy

###DECLARING VARIABLES####
#creatures and spells for Priestess Mage spellbook
dragon1 = Creature("Alfiya", ['Holy', 'Dragon'], 21, 24, 'holy dragon breath', [10, 8, 4], 6)
cleric1 = Creature('Artemis', ['Holy', 'Cleric'], 14, 14, 'a spear', [8, 4], 2, True)
angel1 = Creature('Guardian Angel', ['Holy', 'Angel'], 14, 12, 'a shortsword', [6, 4], 2)
angel2 = Creature('Cassiel', ['Holy', 'Angel', 'Cleric'], 10, 9, 'divine magic', [4, 4], 1, False, 10)
angel3 = Creature('Valshalla', ['Holy', 'Angel'], 16, 21, 'a lightning sword', [8, 6, 4], 3, False, 4)
angel4 = Creature('Selesius', ['Holy', 'Angel'], 15, 21, 'a halberd', [8, 6, 4], 4, False, 4)
angel5 = Creature('Samandriel', ['Holy', 'Hero', 'Angel'], 17, 21, "the greatsword 'Starfire'", [10, 6, 4], 4, False, 4)
dispel1 = Spell('Dispel', ['Metamagic', 'Cure'], ['cure status'], [0], 4, friendly=True)
heal1 = Spell('Lay Hands', ['Holy', 'Healing'], ['heal', 'cure status'], [12, 6], 9, friendly=True)
heal2 = Spell('Minor Heal', ['Holy', 'Healing'], ['heal'], [6, 4], 5, friendly=True)
regen1 = Spell('Sacred Ground', ['Holy', 'area', 'Regeneration'], ['regenerate health'], [6, 4], 8, friendly=True)
divine_protect = Spell('Divine Protection', ['Holy', 'Protection'], ['gain armor', 'cure status'], [6, 6], 8, friendly=True)
holy1 = Spell('Pillar of Righteous Flame', ['Holy', 'Fire', 'attack'], ['take damage', 'be burned', 'be dazed', 'be weakened'], [10, 6, 4], 14, 15)
holy2 = Spell('Sunfire Burst', ['Holy', 'attack'], ['take damage', 'gain disadvantage'], [6, 4], 7)
holy3 = Spell('Luminous Blast', ['Holy', 'attack'], ['take damage', 'be dazed'], [10, 4], 5, 18)
priestess_spellbook = [cleric1, angel1, angel2, angel3, angel4, angel5, dragon1, heal1, heal2, dispel1, regen1, divine_protect, holy1, holy2, holy3]
priestess = Mage('Priestess of Asyra', 'Holy', 34, 15, 12, 'the Staff of Asyra', [8, 4], 4, True, 10)
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
war3 = Spell('Fortified Position', ['Soldier', 'area','Command'], ['gain armor', 'gain advantage'], [8, 8], 6, friendly=True)
earth1 = Spell('Hail of Stones', ['Earth', 'area', 'attack'], ['take damage', 'gain disadvantage'], [8, 4, 4], 8, 8)
earth2 = Spell('Hurl Boulder', ['Earth', 'attack'], ['take damage', 'be dazed'], [12, 8], 8, 15)
warlord_spellbook = [dwarf1, dwarf2, dwarf3, dwarf4, dwarf5, machine1, elephant1, golem1, heal4, dispel2, war1, war2, war3, earth1, earth2]
warlord = Mage('Anvil Throne Warlord', 'Soldier', 34, 12, 9, "Eisenach's Forge Hammer", [8, 8, 4], 14)
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
song2 = Spell('Song of Love', ['Psychic', 'area', 'Song'], ['cure status', 'regenerate health', 'gain armor'], [6, 4], 6, friendly=True)
song3 = Spell('Lullaby', ['Psychic', 'area', 'Song'], ['be dazed', 'be weakened', 'gain disadvantage'], [0], 8, 12)
song4 = Spell('Ballad of Courage', ['Soldier', 'area', 'Song'], ['be inspired', 'gain advantage'], [0], 7, friendly=True)
heal_rain1 = Spell('Renewing Rain', ['Aquatic', 'area', 'healing'], ['heal', 'cure status', 'regenerate health'], [6, 4], 9, friendly=True)
water1 = Spell('Hydrothermal Vent', ['Aquatic', 'trap'], ['spring a trap'], [10, 4], 8, 12)
water2 = Spell('Tsunami', ['Aquatic', 'area', 'attack'], ['take damage'], [6, 6, 6], 14)
water3 = Spell('Geyser', ['Aquatic', 'attack'], ['take damage', 'be burned'], [6, 4], 4, 10)
siren_spellbook = [shark1, shark2, shark3, pirate1, crocodile1, kraken1, kraken2, song1, song2, song3, song4, heal_rain1, water1, water2, water3]
siren = Mage('Siren of Shoalsdeep', 'Aquatic', 30, 13, 12, 'Shoalsdeep Trident', [8, 6, 4], 6, False, 16)
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
necro1 = Spell('Zombie Frenzy', ['Necro', 'area'], ['be inspired', 'gain advantage', 'lose range'], [0], 9, friendly=True)
necro2 = Spell('Drain Soul', ['Necro', 'Vampiric'], ['gain mana', 'lose mana'], [6, 4], 0)
necro3 = Spell('Animate Dead', ['Necro', 'Resurrection'], ['be resurrected'], [10, 6], 12)
necro4 = copy.deepcopy(necro3)
necromancer_spellbook = [skeleton1, skeleton2, skeleton3, zombie1, zombie2, zombie3, zombie4, demon1, dispel3, dispel4, curse1, necro1, necro2, necro3, necro4]
necromancer = Mage('Darkfenne Necromancer', 'Necro', 32, 13, 11, 'the Libro Mortuos tome', [8, 4], 8, True)
necromancer.spellbook = necromancer_spellbook

#creatures and spells for Druid Mage spellbook
plant1 = Creature('Togorah', ['Nature', 'Tree'], 20, 21, 'massive branches', [12, 6, 4], 4, health_regen=15)
plant2 = Creature('Vine Snapper', ['Nature', 'Vine'], 12, 7, 'biting thorns', [8, 4], health_regen=9)
plant3 = Creature('Thornlasher', ['Nature', 'Vine'], 13, 7, 'ensnaring vines', [6, 4], health_regen=10)
plant4 = Creature('Raptor Vine', ['Nature', 'Vine'], 12, 9, 'voracious bites', [10, 4], health_regen=9)
plant5 = Creature('Corrosive Orchid', ['Nature', 'Flower'], 9, 7, 'corrosive mist', [4, 4, 4], 0, True, health_regen=6)
plant6 = Creature('Kralathor', ['Nature', 'Vine', 'Monstrosity'], 15, 16, 'a great maw', [8, 8], 2, False, 10)
spider1 = Creature('Giant Wolf Spider', ['Nature', 'Spider'], 15, 15, 'poison fangs', [8, 8], 4)
plant7 = Spell('Barkskin', ['Nature', 'Healing', 'Protection'], ['gain armor', 'cure status', 'regenerate health'], [6, 6], 4, friendly=True)
heal_rain2 = copy.deepcopy(heal_rain1)
heal5 = copy.deepcopy(heal1)
acid1 = Spell('Acid Ball', ['Acid', 'attack'], ['take damage', 'melt armor'], [4, 4], 5, 4)
plant8 = Spell('Burst of Thorns', ['Nature', 'attack'], ['take damage'], [8, 4], 5)
plant9 = copy.deepcopy(plant8)
plant10 = Spell('Tanglevine', ['Nature', 'area', 'attack'], ['take damage', 'be dazed', 'be weakened'], [4, 4], 5, 13)
plant11 = Spell('Stranglevine', ['Nature', 'attack'], ['take damage', 'gain disadvantage', 'be poisoned'], [8, 4], 7, 10)
druid_spellbook = [plant1, plant2, plant3, plant4, plant5, plant6, spider1, plant7, heal_rain2, heal5, acid1, plant8, plant9, plant10, plant11]
druid = Mage('Wychwood Druid', 'Plant Nature', 35, 12, 13, 'a Vinewhip Staff', [8, 4, 4], 6, True, 14)
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
enchant2 = Spell('Rhino Hide', ['Nature', 'area', 'Enchantment'], ['gain armor', 'regenerate health'], [6, 4], 4, friendly=True)
enchant3 = Spell('Bear Strength', ['Nature', 'area', 'Enchantment'], ['melt armor'], [0], 5, 6)
enchant4 = Spell('Bull Endurance', ['Nature', 'area', 'Enchantment'], ['be inspired'], [0], 5, friendly=True)
enchant5 = Spell('Cheetah Speed', ['Nature', 'area', 'Enchantment'], ['become ranged'], [0], 5, friendly=True)
heal6 = Spell('Mending Wave', ['Holy', 'area', 'Healing'], ['heal', 'cure status'], [4, 4], 5, friendly=True)
dispel5 = copy.deepcopy(dispel1)
beastmaster_spellbook = [animal1, animal2, animal3, animal4, animal5, animal6, animal7, animal8, enchant1, enchant2, enchant3, enchant4, enchant5, heal6, dispel5]
beastmaster = Mage('Johktari Beastmaster', 'Animal Nature', 39, 14, 10, 'a Hunting Bow', [8, 4, 4], 8, True)
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
wizard = Mage('Wizard in Sortilege Manor', 'Metamagic and Elements', 32, 14, 14, 'a Staff of the Arcanum', [8, 6], 6, True)
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
warlock = Mage('Warlock of the Arraxian Crown', 'Demon Fire', 38, 13, 11, 'a Lash of Hellfire', [8, 6, 4], 10)
warlock.spellbook = warlock_spellbook

#declaring a list of Mages to be selected by players
arena_mages = [priestess, warlock, beastmaster, wizard, druid, warlord, siren, necromancer]