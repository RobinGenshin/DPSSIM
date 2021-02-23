from core.unit import Char


class Qiqi(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Qiqi", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def qiqi_c1(self, unit_obj, sim, extra):
        pass

    def qiqi_c2(self, _, sim, __):
        if sim.enemy.element == "Cryo":
            self.live_normal_cond_dmg += 0.15
            self.live_charged_cond_dmg += 0.15


QiqiTest = Qiqi(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(QiqiTest.live_base_atk)
    print(QiqiTest.static_buffs)


if __name__ == '__main__':
    main()
