import csv
from buffs import Buff
from buffs import Debuff

CHARACTER_FILENAME = 'data/Characters.csv'
WEAPON_FILENAME = 'data/Weapons.csv'
ENEMY_FILENAME = 'data/Enemies.csv'
ARTIFACT_FILENAME = 'data/ArtifactSets.csv'
ELERATIO_FILENAME = 'data/ElementalRatio.csv'
PHYSRATIO_FILENAME = 'data/PhysicalRatio.csv'
RAZORAUTO_FILENAME = 'data/RazorAutoRatio.csv'
RAZORQAS_FILENAME = 'data/RazorQASRatio.csv'
ZHONGLIQ_FILENAME = 'data/ZhongliQRatio.csv'
BUFF_FILENAME = 'data/Buffs.csv'
DEBUFF_FILENAME = 'data/Debuffs.csv'
TIME_FILENAME = 'data/times.csv'

# Converts percentage strings to decimals [0, 1]
def pctstr_to_float(pctstr):
    if pctstr == '':
        return 0

    pctstr = pctstr[:-1] # Remove % symbol
    f = float(pctstr)
    return f / 100

def str_to_int(s):
    if s == '':
        return 0
    return int(s)

def str_to_float(s):
    if s == '':
        return 0
    return float(s)

# Reads character data

class Character():
    def __init__(self,character):
        pass

