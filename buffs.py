import csv

class Buff:
    def __init__(self,Buff,Share,Type,Character,Weapon,Rank,Artifact,Constellation,method,Duration,Trigger,Instant,Precast):
        self.name = Buff
        self.share = Share
        self.type = Type
        self.character = Character
        self.constellation = Constellation
        self.weapon = Weapon
        self.weapon_rank = Rank
        self.artifact = Artifact
        self.method = method
        self.duration = Duration
        self.trigger = Trigger
        self.instant = Instant
        self.precast = Precast
        self.time_remaining = self.duration

class Debuff:
    def __init__(self,Debuff,Character,Constellation,Weapon,Rank,Artifact,method,Duration,Trigger):
        self.name = Debuff
        self.character = Character
        self.constellation = Constellation
        self.weapon = Weapon
        self.weapon_rank = Rank
        self.artifact = Artifact
        self.method = method
        self.duration = Duration
        self.trigger = Trigger
        self.time_remaining = self.duration

class StaticBuff:



    def skill_ratio_20pct(self,unit_obj):
        unit_obj.skill_ratio *= 1.2
    def skill_cdr_20pct(self,unit_obj):
        unit_obj.skill_CDR *= 0.8
    def burst_crit_rate_10pct(self,unit_obj):
        unit_obj.burst_crit_rate += 0.1
    def charged_ratio_20pct(self,unit_obj):
        unit_obj.charged_attack_ratio *= 1.2
    def skill_flat_200pct(self,unit_obj):
        unit_obj.skill_flat_ratio += 2
    def burst_level_plus_3(self,unit_obj):
        unit_obj.burst_level += 3
    def skill_level_plus_3(self,unit_obj):
        unit_obj.skill_level += 3
    def skill_cd_minus_20pct(self,unit_obj):
        unit_obj.skill_CDR *= 0.8
    def q_on_use_atk_pct_10pct(self,unit_obj):
        unit_obj.atk_pct += 0
    def burst_refund_15(self,unit_obj):
        unit_obj.burst_energy -= 15
    def skill_dmg_15pct(self,unit_obj):
        unit_obj.skill_dmg += 0.15
    def aimed_shot_dur_minus_60pct(self,unit_obj):
        unit_obj.charged_AT *= 0.4
    def skill_charges_plus_1(self,unit_obj):
        unit_obj.skill_charges += 1
    def q_on_use_200em(self,unit_obj):
        pass
    def electro_on_hit_self_22pct(self,unit_obj):
        pass
    def burst_flat_222pct(self,unit_obj):
        unit_obj.burst_flat_ratio += 2.22
    def electro_on_hit_30pct(self,unit_obj):
        pass
    def charged_cryo_res_15pct(self,unit_obj):
        pass
    def q_on_hit_15_pct(self,unit_obj):
        pass
    def skill_skip_charge(self,unit_obj):
        pass

    ## Weapons

    def amos_bow(self,unit_obj):
        unit_obj.normal_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03
        unit_obj.charged_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03
    
    def skyward_harp(self,unit_obj):
        unit_obj.crit_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def blackcliff(self,unit_obj):
        unit_obj.atk_pct += 0.12 + (unit_obj.weapon_rank-1)*0.03
    
    def rust(self,unit_obj):
        unit_obj.normal_dmg += 0.4 + (unit_obj.weapon_rank-1)*0.1
        unit_obj.charged_dmg -= 0.1

    def stringless(self,unit_obj):
        unit_obj.skill_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.6
        unit_obj.burst_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.6

    def sharpshooter(self,unit_obj):
        unit_obj.charged_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.6

    def slingshot(self,unit_obj):
        unit_obj.charged_dmg += 0.36 + (unit_obj.weapon_rank-1)*0.6

    def skyward_atlas(self,unit_obj):
        unit_obj.elemental_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03

    def wolfs_gravestone(self,unit_obj):
        unit_obj.atk_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def skyward_pride(self,unit_obj):
        unit_obj.all_dmg += 0.8 + (unit_obj.weapon_rank-1)*0.02

    def skyward_spine(self,unit_obj):
        unit_obj.crit_rate += 0.8 + (unit_obj.weapon_rank-1)*0.02

    def crescent_spine(self,unit_obj):
        unit_obj.phys_on_hit += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def deathmatch(self,unit_obj):
        unit_obj.atk_pct += 0.24 + (unit_obj.weapon_rank-1)*0.05 

    def white_tassel(self,unit_obj):
        unit_obj.normal_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.06

    def aquila_favonia(self,unit_obj):
        unit_obj.atk_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def skyward_blade(self,unit_obj):
        unit_obj.crit_rate += 0.04 + (unit_obj.weapon_rank-1)*0.01

    def black_sword(self,unit_obj):
        unit_obj.normal_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.charged_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def festering_desire(self,unit_obj):
        unit_obj.skill_crit_rate += 0.06 + (unit_obj.weapon_rank-1)*0.015
        unit_obj.skill_dmg += 0.16 + (unit_obj.weapon_rank-1)*0.04

