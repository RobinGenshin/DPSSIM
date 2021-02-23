from core.unit import Char
from core.action import Ability, Combo, Action
from core.read_data import buff_dict
import copy

class Ganyu(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Ganyu", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.c6_reset_stack = False

    # Static
    def ganyu_c2(self):
        self.skill_charges += 1

    # Active
    def ganyu_a2(self, _, __):
        self.live_charged_crit_rate += 0.2

    @staticmethod
    def ganyu_a4(unit_obj, _):
        unit_obj.live_cryo_dmg += 0.2

    def ganyu_c1_1(self, _, __, ___):
        self.live_burst_energy_cost += 2

    @staticmethod
    def ganyu_c4(unit_obj, _):
        unit_obj.live_all_dmg += 0.15

    def ganyu_c6(self, _, __, ___):
        self.c6_reset_stack = 1
        self.active_buffs["Ganyu_C6_2"] = copy.deepcopy(buff_dict["Ganyu_C6_2"])
        self.active_buffs["Ganyu_C6_2"].source = self

    def ganyu_c6_2(self, _, __):
        if self.c6_reset_stack == 1:
            self.live_charged_tick_times = [26/60,49/60]
            self.live_charged_cancel = 26/60
            self.live_charged_swap = 26/60
            self.live_charged_skill = 26/60
            self.live_charged_attack = 26/60
            self.triggerable_buffs["Ganyu_C6_3"] = copy.deepcopy(buff_dict["Ganyu_C6_3"])
            self.triggerable_buffs["Ganyu_C6_3"].time_remaining = 30
            self.triggerable_buffs["Ganyu_C6_3"].source = self
        else:
            del self.active_buffs["Ganyu_C6_2"]

    ## Ganyu C6 3 ## Instant ##
    def ganyu_c6_3(self, _, __, ___):
        if self.c6_reset_stack == 1:
            self.c6_reset_stack = 0
            print("C6 GANYU PROC")
            del self.active_buffs["Ganyu_C6_2"]
            del self.triggerable_buffs["Ganyu_C6_3"]


GanyuTest = Ganyu(90, 6, "Harbinger of Dawn", 5, "Noblesse", [10, 10, 10])


def main():
    print(GanyuTest.live_base_atk)
    print(GanyuTest.static_buffs)


if __name__ == '__main__':
    main()
