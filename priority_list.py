
import re
from operator import methodcaller

class PriorityList:
    def __init__(self):
        pass

    def prioritise(self,sim,action_list):
        # Using bursts after skills ##
        if sim.last_action != None:
            if any((action.type == "burst" and action.unit.name == sim.last_action.unit.name) for action in action_list):
                print("Hi")
                return max([x for x in action_list if x.type == "burst" and x.unit.name == sim.last_action.unit.name])

        # Greedy DPS units ##
        for unit in sim.units:
            if unit.name == "Xiao" and "Xiao_Q" in unit.active_buffs:
                return max([x for x in action_list if (x.unit.name == "Xiao" and x.type == "combo")], key=methodcaller('calculate_dps_snapshot',sim))

        # Using skills if bursts are ready ##
        if any(action.type == "skill" for action in action_list):
            skill_list = [x for x in action_list if (x.type == "skill") and any(y.type == "burst" and y.unit.name == x.unit.name for y in action_list)]
            if skill_list != []:
                return max(skill_list,key=methodcaller('calculate_dps_snapshot',sim))

        ## Using 0 DPS Greedy unit bursts ##
        for action in action_list:
            if action.type == "burst" and action.unit.name == "Xiao":
                return action
        
        return max(action_list, key=methodcaller('calculate_dps_snapshot',sim))

        # ## Bennett Q ##
        # for unit in sim.units:
        #     if unit.name == "Bennett" and unit.current_burst_cd == 0 and unit.current_energy == unit.live_burst_energy_cost:
        #         # return ("Bennett","burst")
        #         pass

        # ## Floating particles ##
        # for unit in sim.units:
        #     for energy in {x for x in sim.floating_actions if x.action_type == "energy"}:
        #         if 2 > energy.time_remaining > 0.12 and energy.element == unit.element:
        #             # return("unit","element")
        #             pass
            
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

        

                        
