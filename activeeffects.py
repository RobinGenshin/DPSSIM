import read_data
debuffdict = read_data.read_debuff_data()
from action import WeaponAction

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

    def skyward_harp2(self,unit_obj,sim):
        totatk = unit_obj.base_atk * ( 1 + unit_obj.live_atk_pct ) + unit_obj.live_flat_atk
        crit = 1 + unit_obj.live_crit_dmg * unit_obj.live_crit_rate
        dmg_bon = 1 + unit_obj.live_physical + unit_obj.live_all_dmg
        res = sim.enemy.live_physical_res
        defence = ( 100 + unit_obj.level ) / ( 100 +unit_obj.level + sim.enemy.live_defence )
        damage = totatk * crit * dmg_bon * (1 - res) * defence
        sim.damage += damage
        
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

    # Artifact
    def infused_40pct(self,unit_obj,sim):
        if sim.enemy.element not in {"None","Geo","Anemo"}:
            if sim.enemy.element == "Pyro":
                sim.enemy.active_debuffs["VV_Pyro"] = debuffdict["VV_Pyro"]
            if sim.enemy.element == "Hydro":
                sim.enemy.active_debuffs["VV_Hydro"] = debuffdict["VV_Pyro"]
            if sim.enemy.element == "Electro":
                sim.enemy.active_debuffs["VV_Electro"] = debuffdict["VV_Pyro"]
            if sim.enemy.element == "Cryo":
                sim.enemy.active_debuffs["VV_Cryo"] = debuffdict["VV_Pyro"]
            print(sim.chosen_unit.name + " reduced enemy " + sim.enemy.element + " RES with VV")

class ActiveDebuff:
    def def_15pct(self,unit_obj,sim):
        unit_obj.defence_debuff += 0.15

    def vv_cryo_40pct(self,unit_obj,sim):
        sim.enemy.cryo_res_debuff += 0.4
    
    def vv_hydro_40pct(self,unit_obj,sim):
        sim.enemy.hydro_res_debuff += 0.4

    def vv_pyro_40pct(self,unit_obj,sim):
        sim.enemy.pyro_res_debuff += 0.4

    def vv_electro_40pct(self,unit_obj,sim):
        sim.enemy.electro_res_debuff += 0.4