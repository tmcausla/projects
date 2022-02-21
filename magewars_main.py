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

#prints a list of mages in arena_mages
def list_mages():
    for i in range(len(arena_mages)):
        print(f"{i+1} - {arena_mages[i]}\n")
    print('---------------')

#takes names of players and assigns mage to player based on input, changes mage name to player name, assigns enemy property for self and spells to the opposing mage
def choose_mages(p1_name, p2_name):
#takes input and assigns mage variable to player 1, pops chosen mage out of arena_mages
    list_mages()
    valid_range = [str(i+1) for i in range(len(arena_mages))]
    player1_choice = input(f"{p1_name}, which Mage would you like to take control of? Please choose from the list above and press Enter.\n")
    while player1_choice not in valid_range:
        player1_choice = input(f"That is not a valid choice, {p1_name}. Please choose a Mage from the list above, type the corresponding number and press Enter.\n")
    print(f'\n{p1_name} is the {arena_mages[int(player1_choice) - 1].name}!\n')
    player1 = arena_mages[int(player1_choice) - 1]
    arena_mages.pop(int(player1_choice) - 1)
    player1.name = p1_name
#takes input and assigns mage variable to player 2
    list_mages()
    valid_range = [str(i+1) for i in range(len(arena_mages))]
    player2_choice = input(f"{p2_name}, which Mage would you like to take control of? Please choose from the list above and press Enter.\n")
    while player2_choice not in valid_range:
        player2_choice = input(f"That is not a valid choice, {p2_name}. Please choose a Mage from the list above, type the corresponding number and press Enter.\n")
    print(f'\n{p2_name} is the {arena_mages[int(player2_choice) - 1].name}!\n')
    player2 = arena_mages[int(player2_choice) - 1]
    arena_mages.pop(int(player2_choice) - 1)
    player2.name = p2_name
#assigns the opposing mage as the enemy property
    player1.enemy, player2.enemy = player2, player1
    for i in range(len(player1.spellbook)):
        player1.spellbook[i].enemy, player2.spellbook[i].enemy = player2, player1
    return player1, player2


def explain_rules():
    pass

def list_keywords():
    pass

def take_turn(player):
    pass





print('\n\n')
print('-------------------------------------------------')
print('M   M  AAA   GGGG EEEEE   W   W  AAA  RRRR   SSSS')
print('MM MM A   A G     E       W   W A   A R   R S   ')
print('M M M AAAAA G  GG EEE     W W W AAAAA RRRR   SSS')
print('M   M A   A G   G E       WW WW A   A R  R      S')
print('M   M A   A  GGGG EEEEE   W   W A   A R   R SSSS')
print('-------------------------------------------------\n')

print("Welcome to my very first program: Mage Wars!  This is a two player game about different types of magic users dueling in an arena.  You'll get to summon mighty creatures to fight by your side and cast powerful spells to defeat your opponent.\n")

print("DISCLAIMER: This work is heavily inspired by Mage Wars, a board game designed by Bryan Pope and Arcane Wonders.  Some names and rules have been used straight from the physical game materials which I legally own copies of. I do not have a license nor do I have affiliation with Bryan Pope or Arcane Wonders.\n")

player1_name = input("First, let's get your names.  What is the name of the first player?\n")
player2_name = input(f'\nThank you, {player1_name}.  Next, what is the name of the second player?\n')
print(f'\nHello {player2_name}!\n')
print(f'{player1_name} and {player2_name}...Welcome to the Arena!\n')

player1, player2 = choose_mages(player1_name, player2_name)
initiative = get_initiative(player1)
initiative.cast_spell()
initiative.enemy.cast_spell()
end_of_round(initiative)