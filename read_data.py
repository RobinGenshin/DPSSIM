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
    def __init__ (self,name):
        self.name = ""
        self.element = ""
        self.weapon = ""
        self.artifact = ""
        self.base_atk = 0
        self.atk_pct = 0
        self.flat_atk = 0
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical = 0
        self.anemo = 0
        self.cryo = 0
        self.electro = 0
        self.geo = 0
        self.hydro = 0
        self.pyro = 0
        self.elemental_dmg = 0
        self.elemental_mastery = 0
        self.energy_recharge = 0
        self.base_hp = 0
        self.hp_pct = 0
        self.flat_hp = 0
        self.base_def = 0
        self.def_pct = 0
        self.flat_def = 0
        self.all_dmg = 0
        self.def_red = 0
        self.normal_dmg = 0
        self.normal_speed = 0
        self.charged_dmg = 0
        self.skill_dmg = 0
        self.burst_dmg = 0
        self.healing_bonus = 0
        self.normal_type = ""
        self.normal_hits = 0
        self.normal_AT = ""
        self.normal_AC = ""
        self.normal_tick_times = []
        self.normal_tick_damage = []
        self.normal_tick_units = []
        self.passive_hits = 0
        self.charged_type = 0
        self.charged_hits = 0
        self.charged_AT = 0
        self.charged_AC = ""
        self.charged_tick_times = []
        self.charged_tick_damage = []
        self.charged_tick_units = []
        self.charged_stam = 0
        self.skill_hits = 0
        self.skill_AT = 0
        self.skill_cd = 0
        self.skill_dur = 0
        self.skill_tick_times = []
        self.skill_tick_damage = []
        self.skill_tick_units = []
        self.skill_charges = 0
        self.skill_particles = 0
        self.burst_hits = 0
        self.burst_AT = 0
        self.burst_CD = 0
        self.burst_energy = 0
        self.burst_tick_times = []
        self.burst_tick_damage = []
        self.burst_tick_units = []
        self.burst_charges = 0

