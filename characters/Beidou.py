from core.unit import Char
from core.read_data import buff_dict
from core.action import Ability, Combo
from core.artifact import Artifact
import copy


class Beidou(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Beidou", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # ActiveEffect
    def beidou_q_cast(self, _, sim, __):
        for unit in sim.units:
            unit.triggerable_buffs["Beidou_Q_Trigger"] = copy.deepcopy(buff_dict["Beidou_Q_Trigger"])
            unit.triggerable_buffs["Beidou_Q_Trigger"].time_remaining = 15
            unit.triggerable_buffs["Beidou_Q_Trigger"].source = self

    # ActiveEffect
    def beidou_q_trigger(self, _, sim, __):
        action = BeidouQ(self)
        action.update_time()
        action.add_to_damage_queue(sim)

        for unit in sim.units:
            unit.triggerable_buffs["Beidou_Q_Trigger"].live_cd = 1

    # ActiveEffect
    def beidou_a4(self, _, __):
        self.live_normal_dmg += 0.15
        self.live_charged_dmg += 0.15
        self.live_normal_speed += 0.15
        self.live_charged_speed += 0.15

    # ActiveEffect
    def beidou_c4(self, _, sim, extra):
        if extra[0].loop:
            c4_proc = BeidouC4(self, sim, extra[0].combo)
            c4_proc.update_time()
            c4_proc.add_to_damage_queue(sim)


class BeidouQ(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "burst")
        self.name = "Beidou Q Proc"
        self.ticks = 1
        self.tick_damage = [0.96]
        self.tick_times = [0]
        self.tick_units = [1]


class BeidouC4(Combo):
    def __init__(self, unit_obj, _, combo):
        super().__init__(unit_obj, combo)
        self.name = "Beidou C4 Proc"
        self.ticks = 1
        self.tick_element = ["Electro"]
        self.scaling = [1]
        self.tick_types = ["normal"]
        self.tick_times = [0]
        self.tick_damage = [0.2]
        self.tick_units = [1]
        self.loop = False


BeidouArtifact = Artifact("Noblesse", "pct_atk", "electro_dmg", "crit_rate", 30)

BeidouF2P = Beidou(90, 0, "Favonius Greatsword", 1, BeidouArtifact, [6, 6, 6])


def main():
    print(BeidouTest.live_base_atk)
    print(BeidouTest.static_buffs)


if __name__ == '__main__':
    main()