def read_character_data():
    with open(CHARACTER_FILENAME) as charfile:
        character_dict = {}
        reader = csv.DictReader(charfile, delimiter=',')

        for row in reader:
            name = row["name"]
            newname = Character(name) 
            character_dict[name] = newname

            name = row['name']
            newname = Character(name) 
            character_dict[name] = newname

            newname.name = row['name']
            newname.element = row['element']
            newname.weapon_type = row['weapon_type']

            newname.base_atk = str_to_int(row['base_atk'])
            newname.pct_atk_ = pctstr_to_float(row['pct_atk'])
            newname.flat_atk = str_to_int(row['flat_atk'])

            newname.base_hp = str_to_int(row['base_hp'])
            newname.pct_hp =  pctstr_to_float(row['pct_hp'])
            newname.flat_hp = str_to_int(row['flat_hp'])

            newname.base_def = str_to_int(row['base_def'])
            newname.pct_def =  pctstr_to_float(row['pct_def'])
            newname.flat_def =  str_to_int(row['flat_def'])            

            newname.crit_rate = pctstr_to_float(row['crit_rate'])
            newname.crit_dmg = pctstr_to_float(row['crit_dmg'])

            newname.physical_dmg = pctstr_to_float(row['physical_dmg'])
            newname.anemo_dmg = pctstr_to_float(row['anemo_dmg'])
            newname.cryo_dmg = pctstr_to_float(row['cryo_dmg'])
            newname.electro_dmg = pctstr_to_float(row['electro_dmg'])
            newname.geo_dmg = pctstr_to_float(row['geo_dmg'])
            newname.hydro_dmg = pctstr_to_float(row['hydro_dmg'])
            newname.pyro_dmg = pctstr_to_float(row['pyro_dmg'])

            newname.ele_m = str_to_int(row['ele_m'])
            newname.recharge =  pctstr_to_float(row['recharge'])
            newname.healing_bonus = pctstr_to_float(row['heal_bonus'])

            newname.normal_type = row['normal_type']
            newname.normal_ticks = str_to_int(row['normal_ticks'])
            newname.normal_at =  str_to_float(row['normal_at'])
            newname.normal_ac = row['normal_ac']
            newname.normal_tick_times = [float(item) for item in row['normal_tick_times'].split(',')]
            newname.normal_tick_damage = [float(item) for item in row['normal_tick_damage'].split(',')]
            newname.normal_tick_units = [float(item) for item in row['normal_tick_units'].split(',')]
            newname.normal_tick_hitlag = [float(item) for item in row['normal_tick_hitlag'].split(',')]
            newname.normal_cancel = [float(item) for item in row['normal_cancel'].split(',')]
            newname.normal_swap = [float(item) for item in row['normal_swap'].split(',')]
            newname.normal_skill = [float(item) for item in row['normal_skill'].split(',')]
            newname.normal_burst = [float(item) for item in row['normal_burst'].split(',')]
            newname.normal_attack = [float(item) for item in row['normal_attack'].split(',') if row['normal_attack'].split(',') != [""]]

            newname.charged_type = row['charged_type']
            newname.charged_ticks = str_to_int(row['charged_ticks'])
            newname.charged_stamina_cost = [float(item) for item in row['charged_stamina_cost'].split(',')]
            newname.charged_tick_times = [float(item) for item in row['charged_tick_times'].split(',')]
            newname.charged_tick_damage = [float(item) for item in row['charged_tick_damage'].split(',')]
            newname.charged_tick_units = [float(item) for item in row['charged_tick_units'].split(',')]
            newname.charged_tick_hitlag = [float(item) for item in row['charged_tick_hitlag'].split(',')]
            newname.charged_cancel = str_to_float(row['charged_cancel'])
            newname.charged_swap = str_to_float(row['charged_swap'])
            newname.charged_skill = str_to_float(row['charged_skill'])
            newname.charged_burst = str_to_float(row['charged_burst'])
            newname.charged_attack = str_to_float(row['charged_attack'])

            newname.skill_ticks = str_to_int(row['skill_ticks'])
            newname.skill_cd = str_to_float(row['skill_cd'])
            newname.skill_charges = str_to_int(row['skill_charges'])
            newname.skill_particles = str_to_float(row['skill_particles'])
            newname.skill_tick_times = [float(item) for item in row['skill_tick_times'].split(',')]
            newname.skill_tick_damage = [float(item) for item in row['skill_tick_damage'].split(',')]
            newname.skill_tick_units = [float(item) for item in row['skill_tick_units'].split(',')]
            newname.skill_cancel = str_to_float(row['skill_cancel'])
            newname.skill_swap = str_to_float(row['skill_swap'])
            newname.skill_burst = str_to_float(row['skill_burst'])
            newname.skill_attack = str_to_float(row['skill_attack'])

            newname.burst_ticks = str_to_int(row['burst_ticks'])
            newname.burst_cd = str_to_float(row['burst_cd'])
            newname.burst_energy_cost = str_to_int(row['burst_energy_cost'])
            newname.burst_tick_times = [float(item) for item in row['burst_tick_times'].split(',')]
            newname.burst_tick_damage = [float(item) for item in row['burst_tick_damage'].split(',')]
            newname.burst_tick_units = [float(item) for item in row['burst_tick_units'].split(',')]
            newname.burst_cancel = str_to_float(row['burst_cancel'])
            newname.burst_swap = str_to_float(row['burst_swap'])
            newname.burst_skill = str_to_float(row['burst_skill'])
            newname.burst_attack = str_to_float(row['burst_attack'])

    return character_dict


class Weapon():
    def __init__ (self,weapon):
        pass

# Reads weapon data
def read_weapon_data():
    with open(WEAPON_FILENAME) as weaponfile:
        weapon_dict = {}
        reader = csv.DictReader(weaponfile, delimiter=',')
        for row in reader:
            weapon = row['weapon']
            newweapon = Weapon(weapon)
            weapon_dict[weapon] = newweapon
            
            newweapon.rarity = row['weapon_rarity']
            newweapon.weapon_class = row['weapon_class']
            newweapon.weapon_rank = 0
            newweapon.base_atk = str_to_int(row['base_atk'])
            newweapon.pct_atk = pctstr_to_float(row['pct_atk'])
            newweapon.crit_rate = pctstr_to_float(row['crit_rate'])
            newweapon.crit_dmg = pctstr_to_float(row['crit_dmg'])
            newweapon.physical_dmg = pctstr_to_float(row['physical_dmg'])
            newweapon.ele_m = str_to_float(row['ele_m'])
            newweapon.recharge =  pctstr_to_float(row['recharge'])
            newweapon.pct_hp =  pctstr_to_float(row['pct_hp'])
            newweapon.pct_def =  pctstr_to_float(row['pct_def'])
    return weapon_dict

