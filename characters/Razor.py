from core.unit import Char
from core.read_data import buff_dict, razor_qas_ratio_dict
from core.action import Combo
from core.scaling import ratio_type
import copy


class Razor(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Razor", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.electro_sigil = 0
        self.snapshot_buff = 0

    # Static
    def razor_a2_1(self):
        self.skill_cd *= 0.82

    def razor_c2(self):
        self.crit_rate += 0.03

    # Active
    def razor_e(self, _, __, ___):
        if self.electro_sigil == 3:
            pass
        else:
            self.electro_sigil += 1

    def razor_q_1(self, _, __, ___):
        self.current_energy += 5 * self.electro_sigil
        self.electro_sigil = 0

        self.snapshot_buff = razor_qas_ratio_dict[self.burst_level] * 0.26
        self.active_buffs["Razor_Q_2"] = copy.copy(buff_dict["Razor_Q_2"])
        self.active_buffs["Razor_Q_2"].source = self
        self.triggerable_buffs["Razor_Q_3"] = copy.copy(buff_dict["Razor_Q_3"])
        self.triggerable_buffs["Razor_Q_3"].time_remaining = 18
        self.triggerable_buffs["Razor_Q_3"].source = self

    def razor_q_2(self, _, sim):
        self.live_normal_speed += self.snapshot_buff
        if self != sim.chosen_unit:
            del self.active_buffs["Razor_Q_2"]
            del self.triggerable_buffs["Razor_Q_3"]

    def razor_q_3(self, _, sim, action):
        if action[0].loop:
            razor_q = RazorQ(self, action[0].combo, action[1])
            razor_q.add_to_damage_queue(sim)
            print("Proced Razor Q")

    def razor_a2_2(self, _, __, ___):
        self.live_skill_cd = 0

    def razor_c1(self, _, __, ___):
        self.live_all_dmg += 0.1

    def razor_c6(self, _, sim, action):
        razor_c6 = RazorC6(self, action[0].combo)
        razor_c6.add_to_damage_queue(sim)
        print("Proced Razor C6")
        self.triggerable_buffs["Razor_C6"].live_cd = 10
        if "Razor_Q_2" not in self.active_buffs and self.electro_sigil < 3:
            self.electro_sigil += 1


class RazorQ(Combo):
    def __init__(self, unit_obj, combo, tick):
        super().__init__(unit_obj, combo)
        self.ticks = 1
        self.name = "Razor Q"
        self.element = "Electro"
        self.tick_element = ["Electro"]
        self.tick_scaling = [ratio_type(unit_obj, "burst")[unit_obj.burst_level]]
        self.tick_types = ["normal"]
        self.tick_times = [0]
        self.tick_damage = [0.24 * self.tick_damage[tick]]
        self.tick_units = [1]
        self.loop = False


class RazorC6(Combo):
    def __init__(self, unit_obj, combo):
        super().__init__(unit_obj, combo)
        self.ticks = 1
        self.name = "Razor C6"
        self.element = "Electro"
        self.tick_element = ["Electro"]
        self.tick_scaling = [1]
        self.tick_types = ["normal"]
        self.tick_times = [0]
        self.tick_damage = [1]
        self.tick_units = [1]
        self.loop = False


RazorTest = Razor(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(RazorTest.live_base_atk)
    print(RazorTest.static_buffs)


if __name__ == '__main__':
    main()
