from core.unit import Char
from core.artifact import Artifact


class Diona(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Diona", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def diona_c2(self):
        self.skill_dmg += 0.075

    # Active
    @staticmethod
    def diona_a2(unit_obj, _):
        unit_obj.live_stam_save += 0.1

    def diona_c1(self, _, __, ___):
        self.current_energy += 15

    def diona_c4(self, _, __):
        self.live_charged_speed += 0.6

    @staticmethod
    def diona_c6(unit_obj, _):
        unit_obj.live_ele_m += 200


DionaArtifact = Artifact("Noblesse", "pct_atk", "cryo_dmg", "crit_rate", 30)

DionaF2P = Diona(90, 0, "Favonius Warbow", 1, DionaArtifact, [6, 6, 6])


def main():
    print(DionaTest.live_base_atk)
    print(DionaTest.static_buffs)


if __name__ == '__main__':
    main()
