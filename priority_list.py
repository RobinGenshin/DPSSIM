
import re

class PriorityList:
    def __init__(self):
        pass

    def prioritise(self,sim,action_list):

        ## Bennett Q ##
        for unit in sim.units:
            if unit.name == "Bennett" and unit.current_burst_cd == 0 and unit.current_energy == unit.live_burst_energy_cost:
                # return ("Bennett","burst")
                pass

        ## Floating particles ##
        for unit in sim.units:
            for energy in {x for x in sim.floating_actions if x.action_type == "energy"}:
                if 2 > energy.time_remaining > 0.12 and energy.element == unit.element:
                    # return("unit","element")
                    pass
            
        ## Viridescent Venerer ##
        for unit in sim.units:
            if unit.artifact == "Viridescent Venerer":   
                for x in sim.enemy.active_debuffs:
                    if re.match(r"%vv_.^",x) == True:
                        # return (unit.name,_)
                        pass

        ## Ningguang Q ##
        for unit in sim.units:
            if unit.name == "Ningguang" and unit.current_burst_cd == 0 and unit.current_energy == unit.live_burst_energy_cost:
                if hasattr(unit,"jade_wall") == True:
                    if unit.jade_wall == True:
                        # return 
                        pass
                    else:
                        unit.jade_wall = False

        ## Razor / Klee / Xiao ##
        for unit in sim.units:
            if unit.name in {"Razor", "Klee", "Xiao"} and unit.stance == True:
                if unit.name == sim.chosen_unit:
                    # return 
                    pass

        

                        
