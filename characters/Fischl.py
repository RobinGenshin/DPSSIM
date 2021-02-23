from core.unit import Char
from core.action import Ability, Combo, Action
from core.read_data import buff_dict
from core.artifact import Artifact
import copy

class Fischl(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Fischl", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def fischl_c6_3(self):
        self.skill_ticks = 12
        self.skill_tick_times.extend([11.5,12.5])
        self.skill_tick_damage.extend([0.88,0.88])
        self.skill_tick_units.extend([1,0])

    # Active
    def fischl_e(self, _, __, ___):
        self.current_burst_cd = 12

    def fischl_q_1(self, _, __, ___):
        self.current_skill_cd = 12

    def fischl_q_2(self, _, sim, __):
        action = Ability(self, "skill")

        action.tick_times = [x+2 for x in action.tick_times]
        action.energy_times = [x+4 for x in action.tick_times]
        action.update_time()
        action.add_to_damage_queue(sim)
        action.add_to_energy_queue(sim)

    def fischl_c1(self, _, sim, extra):
        if any((x.unit.character == "Fischl" and x.talent == "skill" and x.action_type == "damage") for x in sim.floating_actions) == False:
            if extra[0].loop:
                action = FischlC1(self, sim, extra[0].combo)
                action.update_time()
                action.add_to_damage_queue(sim)

    def fischl_c2(self, _, sim, extra):
        if extra[0].loop:
            action = FischlC2(self, sim)
            action.update_time()
            action.add_to_damage_queue(sim)
            extra[0].loop = False
            print("Fischl C2 Proc")

    def fischl_c4(self, _, sim, extra):
        if extra[0].loop:
            action = FischlC4(self, sim)
            action.update_time()
            extra[0].loop = False
            action.add_to_damage_queue(sim)

    def fischl_c6_1(self, _, sim, __):
        for unit in sim.units:
            unit.triggerable_buffs["Fischl_C6_2"] = copy.copy(buff_dict["Fischl_C6_2"])
            unit.triggerable_buffs["Fischl_C6_2"].time_remaining = 12
            unit.triggerable_buffs["Fischl_C6_2"].source = self

    def fischl_c6_2(self, _, sim, extra):
        if any((x.unit.character == "Fischl" and x.talent == "skill" and x.action_type == "damage") for x in sim.floating_actions) == True:
            if extra[0].loop:
                action = FischlC6(self, sim)
                action.update_time()
                action.add_to_damage_queue(sim)


class FischlC1(Combo):
    def __init__(self, unit_obj, sim, combo):
        super().__init__(unit_obj, combo)
        self.name = "Fischl C1"
        self.ticks = 1
        self.element = "Electro"
        self.tick_element = ["Electro"]
        self.tick_scaling = [1]
        self.tick_types = ["normal"]
        self.tick_times = [sim.time_into_turn]
        self.tick_damage = [0.22]
        self.tick_units = [0]
        self.tick_used = ["no"]
        self.loop = False


class FischlC2(Ability):
    def __init__(self, unit_obj, sim):
        super().__init__(unit_obj, "skill")
        self.name = "Fischl C2"
        self.ticks = 1
        self.element = "Electro"
        self.tick_element = ["Electro"]
        self.tick_scaling = [1]
        self.tick_types = ["skill"]
        self.tick_times = [sim.time_into_turn]
        self.tick_damage = [2]
        self.tick_units = [0]
        self.loop = False


class FischlC4(Ability):
    def __init__(self, unit_obj, sim):
        super().__init__(unit_obj, "burst")
        self.name = "Fischl C4"
        self.ticks = 1
        self.element = "Electro"
        self.tick_element = ["Electro"]
        self.tick_scaling = [1]
        self.tick_types = ["burst"]
        self.tick_times = [sim.time_into_turn]
        self.tick_damage = [2.22]
        self.tick_units = [0]
        self.loop = False

class FischlC6(Ability):
    def __init__(self, unit_obj, sim):
        super().__init__(unit_obj, "skill")
        self.name = "Fischl C6"
        self.ticks = 1
        self.element = "Electro"
        self.tick_element = ["Electro"]
        self.tick_scaling = [1]
        self.tick_types = ["normal"]
        self.tick_times = [sim.time_into_turn]
        self.tick_damage = [0.3]
        self.tick_units = [0]
        self.tick_used = ["no"]
        self.loop = False


FischlArtifact = Artifact("Thundering Fury", "pct_atk", "electro_dmg", "crit_rate", 30)

FischlF2P = Fischl(90, 0, "The Stringless", 1, FischlArtifact, [6, 6, 6])


def main():
    print(FischlTest.live_base_atk)
    print(FischlTest.static_buffs)


if __name__ == '__main__':
    main()
