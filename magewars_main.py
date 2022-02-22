from magewars_terminal_game import *

#allows player1 to make a 50/50 call to be the first with initiative
def get_initiative(player):
    print(f'{player.name}, you get to call for initiative.  The Mage with initiative is the first to act in a round.  You will roll a d20 and call odd or even.  If you are correct, you get initiative!')
    player_call = input("Please type 'odd' or 'even' and hit Enter.\n")
    count = 1
    while player_call.lower() not in ['odd', 'even']:
        if count > 2:
            player_call = input("I find it 'odd' that you just can't 'even' right now...\n")
        else:
            player_call = input("That is not a valid choice. Please type 'odd' or 'even' and press Enter.\n")
            count += 1
    print('Now rolling...')
    num = random.randint(1, 20)
    print(f'You rolled a {num}.\n')
    if num % 2 == 0:
        if player_call == 'even':
            print(f'Even! {player.name} will have first initiative.\n')
            return player
        else:
            print(f'Even! {player.enemy.name} will have first initiative.\n')
            return player.enemy
    else:
        if player_call == 'odd':
            print(f'Odd! {player.name} will have first initiative.\n')
            return player
        else:
            print(f'Odd! {player.enemy.name} will have first initiative.\n')
            return player

#activates end of round upkeep for each mage and changes initiative
def end_of_round(player):
    player.end_round_upkeep()
    player.enemy.end_round_upkeep()
    initiative = player.enemy
    print(f'{initiative.name} will have initiative for this round.')
    print('---------------')

#prints a list of mages from arena_mages
def list_mages():
    for i in range(len(arena_mages)):
        print(f"{i+1} - {arena_mages[i]}\n")
    print('---------------')

#returns mage variables based on input from players, changes mage names to player names, assigns enemy property for self and spells to the opposing mage
def choose_mages():
    p1_name = input("First, let's get your names.  What is the name of the first player?\n")
    p2_name = input(f'\nThank you, {p1_name}.  Next, what is the name of the second player?\n')
    print(f'\nHello {p2_name}!\n')
    print(f'{p1_name} and {p2_name}... Welcome to the Arena!\n')
#takes input and assigns mage variable to player 1, pops chosen mage out of arena_mages
    list_mages()
    valid_range = [str(i+1) for i in range(len(arena_mages))]
    player1_choice = input(f"{p1_name}, which Mage would you like to take control of? Please choose from the list above and press Enter.\n")
    while player1_choice not in valid_range:
        player1_choice = input(f"That is not a valid choice, {p1_name}. Please choose a Mage from the list above, type the corresponding number and press Enter.\n")
    print(f'\n{p1_name} is the {arena_mages[int(player1_choice) - 1].name}!\n')
    player1 = arena_mages[int(player1_choice) - 1]
    arena_mages.pop(int(player1_choice) - 1)
#takes input and assigns mage variable to player 2
    list_mages()
    valid_range = [str(i+1) for i in range(len(arena_mages))]
    player2_choice = input(f"{p2_name}, which Mage would you like to take control of? Please choose from the list above and press Enter.\n")
    while player2_choice not in valid_range:
        player2_choice = input(f"That is not a valid choice, {p2_name}. Please choose a Mage from the list above, type the corresponding number and press Enter.\n")
    print(f'\n{p2_name} is the {arena_mages[int(player2_choice) - 1].name}!\n')
    player2 = arena_mages[int(player2_choice) - 1]
#changes mage names to player names
    print(f"\nToday's match is going to be the {player1.name} facing off against the {player2.name}!")
    player1.name, player2.name = p1_name, p2_name
#assigns the opposing mage as the enemy property
    player1.enemy, player2.enemy = player2, player1
    for i in range(len(player1.spellbook)):
        player1.spellbook[i].enemy, player2.spellbook[i].enemy = player2, player1
    print('---------------')
    return player1, player2

