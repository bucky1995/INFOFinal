import json
import codecs
import requests
import csv
API_key = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

GameList = ["359550",#Tom Clancy's Rainbow Six Siege
            "814380",#Sekiro™: Shadows Die Twice
            "730",#Counter-Strike: Global Offensive
            "578080",#PLAYERUNKNOWN'S BATTLEGROUNDS
            "292030",#The Witcher 3: Wild Hunt
            "72850",#The Elder Scrolls V: Skyrim
            "365590",#Tom Clancy's The Division
            "582010",#MONSTER HUNTER: WORLD
            "374320",#DARK SOULS™ III
            "812140",#Assassin's Creed Odyssey
            "570",#Dota 2
            "841370",#NBA 2K19
            "582160",#Assassin's Creed Origins
            "883710",#RESIDENT EVIL 2 / BIOHAZARD RE:2
            "530620",#Resident Evil 7 / Biohazard 7 Teaser: Beginning Hour
            "218620",#PAYDAY 2
            "271590",#Grand Theft Auto V
            "377160",#Fallout 4
            "863550",#HITMAN™ 2
            "209160"#Call of Duty: Ghosts
            ]

GameList_Name=["Tom Clancy's Rainbow Six Siege",
               "Sekiro™: Shadows Die Twice",
               "Counter-Strike: Global Offensive",
               "PLAYERUNKNOWN'S BATTLEGROUNDS",
               "The Witcher 3: Wild Hunt",
               "The Elder Scrolls V: Skyrim",
               "Tom Clancy's The Division",
               "MONSTER HUNTER: WORLD",
               "DARK SOULS™ III",
               "Assassin's Creed Odyssey",
               "Dota 2",
               "NBA 2K19",
               "Assassin's Creed Origins",
               "RESIDENT EVIL 2 / BIOHAZARD RE:2",
               "Resident Evil 7 / Biohazard 7 Teaser: Beginning Hour",
               "PAYDAY 2",
               "Grand Theft Auto V",
               "Fallout 4",
               "HITMAN™ 2",
               "Call of Duty: Ghosts"
               ]
for gameid in GameList:
    with open(gameid + '_playtime_forever.csv', 'w') as PF,open(gameid + '_playtime_last_two_weeks.csv', 'w')as PT:
        fieldnames = ['userid', 'playtime_forever', 'playtime_last_two_weeks']
        fieldnamesPF = ['userid', 'playtime_forever']
        fieldnamesPT = ['userid','playtime_last_two_weeks']
        PFwriter = csv.DictWriter(PF, fieldnames=fieldnamesPF)
        PTwriter = csv.DictWriter(PT, fieldnames=fieldnamesPT)
        for i in range(0, 1):
            offset = i * 20
            print(offset)
            url = 'https://store.steampowered.com/appreviews/' + gameid + '?json=1&start_offset=' \
                  + str(offset) + '&day_range=9223372036854775807&filter=updated&review_type=al&purchase_type = all'
            r = requests.get(url)
            content = codecs.decode(r.content, 'utf-8')
            jcontent = json.loads(content)
            PFwriter.writeheader()
            PTwriter.writeheader()
            for user in jcontent["reviews"]:
                print(str(user["author"]['steamid']) + " " + str(user["author"]['playtime_last_two_weeks']) + " " + str(
                    user["author"]['playtime_forever']))
                PFwriter.writerow(
                    {'userid': user["author"]['steamid'],
                     'playtime_forever':user["author"]['playtime_forever']
                     }
                )
                PTwriter.writerow(
                    {'userid': user["author"]['steamid'],
                     'playtime_last_two_weeks': user["author"]['playtime_last_two_weeks']
                     }
                )
        PF.close()
        PT.close()
