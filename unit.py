# pylint: disable=no-member
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
        self.weapon_type = characterdict[name].weapon_type
        self.weapon = weapon
        self.artifact = artifact

        self.constellation = constellation
        self.weapon_rank = weaponrank

        self.normal_level = autolevel
        self.charged_level = autolevel
        self.skill_level = skilllevel
        self.burst_level = burstlevel

        self.actions = {"combo","skill","burst"}
        self.combo_options = {"normal","charged"}

        for stat in {"atk", "hp", "def"}:
            for x in {"base_","flat_","pct_"}:
                setattr(self,x+stat,getattr(characterdict[name],x+stat,0)+getattr(weapondict[weapon],x+stat,0)+
                        getattr(artifactdict[artifact],x+stat,0)+getattr(artifact_stat,x+stat,0))

        for stat in {"anemo_dmg","cryo_dmg","electro_dmg","geo_dmg","hydro_dmg","pyro_dmg","ele_dmg",
                    "physical_dmg","normal_dmg","charged_dmg","skill_dmg","burst_dmg","plunge_dmg","all_dmg",
                    "ele_m","recharge","crit_rate","crit_dmg","heal_bonus",
                    "normal_speed","charged_speed","stam_save","plunge_speed"}:

            setattr(self,stat,getattr(characterdict[name],stat,0)+getattr(weapondict[weapon],stat,0)+
                    getattr(artifactdict[artifact],x+stat,0)+getattr(artifact_stat,stat,0))

        for stat in {"crit_rate","dmg"}:
            setattr(self,"cond_" + stat, getattr(self,stat,0))    

        for action_type in {"normal","charged","skill","burst","plunge"}:
            for x in {"_type","_ticks","_tick_times","_tick_damage","_tick_units","element","_tick_hitlag",
                    "_cancel","_swap","_attack","_skill","_burst","_crit_rate",
                    "_cd","_cdr","_particles","_charges","_energy_cost","_stamina_cost","_stam_save","_ac","_at","_cond_crit_rate"}:
                setattr(self,action_type+x,getattr(characterdict[name],action_type+x,0))

        for reaction in {"overload","superconduct","electro_charged","swirl","vaporise","melt"}:
            setattr(self,reaction + "_dmg", getattr(artifactdict,reaction+"_dmg",0))

        self.static_buffs = {}
        self.triggerable_buffs = {}
        self.active_buffs = {}
        self.triggerable_debuffs = {}

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

        self.base_stats = copy.deepcopy(self.__dict__)
        
        for x in self.base_stats:
            setattr(self, "live_" + x , getattr(self,x))

        self.live_stats = copy.deepcopy({ k:self.__dict__[k] for k in set(self.__dict__) - set(self.base_stats)})

        self.current_skill_cd = 0
        self.current_burst_cd = 0
        self.current_energy = self.live_burst_energy_cost
        self.current_skill_charges = self.live_skill_charges


    def update_stats(self,sim):
        # clears active buffs
        
        for stat in self.live_stats:
            setattr(self, stat, copy.deepcopy(getattr(self,stat.removeprefix("live_"))))

        # call method to reactivate buff
        for _, buff in self.active_buffs.items():
            if buff.weapon != "":
                getattr(a.ActiveBuff(),buff.method)(self,sim,"extra")
            if buff.character != "":
                getattr(a.ActiveBuff(),buff.method)(self,sim,"extra")
            if buff.artifact != "":
                getattr(a.ActiveBuff(),buff.method)(self,sim,"extra")

def main():
    AnemoArtifact = artifact_substats.ArtifactStats("recharge", "anemo_dmg", "crit_rate", "Perfect")
    Main = Unit("Xiao", 90, "Skyward Atlas", "Thundersoother", 0, 5, 6, 6, 6, AnemoArtifact)
    print(Main.name)
    print(Main.skill_cd)
    print(Main.charged_stamina_cost)
    print(Main.live_charged_type)
    print(Main.normal_tick_units)
    print(Main.skill_cancel)
    print(Main.live_plunge_type)
    print(Main.combo_options)
    

if __name__ == '__main__':
    main()