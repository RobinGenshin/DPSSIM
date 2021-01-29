import csv
import read_data as rd

characterdict = rd.character_dict
weapondict = rd.weapon_dict
artifactdict = rd.artifact_dict
eleratiodict = rd.ele_ratio_dict
physratiodict = rd.phys_ratio_dict
razorautoratiodict = rd.razor_auto_ratio_dict
razorqasratiodict = rd.razor_qas_ratio_dict
zhongliqratiodict = rd.zhongli_q_ratio_dict

#Unit/Character
class Unit():
    def __init__(self,name,level,weapon,artifact,constellation,weaponrank,autolevel,skilllevel,burstlevel):
        super(Unit,self).__init__()
        self.name = name
        self.element = characterdict[name].element
        self.level = level
        self.weapon_type = characterdict[name].weapon
        self.weapon = weapon
        self.constellation = constellation
        self.weaponrank = weaponrank
        self.auto_level = autolevel
        self.skill_level = skilllevel
        self.burst_level = burstlevel
        self.base_atk = characterdict[name].base_atk + weapondict[weapon].base_atk + artifactdict[artifact].base_atk
        self.atk_pct = characterdict[name].atk_pct + weapondict[weapon].atk_pct + artifactdict[artifact].atk_pct
        self.flat_atk = characterdict[name].flat_atk + weapondict[weapon].flat_atk + artifactdict[artifact].flat_atk
        self.crit_rate =  characterdict[name].crit_rate + weapondict[weapon].crit_rate + artifactdict[artifact].crit_rate
        self.crit_dmg =  characterdict[name].crit_dmg + weapondict[weapon].crit_dmg + artifactdict[artifact].crit_dmg
        self.physical = characterdict[name].physical + weapondict[weapon].physical + artifactdict[artifact].physical
        self.anemo = characterdict[name].anemo + weapondict[weapon].anemo + artifactdict[artifact].anemo
        self.cryo = characterdict[name].cryo + weapondict[weapon].cryo + artifactdict[artifact].cryo
        self.electro = characterdict[name].electro + weapondict[weapon].electro + artifactdict[artifact].electro
        self.geo = characterdict[name].geo + weapondict[weapon].geo + artifactdict[artifact].geo
        self.hydro = characterdict[name].hydro + weapondict[weapon].hydro + artifactdict[artifact].hydro
        self.pyro = characterdict[name].pyro + weapondict[weapon].pyro + artifactdict[artifact].pyro
        self.elemental_dmg = characterdict[name].elemental_dmg + weapondict[weapon].elemental_dmg + artifactdict[artifact].elemental_dmg
        self.elemental_mastery = characterdict[name].elemental_mastery + weapondict[weapon].elemental_mastery + artifactdict[artifact].elemental_mastery
        self.energy_recharge = characterdict[name].energy_recharge + weapondict[weapon].energy_recharge + artifactdict[artifact].energy_recharge
        self.base_hp = characterdict[name].base_hp + weapondict[weapon].base_hp + artifactdict[artifact].base_hp
        self.hp_pct = characterdict[name].hp_pct + weapondict[weapon].hp_pct + artifactdict[artifact].hp_pct
        self.flat_hp = characterdict[name].flat_hp + weapondict[weapon].flat_hp + artifactdict[artifact].flat_hp
        self.base_def = characterdict[name].base_def + weapondict[weapon].base_def + artifactdict[artifact].base_def
        self.def_pct = characterdict[name].def_pct + weapondict[weapon].def_pct + artifactdict[artifact].def_pct
        self.flat_def = characterdict[name].flat_def + weapondict[weapon].flat_def + artifactdict[artifact].flat_def
        self.all_dmg = characterdict[name].all_dmg + weapondict[weapon].all_dmg + artifactdict[artifact].all_dmg
        self.def_red = characterdict[name].def_red + weapondict[weapon].def_red + artifactdict[artifact].def_red
        self.normal_dmg = characterdict[name].normal_dmg + weapondict[weapon].normal_dmg + artifactdict[artifact].normal_dmg
        self.normal_speed = characterdict[name].normal_speed + weapondict[weapon].normal_speed + artifactdict[artifact].normal_speed
        self.charged_dmg = characterdict[name].charged_dmg + weapondict[weapon].charged_dmg + artifactdict[artifact].charged_dmg
        self.skill_dmg = characterdict[name].skill_dmg + weapondict[weapon].skill_dmg + artifactdict[artifact].skill_dmg
        self.burst_dmg = characterdict[name].burst_dmg + weapondict[weapon].burst_dmg + artifactdict[artifact].burst_dmg
        self.healing_bonus = characterdict[name].healing_bonus + weapondict[weapon].healing_bonus + artifactdict[artifact].healing_bonus
        self.ele_res_red = characterdict[name].ele_res_red + weapondict[weapon].ele_res_red + artifactdict[artifact].ele_res_red
        self.swirl_res_red = characterdict[name].swirl_res_red + weapondict[weapon].swirl_res_red + artifactdict[artifact].swirl_res_red
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
        self.skill_flat_ratio = 0
        self.skill_AT = characterdict[name].skill_AT
        self.skill_CD = characterdict[name].skill_CD
        self.current_skill_CD = 0
        self.skill_hits = characterdict[name].skill_hits
        self.skill_dur = characterdict[name].skill_dur
        self.skill_charges = characterdict[name].skill_charges
        self.skill_RP = characterdict[name].skill_RP
        self.skill_particles = characterdict[name].skill_particles
        self.burst_ratio = characterdict[name].burst_ratio
        self.burst_flat_ratio = 0
        self.burst_AT = characterdict[name].burst_AT
        self.burst_CD = characterdict[name].burst_CD
        self.current_burst_CD = 0
        self.burst_energy = characterdict[name].burst_energy
        self.current_burst_energy = 0
        self.burst_hits = characterdict[name].burst_hits
        self.burst_dur = characterdict[name].burst_dur
        self.burst_charges = characterdict[name].burst_charges
        self.burst_RP = characterdict[name].burst_RP
    
    def normal_attack_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.crit_rate * self.crit_dmg))
        dmg_bon = (1 + self.all_dmg + self.normal_dmg + getattr(self,str(self.normal_attack_type.lower())))

        if self.normal_attack_type == "Physical":
            if self.name == "Razor":
                normal_scaling = razorautoratiodict[self.auto_level]
            else:
                normal_scaling = physratiodict[self.auto_level]
        else:
            normal_scaling = eleratiodict[self.auto_level]
        
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level)) #enemy def will get updated in sim
        restype = str(self.normal_attack_type).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype) #enemy res will get updated in sim
        
        return tot_atk * crit_mult * dmg_bon * self.normal_attack_ratio * normal_scaling * enemy_res * defence

    def charged_attack_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.crit_rate * self.crit_dmg))
        dmg_bon = (1 + self.all_dmg + self.normal_dmg + getattr(self,str(self.charged_attack_type.lower())))

        if self.charged_attack_type == "Physical":
            charged_scaling = physratiodict[self.auto_level]
        else:
            charged_scaling = eleratiodict[self.auto_level]

        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level ))
        restype = str(self.charged_attack_type).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype)
        
        return tot_atk * crit_mult * dmg_bon * self.charged_attack_ratio * charged_scaling * enemy_res * defence

    def skill_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.crit_rate * self.crit_dmg))
        dmg_bon = (1 + self.all_dmg + self.normal_dmg + getattr(self,str(self.charged_attack_type.lower())))
        skill_scaling = eleratiodict[self.skill_level]
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level ))
        restype = str(self.element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype)

        return tot_atk * crit_mult * dmg_bon * self.skill_ratio * skill_scaling * enemy_res * defence

    def burst_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.crit_rate * self.crit_dmg))
        dmg_bon = (1 + self.all_dmg + self.normal_dmg + getattr(self,str(self.charged_attack_type.lower())))
        burst_scaling = eleratiodict[self.burst_level]
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level ))
        restype = str(self.element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype)        

        return tot_atk * crit_mult * dmg_bon * self.burst_ratio * burst_scaling * enemy_res * defence

    def normal_attack_duration(self,enemy):
        non_hitlag_dur = (self.normal_AT / (1 + self.normal_speed))
        if self.weapon_type in ["Sword","Polearm","Claymore"]:
            hitlag = self.normal_hits * (enemy.hitlag / 60)
        else:
            hitlag = 0
        if self.normal_AC == "Yes":
            dash_frames = 0.33
        else:
            dash_frames = 0
        
        return non_hitlag_dur + hitlag + dash_frames

    def charged_attack_duration(self,enemy):
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

    def skill_duration(self):
        return self.skill_AT

    def burst_duration(self):
        return self.burst_AT       

    def normal_attack_dps(self,enemy):
        return self.normal_attack_damage(enemy) / self.normal_attack_duration(enemy)

    def charged_attack_dps(self,enemy):
        return self.charged_attack_damage(enemy) / self.charged_attack_duration(enemy)

    def skill_dps(self,enemy):
        return self.skill_damage(enemy) / self.skill_duration()

    def burst_dps(self,enemy):
        return self.burst_damage(enemy) / self.burst_duration()

#Enemy with stats
class Enemy:
    def __init__ (self, enemy, level):
        enemydict = rd.read_enemy_data()
        self.name = enemydict[enemy].name
        self.level = level
        self.physical_res = enemydict[enemy].physical_res
        self.anemo_res = enemydict[enemy].anemo_res
        self.cryo_res = enemydict[enemy].cryo_res
        self.electro_res = enemydict[enemy].electro_res
        self.geo_res = enemydict[enemy].geo_res
        self.hydro_res = enemydict[enemy].hydro_res
        self.pyro_res = enemydict[enemy].pyro_res
        self.hitlag = enemydict[enemy].hitlag

def main():
    Test = Unit("Amber", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 1, 1, 1)
    Monster = Enemy("Hilichurls", 90)
    print(Test.normal_attack_dps(Monster), Test.charged_attack_dps(Monster), Test.skill_dps(Monster), Test.burst_dps(Monster))

if __name__ == '__main__':
    main()