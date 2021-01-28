import csv
import OOP
import read_data as rd

#Units in team
class Unit(OOP.GeneralObject):
    def __init__(self,name,weapon,constellation,weaponrank,autolevel,skilllevel,burstlevel):
        characterdict = rd.read_character_data()
        weapondict = rd.read_weapon_data()
        self.name = name
        self.element = characterdict[name].element
        self.weapon = weapon
        self.constellation = constellation
        self.weaponrank = weaponrank
        self.auto_level = autolevel
        self.skill_level = skilllevel
        self.base_atk = characterdict[name].base_atk + weapondict[weapon].base_atk
        self.atk_pct = characterdict[name].atk_pct + weapondict[weapon].atk_pct
        self.flat_atk = characterdict[name].flat_atk + weapondict[weapon].flat_atk
        self.crit_rate =  characterdict[name].crit_rate + weapondict[weapon].crit_rate
        self.crit_dmg =  characterdict[name].crit_dmg + weapondict[weapon].crit_dmg
        self.physical = characterdict[name].physical + weapondict[weapon].physical
        self.anemo = characterdict[name].anemo + weapondict[weapon].anemo
        self.cryo = characterdict[name].cryo + weapondict[weapon].cryo
        self.electro = characterdict[name].electro + weapondict[weapon].electro
        self.geo = characterdict[name].geo + weapondict[weapon].geo
        self.hydro = characterdict[name].hydro + weapondict[weapon].hydro
        self.pyro = characterdict[name].pyro + weapondict[weapon].pyro
        self.elemental_dmg = characterdict[name].elemental_dmg + weapondict[weapon].elemental_dmg
        self.elemental_mastery = characterdict[name].elemental_mastery + weapondict[weapon].elemental_mastery
        self.energy_recharge = characterdict[name].energy_recharge + weapondict[weapon].energy_recharge
        self.base_hp = characterdict[name].base_hp + weapondict[weapon].base_hp
        self.hp_pct = characterdict[name].hp_pct + weapondict[weapon].hp_pct
        self.flat_hp = characterdict[name].flat_hp + weapondict[weapon].flat_hp
        self.base_def = characterdict[name].base_def + weapondict[weapon].base_def
        self.def_pct = characterdict[name].def_pct + weapondict[weapon].def_pct
        self.flat_def = characterdict[name].flat_def + weapondict[weapon].flat_def
        self.all_dmg = characterdict[name].all_dmg + weapondict[weapon].all_dmg
        self.def_red = characterdict[name].def_red + weapondict[weapon].def_red
        self.normal_dmg = characterdict[name].normal_dmg + weapondict[weapon].normal_dmg
        self.normal_speed = characterdict[name].normal_speed + weapondict[weapon].normal_speed
        self.charged_dmg = characterdict[name].charged_dmg + weapondict[weapon].charged_dmg
        self.skill_dmg = characterdict[name].charged_dmg + weapondict[weapon].charged_dmg
        self.burst_dmg = characterdict[name].burst_dmg + weapondict[weapon].burst_dmg
        self.healing_bonus = characterdict[name].healing_bonus + weapondict[weapon].healing_bonus
        self.ele_res_red = characterdict[name].ele_res_red + weapondict[weapon].ele_res_red
        self.swirl_res_red = characterdict[name].swirl_res_red + weapondict[weapon].swirl_res_red
        self.normal_attack_type = characterdict[name].normal_attack_type
        self.normal_attack_ratio = characterdict[name].normal_attack_ratio
        self.normal_AT = characterdict[name].normal_AT
        self.normal_AC = characterdict[name].normal_AC
        self.normal_hits = characterdict[name].normal_hits
        self.normal_RP =  characterdict[name].normal_RP
        self.passive_hits = characterdict[name].passive_hits
        self.charged_attack_type = characterdict[name].charged_attack_type
        self.charged_attack_ratio = characterdict[name].charged_attack_ratio
        self.charged_AT = characterdict[name].charged_AT
        self.charged_AC = characterdict[name].charged_AC
        self.charged_hits = characterdict[name].charged_hits
        self.charged_RP = characterdict[name].charged_RP
        self.charged_stam = characterdict[name].charged_stam
        self.skill_ratio = characterdict[name].skill_ratio
        self.skill_AT = characterdict[name].skill_AT
        self.skill_CD = characterdict[name].skill_CD
        self.skill_hits = characterdict[name].skill_hits
        self.skill_dur = characterdict[name].skill_dur
        self.skill_charges = characterdict[name].skill_charges
        self.skill_RP = characterdict[name].skill_RP
        self.skill_particles = characterdict[name].skill_particles
        self.burst_ratio = characterdict[name].burst_ratio
        self.burst_AT = characterdict[name].burst_AT
        self.burst_CD = characterdict[name].burst_CD
        self.burst_energy = characterdict[name].burst_energy
        self.burst_hits = characterdict[name].burst_hits
        self.burst_dur = characterdict[name].burst_dur
        self.burst_charges = characterdict[name].burst_charges
        self.burst_RP = characterdict[name].burst_RP

