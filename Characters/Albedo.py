from core.unit import Char
from core.read_data import buff_dict
from core.action import Action, Ability
from core.scaling import ratio_type
from core.artifact import Artifact
import copy


class Albedo(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Albedo", level, constellation, weapon, weapon_rank, artifact, talent_levels)

        # Albedo C2 #
        self.c2_stacks = 0

    # StaticEffect
    def albedo_a2(self):
        self.skill_dmg += 0.125

    # ActiveEffect
    @staticmethod
    def albedo_a4(unit, _):
        unit.live_ele_m += 100

    # ActiveEffect
    def albedo_e_cast(self, _, sim, __):
        for unit in sim.units:
            unit.triggerable_buffs["Albedo_E_Trigger"] = copy.copy(buff_dict["Albedo_E_Trigger"])
            unit.triggerable_buffs["Albedo_E_Trigger"].time_remaining = 30
            unit.triggerable_buffs["Albedo_E_Trigger"].source = self

    # ActiveEffect
    def albedo_e_trigger(self, _, sim, __):
        action = AlbedoETrigger(self)
        action.update_time()
        action.add_to_damage_queue(sim)
        action.add_to_energy_queue(sim)
        print("Triggered Transient Blossom")

        for unit in sim.units:
            unit.triggerable_buffs["Albedo_E_Trigger"].live_cd = 2

        # Albedo C1 #
        if self.constellation >= 1:
            self.current_energy += 1.2

        # Albedo C2 Stacks #
        if self.constellation >= 2:
            self.c2_stacks = min(4, self.c2_stacks+1)

    # ActiveEffect
    def albedo_c2(self, _, sim, __):
        action = AlbedoC2(self, sim)
        action.update_time()
        action.add_to_damage_queue(sim)
        self.c2_stacks = 0

    # ActiveEffect
    @staticmethod
    def albedo_c4(unit, _):
        unit.live_plunge_dmg += 0.3

    # ActiveEffect
    @staticmethod
    def albedo_c6(unit, _):
        unit.live_all_dmg += 0.17


class AlbedoETrigger(Action):
    def __init__(self, unit):
        super().__init__(unit)
        self.name = "Transient Blossom"
        self.action_type = "damage"
        self.unit = unit
        self.type = "skill"
        self.element = "Geo"
        self.tick_types = ["skill"]

        self.ticks = 1
        self.tick_times = [0.1]
        self.energy_times = [0.1 + 2]
        self.update_time()
        self.tick_element = ["Geo"]
        self.tick_damage = [1.34]
        self.tick_used = ["no"]
        self.tick_units = [1]
        self.snapshot = True
        self.particles = (2 / 3)
        self.scaling = ratio_type(self.unit, self.type)[getattr(unit, self.type + "_level")]

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot = False

    def calculate_tick_damage(self, tick, sim):
        attack_multiplier = self.tick_damage[tick]
        tot_def = self.unit.base_def * (1 + self.unit.live_pct_def) + self.unit.live_flat_def
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        dmg = 1 + self.unit.live_all_dmg + self.unit.live_geo_dmg + self.unit.live_skill_dmg + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_geo_res")
        defence = (100 + self.unit.level) / ((100 + self.unit.level) + sim.enemy.live_defence)
        damage = attack_multiplier * tot_def * tot_crit_mult * dmg * (1 - res) * defence * self.scaling
        return damage


class AlbedoC2(Ability):
    def __init__(self, unit, sim):
        super().__init__(unit, "burst")
        self.tick_damage = [0.3 * unit.c2_stacks] * 8
        self.tick_times = [x + sim.time_into_turn for x in self.tick_times]
        self.tick_units = [0] * 8
        self.scaling = 1

    def calculate_tick_damage(self, tick, sim):
        attack_multiplier = self.tick_damage[tick]
        tot_def = self.unit.base_def * (1 + self.unit.live_pct_def) + self.unit.live_flat_def
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        dmg = 1 + self.unit.live_all_dmg + self.unit.live_geo_dmg + self.unit.live_skill_dmg + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_geo_res")
        defence = (100 + self.unit.level) / ((100 + self.unit.level) + sim.enemy.live_defence)
        damage = attack_multiplier * tot_def * tot_crit_mult * dmg * (1 - res) * defence * self.scaling
        return damage


AlbedoArtifact = Artifact("Archaic Petra", "pct_def", "geo_dmg", "crit_rate", 5)

AlbedoF2P = Albedo(90, 0, "Primordial Jade Cutter", 1, AlbedoArtifact, [6, 6, 6])


def main():
    print(AlbedoTest.live_base_atk)
    print(AlbedoTest.static_buffs)


if __name__ == '__main__':
    main()