def read_character_data():
    with open(CHARACTER_FILENAME) as charfile:
        character_dict = {}
        reader = csv.DictReader(charfile, delimiter=',')
        for row in reader:
            name = row['Character']
            newname = Character(name) 
            character_dict[name] = newname
            newname.name = row['Character']
            newname.element = row['Element']
            newname.weapon = row['Weapon Type']
            newname.base_atk = str_to_int(row['Base ATK'])
            newname.atk_pct = pctstr_to_float(row['ATK%'])
            newname.flat_atk = str_to_int(row['Flat ATK'])
            newname.crit_rate = pctstr_to_float(row['Crit Rate%'])
            newname.crit_dmg = pctstr_to_float(row['Crit Damage%'])
            newname.physical = pctstr_to_float(row['Physical%'])
            newname.anemo = pctstr_to_float(row['Anemo%'])
            newname.cryo = pctstr_to_float(row['Cryo%'])
            newname.electro = pctstr_to_float(row['Electro%'])
            newname.geo = pctstr_to_float(row['Geo%'])
            newname.hydro = pctstr_to_float(row['Hydro%'])
            newname.pyro = pctstr_to_float(row['Pyro%'])
            newname.elemental_dmg = pctstr_to_float(row['Elemental DMG%'])
            newname.elemental_mastery = str_to_int(row['Elemental Mastery'])
            newname.energy_recharge =  pctstr_to_float(row['Energy Recharge%'])
            newname.base_hp = str_to_int(row['Base HP'])
            newname.hp_pct =  pctstr_to_float(row['HP%'])
            newname.flat_hp = str_to_int(row['Flat HP'])
            newname.base_def = str_to_int(row['DEF'])
            newname.def_pct =  pctstr_to_float(row['DEF%'])
            newname.flat_def =  str_to_int(row['Flat DEF'])
            newname.all_dmg =  pctstr_to_float(row['DMG %'])
            newname.def_red =  pctstr_to_float(row['Defence reduce'])
            newname.normal_dmg = pctstr_to_float(row['Normal DMG%'])
            newname.normal_speed = pctstr_to_float(row['Normal Speed'])
            newname.charged_dmg = pctstr_to_float(row['Charged DMG%'])
            newname.skill_dmg = pctstr_to_float(row['Skill DMG%'])
            newname.burst_dmg = pctstr_to_float(row['Burst DMG%'])
            newname.healing_bonus = pctstr_to_float(row['Healing Bonus%'])

            newname.normal_type = row['Normal type']
            newname.normal_hits = str_to_int(row['Normal hits'])
            newname.normal_AT =  str_to_float(row['Normal AT'])
            newname.normal_AC = row['Normal AC']
            newname.normal_tick_times = [float(item) for item in row['Normal tick times'].split(',')]
            newname.normal_tick_damage = [float(item) for item in row['Normal tick damage'].split(',')]
            newname.normal_tick_units = [float(item) for item in row['Normal tick units'].split(',')]
            newname.passive_hits = pctstr_to_float(row['Passive hits'])

            newname.charged_type = row['Charged type']
            newname.charged_hits = str_to_int(row['Charged hits'])
            newname.charged_AT =  str_to_float(row['Charged AT'])
            newname.charged_AC = row['Charged AC']
            newname.charged_tick_times = [float(item) for item in row['Charged tick times'].split(',')]
            newname.charged_tick_damage = [float(item) for item in row['Charged tick damage'].split(',')]
            newname.charged_tick_units = [float(item) for item in row['Charged tick units'].split(',')]
            newname.charged_stam = str_to_float(row['Stamina'])

            newname.skill_hits = str_to_int(row['E hits'])
            newname.skill_AT = str_to_float(row['E AT'])
            newname.skill_CD = str_to_float(row['E cd'])
            newname.skill_tick_times = [float(item) for item in row['E tick times'].split(',')]
            newname.skill_tick_damage = [float(item) for item in row['E tick damage'].split(',')]
            newname.skill_tick_units = [float(item) for item in row['E tick units'].split(',')]
            newname.skill_charges = str_to_int(row['E Charges'])
            newname.skill_particles = str_to_float(row['Particles'])

            newname.burst_hits = str_to_int(row['Q hits'])
            newname.burst_AT = str_to_float(row['Q AT'])
            newname.burst_CD = str_to_float(row['Q cd'])
            newname.burst_energy = str_to_int(row['Q energy'])
            newname.burst_tick_times = [float(item) for item in row['Q tick times'].split(',')]
            newname.burst_tick_damage = [float(item) for item in row['Q tick damage'].split(',')]
            newname.burst_tick_units = [float(item) for item in row['Q tick units'].split(',')]

    return character_dict


class Weapon():
    def __init__ (self,weapon):
        self.name = ""
        self.element = ""
        self.weapon = ""
        self.artifact = ""
        self.constellation = 0
        self.weapon_rank = 0
        self.auto_level = 0
        self.skill_level = 0
        self.burst_level = 0
        self.base_atk = 0
        self.atk_pct = 0
        self.flat_atk = 0
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical = 0
        self.anemo = 0
        self.cryo = 0
        self.electro = 0
        self.geo = 0
        self.hydro = 0
        self.pyro = 0
        self.elemental_dmg = 0
        self.elemental_mastery = 0
        self.energy_recharge = 0
        self.base_hp = 0
        self.hp_pct = 0
        self.flat_hp = 0
        self.base_def = 0
        self.def_pct = 0
        self.flat_def = 0
        self.all_dmg = 0
        self.def_red = 0
        self.normal_dmg = 0
        self.normal_speed = 0
        self.charged_dmg = 0
        self.skill_dmg = 0
        self.burst_dmg = 0
        self.healing_bonus = 0

