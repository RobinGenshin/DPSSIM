import csv
import OOP
CHARACTER_FILENAME = 'data/Characters.csv'
WEAPON_FILENAME = 'data/Weapons.csv'
ENEMY_FILENAME = 'data/Enemies.csv'

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
def read_character_data():
    with open(CHARACTER_FILENAME) as charfile:
        character_dict = {}
        reader = csv.DictReader(charfile, delimiter=',')
        for row in reader:
            name = row['Character']
            newname = OOP.GeneralObject() 
            character_dict[name] = newname

            # TODO may want to consider doing something like: https://stackoverflow.com/a/1305663
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


# Reads weapon data
def read_weapon_data():
    with open(WEAPON_FILENAME) as weaponfile:
        weapon_dict = {}
        reader = csv.DictReader(weaponfile, delimiter=',')
        for row in reader:
            weapon = row['Weapon']
            newweapon = OOP.GeneralObject()
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

# Reads Enemies data
def read_enemy_data():
    with open(ENEMY_FILENAME) as enemyfile:
        enemy_dict = {}
        reader = csv.DictReader(enemyfile, delimiter=',')
        for row in reader:
            enemy = row['Monsters']
            newenemy = OOP.GeneralObject()
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

characterdict = read_character_data()
weapondict = read_weapon_data()
enemydict = read_enemy_data()

def main():
    character_dict = read_character_data()
    #print(character_dict)
    print(character_dict['Amber'])


if __name__ == '__main__':
    main()