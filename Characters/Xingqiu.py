from core.unit import Char
from core.read_data import buff_dict
from core.action import Ability
from math import fmod
import copy


class Xingqiu(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Xingqiu", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.q_tick = 0

    # Static
    def xingqiu_a4(self):
        self.hydro_dmg += 0.2

    def xingqiu_c4(self):
        self.skill_tick_damage = [x*1.5 for x in self.skill_tick_damage]

    def xingqiu_c6(self):
        pass

    # Active
    def xingqiu_q_cast(self, _, sim, __):
        self.q_tick = 0
        for unit in sim.units:
            unit.triggerable_buffs["Xingqiu_Q_Trigger"] = copy.copy(buff_dict["Xingqiu_Q_Trigger"])
            unit.triggerable_buffs["Xingqiu_Q_Trigger"].time_remaining = 15
            unit.triggerable_buffs["Xingqiu_Q_Trigger"].source = self

            if self.constellation >= 2:
                unit.triggerable_buffs["Xingqiu_Q_Trigger"].time_remaining = 18

    def xingqiu_q_trigger(self, _, sim, __):
        if self.constellation >= 6:
            if 0 == fmod(self.q_tick,3):
                action = XingqiuQTick(self, 2)
                action.add_to_damage_queue(sim)

            elif 1 == fmod(self.q_tick,3):
                action = XingqiuQTick(self, 3)
                action.add_to_damage_queue(sim)

            elif 2 == fmod(self.q_tick,3):
                action = XingqiuQTick(self, 5)
                action.add_to_damage_queue(sim)
                self.current_energy += 3
        else:
            if 0 == fmod(self.q_tick,2):
                action = XingqiuQTick(self, 2)
                action.add_to_damage_queue(sim)

            elif 1 == fmod(self.q_tick,2):
                action = XingqiuQTick(self, 3)
                action.add_to_damage_queue(sim)
        self.q_tick += 1
        for unit in sim.units:
            unit.triggerable_buffs["Xingqiu_Q_Trigger"].live_cd = 1


class XingqiuQTick(Ability):
    def __init__(self, unit_obj, ticks):
        super().__init__(unit_obj, "burst")
        self.ticks = ticks
        self.element = "Hydro"
        self.tick_element = ["Hydro"] * ticks
        self.tick_times = [0.25] * ticks
        self.tick_damage = [0.453] * ticks
        self.tick_units = [0] * ticks
        self.tick_units[0] = 1
        self.tick_scaling = [self.tick_scaling[0]] * ticks
        self.tick_types = ["burst"] * ticks
        self.tick_used = ["no"] * ticks


XingqiuTest = Xingqiu(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(XingqiuTest.live_base_atk)
    print(XingqiuTest.static_buffs)


if __name__ == '__main__':
    main()