# Calculate stats into useable values
class UnitStats():
    def __init__ (self, unit):
        self.total_atk = unit.base_atk * (1 + unit.atk_pct) + unit.flat_atk
        self.crit_mult = 1 + (unit.crit_rate * unit.crit_dmg)
        self.total_normal_pct = 1 + unit.all_dmg + unit.normal_dmg + getattr(unit,str(unit.normal_attack_type.lower()))
        self.total_charged_pct = 1 + unit.all_dmg + unit.charged_dmg + getattr(unit,str(unit.charged_attack_type.lower()))
        self.total_skill_pct = 1 + unit.all_dmg + unit.skill_dmg + getattr(unit,str(unit.element.lower()))
        self.total_burst_pct = 1 + unit.all_dmg + unit.burst_dmg + getattr(unit,str(unit.element.lower()))
        self.total_normal_spd = 1 + unit.normal_speed
        self.skill_CD = unit.skill_CD
        self.burst_CD = unit.burst_CD
        self.burst_energy = unit.burst_energy

# Calculate initial damage per action
class UnitDamage():
    def __init__ (self, unit):
        UnitStatsUpd = UnitStats(unit)
        self.ini_auto_dmg = unit.normal_attack_ratio * UnitStatsUpd.total_atk * UnitStatsUpd.total_normal_pct
        self.ini_charged_dmg = unit.charged_attack_ratio * UnitStatsUpd.total_atk * UnitStatsUpd.total_charged_pct
        self.ini_skill_dmg = unit.skill_ratio * UnitStatsUpd.total_atk * UnitStatsUpd.total_skill_pct
        self.ini_burst_dmg = unit.burst_ratio * UnitStatsUpd.total_atk * UnitStatsUpd.total_burst_pct

#Enemy with stats
class Enemy:
    def __init__ (self, enemy):
        enemydict = rd.read_enemy_data()
        self.name = enemydict[enemy].name
        self.anemo_res = enemydict[enemy].anemo_res
        self.cryo_res = enemydict[enemy].cryo_res
        self.electro_res = enemydict[enemy].electro_res
        self.geo_res = enemydict[enemy].geo_res
        self.hydro_res = enemydict[enemy].hydro_res
        self.pyro_res = enemydict[enemy].pyro_res
        self.hitlag = enemydict[enemy].hitlag

class UnitActionDuration():
    def __init__(self, unit, enemy):
        self.normal_dur = (unit.normal_AT / ( 1 + unit.normal_speed ))
        if unit.weapon in ["Sword","Polearm","Claymore"]:
            self.normal_dur += (unit.normal_hits * (enemy.hitlag / 60))
        if unit.normal_AC == "Yes":
            self.normal_dur += 0.33
        self.charged_dur = unit.charged_AT
        if unit.weapon in ["Sword","Polearm","Claymore"]:
            self.charged_dur += (unit.normal_hits * (enemy.hitlag / 60))
        if unit.charged_AC == "Yes":
            self.charged_dur += 0.33
        self.skill_dur = unit.skill_AT
        self.burst_dur = unit.burst_AT

class UnitActionDPS(UnitActionDuration):
    def __init__(self,unit,enemy):
        super(UnitActionDPS, self).__init__(unit,enemy)
        UnitDamageUpd = UnitDamage(unit)
        if self.normal_dur != 0:
            self.normal_dps = UnitDamageUpd.ini_auto_dmg / self.normal_dur
        if self.charged_dur != 0:
            self.charged_dps = UnitDamageUpd.ini_charged_dmg / self.charged_dur
        if self.skill_dur != 0:
            self.skill_dps = UnitDamageUpd.ini_skill_dmg / self.skill_dur
        if self.burst_dur != 0:
            self.burst_dps = UnitDamageUpd.ini_burst_dmg / self.burst_dur


def main():
    Main = Unit("Amber","Prototype Crescent", 0, 1, 1, 1, 1)
    enemy = Enemy("Hilichurls")
    Test = UnitActionDPS(Main,enemy)
    print("Normal DPS is", Test.normal_dps)
    print("Charged DPS is", Test.charged_dps)
    print("Skill DPS is", Test.skill_dps)
    print("Burst DPS is", Test.burst_dps)

def main2():
    Main = Unit("Amber","Prototype Crescent", 0, 1, 1, 1, 1)
    enemy = Enemy("Hilichurls")
    print(Main.base_atk)
    print(Main.normal_hits)
    MainUpd = UnitStats(Main)
    print(MainUpd.total_atk)
    MainUnitActionDuration = UnitActionDuration(Main,enemy)
    print(MainUnitActionDuration.normal_dur)
    print(UnitActionDuration(Main,"Hilichurls").normal_dur)
