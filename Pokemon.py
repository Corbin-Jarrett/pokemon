import json
import random
import time
import os


def getXp(pokemon, amount):
    #Getting data from json
    level = pokemon["Level"]
    xp = pokemon["Xp"]
    nickname = pokemon["Nickname"]

    #adding amount of xp to pokemon's xp
    xp_to_level = level*50
    xp += amount

    #if xp is enough to level up
    if xp >= xp_to_level:
        #lower xp and increase level by 1
        xp -= xp_to_level
        level += 1
        print("Congratulations! Your {} grew to level {}.".format(nickname, level))
        
        #increase stats for 4/6 stats
        list_of_traits = ["Hp","Attack","Defence", "Spa", "Spd", "Speed"]
        
        random.shuffle(list_of_traits)
        for i in range(2):
            list_of_traits.pop()

        for i in list_of_traits:
            pokemon[i] += 1

        #resetting pokemon levels
        pokemon["Xp"] = xp
        pokemon["Level"] = level

        #if pokemon is level to evolve, change name to evolution name
        if level == pokemon["Evolution_Level2"]:
            print("What?! Your {} is evolving!".format(pokemon["Nickname"]))
            time.sleep(3)
            print("Congratulations! Your {} evolved into {}!".format(pokemon["Name"], pokemon["Evolution2"]))
            pokemon["Name"] = pokemon["Evolution2"] 

        elif level == pokemon["Evolution_Level"]:
            print("What?! Your {} is evolving!".format(pokemon["Nickname"]))
            time.sleep(3)
            print("Congratulations! Your {} evolved into {}!".format(pokemon["Nickname"], pokemon["Evolution"]))
            pokemon["Name"] = pokemon["Evolution"]  

        #call getXp with 0 amount added in case there is enough xp to level up again
        getXp(pokemon, 0)

    #return updated json infomation
    return pokemon

#opening pokemon info, this does not change
with open("pokemon.json", 'r') as f:
    poke_info = json.load(f)

def createUser(Username1):
    #Removing any whitespace before or after and if the length is more than 15 characters it is rejected
    Username = Username1.strip()
    if len(Username) > 15:
        print("Name cannot be longer than 15 characters, please try again")
        return

    #opening usernames as a list of usernames
    with open("usernames.txt") as f:
        usernames = f.readlines()
    
    #Removing newline after each username
    for i in usernames:
        usernames[usernames.index(i)] = i.strip("\n")
        
    #if the desired username is already there, it is rejected
    if Username in usernames:
        print("Username already exists, try again")
        return

    #opening usernames and adding new username
    with open("usernames.txt", "a") as f:
        f.write(Username + "\n")

    #adding new user template to users pokemon data
    userTemplate = {"Username": Username,"Level": 1,"Xp": 0,"Starter": False, "Pokemon": []}
    
    with open(f"{Username}.json", 'w') as f:
        json.dump(userTemplate, f, indent=4)

    print("User {} added, welcome {}".format(Username, Username))

        
def removeUser(Username):
    #Getting all usernames
    with open("usernames.txt") as f:
        usernames = f.readlines()

    #Getting rid of the newline after the username
    for i in usernames:
        usernames[usernames.index(i)] = i.strip("\n")

    #if the username is in this list, remove it
    if Username in usernames:
        usernames.pop(usernames.index(Username))

        #Rewrite all usernames without the one removed
        with open("usernames.txt", "w") as f:
            for element in usernames:
                f.write(element + "\n")

        try:
            os.remove(f"{Username}.json")

        except:
            print("No such user exists")

        print("Sucessfully Removed User")

def getAStarter(Username):
    #opening usernames as a list of usernames
    with open("usernames.txt") as f:
        usernames = f.readlines()
    
    #Removing newline after each username
    for i in usernames:
        usernames[usernames.index(i)] = i.strip("\n")
        
    #if the desired username is not there, it is rejected
    if Username not in usernames:
        print("Username does not exist, try again")
        return

    #opening updated users pokemon data
    with open(f"{Username}.json", 'r') as f:
        player_info = json.load(f)

    #checking if they already have a starter
    if player_info["Starter"] == True:
        print("You already have a starter!")
        return
        

    #Getting all the starters and letting them choose
    starters = poke_info["starters"]
    starter_num = input("What starter do you want? 1:{}, 2:{}, or 3:{}? ".format(starters[0]["Name"], starters[1]["Name"], starters[2]["Name"]))
    
    #depending on option chosen, adding this pokemon to their pokemon
    if starter_num == "1":
        nickname = input("What do you want to call your {}? ".format(starters[0]["Name"]))
        poke_info_changed = poke_info
        poke_info_changed["starters"][0]["Nickname"] = nickname
        player_info["Pokemon"].append(poke_info_changed["starters"][0])

    elif starter_num == "2":
        nickname = input("What do you want to call your {}? ".format(starters[1]["Name"]))
        poke_info_changed = poke_info
        poke_info_changed["starters"][1]["Nickname"] = nickname
        player_info["Pokemon"].append(poke_info_changed["starters"][1])

    elif starter_num == "3":
        nickname = input("What do you want to call your {}? ".format(starters[2]["Name"]))
        poke_info_changed = poke_info
        poke_info_changed["starters"][2]["Nickname"] = nickname
        player_info["Pokemon"].append(poke_info_changed["starters"][2])

    else:
        print("Invalid Starter number, try again")
        return

    #making it so they cannot get another starter
    player_info["Starter"] = True
    
    with open(f"{Username}.json", 'w') as f:
        json.dump(player_info, f, indent=4)

    print("Congratulations! You and {} are going to have amazing adventures together!".format(nickname))
    

def encounterPokemon(Username):
    #opening updated users pokemon data
    with open(f"{Username}.json", 'r') as f:
        player_info = json.load(f)
    
    #getting player level and having different pokemon to choose from depending on level

    if 1<= player_info["Level"] <= 5:
        wild_encounter = random.choice(poke_info["wild_set_1"])
    
    elif 6<= player_info["Level"] <= 10:
        wild_encounter = random.choice(poke_info["wild_set_2"])

    elif 11<= player_info["Level"] <= 20:
        wild_encounter = random.choice(poke_info["wild_set_3"])

    elif 21<= player_info["Level"] <= 40:
        wild_encounter = random.choice(poke_info["wild_set_4"])

    else:
        wild_encounter = random.choice(poke_info["wild_set_5"])
    
    
    #Asking if wanting to catch
    answer = input("You have encountered a {}! Do you want to throw a pokeball? y/n ".format(wild_encounter["Name"]))
    if answer.strip() == "y":
        time.sleep(3)

        #getting nickname for pokemon
        nickname = input("You have caught the {}. What would you like to call it? ".format(wild_encounter["Name"]))
        wild_encounter["Nickname"] = nickname

        #adding pokemon to player's pokemon
        player_info["Pokemon"].append(wild_encounter)

        print("I'm sure you and {} are going to be great friends!".format(nickname))

        with open(f"{Username}.json", 'w') as f:
            json.dump(player_info, f, indent=4)
    
    else:
        print("No pokemon for you!")

removeUser("Corbin")

createUser("Corbin")
getAStarter("Corbin")

encounterPokemon("Corbin")


#get xp testing
'''
with open("users.json", 'r') as f:
    info = json.load(f)
pokemon = info[0]["Pokemon"][0]
pokemon = getXp(pokemon, 50000)


info[0]["Pokemon"][0] = pokemon

with open("users.json", 'w') as f:
    json.dump(info, f, indent=4)
'''