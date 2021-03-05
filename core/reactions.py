from core.read_data import buff_dict
from effects.misc import ActiveBuff
from core.action import ElectroCharged
import copy

class React:
    def __init__(self):
        self.print = True

    def check(self, action, tick, enemy, action_units, sim):
        #Anemo
        if action.tick_element[tick] == "Anemo":
            if any(unit > 0 for element, unit in enemy.elements.items()) > 0:
                return self.swirl(action, tick, enemy, action_units, sim)
            else:
                return self.no_reaction(action, tick, enemy, action_units, sim)
        #Geo
        elif action.tick_element[tick] == "Geo":
            if any(unit > 0 for element, unit in enemy.elements.items()) > 0:
                return self.crystallise(action, tick, enemy, action_units, sim)
            else:
                return self.no_reaction(action, tick, enemy, action_units, sim)
        #Hydro
        elif action.tick_element[tick] == "Hydro":
            if enemy.elements == {}:
                return self.enemyhydro(action, tick, enemy, action_units, sim)
            elif "Pyro" in enemy.elements:
                return self.vaporise2(action, tick, enemy, action_units, sim)
            elif "Electro" in enemy.elements:
                return self.electro_charged(action, tick, enemy, action_units, sim)
            elif "Cryo" in enemy.elements or "Frozen" in enemy.elements:
                return self.frozen(action, tick, enemy, action_units, sim)
            else:
                return self.no_reaction(action, tick, enemy, action_units, sim)
        #Cryo
        elif action.tick_element[tick] == "Cryo":
            if enemy.elements == {}:
                return self.enemycryo(action, tick, enemy, action_units, sim)
            if "Hydro" in enemy.elements:
                return self.frozen(action, tick, enemy, action_units, sim)
            if "Pyro" in enemy.elements:
                return self.melt15(action, tick, enemy, action_units, sim)
            if "Electro" in enemy.elements:
                return self.superconduct(action, tick, enemy, action_units, sim)
            else:
                return self.no_reaction(action, tick, enemy, action_units, sim)
        #Electro
        elif action.tick_element[tick] == "Electro":
            if enemy.elements == {}:
                return self.enemyelectro(action, tick, enemy, action_units, sim)
            if "Hydro" in enemy.elements:
                return self.electro_charged(action, tick, enemy, action_units, sim)
            if "Pyro" in enemy.elements:
                return self.overload(action, tick, enemy, action_units, sim)
            if "Cryo" in enemy.elements or "Frozen" in enemy.elements:
                return self.superconduct(action, tick, enemy, action_units, sim)
            else:
                return self.no_reaction(action, tick, enemy, action_units, sim)
        #Pyro
        elif action.tick_element[tick] == "Pyro":
            if enemy.elements == {}:
                return self.enemypyro(action, tick, enemy, action_units, sim)
            if "Hydro" in enemy.elements:
                return self.vaporise15(action, tick, enemy, action_units, sim)
            if "Cryo" in enemy.elements or "Frozen" in enemy.elements:
                return self.melt2(action, tick, enemy, action_units, sim)
            if "Electro" in enemy.elements:
                return self.overload(action, tick, enemy, action_units, sim)
            else:
                return self.no_reaction(action, tick, enemy, action_units, sim)

        else:
            return self.no_reaction(action, tick, enemy, action_units, sim)

    @staticmethod
    def swirl(action, _, enemy, action_units, sim):
        for element, u in enemy.elements.items():
            u -= action_units * 0.5
            if element == "Frozen":
                sim.damage += 722 * (1 + ((4.44 * action.unit.live_ele_m) / (1400 + action.unit.live_ele_m))) * (
                            1 - getattr(enemy, "live_cryo_res"))
            else:
                sim.damage += 722 * (1 + ((4.44 * action.unit.live_ele_m) / (1400 + action.unit.live_ele_m))) * (1 - getattr(enemy, "live_" + element.lower() + "_res"))
            print(action.unit.character + " proced swirl")
        return [1, ["swirl", enemy.elements]]

    @staticmethod
    def crystallise(action, _, enemy, action_units, sim):
        for element, u in enemy.elements.items():
            u -= action_units * 0.5
            print(action.unit.character + " proced crystallise", element)
        for unit in sim.units:
            unit.active_buffs["Shield"] = copy.copy(buff_dict["Shield"])
            unit.active_buffs["Shield"].source = ActiveBuff()
        return [1, ["crystallise", enemy.elements]]

    @staticmethod
    def overload(action, _, enemy, action_units, sim):
        for element, u in enemy.elements.items():
            if element == "Electro" or element == "Pyro":
                u -= action_units * 0.5
                sim.damage += 2406 * (1 + ((4.44 * action.unit.live_ele_m) / (1400 + action.unit.live_ele_m))) * (1 - enemy.live_pyro_res)
                print(action.unit.character + " proced overload")
        return [1, ["overload"]]

    @staticmethod
    def superconduct(action, _, enemy, action_units, sim):
        for element, u in enemy.elements.items():
            if element == "Electro" or element == "Cryo" or element =="Frozen":
                u -= action_units * 0.5
                sim.damage += 601 * (1 + ((4.44 * action.unit.live_ele_m) / (1400 + action.unit.live_ele_m))) * (1 - enemy.live_cryo_res)
        print(action.unit.character + " proced superconduct")
        return [1, ["superconduct"]]

    @staticmethod
    def electro_charged(action, tick, enemy, action_units, sim):
        if any(a.__class__.__name__ == "ElectroCharged" for a in sim.floating_actions):
            for ec in sim.floating_actions:
                if ec.__class__.__name__ == "ElectroCharged":
                    ec.unit = action.unit
        else:
            ec = ElectroCharged(action.unit, sim)
            ec.add_to_damage_queue(sim)
        if action.tick_element[tick] == "Hydro":
            if "Hydro" not in enemy.elements:
                enemy.elements["Hydro"] = action_units
            else:
                enemy.elements["Hydro"] = max(action_units, enemy.elements["Hydro"])
        elif action.tick_element[tick] == "Electro":
            if "Electro" not in enemy.elements:
                enemy.elements["Electro"] = action_units
            else:
                enemy.elements["Electro"] = max(action_units, enemy.elements["Electro"])
        return [1, ["electro_charged"]]

    @staticmethod
    def frozen(action, tick, enemy, action_units, sim):
        if "Hydro" in sim.enemy.elements:
            sim.enemy.elements["Hydro"] -= action_units
        elif "Cryo" in sim.enemy.elements:
            sim.enemy.elements["Cryo"] -= action_units
        sim.enemy.elements["Frozen"] = action_units
        print(action.unit.character + " proced frozen")
        return [1, ["frozen"]]

    @staticmethod
    def vaporise2(action, tick, enemy, action_units, sim):
        enemy.elements["Pyro"] -= action_units * 2
        print(action.unit.character + " proc'd Vaporise for 2x damage")
        return [2 * (1 + (( 2.78 * action.unit.ele_m ) / ( 1400 + action.unit.ele_m ))), ["vaporise"]]

    @staticmethod
    def vaporise15(action, _, enemy, action_units, __):
        enemy.elements["Hydro"] -= action_units * 0.5
        print(action.unit.character + " proc'd Vaporise for 1.5x damage")
        return [1.5 * (1 + (( 2.78 * action.unit.ele_m ) / ( 1400 + action.unit.ele_m ))), ["vaporise"]]

    @staticmethod
    def melt2(action, tick, enemy, action_units, sim):
        if "Frozen" in enemy.elements:
            enemy.elements["Frozen"] -= action_units * 2
        else:
            enemy.elements["Cryo"] -= action_units * 2
        print(action.unit.character + " proc'd Melt for 2x damage")
        return [2 * (1 + (( 2.78 * action.unit.ele_m ) / ( 1400 + action.unit.ele_m ))), ["melt"]]

    @staticmethod
    def melt15(action, tick, enemy, action_units, sim):
        enemy.elements["Pyro"] -= action_units * 0.5
        print(action.unit.character + " proc'd Melt for 1.5x damage")
        return [1.5 * (1 + (( 2.78 * action.unit.ele_m ) / ( 1400 + action.unit.ele_m ))), ["melt"]]

    @staticmethod
    def enemyelectro(action, tick, enemy, action_units, sim):
        enemy.elements["Electro"] = action_units * 0.8
        print(action.unit.character + " applied electro")
        return [1, ["none"]]

    @staticmethod
    def enemypyro(action, tick, enemy, action_units, sim):
        enemy.elements["Pyro"] = action_units * 0.8
        print(action.unit.character + " applied pyro")
        return [1, ["none"]]

    @staticmethod
    def enemycryo(action, tick, enemy, action_units, sim):
        enemy.elements["Cryo"] = action_units * 0.8
        print(action.unit.character + " applied cryo")
        return [1, ["none"]]

    @staticmethod
    def enemyhydro(action, tick, enemy, action_units, sim):
        enemy.elements["Hydro"] = action_units * 0.8
        print(action.unit.character + " applied hydro")
        return [1, ["none"]]

    @staticmethod
    def no_reaction(action, tick, enemy, unit, sim):
        return [1, ["none"]]