# Reads weapon data
def read_weapon_data():
    with open(WEAPON_FILENAME) as weaponfile:
        weapon_dict = {}
        reader = csv.DictReader(weaponfile, delimiter=',')
        for row in reader:
            weapon = row['Weapon']
            newweapon = Weapon(weapon)
            weapon_dict[weapon] = newweapon
            
            newweapon.rarity = row['Rarity']
            newweapon.weapon = row['Type']
            newweapon.weapon_rank = 0
            newweapon.base_atk = str_to_int(row['Base ATK'])
            newweapon.atk_pct = pctstr_to_float(row['ATK%'])
            newweapon.flat_atk = str_to_int(row['Flat ATK'])
            newweapon.crit_rate = pctstr_to_float(row['Crit Rate%'])
            newweapon.crit_dmg = pctstr_to_float(row['Crit Damage%'])
            newweapon.physical = pctstr_to_float(row['Physical%'])
            newweapon.anemo = pctstr_to_float(row['Anemo%'])
            newweapon.cryo = pctstr_to_float(row['Cryo%'])
            newweapon.electro = pctstr_to_float(row['Electro%'])
            newweapon.geo = pctstr_to_float(row['Geo%'])
            newweapon.hydro = pctstr_to_float(row['Hydro%'])
            newweapon.pyro = pctstr_to_float(row['Pyro%'])
            newweapon.elemental_dmg = pctstr_to_float(row['Elemental DMG%'])
            newweapon.elemental_mastery = str_to_float(row['Elemental Mastery'])
            newweapon.energy_recharge =  pctstr_to_float(row['Energy Recharge%'])
            newweapon.base_hp = str_to_int(row['Base HP'])
            newweapon.hp_pct =  pctstr_to_float(row['HP%'])
            newweapon.flat_hp = str_to_int(row['Flat HP'])
            newweapon.base_def = str_to_int(row['DEF'])
            newweapon.def_pct =  pctstr_to_float(row['DEF%'])
            newweapon.flat_def =  str_to_int(row['Flat DEF'])
            newweapon.all_dmg =  pctstr_to_float(row['DMG %'])
            newweapon.def_red =  pctstr_to_float(row['Defence reduce'])
            newweapon.normal_dmg = pctstr_to_float(row['Normal DMG%'])
            newweapon.normal_speed = pctstr_to_float(row['Normal Speed'])
            newweapon.charged_dmg = pctstr_to_float(row['Charged DMG%'])
            newweapon.skill_dmg = pctstr_to_float(row['Skill DMG%'])
            newweapon.burst_dmg = pctstr_to_float(row['Burst DMG%'])
            newweapon.healing_bonus = pctstr_to_float(row['Healing Bonus%'])
    return weapon_dict

class Enemy:
    def __init__ (self, enemy):
        self.name = ""
        self.level = 0
        self.physical_res = 0
        self.anemo_res = 0
        self.cryo_res = 0
        self.electro_res = 0
        self.geo_res = 0
        self.hydro_res = 0
        self.pyro_res = 0
        self.hitlag = 0

# Reads Enemies data
def read_enemy_data():
    with open(ENEMY_FILENAME) as enemyfile:
        enemy_dict = {}
        reader = csv.DictReader(enemyfile, delimiter=',')
        for row in reader:
            enemy = row['Monsters']
            newenemy = Enemy(enemy)
            enemy_dict[enemy] = newenemy

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
        self.name = ""
        self.element = ""
        self.weapon = ""
        self.artifact = ""
        self.constellation = 0
        self.weapon_rank = 0
        self.auto_level = 0
        self.skill_level = 0
        self.burst_level = 0
        self.base_atk = 0
        self.atk_pct = 0
        self.flat_atk = 0
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical = 0
        self.anemo = 0
        self.cryo = 0
        self.electro = 0
        self.geo = 0
        self.hydro = 0
        self.pyro = 0
        self.elemental_dmg = 0
        self.elemental_mastery = 0
        self.energy_recharge = 0
        self.base_hp = 0
        self.hp_pct = 0
        self.flat_hp = 0
        self.base_def = 0
        self.def_pct = 0
        self.flat_def = 0
        self.all_dmg = 0
        self.def_red = 0
        self.normal_dmg = 0
        self.normal_speed = 0
        self.charged_dmg = 0
        self.skill_dmg = 0
        self.burst_dmg = 0
        self.healing_bonus = 0

