from core.unit import Char
from core.action import Ability
from math import fmod
from core.scaling import ratio_type
from core.artifact import Artifact
from core.read_data import buff_dict
import copy

class Klee(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Klee", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.a2_stack = 0
        self.greedy = True
        self.spark = False
        self.c1_stack = 0
        self.selfish_mode = False

    def klee_q(self, _, sim):
        self.active_buffs["Klee_Q"].time_remaining = sim.encounter_limit
        if "Klee_Q_2" not in self.active_buffs:
            self.selfish_mode = False

    def klee_q_1(self, _, __, ___):
        self.active_buffs["Klee_Q_2"] = copy.copy(buff_dict["Klee_Q_2"])
        self.active_buffs["Klee_Q_2"].source = self
        self.selfish_mode = True

    def klee_q_2(self, _, sim):
        if self != sim.chosen_unit:
            self.selfish_mode = False
            del self.active_buffs["Klee_Q_2"]
        self.selfish_mode = True

    def klee_a2_1(self, _, __, ___):
        self.a2_stack += 1

        if 0 == fmod(self.a2_stack, 2):
            self.spark = True
            self.triggerable_buffs["Klee_A2_1"].live_cd = 4

    def klee_a2_2(self, _, __, ___):
        if self.spark:
            self.live_charged_dmg += 0.5
            self.spark = False

    @staticmethod
    def klee_a4(unit_obj, _, __):
        unit_obj.current_energy += 2

    def klee_c1(self, _, sim, __):
        self.c1_stack += 1

        if 0 == fmod(self.c1_stack, 3):
            print("Klee C1 Proc")
            c1_proc = KleeC1(self)
            c1_proc.update_time()
            c1_proc.add_to_damage_queue(sim)
            # print("DAMAGE: " + str(c1_proc.calculate_damage_snapshot(sim)))
            # print(c1_proc.tick_damage)

    ## Klee C4 ## Instant ## Onhit ## Any
    def klee_c4(self, unit_obj, sim, extra):
        pass

    ## Klee C6 1 ## Duration ##
    def klee_c6_1(self, _, __):
        pass

    @staticmethod
    def klee_c6_2(unit_obj, _):
        unit_obj.live_pyro_dmg += 0.1


class KleeC1(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "skill")
        self.name = "Klee C1"
        self.ticks = 1
        self.tick_scaling = [ratio_type(unit_obj, "burst")[getattr(unit_obj, "burst_level")]]
        self.tick_times = [0.5]
        self.tick_damage = [0.464 * 1.2]
        self.tick_units = [0]


KleeArtifact = Artifact("Crimson Witch", "pct_atk", "pyro_dmg", "crit_rate", 30)
KleeF2P = Klee(90, 0, "Solar Pearl", 1, KleeArtifact, [6, 6, 6])


def main():
    print(KleeF2P.live_base_atk)
    print(KleeF2P.static_buffs)


if __name__ == '__main__':
    main()