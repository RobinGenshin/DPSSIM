from core.unit import Char
from core.read_data import buff_dict
from core.action import Ability
from core.artifact import Artifact


class Xinyan(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Xinyan", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def xinyan_c6(self):
        pass

    # Active
    @staticmethod
    def xinyan_a4(unit_obj, sim):
        if unit_obj == sim.chosen_unit:
            unit_obj.live_physical_dmg += 0.15

    def xinyan_c1(self, _, __):
        self.live_normal_speed += 0.15
        self.live_charged_speed += 0.15

    def xinyan_c2(self, _, sim, ___):
        c2 = XinyanC2(self)
        c2.add_to_damage_queue(sim)

    def xinyan_q(self, _, sim, __):
        phys_dmg = XinyanPhysQ(self)
        phys_dmg.add_to_damage_queue(sim)


class XinyanPhysQ(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "burst")
        self.name = "Xinyan Physical Q"
        self.ticks = 1
        self.tick_damage = [3.404]
        self.tick_times = [1.6]
        self.tick_units = [0]
        self.tick_types = ["burst"]
        self.tick_element = ["Physical"]
        if unit_obj.constellation >= 2:
            self.snapshot_crit_rate = 1


class XinyanC2(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "skill")
        self.ticks = 6
        self.tick_damage = [0.336, 0.336, 0.336, 0.336, 0.336, 0.336]
        self.tick_units = [1, 1, 1, 1, 1, 1]
        self.tick_times = [2.083, 4.100, 6.100, 8.000, 10.000, 12.000]
        self.tick_used = ["no"] * 6
        self.tick_types = ["skill"] * 6
        self.tick_element = ["Pyro"] * 6
        self.tick_scaling = [self.tick_scaling[0]] * 6


XinyanArtifact = Artifact("Noblesse", "pct_atk", "pyro_dmg", "crit_rate", 30)

XinyanF2P = Xinyan(90, 0, "Favonius Greatsword", 1, XinyanArtifact, [6, 6, 6])


def main():
    print(XinyanTest.live_base_atk)
    print(XinyanTest.static_buffs)
    print(buff_dict["Xinyan_C1"])

if __name__ == '__main__':
    main()
