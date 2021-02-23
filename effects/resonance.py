from core.action import Particle
from core.read_data import debuff_dict
import copy


class Resonance:

    @staticmethod
    def pyro_resonance(unit_obj, _):
        unit_obj.pct_atk += 0.25

    @staticmethod
    def anemo_resonance(unit_obj, _):
        unit_obj.skilL_cdr *= 0.95
        unit_obj.burst_cdr *= 0.95

    @staticmethod
    def cryo_resonance(unit_obj, sim, _):
        if sim.enemy.element == "Cryo":
            unit_obj.live_cond_crit_rate += 0.15

    @staticmethod
    def electro_resonance(unit_obj, sim, reaction):
        if reaction[0] in {"electro_charged", "overload", "superconduct"}:
            particle = Particle(unit_obj, "Electro", 1)
            particle.add_to_energy_queue(sim)
            for unit in sim.units:
                unit.triggerable_buffs["Electro_Resonance"].live_cd = 5

    @staticmethod
    def geo_resonance(_, sim, action):
        if action[0].element == "Geo":
            sim.enemy.active_debuffs["Geo_Resonance"] = copy.copy(debuff_dict["Geo_Resonance"])