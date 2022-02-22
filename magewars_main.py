from magewars_game_functions import *

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

explain_rules()
list_keywords()

player1, player2 = choose_mages()
initiative = get_initiative(player1)
count = 0
while True:
    while len(initiative.get_active()) > 0 and len(initiative.enemy.get_active()) > 0:
        start_turn(initiative)
        take_turn(initiative)
        start_turn(initiative.enemy)
        take_turn(initiative.enemy)
    if initiative.health == 0 or initiative.enemy.health == 0:
        break
    initiative = end_of_round(initiative)
if initiative.enemy.health == 0:
    print(f"{initiative.name} EMERGES VICTORIOUS!!\n")
else:
    print(f"{initiative.enemy.name} EMERGES VICTORIOUS!!\n")
    
print("I'm thrilled that you actually played a full game.  It means something I've created was enjoyable enough to see through to the end, and is an encouraging promise of what lies ahead for me.\n")
print("Happy gaming, y'all.\n")
print('## ## ## ## ## ##\n')
print('FFFFF IIIII N   N')
print('F       I   NN  N')
print('FFF     I   N N N')
print('F       I   N  NN')
print('F     IIIII N   N\n')
print('## ## ## ## ## ##')