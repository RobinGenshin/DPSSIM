from core.read_data import buff_dict, debuff_dict
import copy


class StaticBuff:
    pass


class ActiveBuff:

    @staticmethod
    def noblesse(unit_obj, _):
        unit_obj.live_pct_atk += 0.2

    @staticmethod
    def crimson_witch(unit_obj, _):
        unit_obj.live_pyro_dmg += 0.075 * unit_obj.active_buffs["Crimson Witch"].stacks

    @staticmethod
    def lavawalker(unit_obj, sim, _):
        if "Pyro" in sim.enemy.elements:
            unit_obj.live_cond_dmg += 0.35

    @staticmethod
    def thundersoother(unit_obj, sim, _):
        if "Electro" in sim.enemy.elements:
            unit_obj.live_cond_dmg += 0.35

    @staticmethod
    def blizzard_strayer(unit_obj, sim, _):
        if "Cryo" in sim.enemy.elements or "Frozen" in sim.enemy.elements:
            unit_obj.live_cond_crit_rate += 0.2
        if "Frozen" in sim.enemy.elements:
            unit_obj.live_cond_crit_rate += 0.2

    def archaic_petra(self, _, sim, reaction):
        if reaction[0] == "crystallise":
            for unit in sim.units:
                for key, _ in reaction[1].items():
                    unit.active_buffs["Archaic Petra"] = copy.copy(buff_dict.get(key + "_petra"))
                    unit.active_buffs["Archaic Petra"].source = self

    @staticmethod
    def cryo_petra(unit_obj, _):
        unit_obj.live_cryo_dmg += 0.35

    @staticmethod
    def electro_petra(unit_obj, _):
        unit_obj.live_electro_dmg += 0.35

    @staticmethod
    def hydro_petra(unit_obj, _):
        unit_obj.live_hydro_dmg += 0.35

    @staticmethod
    def pyro_petra(unit_obj, _):
        unit_obj.live_pyro_dmg += 0.35

    @staticmethod
    def heart_of_depth(unit_obj, _):
        unit_obj.live_normal_dmg += 0.3
        unit_obj.live_charged_dmg += 0.3

    @staticmethod
    def thundering_fury(unit_obj, _, reaction):
        if reaction[0] in {"electro_charged", "overload", "superconduct"}:
            unit_obj.live_skill_cd -= max(0, unit_obj.live_skill_cd - 1)

    @staticmethod
    def viridescent_venerer(_, sim, reaction):
        if reaction[0] == "swirl":
            for key in reaction[1]:
                if key == "Pyro":
                    sim.enemy.active_debuffs["VV_Pyro"] = copy.deepcopy(debuff_dict["VV_Pyro"])
                if key == "Hydro":
                    sim.enemy.active_debuffs["VV_Hydro"] = copy.deepcopy(debuff_dict["VV_Hydro"])
                if key == "Electro":
                    sim.enemy.active_debuffs["VV_Electro"] = copy.deepcopy(debuff_dict["VV_Electro"])
                if key == "Cryo" or key == "Frozen":
                    sim.enemy.active_debuffs["VV_Cryo"] = copy.deepcopy(debuff_dict["VV_Cryo"])
                if key == "Frozen":
                    key = "Cryo"
                print(reaction[2].unit.character + " reduced enemy " + key + " RES with VV")