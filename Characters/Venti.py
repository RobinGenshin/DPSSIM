from core.unit import Char
from core.read_data import debuff_dict
from core.artifact import Artifact
import copy


class Venti(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Venti", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def venti_c1(self):
        self.charged_ticks += 2
        self.charged_tick_times.extend([self.burst_tick_times[0]+0.1, self.burst_tick_times[0]+0.1])
        self.charged_tick_times.extend([self.burst_tick_times[0]+0.15, self.burst_tick_times[0]+0.15])
        self.charged_tick_damage.extend([124/300, 124/300])
        self.charged_tick_units.extend([0, 0])
        self.charged_tick_hitlag.extend([0, 0])
        self.charged_stamina_cost.extend([0, 0])

    # Active
    def venti_q(self, _, sim, reaction):
        if reaction[0] == "swirl" and reaction[2].infused == False:
            reaction[2].infused = True
            infuse = copy.copy(reaction[2])
            infuse.element = reaction[1]
            infuse.tick_damage = [0.188 for x in infuse.tick_damage]
            infuse.add_to_damage_queue(sim)

            for unit in sim.units:
                if unit.element == reaction[1]:
                    unit.current_energy += 15
            self.current_energy += 15

            if self.constellation >= 6:
                sim.enemy.active_debuffs["Venti_C6"] = copy.deepcopy(debuff_dict.get("Venti_C6_" + reaction[1].lower()))

    def venti_c4(self, _, __):
        self.live_anemo_dmg += 0.25


VentiArtifact = Artifact("Viridescent Venerer", "pct_atk", "anemo_dmg", "crit_rate", 30)
VentiF2P = Venti(90, 0, "The Stringless", 1, VentiArtifact, [6, 6, 6])


def main():
    print(VentiF2P.live_base_atk)
    print(VentiF2P.static_buffs)


if __name__ == '__main__':
    main()
