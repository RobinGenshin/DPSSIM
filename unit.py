import csv
import read_data as rd
import buffs as c
import artifact_substats
from enemy import *

characterdict = rd.character_dict
weapondict = rd.weapon_dict
artifactdict = rd.artifact_dict
eleratiodict = rd.ele_ratio_dict
physratiodict = rd.phys_ratio_dict
razorautoratiodict = rd.razor_auto_ratio_dict
razorqasratiodict = rd.razor_qas_ratio_dict
zhongliqratiodict = rd.zhongli_q_ratio_dict
buffdict = rd.buff_dict
debuffdict = rd.debuff_dict

#Unit/Character
class Unit():
    def __init__(self,name,level,weapon,artifact,constellation,weaponrank,autolevel,skilllevel,burstlevel,artifact_stat):
        self.name = name
        self.element = characterdict[name].element
        self.level = level
        self.weapon_type = characterdict[name].weapon
        self.weapon = weapon
        self.artifact = artifact
        self.constellation = constellation
        self.weaponrank = weaponrank
        self.auto_level = autolevel
        self.skill_level = skilllevel
        self.burst_level = burstlevel
        self.base_atk = characterdict[name].base_atk + weapondict[weapon].base_atk
        self.atk_pct = characterdict[name].atk_pct + weapondict[weapon].atk_pct + artifactdict[artifact].atk_pct + artifact_stat.atk_pct
        self.live_atk_pct = self.atk_pct
        self.flat_atk = characterdict[name].flat_atk + weapondict[weapon].flat_atk + artifactdict[artifact].flat_atk + artifact_stat.flat_atk
        self.live_flat_atk = self.flat_atk
        self.crit_rate =  characterdict[name].crit_rate + weapondict[weapon].crit_rate + artifactdict[artifact].crit_rate + artifact_stat.crit_rate
        self.live_crit_rate = self.crit_rate
        self.crit_dmg =  characterdict[name].crit_dmg + weapondict[weapon].crit_dmg + artifactdict[artifact].crit_dmg + artifact_stat.crit_dmg
        self.live_crit_dmg = self.crit_dmg
        self.physical = characterdict[name].physical + weapondict[weapon].physical + artifactdict[artifact].physical+ artifact_stat.physical
        self.live_physical = self.physical
        self.anemo = characterdict[name].anemo + weapondict[weapon].anemo + artifactdict[artifact].anemo + artifact_stat.anemo
        self.live_anemo = self.anemo
        self.cryo = characterdict[name].cryo + weapondict[weapon].cryo + artifactdict[artifact].cryo + artifact_stat.cryo
        self.live_cryo = self.cryo
        self.electro = characterdict[name].electro + weapondict[weapon].electro + artifactdict[artifact].electro + artifact_stat.electro
        self.live_electro = self.electro
        self.geo = characterdict[name].geo + weapondict[weapon].geo + artifactdict[artifact].geo + artifact_stat.geo
        self.live_geo = self.geo
        self.hydro = characterdict[name].hydro + weapondict[weapon].hydro + artifactdict[artifact].hydro + artifact_stat.hydro
        self.live_hydro = self.hydro
        self.pyro = characterdict[name].pyro + weapondict[weapon].pyro + artifactdict[artifact].pyro + artifact_stat.pyro
        self.live_pyro = self.pyro
        self.elemental_dmg = characterdict[name].elemental_dmg + weapondict[weapon].elemental_dmg + artifactdict[artifact].elemental_dmg
        self.live_elemental_dmg = self.elemental_dmg
        self.elemental_mastery = characterdict[name].elemental_mastery + weapondict[weapon].elemental_mastery + artifactdict[artifact].elemental_mastery+ artifact_stat.elemental_mastery
        self.live_elemental_mastery = self.elemental_mastery
        self.energy_recharge = characterdict[name].energy_recharge + weapondict[weapon].energy_recharge + artifactdict[artifact].energy_recharge + artifact_stat.energy_recharge
        self.live_energy_recharge = self.energy_recharge
        self.base_hp = characterdict[name].base_hp + weapondict[weapon].base_hp + artifactdict[artifact].base_hp
        self.hp_pct = characterdict[name].hp_pct + weapondict[weapon].hp_pct + artifactdict[artifact].hp_pct+ artifact_stat.hp_pct
        self.flat_hp = characterdict[name].flat_hp + weapondict[weapon].flat_hp + artifactdict[artifact].flat_hp + artifact_stat.flat_hp
        self.base_def = characterdict[name].base_def + weapondict[weapon].base_def + artifactdict[artifact].base_def
        self.def_pct = characterdict[name].def_pct + weapondict[weapon].def_pct + artifactdict[artifact].def_pct + artifact_stat.def_pct
        self.flat_def = characterdict[name].flat_def + weapondict[weapon].flat_def + artifactdict[artifact].flat_def + artifact_stat.flat_def
        self.all_dmg = characterdict[name].all_dmg + weapondict[weapon].all_dmg + artifactdict[artifact].all_dmg
        self.live_all_dmg = self.all_dmg
        self.def_red = characterdict[name].def_red + weapondict[weapon].def_red + artifactdict[artifact].def_red
        self.normal_dmg = characterdict[name].normal_dmg + weapondict[weapon].normal_dmg + artifactdict[artifact].normal_dmg
        self.live_normal_dmg = self.normal_dmg
        self.normal_speed = characterdict[name].normal_speed + weapondict[weapon].normal_speed + artifactdict[artifact].normal_speed
        self.live_normal_speed = self.normal_speed
        self.charged_dmg = characterdict[name].charged_dmg + weapondict[weapon].charged_dmg + artifactdict[artifact].charged_dmg
        self.live_charged_dmg = self.charged_dmg
        self.skill_dmg = characterdict[name].skill_dmg + weapondict[weapon].skill_dmg + artifactdict[artifact].skill_dmg
        self.live_skill_dmg = self.skill_dmg
        self.burst_dmg = characterdict[name].burst_dmg + weapondict[weapon].burst_dmg + artifactdict[artifact].burst_dmg
        self.live_burst_dmg = self.burst_dmg
        self.healing_bonus = characterdict[name].healing_bonus + weapondict[weapon].healing_bonus + artifactdict[artifact].healing_bonus
        self.normal_attack_element = characterdict[name].normal_attack_type
        self.normal_attack_ratio = characterdict[name].normal_attack_ratio
        self.normal_AT = characterdict[name].normal_AT
        self.normal_AC = characterdict[name].normal_AC
        self.normal_hits = characterdict[name].normal_hits
        self.normal_RP =  characterdict[name].normal_RP
        self.passive_hits = characterdict[name].passive_hits
        self.charged_attack_element = characterdict[name].charged_attack_type
        self.charged_attack_ratio = characterdict[name].charged_attack_ratio
        self.charged_AT = characterdict[name].charged_AT
        self.charged_AC = characterdict[name].charged_AC
        self.charged_hits = characterdict[name].charged_hits
        self.charged_RP = characterdict[name].charged_RP
        self.charged_stam = characterdict[name].charged_stam
        self.skill_element = self.element
        self.skill_ratio = characterdict[name].skill_ratio
        self.skill_flat_ratio = 0
        self.skill_AT = characterdict[name].skill_AT
        self.skill_CD = characterdict[name].skill_CD
        self.live_skill_CD = 0
        self.skill_CDR = 1
        self.live_skill_CDR = self.skill_CDR
        self.skill_hits = characterdict[name].skill_hits
        if characterdict[name].skill_dur == "Instant":
            self.skill_dur = characterdict[name].skill_dur
        else:
            self.skill_dur = rd.str_to_float(characterdict[name].skill_dur)
        self.skill_ticks = characterdict[name].skill_ticks 
        self.skill_charges = characterdict[name].skill_charges
        self.live_skill_charges = self.skill_charges
        self.skill_U = characterdict[name].skill_U
        self.skill_particles = characterdict[name].skill_particles
        self.burst_element = self.element
        self.burst_ratio = characterdict[name].burst_ratio
        self.burst_flat_ratio = 0
        self.burst_crit_rate = 0
        self.burst_AT = characterdict[name].burst_AT
        self.burst_CD = characterdict[name].burst_CD
        self.burst_CDR = 1
        self.live_burst_CDR = self.burst_CDR
        self.live_burst_CD = 0
        self.burst_energy = characterdict[name].burst_energy
        self.live_burst_energy = self.burst_energy
        self.burst_hits = characterdict[name].burst_hits
        if characterdict[name].burst_dur == "Instant":
            self.burst_dur = characterdict[name].burst_dur
        else:
            self.burst_dur = rd.str_to_float(characterdict[name].burst_dur)
        self.burst_ticks = characterdict[name].skill_ticks 
        self.burst_charges = characterdict[name].burst_charges
        self.live_burst_charges = self.burst_charges
        self.burst_U = characterdict[name].burst_U
        self.stam_save = 0
        self.live_stam_save = 0
        self.static_buffs = {}
        self.triggerable_buffs = {}
        self.active_buffs = {}
        self.triggerable_debuffs = {}

        for key, buff in buffdict.items():
            if buff.character == self.name:
                if buff.constellation <= self.constellation:
                    if buff.type == "Static":
                        self.static_buffs[key] = buff
                        getattr(c.StaticBuff(),buff.method)(self)
                    if buff.type == "Active":
                        self.triggerable_buffs[key] = buff
            if buff.weapon == self.weapon:
                if buff.type == "Static":
                    self.static_buffs[key] = buff
                    getattr(c.StaticBuff(),buff.method)(self,buff.rank)
                if buff.type == "Active":
                    self.triggerable_buffs[key] = buff
            if buff.artifact == self.artifact:
                if buff.type == "Static":
                    self.static_buffs[key] = buff
                    getattr(c.StaticBuff(),buff.method)(self)
                if buff.type == "Active":
                    self.triggerable_buffs[key] = buff
        
        for key,debuff in debuffdict.items():
            if debuff.character == self.name:
                if debuff.constellation <= self.constellation:
                        self.triggerable_debuffs[key] = debuff
            if debuff.weapon == self.weapon:
                    self.triggerable_debuffs[key] = debuff
            if debuff.artifact == self.artifact:
                    self.triggerable_debuffs[key] = debuff                

    def update_stats(self):
        # clears active buffs
        x = {"atk_pct", "crit_rate", "crit_dmg", "anemo", "cryo", "electro", "geo", "hydro", "pyro", "elemental_dmg", "all_dmg", "normal_dmg", "normal_speed", "charged_dmg", "skill_dmg", "burst_dmg", "skill_CDR", "burst_CDR"}
        for stat in x:
            setattr(self, "live_" + stat, getattr(self, stat))
        # call method to reactivate buff
        for buff in self.active_buffs.values():
            if buff.weapon != "":
                getattr(c.ActiveBuff(),buff.method)(self,buff.weapon_rank)
            else:
                getattr(c.ActiveBuff(),buff.method)(self)
    
    def normal_attack_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_normal_dmg + getattr(self,"live_" + str(self.normal_attack_element.lower())))

        if self.normal_attack_element == "Physical":
            if self.name == "Razor":
                normal_scaling = razorautoratiodict[self.auto_level]
            else:
                normal_scaling = physratiodict[self.auto_level]
        else:
            normal_scaling = eleratiodict[self.auto_level]
        
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (enemy.live_defence)) #enemy def will get updated in sim
        restype = str(self.normal_attack_element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, "live_" + restype) #enemy res will get updated in sim
        
        return tot_atk * crit_mult * dmg_bon * self.normal_attack_ratio * normal_scaling * enemy_res * defence

    def charged_attack_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_charged_dmg + getattr(self,"live_" + str(self.charged_attack_element.lower())))

        if self.charged_attack_element == "Physical":
            charged_scaling = physratiodict[self.auto_level]
        else:
            charged_scaling = eleratiodict[self.auto_level]

        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (enemy.live_defence))
        restype = str(self.charged_attack_element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, "live_" + restype)
        
        return tot_atk * crit_mult * dmg_bon * self.charged_attack_ratio * charged_scaling * enemy_res * defence

    def skill_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_skill_dmg + getattr(self,"live_" + str(self.element.lower())))
        skill_scaling = eleratiodict[self.skill_level]
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (enemy.live_defence))
        restype = str(self.element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, "live_" + restype)

        return tot_atk * crit_mult * dmg_bon * self.skill_ratio * skill_scaling * enemy_res * defence

    def burst_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_burst_dmg + getattr(self,"live_" + str(self.element.lower())))
        burst_scaling = eleratiodict[self.burst_level]
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (enemy.live_defence))
        restype = str(self.element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, "live_" + restype) 
       
        return tot_atk * crit_mult * dmg_bon * self.burst_ratio * burst_scaling * enemy_res * defence

    def normal_attack_action_time(self,enemy):
        non_hitlag_dur = (self.normal_AT / (1 + self.live_normal_speed))
        if self.weapon_type in ["Sword","Polearm","Claymore"]:
            hitlag = self.normal_hits * (enemy.hitlag / 60)
        else:
            hitlag = 0
        if self.normal_AC == "Yes":
            dash_frames = 0.33
        else:
            dash_frames = 0
        
        return non_hitlag_dur + hitlag + dash_frames

    def charged_attack_action_time(self,enemy):
        non_hitlag_dur = self.charged_AT
        if self.weapon_type in ["Sword","Polearm","Claymore"]:
            hitlag = self.charged_hits * (enemy.hitlag / 60)
        else:
            hitlag = 0
        if self.normal_AC == "Yes":
            dash_frames = 0.33
        else:
            dash_frames = 0
        
        return non_hitlag_dur + hitlag + dash_frames

    def skill_action_time(self,enemy):
        return self.skill_AT

    def burst_action_time(self,enemy):
        return self.burst_AT       

    def normal_attack_dps(self,enemy):
        if self.normal_attack_action_time(enemy) == 0:
            return 0
        else:
            return self.normal_attack_damage(enemy)/self.normal_attack_action_time(enemy)

    def charged_attack_dps(self,enemy):
        if self.charged_attack_action_time(enemy) == 0:
            return 0
        else:
            return self.charged_attack_damage(enemy)/self.charged_attack_action_time(enemy)

    def skill_dps(self,enemy):
        if self.live_skill_CD == 0:
            return self.skill_damage(enemy)/self.skill_action_time(enemy)
        else:
            return 0

    def burst_dps(self,enemy):
        if self.live_burst_CD == 0 and self.live_burst_energy == self.burst_energy:
            return self.burst_damage(enemy)/self.burst_action_time(enemy)
        else:
            return 0

    def highest_dps_action(self,enemy):
        return max(self.normal_attack_dps(enemy),self.charged_attack_dps(enemy),self.skill_dps(enemy),self.burst_dps(enemy))

def main():
    # Unit = Unit(Character, level, weapon, artifact set, constellation, weapon rank, auto level, skill level, burst level)
    TestPyro = artifact_substats.ArtifactStats("atk_pct","pyro","crit_dmg","Perfect")
    Main = Unit("Amber", 90, "Prototype Crescent", "Crimson Witch", 6, 1, 1, 1, 1, TestPyro) 
    Monster = Enemy("Hilichurls", 90)
    print(type(Monster.defence), type(Monster.defence_debuff))
    print(Main.triggerable_buffs)
    print(type(buffdict["Lavawalker"]))

if __name__ == '__main__':
    main()