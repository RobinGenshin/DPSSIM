from core.unit import Char
from core.read_data import buff_dict
from core.action import Combo
from core.scaling import ratio_type
from core.artifact import Artifact
import copy


class Sucrose(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Sucrose", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def sucrose_c1(self):
        self.skill_charges += 1

    def sucrose_c2(self):
        self.burst_ticks += 1
        self.burst_tick_times.append(self.burst_tick_times[2]+2)
        self.burst_tick_damage.append(1.48)
        self.burst_tick_units.append(1)

    # Active
    def sucrose_q(self, unit_obj, sim, reaction):
        if reaction[0] == "swirl":
            if not hasattr(reaction[2], "infused"):
                reaction[2].infused = True
                infuse = copy.copy(reaction[2])
                infuse.element = reaction[1]
                infuse.tick_damage = [0.44 for x in infuse.tick_damage]
                infuse.add_to_damage_queue(sim)

                if unit_obj.constellation >= 6:
                    for unit in sim.units:
                        unit.active_buffs["Sucrose_C6"] = copy.copy(
                            buff_dict.get("Sucrose_C6_" + reaction[1].lower()))
                        unit.active_buffs["Sucrose_C6"].source = self

    def sucrose_a2_1(self, _, sim, reaction):
        if reaction[0] == "swirl":
            for unit in sim.units:
                if reaction[1] == unit.element.lower():
                    unit.active_buffs["Sucrose_A2_2"] = copy.deepcopy(buff_dict["Sucrose_A2_2"])
                    unit.active_buffs["Sucrose_A2_2"].source = self

    @staticmethod
    def sucrose_a2_2(unit_obj, _):
        unit_obj.live_ele_m += 50

    def sucrose_a4_1(self, unit_obj, _):
        em_buff = self.live_ele_m * 0.2
        unit_obj.live_ele_m += em_buff

    def sucrose_c4(self, _, __, ___):
        self.live_skill_cd = max(0, self.live_skilL_cd - (4 / 7))


SucroseArtifact = Artifact("Viridiscent Venerer", "recharge", "anemo_dmg", "crit_rate", 30)

SucroseF2P = Sucrose(90, 0, "Sacrificial Fragments", 1, SucroseArtifact, [6, 6, 6])



def main():
    print(SucroseTest.live_base_atk)
    print(SucroseTest.static_buffs)


if __name__ == '__main__':
    main()
