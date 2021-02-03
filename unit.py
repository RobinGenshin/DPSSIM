import csv
import read_data as rd
import staticeffects as s
import activeeffects as a
import artifact_substats
import copy

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
        self.weapon_rank = weaponrank

        self.normal_level = autolevel
        self.charged_level = autolevel

        self.skill_level = skilllevel
        self.burst_level = burstlevel
        self.base_atk = characterdict[name].base_atk + weapondict[weapon].base_atk
        self.atk_pct = characterdict[name].atk_pct + weapondict[weapon].atk_pct + artifactdict[artifact].atk_pct + artifact_stat.atk_pct
        self.live_atk_pct = self.atk_pct
        self.flat_atk = characterdict[name].flat_atk + weapondict[weapon].flat_atk + artifactdict[artifact].flat_atk + artifact_stat.flat_atk
        self.live_flat_atk = self.flat_atk

        self.crit_rate =  characterdict[name].crit_rate + weapondict[weapon].crit_rate + artifactdict[artifact].crit_rate + artifact_stat.crit_rate
        self.live_crit_rate = self.crit_rate
        self.cond_crit_rate = 0
        self.live_cond_crit_rate = 0

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
        self.live_def_pct = self.def_pct
        self.flat_def = characterdict[name].flat_def + weapondict[weapon].flat_def + artifactdict[artifact].flat_def + artifact_stat.flat_def
        self.live_flat_def = self.flat_def

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
        self.cond_dmg = 0
        self.live_cond_dmg = 0

        self.normal_type = characterdict[name].normal_type
        self.normal_hits = characterdict[name].normal_hits
        self.normal_AT = characterdict[name].normal_AT
        self.normal_AC = characterdict[name].normal_AC
        self.normal_tick_times = characterdict[name].normal_tick_times
        self.normal_tick_damage = characterdict[name].normal_tick_damage
        self.normal_tick_units = characterdict[name].normal_tick_units
        self.passive_hits = characterdict[name].passive_hits

        self.charged_type = characterdict[name].charged_type
        self.charged_hits = characterdict[name].charged_hits
        self.charged_AT = characterdict[name].charged_AT
        self.charged_AC = characterdict[name].charged_AC
        self.charged_tick_times = characterdict[name].charged_tick_times
        self.charged_tick_damage = characterdict[name].charged_tick_damage
        self.charged_tick_units = characterdict[name].charged_tick_units
        self.charged_stam = characterdict[name].charged_stam

        self.skill_type = self.element
        self.skill_hits = characterdict[name].skill_hits
        self.skill_AT = characterdict[name].skill_AT
        self.skill_tick_times = characterdict[name].skill_tick_times
        self.skill_tick_damage = characterdict[name].skill_tick_damage
        self.skill_tick_units = characterdict[name].skill_tick_units
        self.skill_flat_ratio = 0
        self.skill_CD = characterdict[name].skill_CD
        self.live_skill_CD = 0
        self.skill_CDR = 1
        self.live_skill_CDR = self.skill_CDR
        self.skill_charges = characterdict[name].skill_charges
        self.live_skill_charges = self.skill_charges
        self.skill_particles = characterdict[name].skill_particles
        self.skill_crit_rate = 0

        self.burst_type = self.element
        self.burst_hits = characterdict[name].burst_hits
        self.burst_AT = characterdict[name].burst_AT
        self.burst_tick_times = characterdict[name].burst_tick_times
        self.burst_tick_damage = characterdict[name].burst_tick_damage
        self.burst_tick_units = characterdict[name].burst_tick_units
        self.burst_flat_ratio = 0
        self.burst_crit_rate = 0
        self.burst_CD = characterdict[name].burst_CD
        self.live_burst_CD = 0
        self.burst_CDR = 1
        self.live_burst_CDR = self.burst_CDR
        self.burst_energy = characterdict[name].burst_energy
        self.live_burst_energy = self.burst_energy

        self.stam_save = 0
        self.live_stam_save = 0

        self.field_time = 0

        self.static_buffs = {}
        self.triggerable_buffs = {}
        self.triggerable_debuffs = {}
        self.active_buffs = {}

        for key, buff in buffdict.items():
            if buff.character == self.name:
                if buff.constellation <= self.constellation:
                    if buff.type == "Static":
                        self.static_buffs[key] = copy.deepcopy(buff)
                        getattr(s.StaticBuff(),buff.method)(self)
                    if buff.type == "Active":
                        self.triggerable_buffs[key] = copy.deepcopy(buff)
            if self.weapon in buff.weapon:
                if buff.type == "Static":
                    self.static_buffs[key] = copy.deepcopy(buff)
                    getattr(s.StaticBuff(),buff.method)(self)
                if buff.type == "Active":
                    self.triggerable_buffs[key] = copy.deepcopy(buff)
            if buff.artifact == self.artifact:
                if buff.type == "Static":
                    self.static_buffs[key] = copy.deepcopy(buff)
                    getattr(s.StaticBuff(),buff.method)(self)
                if buff.type == "Active":
                    self.triggerable_buffs[key] = copy.deepcopy(buff)
        
        for key,debuff in debuffdict.items():
            if debuff.character == self.name:
                if debuff.constellation <= self.constellation:
                        self.triggerable_debuffs[key] = debuff
            if debuff.weapon == self.weapon:
                    self.triggerable_debuffs[key] = debuff
            if debuff.artifact == self.artifact:
                    self.triggerable_debuffs[key] = debuff                

    def update_stats(self,sim):
        # clears active buffs
        x = {"atk_pct", "crit_rate", "crit_dmg", "anemo", "cryo", "electro", "geo", "hydro", 
        "pyro", "elemental_dmg", "all_dmg", "normal_dmg", "normal_speed", "charged_dmg", 
        "skill_dmg", "burst_dmg", "skill_CDR", "burst_CDR", "cond_dmg", "cond_crit_rate"}
        for stat in x:
            setattr(self, "live_" + stat, getattr(self, stat))
        # call method to reactivate buff
        for _, buff in self.active_buffs.items():
            if buff.weapon != "":
                getattr(a.ActiveBuff(),buff.method)(self,sim)
            if buff.character != "":
                getattr(a.ActiveBuff(),buff.method)(self,sim)
            if buff.artifact != "":
                getattr(a.ActiveBuff(),buff.method)(self,sim)

def main():
    AnemoArtifact = artifact_substats.ArtifactStats("energy_recharge", "anemo", "crit_rate", "Perfect")
    Main = Unit("Albedo", 90, "Skyward Atlas", "Thundersoother", 0, 5, 6, 6, 6, AnemoArtifact)
    print(len(Main.burst_tick_times))
    print(len(Main.burst_tick_damage))
    print(len(Main.burst_tick_units))
    

if __name__ == '__main__':
    main()