from core.unit import Char
from core.read_data import buff_dict, ele_ratio_dict
import copy


class Bennett(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Bennett", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.snapshot_buff = 0

    def bennett_q_cast(self, _, sim, __):
        atk_buff_mult = ele_ratio_dict[self.burst_level] * 0.56

        # Bennett C1 #
        if self.constellation >= 1:
            atk_buff_mult += 0.2

        self.snapshot_buff = atk_buff_mult * self.base_atk

        for unit in sim.units:
            unit.active_buffs["Bennett_Q_Buff"] = copy.deepcopy(buff_dict["Bennett_Q_Buff"])
            unit.active_buffs["Bennett_Q_Buff"].source = self

    def bennett_q_buff(self, _, sim):
        for unit in sim.units:
            unit.live_flat_atk += self.snapshot_buff

        self.live_skill_cdr *= 0.5

    def bennett_a2(self):
        self.skill_cdr *= 0.8

    def bennett_c4(self):
        pass

    @staticmethod
    def bennett_c6(unit, _):
        if unit.weapon_type in {"Claymore", "Polearm", "Sword"}:
            unit.live_pyro_dmg += 0.15
            unit.live_normal_type = "Pyro"
            unit.live_charged_type = "Pyro"


BennettTest = Bennett(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(BennettTest.live_base_atk)
    print(BennettTest.static_buffs)


if __name__ == '__main__':
    main()
