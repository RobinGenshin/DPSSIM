from core.unit import Char
from core.artifact import Artifact


class Lisa(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Lisa", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def lisa_c4(self):
        pass

    def lisa_c5(self):
        pass

    ## Lisa C1 ## Instant ## Onhit ## Skill
    def lisa_c1(self, _, __, ___):
        self.current_energy += 2

    def lisa_c6(self, _, __, ___):
        pass


LisaArtifact = Artifact("Noblesse", "pct_atk", "electro_dmg", "crit_rate", 30)

LisaF2P = Lisa(90, 0, "Favonius Codex", 1, LisaArtifact, [6, 6, 6])


def main():
    print(LisaTest.live_base_atk)
    print(LisaTest.static_buffs)


if __name__ == '__main__':
    main()
