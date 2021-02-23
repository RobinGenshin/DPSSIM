from core.unit import Char
from core.read_data import buff_dict
import copy


class Barbara(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Barbara", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.a4_stacks = 0

    def barbara_a2(self, _, sim):
        self.live_stam_save += sim.turn_time

        if self.constellation >= 2:
            for unit in sim.units:
                unit.live_hydro_dmg += 0.15

    def barbara_a4_1(self, _, sim, __):
        self.a4_stacks = 0
        for unit in sim.units:
            unit.triggerable_buffs["Barbara_A4_2"] = copy.deepcopy(buff_dict["Barbara_A4_2"])
            unit.triggerable_buffs["Barbara_A4_2"].time_remaining = 15
            unit.triggerable_buffs["Barbara_A4_2"].source = self

    ## Barbara A4_2 ## Instant ## Particle ##
    def barbara_a4_2(self, _, sim, __):
        if self.a4_stacks == 5:
            pass
        else:
            for unit in sim.units:
                unit.active_buffs["Barbara_A2"].time_remaining += 1
                unit.triggerable_buffs["Barbara_A4_2"].time_remaining += 1

    ## Barbara C1 ## Instant ## Any
    def barbara_c1(self, _, __, ___):
        self.current_energy += 1
        self.triggerable_buffs["Barbara_C1"].live_cd = 10

    ## Barbara C4 ## Instant ## Onhit ## Charged
    def barbara_c4(self, _, __, ___):
        self.current_energy += 1

    def barbara_c2_1(self):
        self.skill_cdr *= 0.85


BarbaraTest = Barbara(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(BarbaraTest.live_base_atk)
    print(BarbaraTest.static_buffs)


if __name__ == '__main__':
    main()