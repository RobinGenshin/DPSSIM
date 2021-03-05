from core.unit import Char
from core.read_data import buff_dict
from core.action import Action
from core.artifact import Artifact


class Zhongli(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Zhongli", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def zhongli_a4_normal(self, _, sim, __):
        a4_dmg = ZhongliA4(self, "normal")
        a4_dmg.add_to_damage_queue(sim)

    ## Zhongli A4 Charged ## Instant ## Onhit ## Charged
    def zhongli_a4_normal(self, _, sim, __):
        a4_dmg = ZhongliA4(self, "charged")
        a4_dmg.add_to_damage_queue(sim)

    ## Zhongli A4 Skill ## Instant ## Onhit ## Charged
    def zhongli_a4_normal(self, _, sim, __):
        a4_dmg = ZhongliA4(self, "skill")
        a4_dmg.add_to_damage_queue(sim)

    ## Zhongli A4 Burst ## Instant ## Onhit ## Charged
    def zhongli_a4_normal(self, _, sim, __):
        a4_dmg = ZhongliA4(self, "burst")
        a4_dmg.add_to_damage_queue(sim)


class ZhongliA4(Action):
    def __init__(self, unit_obj, talent):
        super().__init__(unit_obj)
        self.name = "Zhongli A4 (" + talent + ")"
        self.ticks = 1
        self.tick_scaling = [1]
        if talent == "normal" or talent == "charged":
            self.tick_damage = [0.0139]
            self.tick_element = [unit_obj.live_normal_type]
        elif talent == "skill":
            self.tick_damage = [0.019]
            self.tick_element = ["Geo"]
        elif talent == "burst":
            self.tick_damage = [0.33]
            self.tick_element = ["Geo"]
        self.tick_times = [0]
        self.tick_used = ["no"]
        self.tick_scaling = [1]
        self.tick_units = [0]
        self.tick_types = [talent]
        self.snapshot_tot_atk = unit_obj.base_hp * (1 + unit_obj.pct_hp) + unit_obj.flat_hp


ZhongliArtifact = Artifact("Archaic Petra", "pct_atk", "geo_dmg", "crit_rate", 30)

ZhongliF2P = Zhongli(90, 0, "Favonius Lance", 1, ZhongliArtifact, [6, 6, 6])


def main():
    print(ZhongliTest.live_base_atk)
    print(ZhongliTest.static_buffs)

if __name__ == '__main__':
    main()
