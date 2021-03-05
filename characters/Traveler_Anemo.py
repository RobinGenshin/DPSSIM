from core.unit import Char
from core.action import Combo
from core.read_data import debuff_dict
from core.artifact import Artifact
import copy


class TravelerAnemo(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Traveler (Anemo)", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def traveler_anemo_c2(self):
        self.recharge += 0.16

    def traveler_anemo_a2(self, _, sim, action):
        if action[1] == 4 and action[0].loop == True:
            proc = TravelerAnemoA2(self, action[0].combo)
            proc.add_to_damage_queue(sim)

    def traveler_anemo_e(self, _, sim, reaction):
        if reaction[0] == "swirl":
            if reaction[2].infused == False:
                reaction[2].infused = True
                infuse = copy.copy(reaction[2])
                infuse.tick_element = [reaction[1]] * infuse.ticks
                infuse.tick_damage = [0.23 * x for x in infuse.tick_damage]
                infuse.add_to_damage_queue(sim)

    def traveler_anemo_q(self, unit_obj, sim, reaction):
        if reaction[0] == "swirl":
            if reaction[2].infused == False:
                reaction[2].infused = True
                infuse = copy.deepcopy(reaction[2])
                infuse.element = reaction[1]
                infuse.tick_damage = [0.248 for x in infuse.tick_damage]
                sim.floating_actions.add(infuse)

                if unit_obj.constellation >= 6:
                    sim.enemy.active_debuffs["Traveler_Anemo_C6"] = copy.deepcopy(
                        debuff_dict.get("Traveler_Anemo_C6_anemo"))
                    sim.enemy.active_debuffs["Traveler_Anemo_C6"] = copy.deepcopy(
                        debuff_dict.get("Traveler_Anemo_C6_" + reaction[1].lower()))

    def traveler_anemo_c6(self, unit_obj, sim, reaction):
        pass


class TravelerAnemoA2(Combo):
    def __init__(self, unit_obj, combo):
        super().__init__(unit_obj, combo)
        self.name = "Traveler (Anemo) A2"
        self.tick_element = ["Anemo"]
        self.tick_times = [0]
        self.tick_damage = [0.6]
        self.tick_units = [1]
        self.tick_types = ["normal"]
        self.ticks = 1
        self.scaling = [1]
        self.loop = False


TravelerAnemoArtifact = Artifact("Viridiscent Venerer", "pct_atk", "anemo_dmg", "crit_rate", 30)

TravelerAnemoF2P = TravelerAnemo(90, 6, "Favonius Sword", 1, TravelerAnemoArtifact, [6, 6, 6])


def main():
    print(TravelerAnemoTest.live_base_atk)
    print(TravelerAnemoTest.static_buffs)


if __name__ == '__main__':
    main()
