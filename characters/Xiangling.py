from core.unit import Char
from core.read_data import buff_dict
from core.action import Combo
from core.artifact import Artifact
import copy


class Xiangling(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Xiangling", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.a4_pickup = None

    # Static
    def xiangling_c4(self):
        pass

    # Active
    def xiangling_a4_cast(self, _, sim, __):
        for unit in sim.units:
            unit.active_buffs["Xiangling_A4_Trigger"] = copy.copy(buff_dict["Xiangling_A4_Trigger"])
            unit.active_buffs["Xiangling_A4_Trigger"].source = self
            unit.active_buffs["Xiangling_A4_Buff_1"] = copy.copy(buff_dict["Xiangling_A4_Buff_1"])
            unit.active_buffs["Xiangling_A4_Buff_1"].source = self
            unit.active_buffs["Xiangling_A4_Buff_2"] = copy.copy(buff_dict["Xiangling_A4_Buff_2"])
            unit.active_buffs["Xiangling_A4_Buff_2"].source = self

    ## Xianling A4 Trigger ## Duration ## Postcast
    def xiangling_a4_trigger(self, _, sim):
        self.a4_pickup = sim.chosen_unit

    def xiangling_a4_buff_1(self, unit_obj, _):
        if unit_obj == self.a4_pickup:
            unit_obj.live_pct_atk -= 0.1

    def xiangling_a4_buff_2(self, unit_obj, _):
        if unit_obj == self.a4_pickup:
            unit_obj.live_pct_atk += 0.1

    def xiangling_c2(self, _, sim, action):
        if action[1] == 8 and action[0].loop == True:
            proc = XianglingC2(self, action[0].combo)
            proc.add_to_damage_queue(sim)

    @staticmethod
    def xiangling_c6(unit_obj, _):
        unit_obj.live_pyro_dmg += 0.15


class XianglingC2(Combo):
    def __init__(self, unit_obj, combo):
        super().__init__(unit_obj, combo)
        self.name = "Xiangling C2"
        self.tick_element = ["Pyro"]
        self.tick_times = [0]
        self.tick_damage = [0.6]
        self.tick_units = [1]
        self.tick_types = ["normal"]
        self.ticks = 1
        self.scaling = [1]
        self.loop = False


XianglingArtifact = Artifact("Noblesse", "pct_atk", "pyro_dmg", "crit_rate", 30)

XianglingF2P = Xiangling(90, 0, "Favonius Lance", 1, XianglingArtifact, [6, 6, 6])


def main():
    print(XianglingTest.live_base_atk)
    print(XianglingTest.static_buffs)


if __name__ == '__main__':
    main()
