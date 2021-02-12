import read_data
debuffdict = read_data.debuff_dict
buffdict = read_data.buff_dict
chardict = read_data.character_dict
eleratiodict = read_data.ele_ratio_dict
razorqasdict = read_data.razor_qas_ratio_dict
physdict = read_data.phys_ratio_dict
from action import Action
from action import WeaponAction
from action import AlbedoTrigger
from action import TartagliaC4
from action import XinyanQ
from action import ZhongliA4
from action import ComboAction
from scaling import ratio_type
import copy
import math


## Explanation ##
## Share-type buffs are given to all units when triggered 
## Some share type buffs need a specific trigger and are linked to a trigger buff 
## i.e. Wolf's Gravestone has a trigger buff which gives everyone an active buff for pct_atk
## Active buffs are checked during the sim at different times depending on their trigger
## Static buffs are simply applied over a duration to respective units


class ActiveBuff:
    
    ################
    ## Characters ##
    ################

    ############
    ## Albedo ##
    ############

    ## Albedo E Cast ## Instant ## Postcast ##
    def albedo_e_cast(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.triggerable_buffs["Albedo_E_Trigger"] = copy.deepcopy(buffdict["Albedo_E_Trigger"])
            unit.triggerable_buffs["Albedo_E_Trigger"].time_remaining = 30

    ## Albedo E Trigger ## Instant ## Onhit ##
    def albedo_e_trigger(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Albedo":
                action = AlbedoTrigger(unit,sim.enemy,sim)
                x = sim.time_into_turn
                action.tick_times = [y+x for y in action.tick_times]
                action.energy_times = [y+x for y in action.energy_times]
                energy_copy = copy.deepcopy(action)
                energy_copy.action_type = "energy"
                sim.floating_actions.add(action)
                sim.floating_actions.add(energy_copy)
                # print("Triggered Transient Blossom")

        for unit in sim.units:
            unit.triggerable_buffs["Albedo_E_Trigger"].live_cd = 2

        ## Albedo C1 ##
        for unit in sim.units:
            if unit.name == "Albedo" and unit.constellation >= 1:
                unit.current_energy += 1.2

        ## Albedo C2 Stacks ##
        for unit in sim.units:
            if unit.name == "Albedo":
                if hasattr(unit, "c2_stacks"):
                    unit.c2_stacks = min(4,unit.c2_stacks+1)
                else:
                    unit.c2_stacks = 1

    ## Albedo A4 ## Duration ## Postcast ##
    def albedo_a4(self,unit_obj,sim,extra):
        unit_obj.live_ele_m += 120

    ## Albedo C2 Proc ## Duration ## Postcast ##
    def albedo_c2(self,unit_obj,sim,extra):
        if hasattr(unit_obj, "c2_stacks"):
            d = unit_obj.c2_stacks
        else:
            d = 0

        action = AlbedoTrigger(unit_obj, sim.enemy, sim)
        action.name = "Albedo C2"
        action.tick_times = copy.deepcopy(chardict["Albedo"].burst_tick_times)
        action.tick_damage = copy.deepcopy(chardict["Albedo"].burst_tick_damage)
        action.tick_units = copy.deepcopy(chardict["Albedo"].burst_tick_units)
        action.scaling = 1

        action.ticks = 8
        action.tick_types = ["burst"]*8
        action.tick_times = [x+0.1 for x in action.tick_times]
        action.tick_damage = [0.3*d for x in action.tick_damage]
        action.tick_units = [0 for x in action.tick_units]
        action.tick_used = ["no"]*8
        action.update_time()

        sim.floating_actions.add(action)

    ## Albedo C4 ## Duration ## Postcast
    def albedo_c4(self,unit_obj,sim,extra):
        unit_obj.live_plunge_dmg += 0.3

    ## Albedo C6 ## Duration ##
    def albedo_c6(self,unit_obj,sim,extra):
        unit_obj.live_all_dmg += 0.17


    ###########
    ## Amber ##
    ###########
    
    ## Amber A4 ## Duration ## Onhit ## Charged ##
    def amber_a4(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += 0.15

    ## Amber C2 ## Instant ## Onhit ## Charged ##
    def amber_c2(self,unit_obj,sim,extra):
        for action in copy.deepcopy(sim.floating_actions):
            if action.unit.name == unit_obj.name and action.type == "skill" and action.action_type == "damage":
                if action.time_remaining > sim.time_into_turn:
                    flat_dmg = Action(unit_obj,"skill")

                    flat_dmg.tick_times = [sim.time_into_turn]
                    flat_dmg.tick_damage = [2]
                    flat_dmg.tick_units = [0]
                    flat_dmg.scaling = [1]

                    flat_dmg.update_time()
                    sim.floating_actions.add(flat_dmg)
                    unit_obj.triggerable_buffs["Amber_C2"].live_cd = 5

                    print("BOOM!")
                    action.tick_times = [sim.time_into_turn]
                    action.energy_times = [sim.time_into_turn+2]
        
    ## Amber C6 ## Duration ## Postcast ## Burst
    def amber_c6(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += 0.15


    #############
    ## Barbara ##
    #############

    ## Barbara A2 ## Duration ## Postcast ## Skill
    def barbara_a2(self,unit_obj,sim,extra):
        unit_obj.live_stam_save += sim.turn_time
        
        ## Barbara C2 ##
        for unit in sim.units:
            if unit.name == "Barbara" and unit.constellation >=2:
                unit.live_hydro_dmg += 0.15

    ## Barbara A4_1 ## Instant ## Postcast ## Skill
    def barbara_a4_1(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.triggerable_buffs["Barbara_A4_2"] = copy.deepcopy(buffdict["Barbara_A4_2"])
            unit.triggerable_buffs["Barbara_A4_2"].time_remaining = 15

    ## Barbara A4_2 ## Instant ## Particle ##
    def barbara_a4_2(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Barbara":
                if hasattr(unit, "a4_stacks") == False:
                    unit.a4_stacks = 1
                    for unit in sim.units:
                        unit.active_buffs["Barbara_A2"].time_remaining += 1
                        unit.triggerable_buffs["Barbara_A4_2"].time_remaining += 1
                elif hasattr(unit, "a4_stacks") == True:
                    if unit.a4_stacks == 5:
                        pass
                    else:
                        unit.a4_stacks += 1
                        unit.active_buffs["Barbara_A2"].time_remaining += 1
                        unit.triggerable_buffs["Barbara_A4_2"].time_remaining += 1

    ## Barbara C1 ## Instant ## Any
    def barbara_c1(self,unit_obj,sim,extra):
        unit_obj.current_energy += 1
        unit_obj.triggerable_buffs["Barbara_C1"].live_cd = 10

    ## Barbara C4 ## Instant ## Onhit ## Charged
    def barbara_c4(self,unit_obj,sim,extra):
        unit_obj.current_energy += 1


    ############
    ## Beidou ##
    ############

    ## Beidou Q Cast ## Instant ## Postcast ## Burst
    def beidou_q_cast(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.triggerable_buffs["Beidou_Q_Trigger"] = copy.deepcopy(buffdict["Beidou_Q_Trigger"])
            unit.triggerable_buffs["Beidou_Q_Trigger"].time_remaining = 15
    
    ## Beidou Q Trigger ## Instant ## Onhit ## Normal, Charged
    def beidou_q_trigger(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Beidou":
                action = Action(unit,"burst")

                action.name = "Beidou Q Proc"
                action.ticks = 1
                action.tick_times = [sim.time_into_turn+0.1]
                action.tick_damage = [0.96]
                action.tick_units = [1]
                sim.floating_actions.add(action)
                action.update_time()

        for unit in sim.units:
            unit.triggerable_buffs["Beidou_Q_Trigger"].live_cd = 1

    ## Beidou A4 ## Duration ## Postcast ## Skill
    def beidou_a4(self,unit_obj,sim,extra):
        unit_obj.live_normal_dmg += 0.15
        unit_obj.live_charged_dmg += 0.15
        unit_obj.live_normal_speed += 0.15
        unit_obj.live_charged_speed += 0.15

    ## Beidou C4 ## Duration ## Midhit ## Normal
    def beidou_c4(self,unit_obj,sim,action):
        if action[0].proc_type == "No":
            convertedpct = ComboAction(unit_obj,action[0].combo)
            convertedpct.ticks = 1
            convertedpct.name = "Beidou C4"
            convertedpct.element = ["Electro"]
            convertedpct.scaling = [1]
            convertedpct.tick_types = [convertedpct.tick_types[action[1]]]
            convertedpct.tick_times = [sim.time_into_turn]
            convertedpct.tick_damage = [0.2]
            convertedpct.tick_units = [0]
            convertedpct.tick_used = ["no"]
            convertedpct.tick_units = [1]
            convertedpct.proc_type = "Yes"
            convertedpct.update_time()

            sim.floating_actions.add(convertedpct)
            print("Proced Beidou C4")

    #############
    ## Bennett ##
    #############

    ## Bennett Q Cast ## Instant ## Precast ## Burst
    def bennett_q_cast(self,unit_obj,sim,extra):
        atk_mult = eleratiodict[unit_obj.burst_level] * 0.56

        ## Bennett C1 ##
        if unit_obj.constellation >= 1:
            atk_mult += 0.2

        snapshot = atk_mult * copy.deepcopy(unit_obj.base_atk)
        unit_obj.snapshot_buff = snapshot
        for unit in sim.units:
            unit.active_buffs["Bennett_Q_Buff"] = copy.deepcopy(buffdict["Bennett_Q_Buff"])

    ## Bennett Q Buff ## Duration ## 
    def bennett_q_buff(self,unit_obj,sim,extra):
        atk_buff = 0
        for unit in sim.units:
            if unit.name == "Bennett":
                atk_buff = unit.snapshot_buff
        if unit_obj != sim.chosen_unit:
            atk_buff = 0
        unit_obj.live_flat_atk += atk_buff

        if unit_obj.name == "Bennett":
            unit_obj.live_skill_cdr *= 0.5

    ## Bennett C4 ## 
    def bennett_c4(self,unit_obj,sim,extra):
        pass

    ## Bennett C6 ## Duration ## Postcast ## Burst
    def bennett_c6(self,unit_obj,sim,extra):
        if unit_obj.weapon_type in {"Claymore", "Polearm", "Sword"}:
            unit_obj.live_pyro_dmg += 0.15
            unit_obj.live_normal_type = "Pyro"
            unit_obj.live_charged_type = "Pyro"

    ##############
    ## Chongyun ##
    ##############

    ## Chongyun E ##
    def chongyun_e(self,unit_obj,sim,extra):
        unit_obj.live_normal_type = "Cryo"
        unit_obj.live_charged_type = "Cryo"

    ## Chongyun A2 ## Duration ## Postcast ## Skill
    def chongyun_a2(self,unit_obj,sim,extra):
        unit_obj.live_normal_speed += 0.08

    ## Chongyun C1 ## Instant ## Midhit ## Normal
    def chongyun_c1(self,unit_obj,sim,tick):
        if tick == 3:
            proc = Action(unit_obj,"normal")
            proc.element = "Cryo"
            proc.tick_times = [sim.time_into_turn + 0.5, sim.time_into_turn + 0.6, sim.time_into_turn + 0.7]
            proc.tick_damage = [0.5,0.5,0.5]
            proc.tick_units = [1,0,0]
            proc.ticks = 3
            proc.scaling = 1
            sim.floating_actions.add(proc)

    ## Chongyun C2 ## Duration ## Postcast ## Skill
    def chongyun_c2(self,unit_obj,sim,extra):
        unit_obj.live_skill_cdr *= 0.85
        unit_obj.live_burst_cdr *= 0.85

    ## Chongyun C4 ## Instant ## Onhit ## Any
    def chongyun_c4(self,unit_obj,sim,extra):
        if sim.enemy.element == "Cryo":
            unit_obj.live_burst_energy_cost += 1
            unit_obj.triggerable_buffs["Chongyun_C4"].live_cd = 2

    ###########
    ## Diluc ##
    ###########

    ## Diluc E ## Duration ## Precast
    def diluc_e(self,unit_obj,sim,extra):

        if hasattr(unit_obj,"e_stacks") == False:
            unit_obj.e_stacks = 0

        if unit_obj.e_stacks == 0:
            unit_obj.start_time = sim.encounter_duration
            unit_obj.e_stacks = 1
            unit_obj.current_skill_cd = 0

        if "Diluc_E_2" in unit_obj.triggerable_buffs:
            unit_obj.live_tick_times = [0.367]
            unit_obj.live_skill_tick_damage = [0.976]
            unit_obj.live_skill_cancel = [0.5]
            unit_obj.live_skill_burst = [1.2]
            unit_obj.live_skill_swap = [0.617]
            unit_obj.live_skill_attack = [0.633]
            unit_obj.current_skill_cd = 0

        elif "Diluc_E_3" in unit_obj.triggerable_buffs:
            unit_obj.live_tick_times = [0.383]
            unit_obj.live_skill_tick_damage = [1.288]
            unit_obj.live_skill_cancel = [0.7]
            unit_obj.live_skill_burst = [1.067]
            unit_obj.live_skill_swap = [1.100]
            unit_obj.live_skill_attack = [0.833]
            unit_obj.current_skill_cd = 0
        else:
            if unit_obj.e_stacks != 1:
                unit_obj.current_skill_cd = unit_obj.live_skill_cd - (sim.encounter_duration - unit_obj.start_time)
                unit_obj.active_buffs.pop("Diluc_E")

    def diluc_e_1(self,unit_obj,sim,extra):
        if unit_obj.e_stacks == 1:
            unit_obj.triggerable_buffs["Diluc_E_2"] = copy.deepcopy(buffdict["Diluc_E_2"])
            unit_obj.triggerable_buffs["Diluc_E_2"].time_remaining = 3
            unit_obj.triggerable_buffs["Diluc_E_1"].live_cd = unit_obj.live_skill_cd
            unit_obj.e_stacks = 2

    def diluc_e_2(self,unit_obj,sim,extra):
        if unit_obj.e_stacks == 2:
            unit_obj.triggerable_buffs["Diluc_E_3"] = copy.deepcopy(buffdict["Diluc_E_3"])
            unit_obj.triggerable_buffs["Diluc_E_3"].time_remaining = 3
            unit_obj.triggerable_buffs.pop("Diluc_E_2")
            unit_obj.e_stacks = 3

    def diluc_e_3(self,unit_obj,sim,extra):
        if unit_obj.e_stacks == 3:
            unit_obj.e_stacks = 0
            unit_obj.triggerable_buffs.pop("Diluc_E_3")
            unit_obj.current_skill_cd = unit_obj.live_skill_cd - (sim.encounter_duration - unit_obj.start_time)
            unit_obj.active_buffs.pop("Diluc_E")


    ## Diluc Q ## Duration ## Postcast ## Burst
    def diluc_q(self,unit_obj,sim,extra):
        unit_obj.live_normal_type = "Pyro"
        unit_obj.live_charged_type = "Pyro"
        unit_obj.live_pyro_dmg += 0.2

    ## Diluc C2 ## Duration ## Any
    def diluc_c2(self,unit_obj,sim,extra):
        pass

    ## Diluc C4 1 ## Duration ## Onhit ## Skill
    def diluc_c4_1(self,unit_obj,sim,extra):
        unit_obj.active_buffs["Diluc_C4_2"] = copy.deepcopy(buffdict["Diluc_C4_2"])
        unit_obj.active_buffs["Diluc_C4_3"] = copy.deepcopy(buffdict["Diluc_C4_3"])

    ## Diluc C4 2 ## Duration ##
    def diluc_c4_2(self,unit_obj,sim,extra):
        unit_obj.live_skill_dmg -= 0.4
                                            ## All this was done to give Diluc a skill buff but only for 2s after NOT using his skill
    ## Diluc C4 3 ## Duration ##
    def diluc_c4_3(self,unit_obj,sim,extra):
        unit_obj.live_skill_dmg += 0.4

    ## Diluc C6 ## Duration ## Postcast # Burst
    def diluc_c6_1(self,unit_obj,sim,extra):
        unit_obj.triggerable_buffs["Diluc_C6_2"] = copy.deepcopy(buffdict["Diluc_C6_2"])
        unit_obj.triggerable_buffs["Diluc_C6_2"].time_remaining = 6

        if hasattr(unit_obj,"c6_stacks") == False:
            unit_obj.stacks = 2
        else:
            unit_obj.c6_stacks = 2

        if unit_obj.stacks > 0:
            unit_obj.live_normal_speed += 0.3
            unit_obj.live_normal_dmg += 0.3

    def diluc_c6_2(self,unit_obj,sim,extra):
        unit_obj.c6_stacks -= 1
        if unit_obj.c6_stacks <= 0:
            unit_obj.active_buffs.pop("Diluc_C6_1")
            unit_obj.triggerable_buffs.pop("Diluc_C6_2")


    ###########
    ## Diona ##
    ###########

    ## Diona A2 ## Duration ## Postcast ## Skill
    def diona_a2(self,unit_obj,sim,extra):
        unit_obj.live_stam_save += 0.1

    ## Diona C1 ## Instant ## Postcast ## Burst
    def diona_c1(self,unit_obj,sim,extra):
        unit_obj.current_energy += 15

    ## Diona C4 ## Duration ## Postcast ## Burst
    def diona_c4(self,unit_obj,sim,extra):
        unit_obj.live_charged_speed += 0.6

    ## Diona C6 ## Duration ## Postcast ## Burst
    def diona_c6(self,unit_obj,sim,extra):
        unit_obj.live_ele_m += 200


    ############
    ## Fischl ##
    ############

    ## Fischl E ## Instant ## Postcast ## Skill
    def fischl_e(self,unit_obj,sim,extra):
        unit_obj.current_burst_cd = max(12,unit_obj.live_skill_cd)
    
    ## Fischl Q ## Instant ## Postcast ## Burst
    def fischl_q_1(self,unit_obj,sim,extra):
        unit_obj.current_skill_cd = max(12,unit_obj.live_burst_CD)

    ## Fischl Q 2 ## Instant ## Postcast ## Burst
    def fischl_q_2(self,unit_obj,sim,extra):
        action = Action(unit_obj,"skill")

        action.tick_times = [x+2 for x in action.tick_times].pop()
        action.energy_times = [x+3.6 for x in action.tick_times].pop()
        action.tick_damage = action.tick_damage.pop()
        action.tick_units = action.tick_units.pop()
        action.update_time()

        energy_copy = copy.deepcopy(action)
        energy_copy.action_type = "energy"
        energy_copy.update_time()

        sim.floating_actions.add(action)
        sim.floating_actions.add(energy_copy)

    ## Fischl C1 ## Instant ## Onhit ## Normal
    def fischl_c1(self,unit_obj,sim,action):
        if any((x.unit.name == "Fischl" and x.type == "skill" and x.action_type == "damage") for x in sim.floating_actions) == False:
            if action[0].proc_type == "No":
                convertedpct = ComboAction(unit_obj,action[0].combo)
                convertedpct.ticks = 1
                convertedpct.name = "Fischl C1"
                convertedpct.element = ["Electro"]
                convertedpct.scaling = [1]
                convertedpct.tick_types = ["normal"]
                convertedpct.tick_times = [sim.time_into_turn]
                convertedpct.tick_damage = [0.22]
                convertedpct.tick_units = [0]
                convertedpct.tick_used = ["no"]
                convertedpct.tick_units = [1]
                convertedpct.proc_type = "Yes"
                convertedpct.update_time()

                sim.floating_actions.add(convertedpct)
                print("Proced Fischl C1")

    ## Fischl C2 ## Instant ## Onhit ## Skill
    def fischl_c2(self,unit_obj,sim,extra):
        flat_dmg = Action(unit_obj,"skill")

        flat_dmg.tick_times = [sim.time_into_turn + 0.05]
        flat_dmg.tick_damage = [2]
        flat_dmg.tick_units = [0]
        flat_dmg.ticks = 1
        flat_dmg.scaling = [1]
        flat_dmg.update_time()

        sim.floating_actions.add(flat_dmg)
        unit_obj.triggerable_buffs["Fischl_C2"].live_cd = unit_obj.current_skill_cd-1


    ## Fischl C4 ## Instant ## Onhit ## Burst
    def fischl_c4(self,unit_obj,sim,extra):
        flat_dmg = Action(unit_obj,"burst")

        flat_dmg.tick_times = [sim.time_into_turn + 0.05]
        flat_dmg.tick_damage = [2.22]        
        flat_dmg.tick_units = [0]
        flat_dmg.ticks = 1
        flat_dmg.scaling = [1]
        flat_dmg.update_time()

        sim.floating_actions.add(flat_dmg)
        unit_obj.triggerable_buffs["Fischl_C2"].live_cd = unit_obj.current_burst_cd-1

    ## Fischl C6 1 ## Instant ## Postcast ## Skill,Burst
    def fischl_c6_1(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.triggerable_buffs["Fischl_C6_2"] = copy.deepcopy(buffdict["Fischl_C6_2"])
            unit.triggerable_buffs["Fischl_C6_2"].time_remaining = 12

    ## Fischl C6 2 ## Instant ## Midhit ## Normal
    def fischl_c6_2(self,unit_obj,sim,action):
        if any((x.unit.name == "Fischl" and x.type == "skill" and x.action_type == "damage") for x in sim.floating_actions) == True:
            if action[0].proc_type == "No":
                convertedpct = ComboAction(unit_obj,action[0].combo)
                convertedpct.ticks = 1
                convertedpct.name = "Fischl C6"
                convertedpct.element = ["Electro"]
                convertedpct.scaling = [1]
                convertedpct.tick_types = ["normal"]
                convertedpct.tick_times = [sim.time_into_turn]
                convertedpct.tick_damage = [0.3]
                convertedpct.tick_units = [0]
                convertedpct.tick_used = ["no"]
                convertedpct.tick_units = [1]
                convertedpct.proc_type = "Yes"
                convertedpct.update_time()

                sim.floating_actions.add(convertedpct)
                print("Proced Fischl C6")



    ###########
    ## Ganyu ##
    ###########

    ## Ganyu A2 ## Duration ## Postcast ## Charged
    def ganyu_a2(self,unit_obj,sim,extra):
        unit_obj.live_charged_crit_rate += 0.2

    ## Ganyu A4 ## Duration ## Postcast ## Burst
    def ganyu_a4(self,unit_obj,sim,extra):
        unit_obj.live_cryo_dmg += 0.2

    ## Ganyu C1 1 ## Instant ## Onhit ## Charged
    def ganyu_c1_1(self,unit_obj,sim,extra):
        unit_obj.live_burst_energy_cost += 2

    ## Ganyu C4 ## Duration ## Postcast ## Burst
    def ganyu_c4(self,unit_obj,sim,extra):
        unit_obj.live_all_dmg += 0.15

    ## Ganyu C6 1 ## Instant ## Postcast ## Skill
    def ganyu_c6(self,unit_obj,sim,extra):
        if hasattr(unit_obj, "c6_reset_stack") == False:
            unit_obj.c6_reset_stack = 1
            unit_obj.active_buffs["Ganyu_C6_2"] = copy.deepcopy(buffdict["Ganyu_C6_2"])
        else:
            unit_obj.c6_reset_stack = 1
            unit_obj.active_buffs["Ganyu_C6_2"] = copy.deepcopy(buffdict["Ganyu_C6_2"])

    ## Ganyu C6 2 ## Duration ##     
    def ganyu_c6_2(self,unit_obj,sim,extra):
        if hasattr(unit_obj, "c6_reset_stack") == False:
            print("Error")
            pass
        else:
            if unit_obj.c6_reset_stack == 1:
                unit_obj.live_charged_tick_times = [26/60,49/60]
                unit_obj.live_charged_cancel = 26/60
                unit_obj.live_charged_swap = 26/60
                unit_obj.live_charged_skill = 26/60
                unit_obj.live_charged_attack = 26/60
                unit_obj.triggerable_buffs["Ganyu_C6_3"] = copy.deepcopy(buffdict["Ganyu_C6_3"])
                unit_obj.triggerable_buffs["Ganyu_C6_3"].time_remaining = 30

    ## Ganyu C6 3 ## Instant ##
    def ganyu_c6_3(self,unit_obj,sim,extra):
        if unit_obj.c6_reset_stack == 1:
            unit_obj.c6_reset_stack = 0
            print("C6 GANYU PROC")
            unit_obj.active_buffs["Ganyu_C6_2"].time_remaining = 0
            unit_obj.triggerable_buffs["Ganyu_C6_3"].time_remaining = 0

    ##########
    ## Jean ##
    ##########

    ## Jean A4 ## Instant ## Postcast ## Burst
    def jean_a4(self,unit_obj,sim,extra):
        unit_obj.live_burst_energy_cost += 16

    ## Jean C1 ##
    def jean_c1(self,unit_obj,sim,extra):
        pass

    ## Jean C2 ## Instant ## Particle
    def jean_c2(self,unit_obj,sim,extra):
        unit_obj.live_normal_speed += 0.15

    ###########
    ## Kaeya ##
    ###########

    ## Kaeya A4 ## Instant ## Reaction 
    def kaeya_a4(self,unit_obj,sim,reaction):
        energy = ""
        if reaction[0] == "frozen":
            energy == Action(unit_obj,"skill")
            energy.action_type = "energy"
            energy.energy_times = [sim.time_into_turn+2]
            sim.floating_actions.add(energy)

    ## Kaeya C1 ## Instant ## Prehit 
    def kaeya_c1(self,unit_obj,sim,extra):
        if sim.enemy.element == "Cryo":
            unit_obj.live_normal_cond_crit_rate += 0.15
            unit_obj.live_charged_cond_crit_rate += 0.15

    ## Kaeya C2 ## Instant ## Prehit 
    def kaeya_c2(self,unit_obj,sim,extra):
        pass

    ## Kaeya C6 ## Instant ## Postcast # Burst 
    def kaeya_c6_2(self,unit_obj,sim,extra):
        unit_obj.current_energy += 15

    ############
    ## Keqing ##
    ############

    ## Keqing A2 ## Duration ## Postcast ## Skill
    def keqing_a2(self,unit_obj,sim,extra):
        unit_obj.live_normal_type = "Electro"
        unit_obj.live_charged_type = "Electro"

    ## Keqing A4 ## Duration ## Postcast ## Burst
    def keqing_a4(self,unit_obj,sim,extra):
        unit_obj.live_crit_rate += 0.15
        unit_obj.live_recharge += 0.15

    ## Diluc E ## Duration ## Precast
    def keqing_e(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"e_stacks") == False:
            unit_obj.e_stacks = 0

        if unit_obj.e_stacks == 0:
            unit_obj.start_time = sim.encounter_duration
            unit_obj.e_stacks = 1
            unit_obj.current_skill_cd = 0

        if "Keqing_E_2" in unit_obj.triggerable_buffs:
            unit_obj.live_tick_times = [0.467]
            unit_obj.live_skill_tick_damage = [1.68]
            unit_obj.live_skill_cancel = [0.283]
            unit_obj.live_skill_burst = [0.700]
            unit_obj.live_skill_swap = [0.867]
            unit_obj.live_skill_attack = [0.717]
            unit_obj.current_skill_cd = 0
        else:
            if unit_obj.e_stacks != 1:
                unit_obj.current_skill_cd = unit_obj.live_skill_cd - (sim.encounter_duration - unit_obj.start_time)
                unit_obj.active_buffs.pop("Keqing_E")

    def keqing_e_1(self,unit_obj,sim,extra):
        if unit_obj.e_stacks == 1:
            unit_obj.triggerable_buffs["Keqing_E_2"] = copy.deepcopy(buffdict["Keqing_E_2"])
            unit_obj.triggerable_buffs["Keqing_E_2"].time_remaining = 5
            unit_obj.triggerable_buffs["Keqing_E_1"].live_cd = unit_obj.live_skill_cd
            unit_obj.e_stacks = 2

    def keqing_e_2(self,unit_obj,sim,extra):
        if unit_obj.e_stacks == 2:
            unit_obj.e_stacks = 0
            unit_obj.triggerable_buffs.pop("Keqing_E_2")
            unit_obj.current_skill_cd = unit_obj.live_skill_cd - (sim.encounter_duration - unit_obj.start_time)
            unit_obj.active_buffs.pop("Keqing_E")

    ## Keqing C1 ## Instant ## Onhit ## Skill
    def keqing_c1(self,unit_obj,sim,action):
        if action[0].proc_type == "No" and action[0].tick_damage == [1.68]:
            convertedpct = Action(unit_obj,"skill")
            convertedpct.ticks = 2
            convertedpct.name = "Keqing C1"
            convertedpct.element = ["Electro","Electro"]
            convertedpct.scaling = [1,1]
            convertedpct.tick_types = ["skill","skill"]
            convertedpct.tick_times = [sim.time_into_turn,sim.time_into_turn]
            convertedpct.tick_damage = [0.5,0.5]
            convertedpct.tick_units = [1,0]
            convertedpct.tick_used = ["no","no"]
            convertedpct.proc_type = "Yes"
            convertedpct.update_time()

            sim.floating_actions.add(convertedpct)
            print("Proced Keqing C1")

    ## Keqing C2 ## Instant ## Prehit
    def keqing_c2(self,unit_obj,sim,extra):
        if sim.enemy.element == "Electro":
            energy = Action(unit_obj,"skill")
            energy.action_type = "energy"
            energy.energy_times = [sim.time_into_turn+1.6]
            energy.particles = 1
            sim.floating_actions.add(energy)
        unit_obj.triggerable_buffs["Keqing_C2"].live_cd = 5

    ## Keqing C4 1 ## Instant ## Reaction
    def keqing_c4_1(self,unit_obj,sim,reaction):
        if reaction[0] in {"overload", "superconduct", "electro_charged"}:
            unit_obj.active_buffs["Keqing_C4_2"] = copy.deepcopy(buffdict["Keqing_C4_2"])

    ## Keqing C4 2 ## Duration ##
    def keqing_c4_2(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += 0.25

    ## Keqing C6 ## Duration ## Onhit # Normal,Charged,Skill,Burst
    def keqing_c6_1(self,unit_obj,sim,extra): ## Normal
        unit_obj.live_electro_dmg += 0.06
    def keqing_c6_2(self,unit_obj,sim,extra): ## Charged
        unit_obj.live_electro_dmg += 0.06
    def keqing_c6_3(self,unit_obj,sim,extra): ## Skill
        unit_obj.live_electro_dmg += 0.06
    def keqing_c6_4(self,unit_obj,sim,extra): ## Burst
        unit_obj.live_electro_dmg += 0.06    

    ##########
    ## Klee ##
    ##########

    ## Klee A2 1 ## Instant ## Onhit ## Normal, Skill
    def klee_a2_1(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"a2_stack") == False:
            unit_obj.a2_stack = 1
        else:
            unit_obj.a2_stack += 1
        
        if  0 == math.fmod(unit_obj.a2_stack,2):
            unit_obj.spark = True
            unit_obj.triggerable_buffs["Klee_A2_1"].live_cd = 4

    ## Klee A2 2 ## Instant ## Prehit ## Charged
    def klee_a2_2(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"sparks") == False:
            unit_obj.sparks = False
        if unit_obj.sparks == True:
            unit_obj.live_charged_dmg += 0.5
            unit_obj.sparks = False

    ## Klee A4 ## Instant ## Onhit ## Charged
    def klee_a4(self,unit_obj,sim,extra):
        unit_obj.live_burst_energy_cost += 2

    ## Klee C1 ## Instant ## Onhit ## Any
    def klee_c1(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"c1_stack") == False:
            unit_obj.c1_stack = 1
        else:
            unit_obj.c1_stack += 1
        
        if  0 == math.fmod(unit_obj.c1_stack,3):
            # print("Klee C1 Proc")

            c1_proc = Action(unit_obj,"skill")
            c1_proc.name = "Klee C1"
            c1_proc.ticks = 1
            c1_proc.tick_times = [sim.time_into_turn+0.1]
            c1_proc.tick_damage = [0.464*1.2]
            c1_proc.tick_units = [0]
            c1_proc.update_time()
            # print("DAMAGE: " + str(c1_proc.calculate_damage_snapshot(sim)))
            # print(c1_proc.tick_damage)

            sim.floating_actions.add(c1_proc)

    ## Klee C4 ## Instant ## Onhit ## Any
    def klee_c4(self,unit_obj,sim,extra):
        pass

    ## Klee C6 1 ## Duration ##
    def klee_c6_1(self,unit_obj,sim,extra):
        pass

    ## Klee C6 2 ## Duration ## Postcast ## Burst
    def klee_c6_2(self,unit_obj,sim,extra):
        unit_obj.live_pyro_dmg += 0.1

    ##########
    ## Lisa ##
    ##########

    ## Lisa C1 ## Instant ## Onhit ## Skill
    def lisa_c1(self,unit_obj,sim,extra):
        unit_obj.live_burst_energy_cost += 2

    def lisa_c6(self,unit_obj,sim,extra):
        pass

    ##########
    ## Mona ##
    ##########

    ## Mona Q Cast ## Instant ## Postcast ## Burst
    def mona_q_cast(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.triggerable_buffs["Mona_Q_Trigger"] = copy.deepcopy(buffdict["Mona_Q_Trigger"])
            unit.triggerable_buffs["Mona_Q_Trigger"].time_remaining = 8
            unit.active_buffs["Mona_Q_Buff_1"] = copy.deepcopy(buffdict["Mona_Q_Buff_1"])
            unit.triggerable_buffs["Mona_Q_Buff_2"] = copy.deepcopy(buffdict["Mona_Q_Buff_2"])

    ## Mona Q Trigger ## Instant ## Onhit ##
    def mona_q_trigger(self,unit_obj,sim,extra):
        for unit in sim.units:
            for action in sim.floating_actions:
                if action.unit.name == "Mona" and action.type == "burst":

                    action.tick_times[1] = sim.time_into_turn + 0.1
                    action.update_time()

                    unit.triggerable_buffs["Mona_Q_Trigger"].time_remaining = 0
                    unit.active_buffs["Mona_Q_Buff_1"] = copy.deepcopy(buffdict["Mona_Q_Buff_1"])
                    unit.active_buffs["Mona_Q_Buff_1"].time_remaining = 5
                    unit.triggerable_buffs["Mona_Q_Buff_2"].time_remaining = 5

    ## Mona Q Buff ## Duration ##
    def mona_q_buff_1(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Mona":
                unit_obj.live_cond_dmg += min( 0.6 , 0.42 + unit.burst_level * 0.02 )

                ## Mona C4 ##
                if unit.constellation >=4:
                    unit_obj.live_cond_crit_rate += 0.15

    ## Mona Q Buff 2 ## Duration ## Onhit
    ## Mona C1 ##
    def mona_q_buff_2(self,unit_obj,sim,extra):
        unit_obj.live_electro_charged_dmg += 0.15
        unit_obj.live_vaporise_dmg += 0.15
        unit_obj.live_hydro_swirl_dmg += 0.15

    ## Mona A2 ##
    def mona_a2(self,unit_obj,sim,extra):
        pass

    ## Mona C2 ##
    def mona_c2(self,unit_obj,sim,extra):
        pass

    ## Mona C6 ##
    def mona_c6(self,unit_obj,sim,extra):
        pass

    ###############
    ## Ningguang ##
    ###############

    ## Ningguang Normal ## Instant ## Onhit ## Normal
    def ningguang_normal(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"jade_stacks") == False:
            unit_obj.jade_stacks = 1
        else:
            if unit_obj.jade_stacks >= 3:
                pass
            else:
                unit_obj.jade_stacks += 1

    ## Ningguang Charged ## Instant ## Onhit ## Charged
    def ningguang_charged(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"jade_stacks") == False:
            unit_obj.jade_stacks = 0
        else:
            if unit_obj.jade_stacks > 0:

                jade_proc = Action(unit_obj,"charged")
                jade_proc.ticks = unit_obj.jade_stacks
                jade_proc.tick_times = list()
                jade_proc.tick_damage = list()
                jade_proc.tick_units = list()
                jade_proc.scaling = list()
                jade_proc.tick_used = list()
                jade_proc.scaling = list()
                jade_proc.element = list()

                for i in range(unit_obj.jade_stacks):
                    jade_proc.tick_times.append(sim.time_into_turn + 0.25 + i*0.1)
                    jade_proc.tick_types.append("charged")
                    jade_proc.scaling.append(ratio_type(unit_obj,"charged")[unit_obj.normal_level])
                    jade_proc.tick_damage.append(0.496)
                    jade_proc.tick_units.append(0)
                    jade_proc.tick_used.append("no")
                    jade_proc.element.append("Geo")

                jade_proc.update_time()

                sim.floating_actions.add(jade_proc)
                unit_obj.jade_stacks = 0

    ## Ningguang A2 ## Duration ## Onhit ## Normal, Burst
    def ningguang_a2(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"jade_stacks") == False:
            unit_obj.jade_stacks = 0
        else:
            if unit_obj.jade_stacks > 0:
                unit_obj.live_charged_stamina_cost = [0]

    ## Ninggaung E ## Instant ## Postcast ## Skill
    def ningguang_e(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"jade_wall") == False:
            unit_obj.jade_wall = 1
        else:
            unit_obj.jade_wall = 1

        ## Ningguang A4 ##
        for unit in sim.units:
            unit.triggerable_buffs["Ningguang_A4_Trigger"] = copy.deepcopy(buffdict["Ningguang_A4_Trigger"])
            unit.triggerable_buffs["Ningguang_A4_Trigger"].time_remaining = 30

    ## Ningguang A4 Trigger ## Duration ## Field ## Temporary
    def ningguang_a4_trigger(self,unit_obj,sim,extra):
        if unit_obj == sim.chosen_unit:
            unit_obj.active_buffs["Ningguang_A4_Buff"] = copy.deepcopy(buffdict["Ningguang_A4_Buff"])

    ## Ningguang A4 Buff ## Duration
    def ningguang_a4_buff(self,unit_obj,sim,extra):
        unit_obj.live_geo_dmg += 0.1

    ## Ningguang Q ## Instant ## Onhit ## Burst
    def ningguang_q(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"jade_wall") == False:
            unit_obj.jade_wall = 0
        else:
            if unit_obj.jade_wall == 1:
                unit_obj.jade_wall = 0

                for unit in sim.units:
                    unit.triggerable_buffs["Ningguang_A4_Trigger"].time_remaining = 0
            
                jade_stars_burst =  Action(unit_obj,"burst")
                jade_stars_burst.ticks = 6
                jade_stars_burst.tick_times = []
                jade_stars_burst.tick_damage = []
                jade_stars_burst.tick_units = []
                for i in range(unit_obj.jade_stacks):
                    jade_stars_burst.ticks.append(sim.time_into_turn+ i*0.1)
                    jade_stars_burst.ticks.append(0.8696)
                    jade_stars_burst.tick_units.append(0)
                    
                jade_stars_burst.update_time()
                sim.floating_actions.append(jade_stars_burst)

                ## Ningguang C2 ##
                if unit_obj.constellation >= 2:
                    unit_obj.live_skill_cd = 0
                
        ## Ningguang C6 ##          
        if unit_obj.constellation >= 6:
            if hasattr(unit_obj,"jade_stacks") == False:
                unit_obj.jade_stacks = 7
            else:
                unit_obj.jade_stacks = 7
        

    ############
    ## Noelle ##
    ############

    ## Noelle Q 1 ## Instant ## Postcast ## Burst
    def noelle_q_1(self,unit_obj,sim,extra):
        def_mult = eleratiodict[unit_obj.burst_level] * 0.4
        if unit_obj.constellation >=6:
            def_mult += 0.5
        snapshot = def_mult * ( 1 + copy.deepcopy(unit_obj.base_def) * ( 1 + copy.deepcopy(unit_obj.live_pct_def) ) + copy.deepcopy(unit_obj.live_flat_def))
        unit_obj.snapshot_buff = snapshot
        unit_obj.active_buffs["Noelle_Q_2"] = copy.deepcopy(buffdict["Noelle_Q_2"])

    ### Noelle Q 2 ## Duration ##
    def noelle_q_2(self,unit_obj,sim,extra):
        unit_obj.live_normal_type = "Geo"
        unit_obj.live_charged_type = "Geo"
        unit_obj.live_flat_atk += unit_obj.snapshot_buff

    ## Noelle E ## Instant ## Postcast ## Skill
    def noelle_e(self,unit_obj,sim,extra):
        def_dmg = AlbedoTrigger(unit_obj,sim.enemy, sim)

        def_dmg.name = "Noelle E"
        def_dmg.ticks = 1
        def_dmg.particles = 0
        def_dmg.tick_times = [0.5]
        def_dmg.tick_damage = [1.2]
        def_dmg.tick_units = [1]

        def_dmg.energy_times = [2.5]

        sim.floating_actions.add(def_dmg)

        ## Noelle C4 ##
        if unit_obj.constellation >= 4:
            action = Action(unit_obj,"skill")
 
            action.particles = 0
            action.tick_times = [0.55]
            action.tick_damage = [4]
            action.tick_units = [0]
            action.scaling = [1]

            action.energy_times = [2.55]
            action.update_time()
            sim.floating_actions.add(action)

    ## Noelle A4 ## Instant ## Onhit ## Normal, Charged
    def noelle_a4(self,unit_obj,sim,extra):
        unit_obj.live_skill_cd -= 0.25

    ## Noelle C1 ##
    def noelle_c1(self,unit_obj,sim,extra):
        pass
    
    ##########
    ## Qiqi ##
    ##########

    ## Qiqi C1 ##
    def qiqi_c1(self,unit_obj,sim,extra):
        pass

    ## Qiqi C2 ## Instant ## Prehit
    def qiqi_c2(self,unit_obj,sim,extra):
        if sim.enemy.element == "Cryo":
            unit_obj.live_normal_cond_dmg += 0.15
            unit_obj.live_charged_cond_dmg += 0.15

    ###########
    ## Razor ##
    ###########

    ## Razor E ## Instant ## Postcast ## Skill
    def razor_e(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"electro_sigil") == False:
            unit_obj.electro_sigil = 1
        else:
            if unit_obj.electro_sigil == 3:
                pass
            else:
                unit_obj.electro_sigil += 1
        
    ## Razor Q 1 ## Instant ## Postcast ## Burst
    def razor_q_1(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"electro_sigil") == False:
            unit_obj.electro_sigil = 1
        else:
            unit_obj.live_burst_energy_cost += 5 * unit_obj.electro_sigil
            unit_obj.electro_sigil = 0

        as_mult = razorqasdict[unit_obj.burst_level] * 0.26
        unit_obj.snapshot_buff = as_mult
        unit_obj.active_buffs["Razor_Q_2"] = copy.deepcopy(buffdict["Razor_Q_2"])
        unit_obj.triggerable_buffs["Razor_Q_3"] = copy.deepcopy(buffdict["Razor_Q_3"])
        unit_obj.triggerable_buffs["Razor_Q_3"].time_remaining = 18

    ## Razor Q 2 ## Duration ##
    def razor_q_2(self,unit_obj,sim,extra):
        unit_obj.live_normal_speed += unit_obj.snapshot_buff
        if unit_obj != sim.chosen_unit:
            unit_obj.active_buffs["Razor_Q_2"].time_remaining = 0

    ## Razor Q 3 ## Instant ## Midhit ## Normal
    def razor_q_3(self,unit_obj,sim,action):
        if action[0].proc_type == "No":
            convertedpct = ComboAction(unit_obj,action[0].combo)
            convertedpct.ticks = 1
            convertedpct.name = "Razor Q"
            convertedpct.element = ["Electro"]
            convertedpct.scaling = [ratio_type(unit_obj,"burst")[unit_obj.burst_level]]
            convertedpct.tick_types = ["normal"]
            convertedpct.tick_times = [sim.time_into_turn]
            convertedpct.tick_damage = [action[0].tick_damage[action[1]]*0.24]
            convertedpct.tick_used = ["no"]
            convertedpct.tick_units = [1]
            convertedpct.proc_type = "Yes"
            convertedpct.update_time()
            sim.floating_actions.add(convertedpct)
            print("Proced Razor Q")

    ## Razor A2 2 ## Instant ## Postcast ## Burst
    def razor_a2_2(self,unit_obj,sim,extra):
        unit_obj.live_skill_cd = 0

    ## Razor C1 ## Duration ## Particle
    def razor_c1(self,unit_obj,sim,extra):
        unit_obj.live_all_dmg += 0.1

    ## Razor C6 ## Instant ## Onhit
    def razor_c6(self,unit_obj,sim,action):
        convertedpct = ComboAction(unit_obj,action[0].combo)
        convertedpct.ticks = 1
        convertedpct.name = "Razor Q"
        convertedpct.element = ["Electro"]
        convertedpct.scaling = [ratio_type(unit_obj,"burst")[unit_obj.burst_level]]
        convertedpct.tick_types = ["normal"]
        convertedpct.tick_times = [sim.time_into_turn]
        convertedpct.tick_damage = [action[0].tick_damage[action[1]]*0.24]
        convertedpct.tick_used = ["no"]
        convertedpct.tick_units = [1]
        convertedpct.proc_type = "Yes"
        convertedpct.update_time()
        sim.floating_actions.add(convertedpct)
        print("Proced Razor C6")
        unit_obj.triggerable_buffs["Razor_C6"].live_cd = 10

    #############
    ## Sucrose ##
    #############

    ## Sucrose Q ## Instant ## Reaction 
    def sucrose_q(self,unit_obj,sim,reaction):
        if reaction[0] == "swirl":
            if hasattr(reaction[2],"infused") == False:
                reaction[2].infused = True
                infuse = copy.deepcopy(reaction[2])
                infuse.element = reaction[1]
                infuse.tick_damage = [0.44 for x in infuse.tick_damage]
                sim.floating_actions.add(infuse)
                
                ## Sucrose C6 ##
                if unit_obj.constellation >= 6:
                    for unit in sim.units:
                        unit.active_buffs["Sucrose_C6"] = copy.deepcopy(buffdict.get("Sucrose_C6_" + reaction[1].lower()))

    ## Sucrose A2 1 ## Instant ## Reaction
    def sucrose_a2_1(self,unit_obj,sim,reaction):
        if reaction[0] == "swirl":
            for unit in sim.units:
                if reaction[1] == unit.element.lower():
                    unit.active_buffs["Sucrose_A2_2"] = copy.deepcopy(buffdict["Sucrose_A2_2"])

    ## Sucrose A2 2 ## Duration ##  
    def sucrose_a2_2(self,unit_obj,sim,reaction):
        unit_obj.live_ele_m += 50

    ## Sucrose A4 1 ## Duration ## Postcast ## Skill, Burst
    def sucrose_a4_1(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Sucrose":
                em_buff = unit.live_ele_m*0.2
        unit_obj.live_ele_m += em_buff

    ## Sucrose C4 ## Instant ## Onhit ## Normal, Charged
    def sucrose_c4(self,unit_obj,sim,extra):
        unit_obj.live_skill_cd -= (4/7)

    ###############
    ## Tartaglia ##
    ###############

    ## Tartaglia Stance Swap ## Instant ## Postcast ## Skill
    def tartaglia_stance_swap(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"stance") == False:
            unit_obj.stance = "melee"
            unit_obj.active_buffs["Tartaglia_Stance"] = copy.deepcopy(buffdict["Tartaglia_Stance"])
            unit_obj.active_buffs["Tartaglia_Stance"].time_remaining = 45
        else:
            if unit_obj.stance == "ranged":
                unit_obj.stance = "melee"
                unit_obj.active_buffs["Tartaglia_Stance"] = copy.deepcopy(buffdict["Tartaglia_Stance"])
                unit_obj.active_buffs["Tartaglia_Stance"].time_remaining = 45
            elif unit_obj.stance == "melee":
                if hasattr(unit_obj,"c6_reset") == True:
                    if unit_obj.c6_reset == True:
                        unit_obj.live_skill_cd = 1
                        unit_obj.c6_reset = False
                else:
                    unit_obj.stance = "ranged"
                    unit_obj.active_buffs.pop("Tartaglia_Stance")
                    unit_obj.live_skill_cd = (45 - copy.deepcopy(unit_obj.active_buffs["Tartaglia_Stance_Swap"].time_remaining))*2 + 6
            else:
                print("Error")

    ## Tartaglia Stance ## Instant ## Postcast
    def tartaglia_stance(self,unit_obj,sim,extra):
        if unit_obj.stance == "ranged":
            pass
        elif unit_obj.stance == "melee":

            unit_obj.live_normal_type = "Hydro"
            unit_obj.live_normal_AT = 3.017
            unit_obj.live_normal_AC = "No"
            unit_obj.live_normal_hits = 7
            unit_obj.live_normal_tick_times = [0.083,0.417,0.717,1.083,1.667,2.017,2.300]
            unit_obj.live_normal_tick_damage = [0.3887,0.4162,0.5633,0.5994,0.553,0.3543,0.3767]
            unit_obj.live_normal_tick_units = [1,0,0,0,0,1,0]

            unit_obj.live_charged_type = "Hydro"
            unit_obj.live_charged_AT = 1.517
            unit_obj.live_charged_AC = "No"
            unit_obj.live_charged_hits = 3
            unit_obj.live_charged_tick_times = [0.083,0.583,0.683]
            unit_obj.live_charged_tick_damage = [0.3887,0.602,0.7198]
            unit_obj.live_charged_tick_units = [1,0,0]
            unit_obj.live_charged_stam = 20

            unit_obj.live_burst_AT = 1.717
            unit_obj.live_burst_hits = 1
            unit_obj.live_burst_tick_times = [1.10]
            unit_obj.live_burst_tick_damage = [4.64]
            unit_obj.live_burst_tick_units = [2]

    ## Tartaglia Riptide ## Instant ## Onhit
    def riptide_apply(self,unit_obj,sim,extra):
        sim.enemy.active_debuffs["Riptide"] = copy.deepcopy(debuffdict["Riptide_debuff"])

    ## Tartaglia Aimed Passive ## Instant ## Onhit ## Charged
    def tartaglia_aimed_riptide_proc(self,unit_obj,sim,extra):

        if hasattr(unit_obj,"stance") == False:
            unit_obj.stance = "ranged"

        if unit_obj.stance == "ranged":
            if "Riptide" in sim.enemy.active_debuffs:
        
                charged_proc = Action(unit_obj,"normal")
                charged_proc.ticks = 3

                charged_proc.tick_times = [sim.time_into_turn + 0.25, sim.time_into_turn + 0.3, sim.time_into_turn + 0.3]
                charged_proc.tick_damage = [0.123,0.123,0.123]
                charged_proc.tick_units = [0,0,0]
                charged_proc.scaling = eleratiodict[unit_obj.normal_level]
                charged_proc.update_time()
                sim.floating_actions.add(charged_proc)

                energy_copy = copy.deepcopy(charged_proc)
                energy_copy.action_type = "energy"
                energy_copy.particles = 1
                energy_copy.energy_times = [x+2 for x in energy_copy.tick_times]
                sim.floating_actions.add(energy_copy)

    ## Tartaglia Melee Passive ## Instant ## Onhit ## Normal, Charged
    def tartaglia_melee_riptide_proc(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"stance") == False:
            unit_obj.stance = "ranged"

        if unit_obj.stance == "melee":
            if "Riptide" in sim.enemy.active_debuffs:
                melee_proc = Action(unit_obj,"skill")
                melee_proc.ticks = 1

                melee_proc.tick_times = [sim.time_into_turn+0.25]
                melee_proc.tick_damage = [0.602]
                melee_proc.tick_units = [1]
                melee_proc.scaling = physdict[unit_obj.skill_level]
                melee_proc.update_time()
                sim.floating_actions.add(melee_proc)
                unit_obj.triggerable_buffs["Tartaglia_Melee_Proc"].live_cd = 1.5
                energy_copy = copy.deepcopy(melee_proc)
                energy_copy.particles = 1
                energy_copy.energy_times = [x+2 for x in energy_copy.tick_times]
                sim.floating_actions.add(energy_copy)

                ## Tartaglia C4 ##
                if unit_obj.constellation >= 4:
                    if any(type(x) == TartagliaC4 for x in sim.floating_actions) == True:
                        pass
                    else:
                        c4_proc = TartagliaC4(unit_obj,sim.enemy,sim)

                        c4_proc.tick_times = [x+sim.time_into_turn for x in c4_proc.tick_times]
                        c4_proc.energy_times = [x+sim.time_into_turn for x in c4_proc.energy_times]

                        sim.floating_actions.add(c4_proc)
                        
                        energy_copy = copy.deepcopy(c4_proc)
                        energy_copy.action_type = "energy"

                        sim.floating_actions.add(energy_copy)

    ## Tartaglia Burst Passive ## Instant ## Onhit ## Burst                    
    def tartaglia_burst_riptide_proc(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"stance") == False:
            unit_obj.stance = "ranged"

        if unit_obj.stance == "melee":
            if "Riptide" in sim.enemy.active_debuffs:
                sim.enemy.active_debuffs["Riptide"].time_remaining = 0

                burst_proc = Action(unit_obj,"burst")
                burst_proc.ticks = 1

                burst_proc.tick_times = [sim.time_into_turn+0.25]
                burst_proc.tick_damage = [1.2]
                burst_proc.tick_units = [1]
                burst_proc.scaling = eleratiodict[unit_obj.burst_level]
                burst_proc.update_time()
                sim.floating_actions.add(burst_proc)
                unit_obj.live_burst_energy_cost += 15

    def tartaglia_c6(self,unit_obj,sim,extra):
        if hasattr(unit_obj,"stance") == False:
            unit_obj.stance = "ranged"
        
        if unit_obj.stance == "melee":
            unit_obj.c6_reset = True

    ######################
    ## Traveler (Anemo) ##
    ######################

    ## Traveler (Anemo) A4 ## Instant ## Midhit ## Normal
    def traveler_anemo_a2(self,unit_obj,sim,action):
        if action[1] == 4 and action[0].proc_type == "No":
            proc = ComboAction(unit_obj,action[0].combo)
            proc.name = "Traveler (Anemo) A2"
            proc.element = ["Anemo"]
            proc.tick_times = [sim.time_into_turn + 0.5]
            proc.tick_damage = [0.6]
            proc.tick_units = [1]
            proc.tick_types = ["normal"]
            proc.ticks = 1
            proc.scaling = [1]
            sim.floating_actions.add(proc)
            proc.proc_type == "Yes"
            
    ## Traveler (Anemo) E ## Instant ## Reaction:
    def traveler_anemo_e(self,unit_obj,sim,reaction):
        if reaction[0] == "swirl":
            if hasattr(reaction[2],"infused") == False:
                reaction[2].infused = True
                infuse = copy.deepcopy(reaction[2])
                infuse.element = reaction[1]
                infuse.tick_damage = [0.23*x for x in infuse.tick_damage]
                sim.floating_actions.add(infuse)

    ## Traveler (Anemo) Q ## Instant ## Reaction
    def traveler_anemo_q(self,unit_obj,sim,reaction):
        if reaction[0] == "swirl":
            if hasattr(reaction[2],"infused") == False:
                reaction[2].infused = True
                infuse = copy.deepcopy(reaction[2])
                infuse.element = reaction[1]
                infuse.tick_damage = [0.248 for x in infuse.tick_damage]
                sim.floating_actions.add(infuse)

                ## Traveler (Anemo) C6 ##
                if unit_obj.constellation >= 6:
                    sim.enemy.active_debuffs["Traveler_Anemo_C6"] = copy.deepcopy(debuffdict.get("Traveler_Anemo_C6_anemo"))  
                    sim.enemy.active_debuffs["Traveler_Anemo_C6"] = copy.deepcopy(debuffdict.get("Traveler_Anemo_C6_" + reaction[1].lower()))

    def traveler_anemo_c6(self,unit_obj,sim,reaction):
        pass

    ####################
    ## Traveler (Geo) ##
    ####################

    ## Traveler (Geo) A4 ## Instant ## Midhit ## Normal
    def traveler_geo_a4(self,unit_obj,sim,action):
        if action[1] == 4 and action[0].proc_type == "No":
            proc = ComboAction(unit_obj,action[0].combo)
            proc.name = "Traveler (Geo) A4"
            proc.element = ["Geo"]
            proc.tick_times = [sim.time_into_turn + 0.5]
            proc.tick_damage = [0.6]
            proc.tick_units = [1]
            proc.tick_types = ["normal"]
            proc.ticks = 1
            proc.scaling = [1]
            sim.floating_actions.add(proc)
            proc.proc_type == "Yes"

    ## Traveler (Geo) Q Cast ## Instant ## Postcast ## Burst
    def traveler_geo_q_cast(self,unit_obj,sim,extra):

        ## Traveler (Geo) C6 ##
        if unit_obj.constellation >6:
            time = 20
        else:
            time = 15

        ## Traveler (Geo) C1 ##
        if unit_obj.constellation >= 1:
            for unit in sim.units:
                unit.active_buffs["Traveler_(Geo)_Q_Buff"] = copy.deepcopy(buffdict["Traveler_(Geo)_Q_Buff"])
                unit.active_buffs["Traveler_(Geo)_Q_Buff"].time_remaining = time

    ## Traveler (Geo) C1 ##
    ## Traveler (Geo) Q Buff ## Duration
    def traveler_geo_q_buff(self,unit_obj,sim,extra):
        if unit_obj == sim.chosen_unit:
            unit_obj.live_crit_rate += 0.1

    ## Traveler (Geo) C4 ## Instant ## Postcast ## Burst
    def traveler_geo_c4(self,unit_obj,sim,extra):
        unit_obj.live_burst_energy_cost += 5

    ###########
    ## Venti ##
    ###########

    ## Venti Q ## Instant ## Reaction
    def venti_q(self,unit_obj,sim,reaction):
        if reaction[0] == "swirl":
            if hasattr(reaction[2],"infused") == False:
                reaction[2].infused = True
                infuse = copy.deepcopy(reaction[2])
                infuse.element = reaction[1]
                infuse.tick_damage = [0.188 for x in infuse.tick_damage]
                sim.floating_actions.add(infuse)

                ## Venti A4 ##
                for unit in sim.units:
                    if unit.element == reaction[1] or unit.name == "Venti":
                        unit.live_burst_energy_cost

                ## Venti C6 ##
                if unit_obj.constellation >= 6:
                    sim.enemy.active_debuffs["Venti_C6"] = copy.deepcopy(debuffdict.get("Venti_C6_" + reaction[1].lower()))

    ## Venti C4 ## Instant ## Particle
    def venti_c4(self,unit_obj,sim,extra):
        unit_obj.live_anemo_dmg += 0.25

    ###############
    ## Xiangling ##
    ###############

    ## Xiangling A4 Cast ## Instant ## Postcast ## Skill
    def xiangling_a4_cast(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.active_buffs["Xiangling_A4_Trigger"] = copy.deepcopy(buffdict["Xiangling_A4_Trigger"])
            unit.active_buffs["Xiangling_A4_Buff_1"] = copy.deepcopy(buffdict["Xiangling_A4_Buff_1"])
            unit.active_buffs["Xiangling_A4_Buff_2"] = copy.deepcopy(buffdict["Xiangling_A4_Buff_2"])

    ## Xianling A4 Trigger ## Duration ## Postcast
    def xiangling_a4_trigger(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Xiangling":
                unit.a4_pickup = sim.chosen_unit

    ## Xiangling A4 Buff 1 ## Duration ##
    def xiangling_a4_buff_1(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Xiangling":
                if hasattr(unit,"a4pickup") == False:
                    pass
                else:
                    for unit2 in sim.units:
                        if unit2 == unit.a4_pickup:
                            unit2.live_pct_atk -= 0.1

    ## Xiangling A4 Buff 2 ## Duration ##
    def xiangling_a4_buff_2(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Xiangling":
                if hasattr(unit,"a4pickup") == False:
                    pass
                else:
                    for unit2 in sim.units:
                        if unit2 == unit.a4_pickup:
                            unit2.live_pct_atk += 0.1

    ## Xiangling C2 ## Instant ## Midhit ## Normal
    def xiangling_c2(self,unit_obj,sim,tick):
        if tick == 8:
            proc = Action(unit_obj,"normal")
            proc.element = "Pyro"
            proc.tick_times = [sim.time_into_turn + 0.75]
            proc.tick_damage = [0.6]
            proc.tick_units = [1]
            proc.ticks = 1
            proc.scaling = 1
            sim.floating_actions.add(proc)

    ## Xiangling C6 ## Duration ## Postcast ## Burst
    def xiangling_c6(self,unit_obj,sim,extra):
        unit_obj.live_pyro_dmg += 0.15

    ##########
    ## Xiao ##
    ##########

    ## Xiao Q ## Duration ## Postcast ## Burst
    def xiao_q(self,unit_obj,sim,extra):
        if unit_obj != sim.chosen_unit:
            unit_obj.active_buffs["Xiao_Q"].time_remaining = 0
        unit_obj.live_normal_type = "Anemo"
        unit_obj.live_charged_type = "Anemo"
        unit_obj.live_combo_options.add("plunge")
        unit_obj.live_normal_dmg += 0.55 + unit_obj.burst_level*0.035
        unit_obj.live_charged_dmg += 0.55 + unit_obj.burst_level*0.035
        unit_obj.live_plunge_dmg += 0.55 + unit_obj.burst_level*0.035

    ## Xiao A2 ## Duration ## Postcast ## Burst
    def xiao_a2(self,unit_obj,sim,extra):
        unit_obj.live_all_dmg += 0.15

    ## Xiao A4 ## Duration ## Postcast ## Skill
    def xiao_a4(self,unit_obj,sim,extra):
        unit_obj.live_skill_dmg += unit_obj.active_buffs["Xiao_A4"].stacks

    ## Xiao C2 ## Duration ## Postcast ## Any
    def xiao_c2(self,unit_obj,sim,extra):
        if unit_obj != sim.chosen_unit:
            unit_obj.live_recharge += 0.25
            unit_obj.active_buffs["Xiao_C2"].time_remaining = sim.encounter_limit

    ## Xiao C6 ## 
    def xiao_c6(self,unit_obj,sim,extra):
        pass

    #############
    ## Xingqiu ##
    #############

    ## Xingqiu Q Cast ## Instant ## Postcast ## Burst
    def xingqiu_q_cast(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.triggerable_buffs["Xingqiu_Q_Trigger"] = copy.deepcopy(buffdict["Xingqiu_Q_Trigger"])
            unit.triggerable_buffs["Xingqiu_Q_Trigger"].time_remaining = 15

            ## Xingqiu C2 ##
            if unit_obj.constellation >=2:
                unit.triggerable_buffs["Xingqiu_Q_Trigger"].time_remaining = 18

            unit_obj.q_tick = 0
    
    ## Xingqiu Q Trigger ## Instant ## Onhit ## Normal, Charged
    def xingqiu_q_trigger(self,unit_obj,sim,extra):
        for unit in sim.units:
            if unit.name == "Xingqiu":

                ## Xingqiu C6 ##
                if unit.constellation >=6:
                    if 0 == math.fmod(unit.q_tick,3):
                        action = Action(unit, "burst")
                        action.ticks = 2
                        action.element = ["Hydro"]*2
                        action.tick_types = ["burst"]*2
                        action.tick_times = [sim.time_into_turn+0.1,sim.time_into_turn+0.15]
                        action.tick_damage = [0.453,0.453]
                        action.tick_units = [1,0]
                        action.tick_used = ["no"]*2
                        action.scaling = [ratio_type(unit,"burst")[getattr(unit,"burst_level")]]*action.ticks
                        action.update_time()
                        sim.floating_actions.add(action)

                    elif 1 == math.fmod(unit.q_tick,3):
                        action = Action(unit, "burst")
                        action.ticks = 3
                        action.element = ["Hydro"]*3
                        action.tick_types = ["burst"]*3
                        action.tick_times = [sim.time_into_turn+0.1,sim.time_into_turn+0.15,sim.time_into_turn+0.2]
                        action.tick_damage = [0.453,0.453,0.453]
                        action.tick_units = [1,0,0]
                        action.tick_used = ["no"]*3
                        action.scaling = [ratio_type(unit,"burst")[getattr(unit,"burst_level")]]*action.ticks
                        action.update_time()
                        sim.floating_actions.add(action)

                    elif 2 == math.fmod(unit.q_tick,3):
                        action = Action(unit, "burst")
                        action.ticks = 5
                        action.element = ["Hydro"]*5
                        action.tick_types = ["burst"]*5
                        action.tick_times = [sim.time_into_turn+0.1,sim.time_into_turn+0.15,sim.time_into_turn+0.2,sim.time_into_turn+0.25,sim.time_into_turn+0.3]
                        action.tick_damage = [0.453,0.453,0.453,0.453,0.453]
                        action.tick_units = [1,0,0,0,0]
                        action.tick_used = ["no"]*5
                        action.scaling = [ratio_type(unit,"burst")[getattr(unit,"burst_level")]]*action.ticks
                        action.update_time()
                        sim.floating_actions.add(action)
                        unit.current_energy += 3

                ## Without C6 ##        
                else:
                    if 0 == math.fmod(unit.q_tick,2):
                        action = Action(unit, "burst")
                        action.ticks = 2
                        action.element = ["Hydro"]*2
                        action.tick_types = ["burst"]*2
                        action.tick_times = [sim.time_into_turn+0.1,sim.time_into_turn+0.15]
                        action.tick_damage = [0.453,0.453]
                        action.tick_units = [1,0]
                        action.tick_used = ["no"]*2
                        action.scaling = [ratio_type(unit,"burst")[getattr(unit,"burst_level")]]*action.ticks
                        action.update_time()
                        sim.floating_actions.add(action)

                    elif 1 == math.fmod(unit.q_tick,2):
                        action = Action(unit, "burst")
                        action.ticks = 3
                        action.element = ["Hydro"]*3
                        action.tick_types = ["burst"]*3
                        action.tick_times = [sim.time_into_turn+0.1,sim.time_into_turn+0.15,sim.time_into_turn+0.2]
                        action.tick_damage = [0.453,0.453,0.453]
                        action.tick_units = [1,0,0]
                        action.tick_used = ["no"]*3
                        action.scaling = [ratio_type(unit,"burst")[getattr(unit,"burst_level")]]*action.ticks
                        action.update_time()
                        sim.floating_actions.add(action)
                unit.q_tick += 1
        for unit in sim.units:
            unit.triggerable_buffs["Xingqiu_Q_Trigger"].live_cd = 1


    ############
    ## Xinyan ##
    ############

    ## Xinyan A4 ## Duration ## Postcast ## Skill
    def xinyan_a4(self,unit_obj,sim,extra):
        if unit_obj == sim.chosen_unit:
            unit_obj.live_physical_dmg += 0.15

    ## Xinyan C1 ## Duration ## Onhit ## Normal, Charged
    def xinyan_c1(self,unit_obj,sim,extra):
        unit_obj.live_normal_speed += 0.15
        unit_obj.live_charged_speed += 0.15

    def xinyan_c2(self,unit_obj,sim,extra):
        pass

    ## Xinyan Q ## Instant ## Onhit ## Burst
    def xinyan_q(self,unit_obj,sim,extra):
        phys_dmg = XinyanQ(unit_obj,sim.enemy, sim)
        sim.floating_actions.add(phys_dmg)

    #############
    ## Zhongli ##
    #############

    ## Zhongli A4 Normal ## Instant ## Onhit ## Normal
    def zhongli_a4_normal(self,unit_obj,sim,extra):
        auto_dmg = ZhongliA4(unit_obj,"normal", sim.enemy,"sim")
        sim.floating_actions.add(auto_dmg)

    ## Zhongli A4 Charged ## Instant ## Onhit ## Charged
    def zhongli_a4_charged(self,unit_obj,sim,extra):
        charged_dmg = ZhongliA4(unit_obj,"charged", sim.enemy,"sim")
        sim.floating_actions.add(charged_dmg)

    ## Zhongli A4 Skill ## Instant ## Onhit ## Charged
    def zhongli_a4_skill(self,unit_obj,sim,extra):
        skill_dmg = ZhongliA4(unit_obj,"skill", sim.enemy,"sim")
        sim.floating_actions.add(skill_dmg)

    ## Zhongli A4 Burst ## Instant ## Onhit ## Charged
    def zhongli_a4_burst(self,unit_obj,sim,extra):
        burst_dmg = ZhongliA4(unit_obj,"burst", sim.enemy,"sim")
        sim.floating_actions.add(burst_dmg)

    ## Zhongli E ## Instant ## Postcast ## Skill
    def zhongli_e(self,unit_obj,sim,extra):
        pass

    #############
    ## Weapons ##
    #############

    ##########
    ## Bows ##
    ##########

    def skyward_harp_2(self,unit_obj,sim,extra):
        skyward_harp = WeaponAction(unit_obj,1)
        skyward_harp.ticks = 1
        skyward_harp.tick_damage = [1.25]
        skyward_harp.tick_times = [0.5+sim.time_into_turn]
        skyward_harp.tick_units = [0]
        skyward_harp.tick_used = ["no"]
        skyward_harp.initial_time = max(skyward_harp.tick_times)
        skyward_harp.time_remaining = max(skyward_harp.tick_times)
        unit_obj.triggerable_buffs["Skyward Harp 2"].live_cd = 4 - ((unit_obj.weapon_rank-1)*0.5)
        sim.floating_actions.add(skyward_harp)
        print(unit_obj.name + " proced Skyward Harp")
        
    def compound_bow_2(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += (0.04 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Compound Bow 2"].stacks
        unit_obj.live_normal_speed += (0.012 + (unit_obj.weapon_rank-1)*0.003) * unit_obj.active_buffs["Compound Bow 2"].stacks
        unit_obj.triggerable_buffs["Compound Bow 2"].live_cd = 0.3

    def viridescent_hunt_2(self,unit_obj,sim,extra):
        viri_hunt = WeaponAction(unit_obj,8)
        viri_hunt.ticks = 8
        t = (unit_obj.weapon_rank-1)*0.25 + 1
        s = sim.time_into_turn
        viri_hunt.tick_damage = [0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t,0.4*t]
        viri_hunt.tick_times = [0.5+s,1+s,1.5+s,2+s,2.5+s,3+s,3.5+s,4+s,]
        viri_hunt.tick_units = [0,0,0,0,0,0,0,0]
        viri_hunt.tick_used = ["no","no","no","no","no","no","no","no"]
        viri_hunt.initial_time = max(viri_hunt.tick_times)
        viri_hunt.time_remaining = max(viri_hunt.tick_times)
        unit_obj.triggerable_buffs["The Viridescent Hunt 2"].live_cd = 14 - ((unit_obj.weapon_rank-1))
        sim.floating_actions.add(viri_hunt)
        print(unit_obj.name + " proced The Viridescent Hunt")

    def prototype_crescent_2(self,unit_obj,sim,extra):
        unit_obj.live_charged_dmg += 0.36 + (unit_obj.weapon_rank-1)*0.09

    # Claymores

    def prototype_archaic_2(self,unit_obj,sim,extra):
        archaic = WeaponAction(unit_obj,1)
        archaic.ticks = 1
        d = 2.4 + (unit_obj.weapon_rank-1)*0.6
        archaic.tick_damage = [d]
        archaic.tick_times = [0.5+sim.time_into_turn]
        archaic.tick_units = [0]
        archaic.tick_used = ["no"]
        archaic.initial_time = max(archaic.tick_times)
        archaic.time_remaining = max(archaic.tick_times)
        unit_obj.triggerable_buffs["Prototype Archaic 2"].live_cd = 15
        sim.floating_actions.add(archaic)

    def wolfs_gravestone_2(self,unit_obj,sim,extra):
        for unit in sim.units:
            unit.active_buffs["Wolf's Gravestone 3"] = copy.deepcopy(buffdict["Wolf's Gravestone 3"])
        print(unit_obj.name + " proced Wolf's Gravestone")
        unit_obj.triggerable_buffs["Wolf's Gravestone 2"].live_cd = 30

    def wolfs_gravestone_3(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += 0.4 + (unit_obj.weapon_rank-1)*0.1

    def rainslasher_2(self,unit_obj,sim,extra):
        if sim.enemy.element == "Hydro" or sim.enemy.element == "Electro":
            unit_obj.live_cond_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def whiteblind_2(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += (0.06 + (unit_obj.weapon_rank-1)*0.015) * unit_obj.active_buffs["Whiteblind 2"].stacks
        unit_obj.live_pct_def += (0.06 + (unit_obj.weapon_rank-1)*0.015) * unit_obj.active_buffs["Whiteblind 2"].stacks
        unit_obj.triggerable_buffs["Whiteblind 2"].live_cd = 0.5

    def skyrider_2(self,unit_obj,sim,extra):
        unit_obj.livek_pct_at += (0.06 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Whiteblind 2"].stacks
        unit_obj.triggerable_buffs["Skyrider 2"].live_cd = 0.5

    def serpent_2(self,unit_obj,sim,extra):
        pass

    def skyward_pride_2(self,unit_obj,sim,extra):
        unit_obj.triggerable_buffs["Skyward Pride 3"] = copy.deepcopy(buffdict["Skyward Pride 3"])
        unit_obj.triggerable_buffs["Skyward Pride 3"].time_remaining = 20
        unit_obj.triggerable_buffs["Skyward Pride 3"].stacks = 8

    def skyward_pride_3(self,unit_obj,sim,extra):
        sp = WeaponAction(unit_obj,6)
        sp.ticks = 6
        d = (unit_obj.weapon_rank-1)*0.2 + 0.8
        s = sim.time_into_turn
        sp.tick_damage = [d]
        sp.tick_times = [0.1+s]
        sp.tick_units = [0]
        sp.tick_used = ["no"]
        sp.initial_time = max(sp.tick_times)
        sp.time_remaining = max(sp.tick_times)
        sim.floating_actions.add(sp)
        unit_obj.triggerable_buffs["Skyward Pride 3"].stacks -= 1

    #Catalysts

    def lost_prayers_2(self,unit_obj,sim,extra):
        unit_obj.live_ele_dmg += (0.04 * round(unit_obj.field_time/4)) * ( 1 + (unit_obj.weapon_rank-1)*0.25) 

    def skyward_atlas_2(self,unit_obj,sim,extra):
        atlas = WeaponAction(unit_obj,6)
        atlas.ticks = 6
        d = (unit_obj.weapon_rank-1)*0.4 + 1.6
        s = sim.time_into_turn
        atlas.tick_damage = [d,d,d,d,d,d]
        atlas.tick_times = [2.5+s,5+s,7.5+s,10+s,12.5+s,15+s]
        atlas.tick_units = [0,0,0,0,0,0]
        atlas.tick_used = ["no","no","no","no","no","no"]
        atlas.initial_time = max(atlas.tick_times)
        atlas.time_remaining = max(atlas.tick_times)
        unit_obj.triggerable_buffs["Skyward Atlas 2"].live_cd = 30
        sim.floating_actions.add(atlas)
        print(unit_obj.name + " proced Skyward Atlas")

    def solar_pearl_normal_buff_2(self,unit_obj,sim,extra):
        unit_obj.live_normal_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def solar_pearl_ability_buff_2(self,unit_obj,sim,extra):
        unit_obj.live_skill_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.live_burst_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def eye_of_perception_2(self,unit_obj,sim,extra):
        eop = WeaponAction(unit_obj,1)
        eop.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.3 + 2.4
        s = sim.time_into_turn
        eop.tick_damage = [d]
        eop.tick_times = [0.1+s]
        eop.tick_units = [0]
        eop.tick_used = ["no"]
        eop.initial_time = max(eop.tick_times)
        eop.time_remaining = max(eop.tick_times)
        unit_obj.triggerable_buffs["Eye of Perception 2"].live_cd = 12 - (unit_obj.weapon_rank-1)
        sim.floating_actions.add(eop)

    def widsith_2(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.live_ele_dmg += 0.16 + (unit_obj.weapon_rank-1)*0.04
        unit_obj.live_ele_m += 80 + (unit_obj.weapon_rank-1)*20

    def prototype_amber_2(self,unit_obj,sim,extra):
        energy_gain = ( 4 + (unit_obj.weapon_rank-1)*0.5 ) * 3
        for unit in sim.units:
            unit.live_burst_energy_cost = min(unit.burst_energy, unit.live_burst_energy + energy_gain)

    def mappa_marre_2(self,unit_obj,sim,extra):
        unit_obj.live_all_dmg += (0.08 + (unit_obj.weapon_rank-1)*0.02) * unit_obj.active_buffs["Mappa Marre 2"].stacks

    # Polearms

    def skyward_spine_2(self,unit_obj,sim,extra):
        skyward_spine = WeaponAction(unit_obj,1)
        skyward_spine.ticks = 1
        d = 0.4 + (unit_obj.weapon_rank-1)*0.1
        skyward_spine.tick_damage = [d]
        skyward_spine.tick_times = [0.1+sim.time_into_turn]
        skyward_spine.tick_units = [0]
        skyward_spine.tick_used = ["no"]
        skyward_spine.initial_time = max(skyward_spine.tick_times)
        skyward_spine.time_remaining = max(skyward_spine.tick_times)
        unit_obj.triggerable_buffs["Skyward Spine 2"].live_cd = 2
        sim.floating_actions.add(skyward_spine)

    def lithic_spear_2(self,unit_obj,sim,extra):
        pass

    def primordial_spear_2(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += (0.032 + (unit_obj.weapon_rank-1)*0.007) * unit_obj.active_buffs["Prim Spear 2"].stacks
        if unit_obj.active_buffs["Prim Spear 2"].stacks == 7:
            unit_obj.live_all_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.06
        unit_obj.triggerable_buffs["Prim Spear 2"].live_cd = 0.5

    def prototype_starglitter_2(self,unit_obj,sim,extra):
        unit_obj.live_normal_dmg += (0.08 + (unit_obj.weapon_rank-1)*0.02) * unit_obj.active_buffs["Prototype Starglitter 2"].stacks

    def crescent_pike_2(self,unit_obj,sim,extra):
        cres = WeaponAction(unit_obj,1)
        cres.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.05 + 0.2
        s = sim.time_into_turn
        cres.tick_damage = [d]
        cres.tick_times = [0.1+s]
        cres.tick_units = [0]
        cres.tick_used = ["no"]
        cres.initial_time = max(cres.tick_times)
        cres.time_remaining = max(cres.tick_times)
        sim.floating_actions.add(cres)

    # Swords

    def lions_roar_2(self,unit_obj,sim,extra):
        if sim.enemy.element == "Pyro" or sim.enemy.element == "Electro":
            unit_obj.live_cond_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def aquila_favonia_2(self,unit_obj,sim,extra):
        aq = WeaponAction(unit_obj,1)
        aq.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.3 + 2
        s = sim.time_into_turn
        aq.tick_damage = [d]
        aq.tick_times = [0.1+s]
        aq.tick_units = [0]
        aq.tick_used = ["no"]
        aq.initial_time = max(aq.tick_times)
        aq.time_remaining = max(aq.tick_times)
        unit_obj.triggerable_buffs["Aquila Favonia 2"].live_cd = 15
        sim.floating_actions.add(aq)

    def prototype_rancour_2(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += (0.04 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Rancour 2"].stacks
        unit_obj.live_pct_def += (0.04 + (unit_obj.weapon_rank-1)*0.01) * unit_obj.active_buffs["Rancour 2"].stacks
        unit_obj.triggerable_buffs["Rancour 2"].live_cd = 0.5

    def skyward_blade_2(self,unit_obj,sim,extra):
        unit_obj.live_normal_speed += 0.1
        unit_obj.triggerable_buffs["Skyward Blade 3"] = copy.deepcopy(buffdict["Skyward Blade 3"])
        unit_obj.triggerable_buffs["Skyward Blade 3"].time_remaining = 12

    def skyward_blade_3(self,unit_obj,sim,extra):
        sb = WeaponAction(unit_obj,1)
        sb.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.05 + 0.2
        s = sim.time_into_turn
        sb.tick_damage = [d]
        sb.tick_times = [0.1+s]
        sb.tick_units = [0]
        sb.tick_used = ["no"]
        sb.initial_time = max(sb.tick_times)
        sb.time_remaining = max(sb.tick_times)
        sim.floating_actions.add(sb)

    def the_flute_2(self,unit_obj,sim,extra):
        tf = WeaponAction(unit_obj,1)
        tf.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.05 + 0.2
        s = sim.time_into_turn
        tf.tick_damage = [d]
        tf.tick_times = [0.1+s]
        tf.tick_units = [0]
        tf.tick_used = ["no"]
        tf.initial_time = max(tf.tick_times)
        tf.time_remaining = max(tf.tick_times)
        sim.floating_actions.add(tf)
        unit_obj.triggerable_buffs["Flute 2"].live_cd = 0.5

    def iron_sting_2(self,unit_obj,sim,extra):
        unit_obj.live_all_dmg += (0.06 + (unit_obj.weapon_rank-1)*0.015) * unit_obj.active_buffs["Iron Sting 2"].stacks

    # Misc

    def favonius(self,unit_obj,sim,extra):
        pass

    def sacrificial(self,unit_obj,sim,extra):
        unit_obj.live_skill_cd = 0 
        unit_obj.triggerable_buffs["Sacrificial"].live_cd = 30 - ((unit_obj.weapon_rank-1))*4
        
    def geo_weapons(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += (0.08 + (unit_obj.weapon_rank-1)*0.02) * unit_obj.active_buffs["Geo Weapon"].stacks
        unit_obj.triggerable_buffs["Geo Weapon"].live_cd = 0.3

    def dragonspine(self,unit_obj,sim,extra):
        dragonspine = WeaponAction(unit_obj,1)
        dragonspine.ticks = 1
        d = (unit_obj.weapon_rank-1)*0.15 + 0.8
        s = sim.time_into_turn
        if sim.enemy.element == "Cryo":
            d *= 2.5
        dragonspine.tick_damage = [d]
        dragonspine.tick_times = [0.1+s]
        dragonspine.tick_units = [0]
        dragonspine.tick_used = ["no"]
        dragonspine.initial_time = max(dragonspine.tick_times)
        dragonspine.time_remaining = max(dragonspine.tick_times)
        unit_obj.triggerable_buffs["Dragonspine"].live_cd = 10
        sim.floating_actions.add(dragonspine)
        print("Dragonspine effect")
    

    # Artifacts

    def noblesse(self,unit_obj,sim,extra):
        unit_obj.live_pct_atk += 0.2

    def crimson_witch(self,unit_obj,sim,extra):
        unit_obj.live_pyro_dmg += 0.075 * unit_obj.active_buffs["Crimson Witch"].stacks

    def lavawalker(self,unit_obj,sim,extra):
        if sim.enemy.element == "Pyro":
            unit_obj.live_cond_dmg += 0.35

    def thundersoother(self,unit_obj,sim,extra):
        if sim.enemy.element == "Electro":
            unit_obj.live_cond_dmg += 0.35

    def blizzard_strayer(self,unit_obj,sim,extra):
        if sim.enemy.element == "Cryo":
            unit_obj.live_crit_rate += 0.2
        if sim.enemy.frozen == "Frozen":
            unit_obj.live_crit_rate += 0.2

    def archaic_petra(self,unit_obj,sim,reaction):
        if reaction[0] == "crystallise":
            for unit in sim.units:
                unit.active_buffs["Archaic Petra"] = copy.deepcopy(buffdict.get(reaction[1]+"_petra"))

    def cryo_petra(self,unit_obj,sim,extra):
        unit_obj.live_cryo_dmg += 0.35

    def electro_petra(self,unit_obj,sim,extra):
        unit_obj.live_electro_dmg += 0.35

    def hydro_petra(self,unit_obj,sim,extra):
        unit_obj.live_hydro_dmg_dmg += 0.35

    def pyro_petra(self,unit_obj,sim,extra):
        unit_obj.live_pyro_dmg_dmg += 0.35

    def heart_of_depth(self,unit_obj,sim,extra):
        unit_obj.live_normal_dmg += 0.3
        unit_obj.live_charged_dmg += 0.3
    
    def thundering_fury(self,unit_obj,sim,extra):
        unit_obj.live_skill_cd -= max(0, unit_obj.live_skill_cd - 1)

    def viridescent_venerer(self,unit_obj,sim,reaction):
        if reaction[0] == "swirl":
            if reaction[1] == "Pyro":
                sim.enemy.active_debuffs["VV_Pyro"] = copy.deepcopy(debuffdict["VV_Pyro"])
            if reaction[1] == "Hydro":
                sim.enemy.active_debuffs["VV_Hydro"] = copy.deepcopy(debuffdict["VV_Hydro"])
            if reaction[1] == "Electro":
                sim.enemy.active_debuffs["VV_Electro"] = copy.deepcopy(debuffdict["VV_Electro"])
            if reaction[1] == "Cryo":
                sim.enemy.active_debuffs["VV_Cryo"] = copy.deepcopy(debuffdict["VV_Cryo"])
            print(sim.chosen_unit.name + " reduced enemy " + sim.enemy.element + " RES with VV")

class ActiveDebuff:

    ## Beidou ##

    def beidou_c6(self,unit_obj,sim):
        sim.enemy.electro_res_debuff += 0.15

    ## Chongyun ##

    def chongyun_a4(self,unit_obj,sim):
        pass

    ## Jean ##

    def jean_c4(self,unit_obj,sim):
        sim.enemy.anemo_res_debuff += 0.4

    ## Klee ##

    def klee_c2(self,unit_obj,sim):
        sim.enemy.defence_debuff += 0.23

    ## Lisa ##

    def lisa_a4(self,unit_obj,sim):
        sim.enemy.defence_debuff += 0.15

    ## Razor ##

    def razor_c4(self,unit_obj,sim):
        sim.enemy.defence_debuff += 0.15

    ## Taratglia ##

    def riptide_debuff(self,unit_obj,sim):
        pass

    ## Venti ##

    def venti_c2_1(self,unit_obj,sim):
        sim.enemy.anemo_res_debuff += 0.12
        sim.enemy.physical_res_debuff += 0.12

    def venti_c2_2(self,unit_obj,sim):
        sim.enemy.anemo_res_debuff += 0.12
        sim.enemy.physical_res_debuff += 0.12

    def venti_c6(self,unit_obj,sim):
        pass

    ## Xinyan ##

    def xinyan_c4(self,unit_obj,sim):
        sim.enemy.physical_res_debuff += 0.15

    ## Xingqiu ##
    def xingqiu_c2(self,unit_obj,sim):
        sim.enemy.hydro_res_debuff += 0.15

    def vv_cryo(self,unit_obj,sim):
        sim.enemy.cryo_res_debuff += 0.4
    
    def vv_hydro(self,unit_obj,sim):
        sim.enemy.hydro_res_debuff += 0.4

    def vv_pyro(self,unit_obj,sim):
        sim.enemy.pyro_res_debuff += 0.4

    def vv_electro(self,unit_obj,sim):
        sim.enemy.electro_res_debuff += 0.4

    def traveler_anemo_anemo(self,unit_obj,sim):
        sim.enemy.anemo_res_debuff += 0.2

    def traveler_anemo_hydro(self,unit_obj,sim):
        sim.enemy.hydro_res_debuff += 0.2

    def traveler_anemo_pyro(self,unit_obj,sim):
        sim.enemy.pyro_res_debuff += 0.2

    def traveler_anemo_electro(self,unit_obj,sim):
        sim.enemy.electro_res_debuff += 0.2

    def traveler_anemo_cryo(self,unit_obj,sim):
        sim.enemy.cryo_res_debuff += 0.2