# Reads artifact set data
def read_artifact_set_data():
    with open(ARTIFACT_FILENAME) as artifact_set_file:
        artifact_dict = {}
        reader = csv.DictReader(artifact_set_file, delimiter=',')
        for row in reader:
            artifact = row['Artifact']
            newarti = Artifact(artifact) 
            artifact_dict[artifact] = newarti

            # TODO may want to consider doing something like: https://stackoverflow.com/a/1305663
            newarti.artifact_rarity = row['Rarity']
            newarti.base_atk = str_to_int(row['Base ATK'])
            newarti.atk_pct = pctstr_to_float(row['ATK%'])
            newarti.flat_atk = str_to_int(row['Flat ATK'])
            newarti.crit_rate = pctstr_to_float(row['Crit Rate%'])
            newarti.crit_dmg = pctstr_to_float(row['Crit Damage%'])
            newarti.physical = pctstr_to_float(row['Physical%'])
            newarti.anemo = pctstr_to_float(row['Anemo%'])
            newarti.cryo = pctstr_to_float(row['Cryo%'])
            newarti.electro = pctstr_to_float(row['Electro%'])
            newarti.geo = pctstr_to_float(row['Geo%'])
            newarti.hydro = pctstr_to_float(row['Hydro%'])
            newarti.pyro = pctstr_to_float(row['Pyro%'])
            newarti.elemental_dmg = pctstr_to_float(row['Elemental DMG%'])
            newarti.elemental_mastery = str_to_int(row['Elemental Mastery'])
            newarti.energy_recharge =  pctstr_to_float(row['Energy Recharge%'])
            newarti.base_hp = str_to_int(row['Base HP'])
            newarti.hp_pct =  pctstr_to_float(row['HP%'])
            newarti.flat_hp = str_to_int(row['Flat HP'])
            newarti.base_def = str_to_int(row['DEF'])
            newarti.def_pct =  pctstr_to_float(row['DEF%'])
            newarti.flat_def =  str_to_int(row['Flat DEF'])
            newarti.all_dmg =  pctstr_to_float(row['DMG %'])
            newarti.def_red =  pctstr_to_float(row['Defence reduce'])
            newarti.normal_dmg = pctstr_to_float(row['Normal DMG%'])
            newarti.normal_speed = pctstr_to_float(row['Normal Speed'])
            newarti.charged_dmg = pctstr_to_float(row['Charged DMG%'])
            newarti.skill_dmg = pctstr_to_float(row['Skill DMG%'])
            newarti.burst_dmg = pctstr_to_float(row['Burst DMG%'])
            newarti.healing_bonus = pctstr_to_float(row['Healing Bonus%'])
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
            newbuff.weapon = (row['Weapon'])
            newbuff.artifact = (row['Artifact'])
            newbuff.method = (row['method'])
            newbuff.duration = str_to_float(row['Duration'])
            newbuff.trigger = (row['Trigger'])
            newbuff.instant = (row['Instant'])
            newbuff.cooldown = str_to_float(row['Cooldown'])
            newbuff.stacks = str_to_int(row['Stacks'])
            newbuff.time_remaining = newbuff.duration
            newbuff.live_cooldown = 0
        return buff_dict

def read_debuff_data():
    with open(DEBUFF_FILENAME) as debuff_file:
        debuff_dict = {}
        reader = csv.DictReader(debuff_file,delimiter=',')
        for row in reader:
            debuff = (row['Debuff'])
            newdebuff = Debuff(debuff)
            debuff_dict[debuff] = newdebuff

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
    for character in character_dict:
        print(character_dict[character].normal_tick_times)
    
if __name__ == '__main__':
    main()