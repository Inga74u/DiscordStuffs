import json
import time

BotToken = None
DefaultPrefix = None
OsuKey = None
OwnerId = None

try:
    with open(".\\Bot\\Data.json", "r") as DataFile:
        Data = json.load(DataFile)

    a = ""
    while a != "y" and a != "n":
        print("\n"*150)
        a = input("Would you like to change the bot token (y/n)?\n")

    if a == "y":
        print("\n"*150)
        BotToken = input("What is the new bot token?\n")

    a = ""
    while a != "y" and a != "n":
        print("\n"*150)
        a = input("Would you like to change the bot default prefix (y/n)?\n")

    if a == "y":
        print("\n"*150)
        DefaultPrefix = input("What is the new bot default prefix?\n")

    a = ""
    while a != "y" and a != "n":
        print("\n"*150)
        a = input("Would you like to change the bot osu key (y/n)?\n")

    if a == "y":
        print("\n"*150)
        OsuKey = input("What is the new bot osu key?\n")
        if OsuKey.strip() == "":
            OsuKey = None

    a = ""
    while a != "y" and a != "n":
        print("\n"*150)
        a = input("Would you like to change the bot owner id (y/n)?\n")

    if a == "y":
        print("\n"*150)
        OwnerId = input("What is the new bot owner id?\n")

    
    if BotToken != None:
        Data['BotConfig']['Token'] = BotToken

    if DefaultPrefix != None:
        Data['BotConfig']['Prefix'] = DefaultPrefix

    if OsuKey != None:
        Data['BotConfig']['OsuKey'] = OsuKey
        Data['BotConfig']['OsuCmds'] = True

    if OwnerId != None:
        Data['BotConfig']['OwnerId'] = OwnerId

    with open(".\\Bot\\Data.json", "w") as DataFile:
        json.dump(Data, DataFile, indent = 4)

    print("\n"*150)
    print("Your settings have been saved.")
    time.sleep(5)
except:
    print("\n"*150)
    print("You need to let the bot run first!")
    time.sleep(5)
