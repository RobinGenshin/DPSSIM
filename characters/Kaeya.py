from core.unit import Char
from core.action import Ability
from core.artifact import Artifact


class Kaeya(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Kaeya", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def kaeya_c6_1(self):
        self.burst_ticks = 16
        self.burst_tick_times.extend([8.217+0.666, 8.217+0.666*2, 8.217+0.666*3, 8.217*4])
        self.burst_tick_times = [x*(3/4) for x in self.burst_tick_times]
        self.burst_tick_damage.extend([0.776,0.776, 0.776, 0.776])
        self.burst_tick_units.extend([0, 1, 0, 1])

    # Active
    def kaeya_a4(self, _, sim, reaction):
        if reaction[0] == "frozen":
            energy = Ability(self, "skill")
            energy.energy_times = [sim.time_into_turn+2]
            energy.update_time()
            energy.add_to_energy_queue(sim)

    def kaeya_c1(self, _, sim, __):
        if "Cryo" in sim.enemy.elements or "Frozen" in sim.enemy.elements:
            self.live_normal_cond_crit_rate += 0.15
            self.live_charged_cond_crit_rate += 0.15

    def kaeya_c2(self, unit_obj, sim, extra):
        pass

    def kaeya_c6_2(self, _, __, ___):
        self.current_energy += 15


KaeyaArtifact = Artifact("Noblesse", "recharge", "cryo_dmg", "crit_rate", 30)

KaeyaF2P = Kaeya(90, 0, "Favonius Sword", 5, KaeyaArtifact, [6, 6, 6])


def main():
    print(KaeyaTest.live_base_atk)
    print(KaeyaTest.static_buffs)


if __name__ == '__main__':
    main()
