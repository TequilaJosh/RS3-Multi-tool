import requests
import json
from tkinter import *
from tkinter import ttk


SKILLS_LIST = ['Overall', 'Attack', 'Defence', 'Strength', 'Constitution', 'Ranged', 'Prayer', 'Magic', 'Cooking',
               'Woodcutting', 'Fletching', 'Fishing', 'Firemaking', 'Crafting', 'Smithing', 'Mining', 'Herblore', 'Agility',
               'Thieving', 'Slayer', 'Farming', 'Runecrafting', 'Hunter', 'Construction', 'Summoning', 'Dungeoneering',
               'Divination', 'Invention', 'Archaeology', 'Bounty Hunter', 'B.H. Rogues', 'Dominion Tower',
               'The Crucible', 'Castle Wars games', 'B.A. Attackers', 'B.A. Defenders', 'B.A. Collectors',
               'B.A. Healers', 'Duel Tournament', 'Mobilising Armies', 'Conquest', 'Fist of Guthix', 'GG: Athletics',
               'GG: Resource Race', 'WE2: Armadyl Lifetime Contribution', 'WE2: Bandos Lifetime Contribution',
               'WE2: Armadyl PvP kills', 'WE2: Bandos PvP kills', 'Heist Guard Level', 'Heist Robber Level',
               'CFP: 5 game average', 'AF15: Cow Tipping', 'AF15: Rats killed after the miniquest',
               'RuneScore', 'Clue Scrolls Easy', 'Clue Scrolls Medium', 'Clue Scrolls Hard', 'Clue Scrolls Elite',
               'Clue Scrolls Master']


def lower_dict(d):
    new_dict = dict((k.lower(), v.lower()) for k, v in d.items())
    return new_dict


# load all ge items
file = open('itemIDs.json')
id_dict = json.load(file)
item_id_dict = lower_dict(id_dict)

root = Tk()
root.title('RS3 Multi')
tabControl = ttk.Notebook(root)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Tab 1')
tabControl.add(tab2, text='Tab 2')
tabControl.pack(expand=1, fill="both")

ttk.Label(tab1, text="Enter any item").grid(column=0, row=0, padx=(30, 0), pady=30)

lookup_entry_t1 = ttk.Entry(tab1)
lookup_entry_t1.grid(column=1, row=0, padx=10)
lookup_label_t1 = ttk.Label(tab1, text="")
lookup_label_t1.grid(column=1, row=1, padx=10, pady=30)


def lookup():
    try:
        item_id = list(item_id_dict.keys())[list(item_id_dict.values()).index(lookup_entry_t1.get())]  # locate needed item id
        response = requests.get(f"https://secure.runescape.com/m=itemdb_rs/api/catalogue/detail.json?item={item_id}").json()
    except ValueError:
        lookup_label_t1.config(text='please try again')
    else:
        dict1 = response['item']
        current_dict = dict1['current']
        lookup_label_t1.config(text=f'{current_dict["price"]} GP')


ttk.Button(tab1, text='lookup item', command=lookup).grid(column=2, row=0, padx=(0, 30))

# tab 2 setup
ttk.Label(tab2, text="Enter a player name: ").grid(column=0, row=0, padx=(30, 0), pady=30)
hs_entry = Entry(tab2, )
hs_entry.grid(column=1, row=0, padx=10)


def highscore():
    # find requested players stats and xp
    high_score = requests.get(f'https://secure.runescape.com/m=hiscore/index_lite.ws?player={hs_entry.get()}').text
    high_score_list = high_score.split('\n')
    high_score_list.pop(-1)
    hs_split = []
    for skill in high_score_list:
        hs_split.append(skill.rsplit(',', maxsplit=2))
    lvl_list = [lvl[1] for lvl in hs_split]
    xp_list = [int(xp[2]) for xp in hs_split if len(xp) > 2]

    # create labels that contain the stats of the player
    label_index = 0
    for col_num in range(0, 3):
        col_index = col_num
        for row_num in range(1, 10):
            ttk.Label(tab2, text=f'{SKILLS_LIST[label_index]}: {lvl_list[label_index]}-{xp_list[label_index]:,} ',
                      justify=LEFT).grid(column=col_index, row=row_num, padx=(20, 10))
            label_index += 1


ttk.Button(tab2, text="Find player", command=highscore).grid(column=2, row=0)

root.mainloop()
