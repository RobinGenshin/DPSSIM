from core.unit import Char
from core.action import Ability
from core.artifact import Artifact


class Chongyun(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Chongyun", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    @staticmethod
    def chongyun_e(unit_obj):
        unit_obj.live_normal_type = "Cryo"
        unit_obj.live_charged_type = "Cryo"

    @staticmethod
    def chongyun_a2(unit_obj):
        unit_obj.live_normal_speed += 0.08

    def chongyun_c1(self, _, sim, action):
        if action[1] == 3:
            proc = Ability(self, "normal")
            proc.tick_element = "Cryo"
            proc.tick_times = [sim.time_into_turn + 0.5, sim.time_into_turn + 0.6, sim.time_into_turn + 0.7]
            proc.tick_damage = [0.5, 0.5, 0.5]
            proc.tick_units = [1, 0, 0]
            proc.ticks = 3
            proc.scaling = 1
            sim.floating_actions.add(proc)

    @staticmethod
    def chongyun_c2(unit_obj):
        unit_obj.live_skill_cdr *= 0.85
        unit_obj.live_burst_cdr *= 0.85

    def chongyun_c4(self, _, sim, ___):
        if sim.enemy.element == "Cryo":
            self.live_burst_energy_cost += 1
            self.triggerable_buffs["Chongyun_C4"].live_cd = 2

    def chongyun_c6(self):
        self.burst_ticks = 4
        self.burst_tick_times.append(self.burst_tick_times[2]+0.05)
        self.burst_tick_damage.append(1.424)
        self.burst_tick_units.append(1)
        self.burst_dmg += 0.075


ChongyunArtifact = Artifact("Noblesse", "recharge", "pyro_dmg", "crit_rate", 30)

ChongyunF2P = Chongyun(90, 0, "Festering Desire", 5, ChongyunArtifact, [6, 6, 6])


def main():
    print(ChongyunTest.live_base_atk)
    print(ChongyunTest.static_buffs)


if __name__ == '__main__':
    main()
