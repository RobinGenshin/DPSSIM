import csv
import activebuffs as ab

CHARACTER_FILENAME = 'data/Characters.csv'
WEAPON_FILENAME = 'data/Weapons.csv'
ENEMY_FILENAME = 'data/Enemies.csv'
ARTIFACT_FILENAME = 'data/ArtifactSets.csv'
ELERATIO_FILENAME = 'data/ElementalRatio.csv'
PHYSRATIO_FILENAME = 'data/PhysicalRatio.csv'
RAZORAUTO_FILENAME = 'data/RazorAutoRatio.csv'
RAZORQAS_FILENAME = 'data/RazorQASRatio.csv'
ZHONGLIQ_FILENAME = 'data/ZhongliQRatio.csv'
CONST_FILENAME = 'data/Constellations.csv'
CHARBUFF_FILENAME = 'data/ActiveCharBuffs.csv'


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
        self.ele_res_red = 0
        self.swirl_res_red = 0
        self.phys_res_red = 0
        self.normal_attack_type = ""
        self.normal_attack_ratio = 0
        self.normal_AT = ""
        self.normal_AC = 0
        self.normal_hits = 0
        self.normal_RP = 0
        self.passive_hits = 0
        self.charged_attack_type = 0
        self.charged_attack_ratio = 0
        self.charged_AT = 0
        self.charged_AC = ""
        self.charged_hits = 0
        self.charged_RP = 0
        self.charged_stam = 0
        self.skill_ratio = 0
        self.skill_flat_ratio = 0
        self.skill_AT = 0
        self.skill_CD = 0
        self.skill_hits = 0
        self.skill_dur = 0
        self.skill_charges = 0
        self.skill_RP = 0
        self.skill_particles = 0
        self.burst_ratio = 0
        self.burst_flat_ratio = 0
        self.burst_AT = 0
        self.burst_CD = 0
        self.burst_energy = 0
        self.burst_hits = 0
        self.burst_dur = 0
        self.burst_charges = 0
        self.burst_RP = 0

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
            newname.constellation = 0
            newname.weapon_rank = 0
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
            newname.ele_res_red = pctstr_to_float(row['Ele Res Reduce'])
            newname.swirl_res_red = pctstr_to_float(row['Swirl Res Reduce'])
            newname.phys_res_red = pctstr_to_float(row['Phys Res Reduce'])
            newname.normal_attack_type = row['Normal Attack Type']
            newname.normal_attack_ratio = pctstr_to_float(row['Normal Attack Ratio'])
            newname.normal_AT =  str_to_float(row['Normal AT'])
            newname.normal_AC = row['Normal AC']
            newname.normal_hits =  str_to_int(row['Normal attack hits'])
            newname.normal_RP =  str_to_float(row['Normal RP'])
            newname.passive_hits = pctstr_to_float(row['Passive hits'])
            newname.charged_attack_type = row['Charged Attack Type']
            newname.charged_attack_ratio = pctstr_to_float(row['Charged Attack Ratio'])
            newname.charged_AT =  str_to_float(row['Charged AT'])
            newname.charged_AC = row['Charged AC']
            newname.charged_hits =  str_to_int(row['Charged attack hits'])
            newname.charged_RP = str_to_float(row['Charged RP'])
            newname.charged_stam = str_to_float(row['Stamina'])
            newname.skill_ratio = pctstr_to_float(row['E Ratio'])
            newname.skill_AT = str_to_float(row['E AT'])
            newname.skill_CD = str_to_float(row['E cd'])
            newname.skill_hits = str_to_int(row['E hits'])
            newname.skill_dur = str_to_int(row['E duration'])
            newname.skill_charges = str_to_int(row['E Charges'])
            newname.skill_RP = str_to_int(row['E RP'])
            newname.skill_particles = str_to_float(row['Particles'])
            newname.burst_ratio = pctstr_to_float(row['Q Ratio'])
            newname.burst_AT = str_to_float(row['Q AT'])
            newname.burst_CD = str_to_float(row['Q cd'])
            newname.burst_energy = str_to_int(row['Q energy'])
            newname.burst_hits = str_to_int(row['Q hits'])
            newname.burst_dur = str_to_float(row['Q duration'])
            newname.burst_charges = ""
            newname.burst_RP =  str_to_float(row['Q RP'])

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
        self.ele_res_red = 0
        self.swirl_res_red = 0
        self.phys_res_red = 0

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
            newweapon.ele_res_red = pctstr_to_float(row['Ele Res Reduce'])
            newweapon.swirl_res_red = pctstr_to_float(row['Swirl Res Reduce'])
            newweapon.phys_res_red = pctstr_to_float(row['Phys Res Reduce'])
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
        self.ele_res_red = 0
        self.swirl_res_red = 0
        self.phys_res_red = 0

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
            newarti.ele_res_red = pctstr_to_float(row['Ele Res Reduce'])
            newarti.swirl_res_red = pctstr_to_float(row['Swirl Res Reduce'])
            newarti.phys_res_red = pctstr_to_float(row['Phys Res Reduce'])
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

# Reads constellation info
def read_constellation_data():
    with open(CONST_FILENAME) as constellation_file:
        constellation__dict = {}
        reader = csv.DictReader(constellation_file, delimiter=',')
        for row in reader:
            character = (row['Character'])
            constellation__dict[character] = {"C1":(row['C1']).split(", "),"C2":(row['C2']).split(", "),"C3":(row['C3']).split(", "),"C4":(row['C4']).split(", "),"C5":(row['C5']).split(", "),"C6":(row['C6']).split(", ")}
    return constellation__dict

def read_char_buff_data():
    with open(CHARBUFF_FILENAME) as charbuff_file:
        charbuff_dict = {}
        reader = csv.DictReader(charbuff_file, delimiter=',')
        for row in reader:
            buff = (row['Buff'])
            charbuff_dict[buff] = ab.ActiveCharBuff((row['Character']),str_to_int(row['Constellation']),(row['Stat']),str_to_float(row['Value']),str_to_float(row['Duration']),(row['Trigger']),(row['Share']))
    return charbuff_dict

character_dict = read_character_data()
weapon_dict = read_weapon_data()
enemy_dict = read_enemy_data()
artifact_dict = read_artifact_set_data()
ele_ratio_dict = read_ele_ratio_data()
phys_ratio_dict = read_phys_ratio_data()
razor_auto_ratio_dict = read_razor_auto_ratio_data()
razor_qas_ratio_dict = read_razor_qas_ratio_data()
zhongli_q_ratio_dict = read_zhongli_q_ratio_data()
const_dict = read_constellation_data()
charbuff_dict = read_char_buff_data()

def main():
    # print(character_dict)
    # print(character_dict['Amber'])
    # print(artifact_dict)
    # print(artifact_dict["Gladiator's Finale"])
    # print(ele_ratio_dict)
    # print(phys_ratio_dict)
    # print(razor_auto_ratio_dict)
    # print(razor_qas_ratio_dict)
    # print(zhongli_q_ratio_dict)
    print(const_dict["Amber"])
    print(charbuff_dict)
    
if __name__ == '__main__':
    main()