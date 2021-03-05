from core.unit import Char
from core.artifact import Artifact


class Jean(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Jean", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def jean_a4(self, _, __, ___):
        self.current_energy += 16

    def jean_c1(self, _, __, ___):
        pass

    @staticmethod
    def jean_c2(unit_obj, __):
        unit_obj.live_normal_speed += 0.15


JeanArtifact = Artifact("Viridescent Venerer", "pct_atk", "anemo_dmg", "crit_rate", 30)

JeanF2P = Jean(90, 0, "Favonius Sword", 1, JeanArtifact, [6, 6, 6])



def main():
    print(JeanTest.live_base_atk)
    print(JeanTest.static_buffs)


if __name__ == '__main__':
    main()

