from wowapi.api import WoWApi
wowapi = WoWApi()



def getchar(name):
     try:
         charinfo = wowapi.get_character('eu','Ragnaros',name,['items'])
         char = charinfo['data']['class']
         achi = charinfo['data']['achievementPoints']
         level = charinfo['data']['level']
         race = charinfo['data']['race']
         gender = charinfo['data']['gender']
     
         classes = ['none', 'Warrior', 'Paladin', 'Hunter', 'Rouge', 'Priest', 'Deathknight', 'Shaman', 'Mage', 'Warlock', 'tio', 'druid']
         races = ['none', 'Human', 'Orc', 'Dwarf', 'Nightelf', 'Undead', 'Tauren', 'Gnome', 'Troll', 'Goblin', 'Bloodelf', 'Draenei', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', 'Worgen']
         genders = ['Male', 'Female']
         
         items = charinfo['data']['items']['averageItemLevelEquipped']
         
         return name+": A level", level, races[race], genders[gender], classes[char], "with", items, "avg. ilvl"
     except:
         print 'ERROR'