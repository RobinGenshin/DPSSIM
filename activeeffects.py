import read_data
debuffdict = read_data.read_debuff_data()
buffdict = read_data.read_buff_data()
from action import WeaponAction
from action import AlbedoTrigger
import copy

class ActiveBuff:

    ## Characters ##

    def albedo_e(self,unit_obj,sim):
        for unit in sim.units:
            unit.triggerable_buffs["Albedo_E_Trigger"] = copy.deepcopy(buffdict["Albedo_E_trigger"])
        
    def albedo_e_trigger(self,unit_obj,sim):
        for unit in sim.units:
            if unit.name == "Albedo":
                action = AlbedoTrigger(unit, sim.enemy)
        x = sim.time_into_turn
        action.tick_times = [y+x for y in action.tick_times]
        action.energy_times = [y+x+1.6 for y in action.energy_times]
        sim.floating_actions_damage.add(action)
        print("#" + str(sim.action_order) + " " + str(round((sim.encounter_duration + sim.time_into_turn),2)) + " Albedo E PROC")
        for unit in sim.units:
            unit.triggerable_buffs["Albedo_E_Trigger"].live_cd = 2

    def albedo_a4(self,unit_obj,sim):
        unit_obj.live_elemental_mastery += 120

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

    # Bows

    def skyward_harp2(self,unit_obj,sim):
        skyward_harp = WeaponAction(unit_obj,sim.enemy)
        skyward_harp.ticks = 1
        skyward_harp.tick_damage = [1.25]
        skyward_harp.tick_times = [0.5+sim.time_into_turn]
        skyward_harp.tick_units = [0]
        skyward_harp.tick_used = ["no"]
        skyward_harp.initial_time = max(skyward_harp.tick_times)
        skyward_harp.time_remaining = skyward_harp.initial_time
        unit_obj.triggerable_buffs["Skyward Harp 2"].live_cd = 4 - ((unit_obj.weapon_rank-1)*0.5)
        sim.floating_actions_damage.add(skyward_harp)
        print(unit_obj.name + " proced Skyward Harp")
        
    def compound_bow2(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.04 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Compound Bow 2"].stacks
        unit_obj.live_normal_speed += (0.012 + (unit_obj.weapon_rank-1)*0.003) * unit_obj.active_buffs["Compound Bow 2"].stacks
        unit_obj.triggerable_buffs["Compound Bow 2"].live_cd = 0.3

    def viridescent_hunt2(self,unit_obj,sim):
        viri_hunt = WeaponAction(unit_obj,sim.enemy)
        viri_hunt.ticks = 8
        t = (unit_obj.weapon_rank-1)*0.25 + 1
        s = sim.time_into_turn
        viri_hunt.tick_damage = [0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t]
        viri_hunt.tick_times = [0.5+s,1+s,1.5+s,2+s,2.5+s,3+s,3.5+s,4+s,]
        viri_hunt.tick_units = [0,0,0,0,0,0,0,0]
        viri_hunt.tick_used = ["no","no","no","no","no","no","no","no"]
        viri_hunt.initial_time = max(viri_hunt.tick_times)
        viri_hunt.time_remaining = viri_hunt.initial_time
        unit_obj.triggerable_buffs["The Viridescent Hunt 2"].live_cd = 14 - ((unit_obj.weapon_rank-1))
        sim.floating_actions_damage.add(viri_hunt)
        print(unit_obj.name + " proced Skyward Harp")

    def prototype_crescent2(self,unit_obj,sim):
        unit_obj.live_charged_dmg += 0.36 + (unit_obj.weapon_rank-1)*0.09

    # Claymores

    def prototype_archaic2(self,unit_obj,sim):
        archaic = WeaponAction(unit_obj,sim.enemy)
        archaic.ticks = 1
        d = 2.4 + (unit_obj.weapon_rank-1)*0.6
        archaic.tick_damage = [d]
        archaic.tick_times = [0.5+sim.time_into_turn]
        archaic.tick_units = [0]
        archaic.tick_used = ["no"]
        archaic.initial_time = max(archaic.tick_times)
        archaic.time_remaining = archaic.initial_time
        unit_obj.triggerable_buffs["Prototype Archaic 2"].live_cd = 15
        sim.floating_actions_damage.add(archaic)

    def wolfs_gravestone2(self,unit_obj,sim):
        for unit in sim.units:
            unit.live_atk_pct += 0.4 + (unit_obj.weapon_rank-1)*0.1
        unit_obj.triggerable_buffs["Wolf's Gravestone 2"].live_cd = 30

    def rainslasher2(self,unit_obj,sim):
        if sim.enemy.element == "Hydro" or sim.enemy.element == "Electro":
            unit_obj.live_cond_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def whiteblind2(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.06 + (unit_obj.weapon_rank-1)*0.015) * unit_obj.active_buffs["Whiteblind 2"].stacks
        unit_obj.live_def_pct += (0.06 + (unit_obj.weapon_rank-1)*0.015) * unit_obj.active_buffs["Whiteblind 2"].stacks
        unit_obj.triggerable_buffs["Whiteblind 2"].live_cd = 0.5

    def skyrider2(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.06 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Whiteblind 2"].stacks
        unit_obj.triggerable_buffs["Skyrider 2"].live_cd = 0.5

    def serpent2(self,unit_obj,sim):
        pass

    def skyward_pride2(self,unit_obj,sim):
        unit_obj.triggerable_buffs["Skyward Pride 3"] = copy.deepcopy(buffdict["Skyward Pride 3"])
        unit_obj.triggerable_buffs["Skyward Pride 3"].time_remaining = 20
        unit_obj.triggerable_buffs["Skyward Pride 3"].stacks = 8

    def skyward_pride3(self,unit_obj,sim):
        sp = WeaponAction(unit_obj,sim.enemy)
        sp.ticks = 6
        d = (unit_obj.weapon_rank-1)*0.2 + 0.8
        s = sim.time_into_turn
        sp.tick_damage = [d]
        sp.tick_times = [0.1+s]
        sp.tick_units = [0]
        sp.tick_used = ["no"]
        sp.initial_time = max(sp.tick_times)
        sp.time_remaining = sp.initial_time
        sim.floating_actions_damage.add(sp)
        unit_obj.triggerable_buffs["Skyward Pride 3"].stacks -= 1

    #Catalysts

    def lost_prayers2(self,unit_obj,sim):
        unit_obj.live_elemental_dmg += (0.04 * round(unit_obj.field_time/4)) * ( 1 + (unit_obj.weapon_rank-1)*0.25) 

    def skyward_atlas2(self,unit_obj,sim):
        atlas = WeaponAction(unit_obj,sim.enemy)
        atlas.ticks = 6
        d = (unit_obj.weapon_rank-1)*0.4 + 1.6
        s = sim.time_into_turn
        atlas.tick_damage = [d,d,d,d,d,d]
        atlas.tick_times = [2.5+s,5+s,7.5+s,10+s,12.5+s,15+s]
        atlas.tick_units = [0,0,0,0,0,0]
        atlas.tick_used = ["no","no","no","no","no","no"]
        atlas.initial_time = max(atlas.tick_times)
        atlas.time_remaining = atlas.initial_time
        unit_obj.triggerable_buffs["Skyward Atlas 2"].live_cd = 30
        sim.floating_actions_damage.add(atlas)

    def solar_pearl_normal_buff2(self,unit_obj,sim):
        unit_obj.live_normal_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def solar_pearl_ability_buff2(self,unit_obj,sim):
        unit_obj.live_skill_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.live_burst_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def eye_of_perception2(self,unit_obj,sim):
        eop = WeaponAction(unit_obj,sim.enemy)
        eop.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.3 + 2.4
        s = sim.time_into_turn
        eop.tick_damage = [d]
        eop.tick_times = [0.1+s]
        eop.tick_units = [0]
        eop.tick_used = ["no"]
        eop.initial_time = max(eop.tick_times)
        eop.time_remaining = eop.initial_time
        unit_obj.triggerable_buffs["Eye of Perception 2"].live_cd = 12 - (unit_obj.weapon_rank-1)
        sim.floating_actions_damage.add(eop)

    def widsith2(self,unit_obj,sim):
        unit_obj.live_atk_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.live_elemental_dmg += 0.16 + (unit_obj.weapon_rank-1)*0.04
        unit_obj.live_elemental_mastery += 80 + (unit_obj.weapon_rank-1)*20

    def prototype_amber2(self,unit_obj,sim):
        energy_gain = ( 4 + (unit_obj.weapon_rank-1)*0.5 ) * 3
        for unit in sim.units:
            unit.live_burst_energy = min(unit.burst_energy, unit.live_burst_energy + energy_gain)

    def mappa_marre2(self,unit_obj,sim):
        unit_obj.live_all_dmg += (0.08 + (unit_obj.weapon_rank-1)*0.02) * unit_obj.active_buffs["Mappa Marre 2"].stacks

    # Polearms

    def skyward_spine2(self,unit_obj,sim):
        skyward_spine = WeaponAction(unit_obj,sim.enemy)
        skyward_spine.ticks = 1
        d = 0.4 + (unit_obj.weapon_rank-1)*0.1
        skyward_spine.tick_damage = [d]
        skyward_spine.tick_times = [0.1+sim.time_into_turn]
        skyward_spine.tick_units = [0]
        skyward_spine.tick_used = ["no"]
        skyward_spine.initial_time = max(skyward_spine.tick_times)
        skyward_spine.time_remaining = skyward_spine.initial_time
        unit_obj.triggerable_buffs["Skyward Spine 2"].live_cd = 2
        sim.floating_actions_damage.add(skyward_spine)

    def lithic_spear2(self,unit_obj,sim):
        pass

    def primordial_spear2(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.032 + (unit_obj.weapon_rank-1)*0.007) * unit_obj.active_buffs["Prim Spear 2"].stacks
        if unit_obj.active_buffs["Prim Spear 2"].stacks == 7:
            unit_obj.live_all_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.06
        unit_obj.triggerable_buffs["Prim Spear 2"].live_cd = 0.5

    def prototype_starglitter2(self,unit_obj,sim):
        unit_obj.live_normal_dmg += (0.08 + (unit_obj.weapon_rank-1)*0.02) * unit_obj.active_buffs["Prototype Starglitter 2"].stacks

    def crescent_spine2(self,unit_obj,sim):
        cres = WeaponAction(unit_obj,sim.enemy)
        cres.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.05 + 0.2
        s = sim.time_into_turn
        cres.tick_damage = [d]
        cres.tick_times = [0.1+s]
        cres.tick_units = [0]
        cres.tick_used = ["no"]
        cres.initial_time = max(cres.tick_times)
        cres.time_remaining = cres.initial_time
        sim.floating_actions_damage.add(cres)

    # Swords

    def lions_roar2(self,unit_obj,sim):
        if sim.enemy.element == "Pyro" or sim.enemy.element == "Electro":
            unit_obj.live_cond_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def aquila_favonia2(self,unit_obj,sim):
        aq = WeaponAction(unit_obj,sim.enemy)
        aq.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.3 + 2
        s = sim.time_into_turn
        aq.tick_damage = [d]
        aq.tick_times = [0.1+s]
        aq.tick_units = [0]
        aq.tick_used = ["no"]
        aq.initial_time = max(aq.tick_times)
        aq.time_remaining = aq.initial_time
        unit_obj.triggerable_buffs["Aquila Favonia 2"].live_cd = 15
        sim.floating_actions_damage.add(aq)

    def prototype_rancour2(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.04 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Rancour 2"].stacks
        unit_obj.live_def_pct += (0.04 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Rancour 2"].stacks
        unit_obj.triggerable_buffs["Rancour 2"].live_cd = 0.5

    def skyward_blade2(self,unit_obj,sim):
        unit_obj.live_normal_speed += 0.1
        unit_obj.triggerable_buffs["Skyward Blade 3"] = copy.deepcopy(buffdict["Skyward Blade 3"])
        unit_obj.triggerable_buffs["Skyward Blade 3"].time_remaining = 12

    def skyward_blade3(self,unit_obj,sim):
        sb = WeaponAction(unit_obj,sim.enemy)
        sb.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.05 + 0.2
        s = sim.time_into_turn
        sb.tick_damage = [d]
        sb.tick_times = [0.1+s]
        sb.tick_units = [0]
        sb.tick_used = ["no"]
        sb.initial_time = max(sb.tick_times)
        sb.time_remaining = sb.initial_time
        sim.floating_actions_damage.add(sb)

    def the_flute2(self,unit_obj,sim):
        tf = WeaponAction(unit_obj,sim.enemy)
        tf.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.05 + 0.2
        s = sim.time_into_turn
        tf.tick_damage = [d]
        tf.tick_times = [0.1+s]
        tf.tick_units = [0]
        tf.tick_used = ["no"]
        tf.initial_time = max(tf.tick_times)
        tf.time_remaining = tf.initial_time
        sim.floating_actions_damage.add(tf)
        unit_obj.triggerable_buffs["Flute 2"].live_cd = 0.5

    def iron_sting2(self,unit_obj,sim):
        unit_obj.live_all_dmg += (0.06 + (unit_obj.weapon_rank-1)*0.015) * unit_obj.active_buffs["Iron Sting 2"].stacks

    # Misc

    def favonius(self,unit_obj,sim):
        for unit in sim.units:
            if unit == sim.chosen_unit:
                unit.live_burst_energy = max( 6 * (1+unit.live_energy_recharge) + unit.live_burst_energy, unit.burst_energy)
            else:
                unit.live_burst_energy = max( 3.6 * (1+unit.live_energy_recharge) + unit.live_burst_energy, unit.burst_energy)
        unit_obj.triggerable_buffs["Favonius"].live_cd = 14 - ((unit_obj.weapon_rank-1))
        print(unit_obj.name + "proced favonius")

    def sacrificial(self,unit_obj,sim):
        unit_obj.live_skill_CD = 0 
        unit_obj.triggerable_buffs["Sacrificial"].live_cd = 30 - ((unit_obj.weapon_rank-1))*4
        
    def geo_weapons(self,unit_obj,sim):
        unit_obj.live_atk_pct += (0.08 + (unit_obj.weapon_rank-1)*0.02) * unit_obj.active_buffs["Geo Weapon"].stacks
        unit_obj.triggerable_buffs["Geo Weapon"].live_cd = 0.3

    def dragonspine(self,unit_obj,sim):
        dragonspine = WeaponAction(unit_obj,sim.enemy)
        dragonspine.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.15 + 0.8
        s = sim.time_into_turn
        if sim.enemy.element == "Cryo":
            d *= 2.5
        dragonspine.tick_damage = [d]
        dragonspine.tick_times = [0.1+s]
        dragonspine.tick_units = [0]
        dragonspine.tick_used = ["no"]
        dragonspine.initial_time = 0.5+s
        dragonspine.time_remaining = dragonspine.initial_time
        unit_obj.triggerable_buffs["Dragonspine"].live_cd = 10
        sim.floating_actions_damage.add(dragonspine)
        print("Dragonspine effect")
    

    # Artifacts

    def noblesse(self,unit_obj,sim):
        unit_obj.live_atk_pct += 0.2

    def crimson_witch(self,unit_obj,sim):
        unit_obj.live_pyro += 0.075 * unit_obj.active_buffs["Crimson Witch"].stacks

    def lavawalker(self,unit_obj,sim):
        if sim.enemy.element == "Pyro":
            unit_obj.live_cond_dmg += 0.35

    def thundersoother(self,unit_obj,sim):
        if sim.enemy.element == "Electro":
            unit_obj.live_cond_dmg += 0.35

    def blizzard_strayer(self,unit_obj,sim):
        if sim.enemy.element == "Cryo":
            unit_obj.live_crit_rate += 0.2
        if sim.enemy.frozen == "Frozen":
            unit_obj.live_crit_rate += 0.2

    def archaic_petra(self,unit_obj,sim):
        pass

    def heart_of_depth(self,unit_obj,sim):
        unit_obj.live_normal_dmg += 0.3
        unit_obj.live_charged_dmg += 0.3
    
    def thundering_fury(self,unit_obj,sim):
        unit_obj.live_skill_CD -= max(0, unit_obj.live_skill_CD - 1)

    def viridescent_venerer(self,unit_obj,sim):
        if sim.enemy.element not in {"None","Geo","Anemo"}:
            if sim.enemy.element == "Pyro":
                sim.enemy.active_debuffs["VV_Pyro"] = debuffdict["VV_Pyro"]
            if sim.enemy.element == "Hydro":
                sim.enemy.active_debuffs["VV_Hydro"] = debuffdict["VV_Hydro"]
            if sim.enemy.element == "Electro":
                sim.enemy.active_debuffs["VV_Electro"] = debuffdict["VV_Electro"]
            if sim.enemy.element == "Cryo":
                sim.enemy.active_debuffs["VV_Cryo"] = debuffdict["VV_Cryo"]
            sim.enemy.update_stats()
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