class ActiveBuff:

    ## Characters ##

    def venti_infuse_15e_refund(self,unit_obj,sim):
        for unit in sim.units:
            if unit != unit_obj:
                if unit.element == sim.enemy.element:
                   unit.live_burst_energy = min(unit.live_burst_energy+15,unit.burst_energy)

    def atk_15pct(self,unit_obj,sim):
        unit_obj.live_atk_pct += 0.15
    def cryo_dmg_20pct(self,unit_obj,sim):
        unit_obj.live_cryo += 0.2
    def dmg_15pct(self,unit_obj,sim):
        unit_obj.live_all_dmg += 0.15
    def em_200(self,unit_obj,sim):
        unit_obj.live_elemental_mastery += 200
    def melee_pyro_15pct(self,unit_obj,sim):
        if unit_obj.weapon_type in ("Polearm,","Claymore","Sword"):
            unit_obj.live_pyro += 0.15
    def ben_q(self,unit_obj,sim):
        pass
    def ganyu_charged_reset(self,unit_obj,sim):
        unit_obj.live_charged_speed = 0
    def charged_speed_60pct(self,unit_obj,sim):
        pass
    def skill_cdr_50pct(self,unit_obj,sim):
        pass
    def stam_10pct(self,unit_obj,sim):
        unit_obj.live_stam_save += 0.1

    
    # Weapons

    def skyward_harp_2(self,unit_obj,sim):
        pass
        
    def compound_bow(self,unit_obj,sim):
        pass

    def viridescent_hunt(self,unit_obj,sim):
        pass

    def prototye_crescent(self,unit_obj,sim):
        unit_obj.live_charged_dmg += 0.36 + (unit_obj.weapon_rank-1)*0.09

    def favonius(self,unit_obj,sim):
        for unit in sim.units:
            if unit == sim.chosen_unit:
                unit.live_burst_energy = max( 6 * (1+unit.live_energy_recharge) + unit.live_burst_energy, unit.burst_energy)
            else:
                unit.live_burst_energy = max( 3.6 * (1+unit.live_energy_recharge) + unit.live_burst_energy, unit.burst_energy)
        for buff in unit_obj.triggerable_buffs:
            if buff.name == "Favonius":
                buff.cooldown = 12 - (unit_obj.weapon_rank-1)*1.5

    def sacrificial(self,unit_obj,sim):
        unit_obj.live_skill_CD = 0
        for buff in unit_obj.triggerable_buffs:
            if buff.name == "Sacrificial":
                buff.cooldown = 30 - (unit_obj.weapon_rank-1)*4
        
    def lost_prayers(self,unit_obj,sim):
        unit_obj.live_elemental_dmg += (0.04 * round(unit_obj.field_time/4)) * ( 1 + (unit_obj.weapon_rank-1)*0.25)

    # Unfinished
    def shield_weapons(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.04)*sim.chosen_action.hits

    def skyward_atlas_2(self,unit_obj,sim):
        pass

    def solar_pearl_normal_buff(self,unit_obj,sim):
        unit_obj.live_normal_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def solar_pearl_ability_buff(self,unit_obj,sim):
        unit_obj.live_skill_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.live_burst_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def eye_of_perception(self,unit_obj,sim):
        pass

    def widsith(self,unit_obj,sim):
        unit_obj.live_atk_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.live_elemental_dmg += 0.16 + (unit_obj.weapon_rank-1)*0.04
        unit_obj.live_elemental_mastery += 80 + (unit_obj.weapon_rank-1)*20

    def dragonspine_wep(self,unit_obj,sim):
        pass

    def prototye_amber(self,unit_obj,sim):
        pass

    def skuward_spine_2(self,unit_obj,sim):
        pass

    def primordial_spear(self,unit_obj,sim):
        pass

    def prototype_starglitter(self,unit_obj,sim):
        unit_obj.live_normal_dmg += 0.8 + (unit_obj.weapon_rank-1)*0.02

    def skyward_blade2(self,unit_obj,sim):
        unit_obj.live_normal_speed += 0.1
        pass

    def iron_sting(self,unit_obj,sim):
        unit_obj.live_all_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03
    

    # Artifacts
    def atk_20pct(self,unit_obj,sim):
        unit_obj.live_atk_pct += 0.2

    def pyro_7pct(self,unit_obj,sim):
        unit_obj.live_pyro += 0.075
    def lavawalker(self,unit_obj,sim):
        if sim.enemy.element == "Pyro":
            unit_obj.live_all_dmg += 0.35
    def thundersoother(self,unit_obj,sim):
        if sim.enemy.element == "Electro":
            unit_obj.live_all_dmg += 0.35
    def blizzard_strayer(self,unit_obj,sim):
        if sim.enemy.element == "Cryo":
            unit_obj.live_crit_rate += 0.2
        if sim.enemy.element == "Frozen":
            unit_obj.live_crit_rate += 0.2
    def archaic_petra(self,unit_obj,sim):
        pass

    def normal_charged_30pct(self,unit_obj,sim):
        unit_obj.live_normal_dmg += 0.3
        unit_obj.live_charged_dmg += 0.3
    
    def thundering_fury(self,unit_obj,sim):
        unit_obj.live_skill_CD -= max(0, unit_obj.live_skill_CD - 1)

class ActiveDebuff:
    def def_15pct(self,unit_obj,sim):
        unit_obj.defence_debuff += 0.15

    # Artifact
    def infused_40pct(self,unit_obj,sim):
        if sim.enemy.element != "None":
            setattr(sim.enemy, getattr(sim.enemy,"element").lower() + "_res_debuff", getattr(sim.enemy,(getattr(sim.enemy,"element").lower() +"_res_debuff")) + 0.4)

