from core.unit import Char
from core.action import Ability
from core.artifact import Artifact
import copy

class Amber(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Amber", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # StaticEffect
    def amber_a2(self):
        self.burst_crit_rate += 0.1

    # ActiveEffect
    def amber_a4(self):
        self.live_pct_atk += 0.15

    # StaticEffect
    def amber_c1(self):
        self.charged_ticks += 1
        self.charged_tick_times.append(self.charged_tick_times[0] + 0.1)
        self.charged_tick_damage.append(1.24 * 0.2)
        self.charged_tick_units.append(1)
        self.charged_tick_hitlag.append(0)

    # ActiveEffect
    def amber_c2(self, _, sim, __):
        for action in sim.floating_actions:
            if action.name == "Amber skill" and action.action_type == "damage" and action.loop == True:
                flat_dmg = AmberC2(self)
                flat_dmg.add_to_damage_queue(sim)
                print("BOOM!")
                action.tick_times = [sim.time_into_turn]
                action.update_time()
                for energy in copy.copy(sim.floating_actions):
                    if energy.name == "Amber skill" and energy.action_type == "energy":
                        energy.energy_times = [sim.time_into_turn + 2]
                        energy.update_time()

    # StaticEffect
    def amber_c4(self):
        self.skill_charges += 1
        self.skill_cdr *= 0.8

    # ActiveEffect
    @staticmethod
    def amber_c6(unit, _):
        unit.live_pct_atk += 0.15


class AmberC2(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "skill")
        self.name = "Amber C2"
        self.tick_damage = [2]
        self.tick_scaling = [1]
        self.tick_units = [0]
        self.tick_times = [0]
        self.loop = False


AmberArtifact = Artifact("Noblesse", "pct_atk", "pyro_dmg", "crit_rate", 30)

AmberF2P = Amber(90, 0, "The Stringless", 1, AmberArtifact, [6, 6, 6])


def main():
    print(AmberTest.live_base_atk)
    print(AmberTest.static_buffs)


if __name__ == '__main__':
    main()