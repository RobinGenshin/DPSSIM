import csv
import read_data as rd
import staticbuffs as c

characterdict = rd.character_dict
weapondict = rd.weapon_dict
artifactdict = rd.artifact_dict
eleratiodict = rd.ele_ratio_dict
physratiodict = rd.phys_ratio_dict
razorautoratiodict = rd.razor_auto_ratio_dict
razorqasratiodict = rd.razor_qas_ratio_dict
zhongliqratiodict = rd.zhongli_q_ratio_dict
constdict = rd.const_dict
charbuffdict = rd.charbuff_dict

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
        self.live_atk_pct = self.atk_pct
        self.flat_atk = characterdict[name].flat_atk + weapondict[weapon].flat_atk + artifactdict[artifact].flat_atk
        self.crit_rate =  characterdict[name].crit_rate + weapondict[weapon].crit_rate + artifactdict[artifact].crit_rate
        self.live_crit_rate = self.crit_rate
        self.crit_dmg =  characterdict[name].crit_dmg + weapondict[weapon].crit_dmg + artifactdict[artifact].crit_dmg
        self.live_crit_dmg = self.crit_dmg
        self.physical = characterdict[name].physical + weapondict[weapon].physical + artifactdict[artifact].physical
        self.live_physical = self.physical
        self.anemo = characterdict[name].anemo + weapondict[weapon].anemo + artifactdict[artifact].anemo
        self.live_anemo = self.anemo
        self.cryo = characterdict[name].cryo + weapondict[weapon].cryo + artifactdict[artifact].cryo
        self.live_cryo = self.cryo
        self.electro = characterdict[name].electro + weapondict[weapon].electro + artifactdict[artifact].electro
        self.live_electro = self.electro
        self.geo = characterdict[name].geo + weapondict[weapon].geo + artifactdict[artifact].geo
        self.live_geo = self.geo
        self.hydro = characterdict[name].hydro + weapondict[weapon].hydro + artifactdict[artifact].hydro
        self.live_hydro = self.hydro
        self.pyro = characterdict[name].pyro + weapondict[weapon].pyro + artifactdict[artifact].pyro
        self.live_pyro = self.pyro
        self.elemental_dmg = characterdict[name].elemental_dmg + weapondict[weapon].elemental_dmg + artifactdict[artifact].elemental_dmg
        self.live_elemental_dmg = self.elemental_dmg
        self.elemental_mastery = characterdict[name].elemental_mastery + weapondict[weapon].elemental_mastery + artifactdict[artifact].elemental_mastery
        self.live_elemental_mastery = self.elemental_mastery
        self.energy_recharge = characterdict[name].energy_recharge + weapondict[weapon].energy_recharge + artifactdict[artifact].energy_recharge
        self.live_energy_recharge = self.energy_recharge
        self.base_hp = characterdict[name].base_hp + weapondict[weapon].base_hp + artifactdict[artifact].base_hp
        self.hp_pct = characterdict[name].hp_pct + weapondict[weapon].hp_pct + artifactdict[artifact].hp_pct
        self.flat_hp = characterdict[name].flat_hp + weapondict[weapon].flat_hp + artifactdict[artifact].flat_hp
        self.base_def = characterdict[name].base_def + weapondict[weapon].base_def + artifactdict[artifact].base_def
        self.def_pct = characterdict[name].def_pct + weapondict[weapon].def_pct + artifactdict[artifact].def_pct
        self.flat_def = characterdict[name].flat_def + weapondict[weapon].flat_def + artifactdict[artifact].flat_def
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
        self.skill_CDR = 1
        self.live_skill_CDR = self.skill_CDR
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
        self.burst_CDR = 1
        self.live_burst_CDR = self.burst_CDR
        self.current_burst_CD = 0
        self.burst_energy = characterdict[name].burst_energy
        self.current_burst_energy = self.burst_energy
        self.burst_hits = characterdict[name].burst_hits
        self.burst_dur = characterdict[name].burst_dur
        self.burst_charges = characterdict[name].burst_charges
        self.burst_RP = characterdict[name].burst_RP
        self.const_config = constdict[name]
        for constellation in self.const_config:
            key = constellation.translate({ord('C'):None})
            if self.constellation >= int(key):
                for x in range(0,len(self.const_config[constellation])):
                    getattr(c.StaticBuff(),self.const_config[constellation][x])(self)
        self.triggerable_char_buffs = {}
        for buff in charbuffdict:
            if charbuffdict[buff].character == self.name:
                if charbuffdict[buff].constellation <= self.constellation:
                    self.triggerable_char_buffs[buff] = charbuffdict[buff]
        self.active_char_buffs = {}

    def update_stats(self):
        # clears stat buffs
        for key in self.active_char_buffs:
            setattr(self, "live_"+self.active_char_buffs[key].stat , getattr(self,self.active_char_buffs[key].stat))
        # adds up stat buffs
        for key in self.active_char_buffs:
            setattr(self, "live_" + self.active_char_buffs[key].stat,getattr(self,"live_" + self.active_char_buffs[key].stat)+self.active_char_buffs[key].value)
    
    def normal_attack_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_normal_dmg + getattr(self,"live_" + str(self.normal_attack_type.lower())))

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
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_charged_dmg + getattr(self,"live_" + str(self.charged_attack_type.lower())))

        if self.charged_attack_type == "Physical":
            charged_scaling = physratiodict[self.auto_level]
        else:
            charged_scaling = eleratiodict[self.auto_level]

        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level ))
        restype = str(self.charged_attack_type).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype)
        
        return tot_atk * crit_mult * dmg_bon * self.charged_attack_ratio * charged_scaling * enemy_res * defence

    def skill_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_skill_dmg + getattr(self,"live_" + str(self.element.lower())))
        skill_scaling = eleratiodict[self.skill_level]
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level ))
        restype = str(self.element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype)

        return tot_atk * crit_mult * dmg_bon * self.skill_ratio * skill_scaling * enemy_res * defence

    def burst_damage(self,enemy):
        tot_atk = (self.base_atk * (1 + self.live_atk_pct) + self.flat_atk)
        crit_mult = ( 1 + (self.live_crit_rate * self.live_crit_dmg))
        dmg_bon = (1 + self.live_all_dmg + self.live_burst_dmg + getattr(self,"live_" + str(self.element.lower())))
        burst_scaling = eleratiodict[self.burst_level]
        defence  = ( 100 + self.level ) / (( 100 + self.level ) + (100 + enemy.level ))
        restype = str(self.element).lower()+"_res"
        enemy_res = 1 - getattr(enemy, restype) 
       
        return tot_atk * crit_mult * dmg_bon * self.burst_ratio * burst_scaling * enemy_res * defence

    def normal_attack_duration(self,enemy):
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
        if self.normal_attack_duration(enemy) == 0:
            return 0
        else:
            return self.normal_attack_damage(enemy)/self.normal_attack_duration(enemy)

    def charged_attack_dps(self,enemy):
        if self.charged_attack_duration(enemy) == 0:
            return 0
        else:
            return self.charged_attack_damage(enemy)/self.charged_attack_duration(enemy)

    def skill_dps(self,enemy):
        if self.current_skill_CD == 0:
            return self.skill_damage(enemy)/self.skill_duration()
        else:
            return 0
        return self.skill_damage(enemy)/self.skill_duration()

    def burst_dps(self,enemy):
        if self.current_burst_CD == 0 and self.current_burst_energy == self.burst_energy:
            return self.burst_damage(enemy)/self.burst_duration()
        else:
            return 0

    def highest_dps(self,enemy):
        return max(self.normal_attack_dps(enemy),self.charged_attack_dps(enemy),self.skill_dps(enemy),self.burst_dps(enemy))

    # Returns highest_dps_action
    def highest_dps_action(self,enemy):
        self.update_stats()
        action = self.highest_dps(enemy)
        if action == self.normal_attack_dps(enemy):
            return "normal"
        if action == self.charged_attack_dps(enemy):
            return "charged"
        if action == self.skill_dps(enemy):
            return "skill"
        if action == self.burst_dps(enemy):
            return "burst"

