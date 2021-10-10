'''import json

with open("pokemon.json", 'r') as f:
    poke_info = json.load(f)

class Player:

    def __init__(self, username, level, xp, starter, pokemon):
        self.username = username
        self.level = level
        self.xp = xp
        self.starter = starter
        self.pokemon = pokemon
    
    def getXp(self, amount):

        xp_to_level = self.level*50
        self.xp += amount

        if self.xp >= xp_to_level:
            self.xp -= xp_to_level
            self.level += 1



file = open("testing.json", "w")



file.close()
'''
#player1 = Player("Corbin")

#This would not work as the whole code because nothing is stored and creating different players is not possible through code (as per my knowledge)

#This can be used to make some parts easier though such as level control, pokemon, and battle


import sys
import time
import os

def delay_print(string):
    for character in string:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.03125)
    sys.stdout.write("\n")


delay_print("Hellooooooo")
delay_print("Testing testing testing")

os.system('cls')