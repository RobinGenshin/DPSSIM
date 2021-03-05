from core.unit import Char
from core.artifact import Artifact


class Qiqi(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Qiqi", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def qiqi_c1(self, unit_obj, sim, extra):
        pass

    def qiqi_c2(self, _, sim, __):
        if "Cryo" in sim.enemy.elements or "Frozen" in sim.enemy.elements:
            self.live_normal_cond_dmg += 0.15
            self.live_charged_cond_dmg += 0.15


QiqiArtifact = Artifact("Noblesse", "recharge", "cryo_dmg", "crit_rate", 30)

QiqiF2P = Qiqi(90, 0, "Sacrificial Sword", 5, QiqiArtifact, [6, 6, 6])


def main():
    print(QiqiTest.live_base_atk)
    print(QiqiTest.static_buffs)


if __name__ == '__main__':
    main()
