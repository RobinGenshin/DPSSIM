from core.unit import Char
from core.action import Ability, Particle
from core.read_data import buff_dict
from core.artifact import Artifact
import copy


class Keqing(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Keqing", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.e_stacks = 0

    def keqing_a2(self, _, __):
        self.live_normal_type = "Electro"
        self.live_charged_type = "Electro"

    def keqing_a4(self, _, __):
        self.live_crit_rate += 0.15
        self.live_recharge += 0.15

    def keqing_e(self, _, sim):
        if self.e_stacks == 0:
            self.start_time = sim.encounter_duration
            self.e_stacks = 1
            self.current_skill_cd = 0

        if "Keqing_E_2" in self.triggerable_buffs:
            self.live_tick_times = [0.467]
            self.live_skill_tick_damage = [1.68]
            self.live_skill_cancel = [0.283]
            self.live_skill_burst = [0.700]
            self.live_skill_swap = [0.867]
            self.live_skill_attack = [0.717]
            self.current_skill_cd = 0
        else:
            if self.e_stacks != 1:
                self.current_skill_cd = self.live_skill_cd - (sim.encounter_duration - self.start_time)
                self.active_buffs.pop("Keqing_E")

    def keqing_e_1(self, _, __, ___):
        if self.e_stacks == 1:
            self.triggerable_buffs["Keqing_E_2"] = copy.copy(buff_dict["Keqing_E_2"])
            self.triggerable_buffs["Keqing_E_2"].time_remaining = 5
            self.triggerable_buffs["Keqing_E_2"].source = self
            self.e_stacks = 2

    def keqing_e_2(self, _, sim, __):
        if self.e_stacks == 2:
            self.e_stacks = 0
            self.triggerable_buffs.pop("Keqing_E_2")
            self.current_skill_cd = self.live_skill_cd - (sim.encounter_duration - self.start_time)
            self.active_buffs.pop("Keqing_E")

    def keqing_c1(self, _, sim, action):
        if action[0].loop == True and action[0].tick_damage == [1.68]:
            action = KeqingC1(self, sim)
            action.add_to_damage_queue(sim)
            print("Proced Keqing C1")

    def keqing_c2(self, _, sim, __):
        if "Electro" in sim.enemy.elements:
            energy = Particle(self, "Electro", 1, sim)
            energy.add_to_energy_queue(sim)
            self.triggerable_buffs["Keqing_C2"].live_cd = 5

    def keqing_c4_1(self, _, __, reaction):
        if reaction[0] in {"overload", "superconduct", "electro_charged"}:
            self.active_buffs["Keqing_C4_2"] = copy.copy(buff_dict["Keqing_C4_2"])
            self.active_buffs["Keqing_C4_2"].source = self

    def keqing_c4_2(self, _, __):
        self.live_pct_atk += 0.25

    def keqing_c6_1(self, _, __):  # Normal
        self.live_electro_dmg += 0.06

    def keqing_c6_2(self, _, __):  # Charged
        self.live_electro_dmg += 0.06

    def keqing_c6_3(self, _, __):  # Skill
        self.live_electro_dmg += 0.06

    def keqing_c6_4(self, _, __):  # Burst
        self.live_electro_dmg += 0.06


class KeqingC1(Ability):
    def __init__(self, unit_obj, sim):
        super().__init__(unit_obj, "skill")
        self.name = "Keqing C1"
        self.ticks = 2
        self.tick_element = ["Electro", "Electro"]
        self.tick_scaling = [1, 1]
        self.tick_types = ["skill", "skill"]
        self.tick_times = [0, 0]
        self.tick_damage = [0.5, 0.5]
        self.tick_units = [1, 0]
        self.tick_used = ["no", "no"]
        self.loop = False


KeqingArtifact = Artifact("Thundering Fury", "pct_atk", "electro_dmg", "crit_rate", 30)

KeqingF2P = Keqing(90, 0, "The Black Sword", 1, KeqingArtifact, [6, 6, 6])

def main():
    print(KeqingTest.live_base_atk)
    print(KeqingTest.static_buffs)


if __name__ == '__main__':
    main()