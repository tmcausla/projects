from magewars_terminal_game import *

print('\n\n')
print('M   M  AAA   GGGG EEEEE   W   W  AAA  RRRR   SSSS')
print('MM MM A   A G     E       W   W A   A R   R S   ')
print('M M M AAAAA G  GG EEE     W W W AAAAA RRRR   SSS')
print('M   M A   A G   G E       WW WW A   A R  R      S')
print('M   M A   A  GGGG EEEEE   W   W A   A R   R SSSS\n')

print("Welcome to my very first program: Mage Wars!  This is a two player game about different types of magic users dueling in an arena.  You'll get to summon mighty creatures to fight by your side and cast powerful spells to defeat your opponent.\n")

print("DISCLAIMER: This work is heavily inspired by Mage Wars, a board game designed by Bryan Pope and Arcane Wonders.  Some names and rules have been used straight from the physical game materials which I legally own copies of. I do not have a license nor do I have affiliation with Bryan Pope or Arcane Wonders.\n")


for i in range(len(arena_mages)):
    print(f'{i+1} - The {arena_mages[i]}\n')

    