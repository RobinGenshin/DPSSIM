
import re
from operator import methodcaller

class PriorityList:
    def __init__(self):
        pass

    def prioritise(self,sim,action_list):
        # Using bursts after skills ##
        if sim.last_action != None:
            if any((action.type == "burst" and (action.unit.name == sim.last_action.unit.name) and (sim.last_action.type == "skill")) for action in action_list):
                return [x for x in action_list if x.type == "burst" and x.unit.name == sim.last_action.unit.name][0]

        # Greedy DPS units ##
        for unit in sim.units:
            if unit.name == "Xiao" and "Xiao_Q" in unit.active_buffs:
                return max([x for x in action_list if (x.unit.name == "Xiao" and x.type == "combo")], key=methodcaller('calculate_dps_snapshot',sim))

        for action in sim.floating_actions:
            if any((action.type == "burst" and action.unit.name == "Klee" and action.action_type == "damage") for action in sim.floating_actions):
                print("KLEE Q FIELD")
                return max([x for x in action_list if (x.unit.name == "Klee" and (x.type == "combo" or x.type == "skill"))], key=methodcaller('calculate_dps_snapshot',sim))

        for unit in sim.units:
            if unit.name == "Razor" and "Razor_Q_2" in unit.active_buffs:
                return max([x for x in action_list if (x.unit.name == "Razor" and x.type == "combo")], key=methodcaller('calculate_dps_snapshot',sim))

        # Picking up particles ##
        a_dict = dict()
        for unit in sim.units:
            if (unit.current_energy/unit.live_burst_energy_cost) < (unit.current_burst_cd / unit.live_burst_cd):
                a_dict[unit] = 0
                for energy in {x for x in sim.floating_actions if x.action_type == "energy"}:
                    if 2 > energy.time_remaining > 0.12 and energy.element == unit.element:
                        a_dict[unit] += energy.particles * ( 1 + unit.recharge )

        if any(value == 0 for value in a_dict.items()):
            choose = max(a_dict,key=lambda x: a_dict[x])
            unit_actions = [x for x in action_list if x.unit.name == choose.name]
            return max(unit_actions, key=methodcaller('calculate_dps_snapshot',sim))

        ## Bennett Q ##
        for action in action_list:
            if action.unit == "Bennet" and action.type == "burst":
                return action

        # Using skills if bursts are ready ##
        if any(action.type == "skill" for action in action_list):
            skill_list = [x for x in action_list if (x.type == "skill") and any(y.type == "burst" and y.unit.name == x.unit.name for y in action_list)]
            pairs = [(x,y) for x in skill_list for y in action_list if y.unit.name == x.unit.name and y.type == "burst"]
            if pairs != []:
                return max(pairs,key=lambda x: (x[0].calculate_damage_snapshot(sim)+x[1].calculate_damage_snapshot(sim)))[0]

        ## Using 0 DPS Greedy unit bursts ##
        for action in action_list:
            if action.type == "burst" and action.unit.name == "Xiao":
                return action

        # print("Last priority")
        # action = max(action_list, key=methodcaller('calculate_dps_snapshot',sim))
        # print(action.calculate_dps_snapshot(sim),action.unit.name,action.type,action.unit.active_buffs,action.tick_damage,action.unit.live_charged_crit_rate)
        return max(action_list, key=methodcaller('calculate_dps_snapshot',sim))
                
            
        # ## Viridescent Venerer ##
        # for unit in sim.units:
        #     if unit.artifact == "Viridescent Venerer":   
        #         for x in sim.enemy.active_debuffs:
        #             if re.match(r"%vv_.^",x) == True:
        #                 # return (unit.name,_)
        #                 pass

        # ## Ningguang Q ##
        # for unit in sim.units:
        #     if unit.name == "Ningguang" and unit.current_burst_cd == 0 and unit.current_energy == unit.live_burst_energy_cost:
        #         if hasattr(unit,"jade_wall") == True:
        #             if unit.jade_wall == True:
        #                 # return 
        #                 pass
        #             else:
        #                 unit.jade_wall = False

        # ## Razor / Klee / Xiao ##
        # for unit in sim.units:
        #     if unit.name in {"Razor", "Klee", "Xiao"} and unit.stance == True:
        #         if unit.name == sim.chosen_unit:
        #             # return 
        #             pass