#Action Class
class ChosenAction:
    def __init__ (self,unit,enemy):
        self.unit = unit
        self.type = unit.highest_dps_action(enemy)
        self.dps = unit.highest_dps(enemy)

        if self.type == 'normal':
            self.cd = 0
            self.damage = unit.normal_attack_damage(enemy)
            self.duration = unit.normal_attack_duration(enemy)
            self.particles = 0

        if self.type == 'charged':
            self.cd = 0
            self.damage = unit.charged_attack_damage(enemy)
            self.duration = unit.charged_attack_duration(enemy)
            self.particles = 0

        if self.type == 'skill':
            self.cd = unit.skill_CD
            self.damage = unit.skill_damage(enemy)
            self.particles = unit.skill_particles
            self.duration = unit.skill_duration()

        if self.type == 'burst':
            self.cd = unit.skill_CD
            self.damage = unit.burst_damage(enemy)
            self.duration = unit.burst_duration()
            self.particles = 0
            self.energy = unit.burst_energy



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
    # Unit = Unit(Character, level, weapon, artifact set, constellation, weapon rank, auto level, skill level, burst level)
    Main = Unit("Amber", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 1, 1, 1)
    # Monster = Enemy("Hilichurls", 90)
    print(Main.const_config)
    print(constdict["Diona"])
    print(Main.charged_attack_ratio)
    print(Main.skill_flat_ratio)
    print(Main.burst_level)
    print(Main.skill_charges)
    print(Main.triggerable_char_buffs)
    for key, value in Main.triggerable_char_buffs.items():
        print(key,value)
    print(Main.atk_pct)
    Main.update_stats()
    print(type(Main.triggerable_char_buffs["Burst_atk_buff"].stat))
    print(Main.atk_pct)

if __name__ == '__main__':
    main()