class Enemy:
    def __init__ (self, enemy):
        pass

# Reads Enemies data
def read_enemy_data():
    with open(ENEMY_FILENAME) as enemyfile:
        enemy_dict = {}
        reader = csv.DictReader(enemyfile, delimiter=',')
        for row in reader:
            enemy = row['Monsters']
            newenemy = Enemy(enemy)
            enemy_dict[enemy] = newenemy

            newenemy.name = row['Monsters']
            newenemy.anemo_res = pctstr_to_float(row['Anemo RES'])
            newenemy.cryo_res = pctstr_to_float(row['Cryo RES'])
            newenemy.electro_res = pctstr_to_float(row['Electro RES'])
            newenemy.geo_res = pctstr_to_float(row['Geo RES'])
            newenemy.hydro_res = pctstr_to_float(row['Hydro RES'])
            newenemy.pyro_res = pctstr_to_float(row['Pyro RES'])
            newenemy.physical_res = pctstr_to_float(row['Physical RES'])
            newenemy.hitlag = str_to_float(row['Hitlag'])
    return enemy_dict

class Artifact():
    def __init__ (self,weapon):
        pass

# Reads artifact set data
def read_artifact_set_data():
    with open(ARTIFACT_FILENAME) as artifact_set_file:
        artifact_dict = {}
        reader = csv.DictReader(artifact_set_file, delimiter=',')
        for row in reader:
            artifact = row['artifact']
            newarti = Artifact(artifact) 
            artifact_dict[artifact] = newarti

            # TODO may want to consider doing something like: https://stackoverflow.com/a/1305663
            newarti.artifact_rarity = row['artifact_rarity']
            newarti.pct_atk = pctstr_to_float(row['pct_atk'])
            newarti.crit_rate = pctstr_to_float(row['crit_rate'])
            newarti.physical_dmg = pctstr_to_float(row['physical_dmg'])
            newarti.anemo_dmg = pctstr_to_float(row['anemo_dmg'])
            newarti.cryo_dmg = pctstr_to_float(row['cryo_dmg'])
            newarti.electro_dmg = pctstr_to_float(row['electro_dmg'])
            newarti.geo_dmg = pctstr_to_float(row['geo_dmg'])
            newarti.hydro_dmg = pctstr_to_float(row['hydro_dmg'])
            newarti.pyro_dmg = pctstr_to_float(row['pyro_dmg'])
            newarti.ele_m = str_to_int(row['ele_m'])
            newarti.recharge =  pctstr_to_float(row['recharge'])
    return artifact_dict

# Reads elemental ratio data
def read_ele_ratio_data():
    with open(ELERATIO_FILENAME) as ele_ratio_file:
        ele_ratio_dict = {}
        reader = csv.DictReader(ele_ratio_file, delimiter=',')
        for row in reader:
            level = str_to_float(row['Level'])
            ele_ratio_dict[level] = pctstr_to_float(row['Ratio'])
    return ele_ratio_dict

# Reads elemental ratio data
def read_phys_ratio_data():
    with open(PHYSRATIO_FILENAME) as phys_ratio_file:
        phys_ratio_dict = {}
        reader = csv.DictReader(phys_ratio_file, delimiter=',')
        for row in reader:
            level = str_to_float(row['Level'])
            phys_ratio_dict[level] = pctstr_to_float(row['Ratio'])
    return phys_ratio_dict

# Reads razor auto ratio data
def read_razor_auto_ratio_data():
    with open(RAZORAUTO_FILENAME) as razor_auto_ratio_file:
        razor_auto_ratio_dict = {}
        reader = csv.DictReader(razor_auto_ratio_file, delimiter=',')
        for row in reader:
            level = str_to_float(row['Level'])
            razor_auto_ratio_dict[level] = pctstr_to_float(row['Ratio'])
    return razor_auto_ratio_dict