#prints out general rules of the game
def explain_rules():
    print('The goal of this game is to use your Mage to attack the other Mage until the health of you or your opponent reaches zero.  Your Mage is allowed to make one attack on your turn.\n')
    print("But! A Mage wouldn't be much if all it did was attack.  Each Mage has a spellbook at their disposal from which they can cast spells.  Casting a spell takes up your Mage's action.\n")
    blank = input('(press Enter)\n')
    print("These spells can attack or curse your foes, and provide healing benefits for your allies.\nImportantly you'll also find Creatures in these spellbooks.  These are powerful allies you can summon that will have opportunities to attack your opponents on top of what your Mage can do!")
    print("You will not always have enough mana to cast the most powerful spells, but each Mage will regain a certain amount of mana each round.\n")
    blank = input('(press Enter)\n')
    print("Beware!  Each spell can only be cast once.  Once a creature dies or a heal/attack spell is used they are sent to your graveyard.  Think of it as your discard pile like in some card games.")
    print("Of course, some Mages might have abilities that can break even this simple rule... Have fun exploring your Mage's abilities!\n")
    blank = input('(press Enter)\n')
    print("You will play over the course of several rounds.  During a round, you will take actions with every allied Mage and Creature until they have all been used.  At this point Mages regain mana, dead units are cleared from the arena and every other unit is refreshed for a new round to begin.\n")
    print("You will keep going through rounds until one player is crowned the victor!")
    print('---------------')

#prints out keywords used in spells and describes their function
def list_keywords():
    print("There are lots of words used by the spell cards that won't be immediately intuitive, especially if you're unfamiliar with dueling card games.  Let's go over what you'll see as you go through your spellbooks!\n")
    print("HEALTH AND ARMOR - Health is the value that represents the life of the unit.  If your Mage's Health reaches zero, you lose!\nArmor must be depleted before applying damage to a unit's Health, and it is replenished back to the full armor value between rounds.\n")
    print("REGENERATE HEALTH - The unit will regain health between rounds, then the health regen value will be decreased by one.\n")
    print("MELT ARMOR - This permanently removes a unit's armor.\n")
    print("MANA - this is the currency your Mage uses to cast spells.  They replenish mana between rounds.\n")
    print("AREA - This kind of spell targets more than one friendly/enemy unit, depending on the effect.\n")
    print("POISONED - The unit will take a small amount of damage between rounds, with a small chance of going away on its own.\n")
    print("BURNED - The unit takes damage between rounds, with a high chance of going away on its own.\n")
    print("WEAK - When attacked, the attacking unit will roll its smallest attack die and add it to the damage result, with a chance of going away on its own between rounds.\n")
    print("(DIS)ADVANTAGE - When attacking, a unit with advantage rolls their attack dice twice and takes the higher result.  A disadvantaged unit rolls twice but takes the lower result.  Units lose this status after they make an attack action.\n")
    print("CURE STATUS - The unit will be removed of negative conditions affecting it.  This means poison, burns, weak, and disadvantage.\n")
    print("CURSE - The target is burdened with all of the negative status conditions.  This means the unit is poisoned, burned, weakened, and it gains disadvantage.\n")
    print("GUARD - If your Mage is targeted by an attack, you may choose an active creature to take the hit for you.  This is considered that unit's action for the round.\nThis does not activate if your Mage is attacked from range or by a spell.\n")
    print("RANGE - Range refers to a unit attacking from afar or it moves too quickly for opponents to react.  Units with range cannot be guarded when they target the enemy Mage.\n")
    print("INSPIRED - This allows a unit that has already acted to take another action this round.\n")
    print("DAZED - This will prevent a unit from taking an action this round.\n")
    print("RESURRECTED - The Mage chooses a previously defeated unit to summon back to the arena.  The unit can be chosen from either player's graveyard.  The resurrected unit is cursed and loses its smallest attack die.")
    print('---------------')