# Reads razor q attack speed ratio data
def read_razor_qas_ratio_data():
    with open(RAZORQAS_FILENAME) as razor_qas_ratio_file:
        razor_qas_ratio_dict = {}
        reader = csv.DictReader(razor_qas_ratio_file, delimiter=',')
        for row in reader:
            level = str_to_float(row['Level'])
            razor_qas_ratio_dict[level] = pctstr_to_float(row['Ratio'])
    return razor_qas_ratio_dict

# Reads zhongli q ratio data
def read_zhongli_q_ratio_data():
    with open(ZHONGLIQ_FILENAME) as zhongli_q_ratio_file:
        zhongli_q_ratio_dict = {}
        reader = csv.DictReader(zhongli_q_ratio_file, delimiter=',')
        for row in reader:
            level = str_to_float(row['Level'])
            zhongli_q_ratio_dict[level] = pctstr_to_float(row['Ratio'])
    return zhongli_q_ratio_dict

def read_buff_data():
    with open(BUFF_FILENAME) as buff_file:
        buff_dict = {}
        reader = csv.DictReader(buff_file,delimiter=',')
        for row in reader:
            buff = (row['Buff'])
            newbuff = Buff(buff)
            buff_dict[buff] = newbuff

            newbuff.share = (row['Share'])
            newbuff.type =  (row['Type'])
            newbuff.type2 = (row['Type2'])
            newbuff.character = (row['Character'])
            newbuff.constellation = str_to_int(row['Constellation'])
            newbuff.weapon = row['Weapon'].split(',')
            newbuff.artifact = (row['Artifact'])
            newbuff.method = (row['method'])
            if row['Duration'] == "Instant":
                newbuff.duration = row['Duration']
            else:
                newbuff.duration = str_to_float(row['Duration'])
            newbuff.trigger = row['Trigger'].split(',')
            newbuff.instant = (row['Instant'])
            newbuff.time_remaining = newbuff.duration
            newbuff.live_cd = 0
            newbuff.field = (row['Field'])
            newbuff.max_stacks = str_to_int(row['Max Stacks'])
            newbuff.stacks = 0
            newbuff.temporary = (row['Temporary'])

        return buff_dict

def read_debuff_data():
    with open(DEBUFF_FILENAME) as debuff_file:
        debuff_dict = {}
        reader = csv.DictReader(debuff_file,delimiter=',')
        for row in reader:
            debuff = (row['Debuff'])
            newdebuff = Debuff(debuff)
            debuff_dict[debuff] = newdebuff

            newdebuff.type2 = (row['Type2'])
            newdebuff.character = (row['Character'])
            newdebuff.constellation = str_to_int(row['Constellation'])
            newdebuff.weapon = (row['Weapon'])
            newdebuff.artifact = (row['Artifact'])
            newdebuff.method = (row['method'])
            newdebuff.duration = str_to_float(row['Duration'])
            newdebuff.trigger = (row['Trigger'])
            newdebuff.time_remaining = newdebuff.duration
        return debuff_dict

character_dict = read_character_data()
weapon_dict = read_weapon_data()
enemy_dict = read_enemy_data()
artifact_dict = read_artifact_set_data()
ele_ratio_dict = read_ele_ratio_data()
phys_ratio_dict = read_phys_ratio_data()
razor_auto_ratio_dict = read_razor_auto_ratio_data()
razor_qas_ratio_dict = read_razor_qas_ratio_data()
zhongli_q_ratio_dict = read_zhongli_q_ratio_data()
buff_dict = read_buff_data()
debuff_dict = read_debuff_data()

def main():
    # print(character_dict)
    # print(character_dict['Amber'])
    # print(artifact_dict)
    # print(artifact_dict["Gladiator's Finale"])
    # print(ele_ratio_dict)
    # print(phys_ratio_dict)
    # print(razor_auto_ratio_dict)
    # print(razor_qas_ratio_dict)
    print(buff_dict["Skyward Blade 3"].type2)
    print(len(character_dict["Xinyan"].normal_attack))
    
if __name__ == '__main__':
    main()