#allows a player to choose an active unit and take an action.  This constitutes their turn during a round.
def take_turn(player):
    print(f'{player.name}!  It is your turn.\n')
    blank = input('(press Enter)\n')
    if len(player.get_active()) < 1:
        print(f'{player.name}, you have no active units.  You will have to wait until next round.\n')
    else:
        active_unit = None
        confirm = 'n'
        while confirm != 'y':
            active_unit = player.choose_active_unit()
            confirm = input(f"You have chosen {active_unit.name} to take an action, would you like to proceed? y/n\n").lower()
        if isinstance(active_unit, Creature):
            active_unit.attack()
        else:
            player_choice = input("Would you like to attack an enemy or cast a spell from your spellbook? Type 'attack' or 'spell' and press Enter.\n").lower()
            while player_choice not in ['attack', 'spell']:
                player_choice = input("That is not an option for your Mage.  Please choose to 'attack' or cast a 'spell' and press Enter.\n").lower()
            if player_choice == 'attack':
                active_unit.attack()
            elif player_choice == 'spell':
                active_unit.cast_spell()
    print('---------------')

#allows a player to look at relevant lists around the arena before taking their turn
def start_turn(player):
    player_choice = '0'
    while player_choice != '2':
        print(f'{player.name}!  It is your turn.  Would you like to look at the state of the arena or proceed to take your action?\n')
        print("1 - Look around the arena.\n2 - Take my turn.\n")
        player_choice = input('Please select a number and press Enter.\n')
        while player_choice not in ['1', '2']:
            player_choice = input("That is not an option right now.  Please type 1 to look around, or type 2 to take an action and then press Enter.\n")
        if player_choice == '1':
            list_choice = '0'
            while list_choice != '7':
                print(f"{player.name}, what would you like to see?\n")
                print("1 - I would like to see the spells in my spellbook.")
                print("2 - I would like to see my allies in the arena.")
                print("3 - I would like to see my active units that can still take actions.")
                print("4 - I would like to look in the graveyard piles.")
                print("5 - I would like to see my enemies in the arena.")
                print("6 - I would like to see my opponent's active units that can still take an action.")
                print("7 - Proceed and take my turn.")
                print('---------------')
                list_choice = input("What do you want to look at? Choose an option from the list above and press Enter.\n")
                while list_choice not in ['1', '2', '3', '4', '5', '6', '7']:
                    list_choice = input('That is not a valid option. Select a number from 1-6 to look at various lists of the arena, or select 7 to proceed with your action.\n')
                if list_choice == '1':
                    player.list_spellbook()
                elif list_choice == '2':
                    player.list_front_line()
                elif list_choice == '3':
                    player.list_active()
                elif list_choice == '4':
                    player.list_graveyard()
                    player.enemy.list_graveyard()
                elif list_choice == '5':
                    player.list_targets()
                elif list_choice == '6':
                    player.enemy.list_active()
                elif list_choice == '7':
                    player_choice = '2'
                    break
    

 # # ### ### ### ### ## ### # #
# # ### GAME STARTS HERE ### # #
 # # ### ## ### ### ### ### # #

print('\n\n')
print('-------------------------------------------------')
print('M   M  AAA   GGGG EEEEE   W   W  AAA  RRRR   SSSS')
print('MM MM A   A G     E       W   W A   A R   R S   ')
print('M M M AAAAA G  GG EEE     W W W AAAAA RRRR   SSS')
print('M   M A   A G   G E       WW WW A   A R  R      S')
print('M   M A   A  GGGG EEEEE   W   W A   A R   R SSSS')
print('-------------------------------------------------\n')

print("Welcome to my very first independent project: Mage Wars!  This is a two player game about different types of magic users dueling in an arena.  You'll get to summon mighty creatures to fight by your side and cast powerful spells to defeat your opponent.\n")

print("DISCLAIMER: This work is heavily inspired by Mage Wars, a board game designed by Bryan Pope and Arcane Wonders.  Some names and rules have been used straight from the physical game materials which I legally own copies of. I do not have a license nor do I have affiliation with Bryan Pope or Arcane Wonders.\n")




#player1, player2 = choose_mages(player1_name, player2_name)
#initiative = get_initiative(player1)

#end_of_round(initiative)
