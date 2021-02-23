from core.unit import Char
from core.read_data import buff_dict
from core.artifact import Artifact
from core.sim import Sim, Monster
import copy


class Diluc(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Diluc", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.e_stacks = 0
        self.c6_stacks = 0
        self.start_time = 0

    def diluc_a2(self):
        self.charged_stam_save += 0.3

    def diluc_c1(self):
        self.all_dmg += 0.075

    def diluc_e(self, _, sim):
        if self.e_stacks == 0:
            self.start_time = sim.encounter_duration
            self.e_stacks = 1
            self.current_skill_cd = 0

        if "Diluc_E_2" in self.triggerable_buffs:
            self.live_tick_times = [0.367]
            self.live_skill_tick_damage = [0.976]
            self.live_skill_cancel = [0.5]
            self.live_skill_burst = [1.2]
            self.live_skill_swap = [0.617]
            self.live_skill_attack = [0.633]
            self.current_skill_cd = 0

        elif "Diluc_E_3" in self.triggerable_buffs:
            self.live_tick_times = [0.383]
            self.live_skill_tick_damage = [1.288]
            self.live_skill_cancel = [0.7]
            self.live_skill_burst = [1.067]
            self.live_skill_swap = [1.100]
            self.live_skill_attack = [0.833]
            self.current_skill_cd = 0
        else:
            if self.e_stacks != 1:
                self.current_skill_cd = self.live_skill_cd - (sim.encounter_duration - self.start_time)
                self.active_buffs.pop("Diluc_E")

    def diluc_e_1(self, _, __, ___):
        if self.e_stacks == 1:
            self.triggerable_buffs["Diluc_E_2"] = copy.copy(buff_dict["Diluc_E_2"])
            self.triggerable_buffs["Diluc_E_2"].time_remaining = 3
            self.triggerable_buffs["Diluc_E_2"].source = self
            self.triggerable_buffs["Diluc_E_1"].live_cd = self.live_skill_cd
            self.e_stacks = 2

    def diluc_e_2(self, _, __, ___):
        if self.e_stacks == 2:
            self.triggerable_buffs["Diluc_E_3"] = copy.copy(buff_dict["Diluc_E_3"])
            self.triggerable_buffs["Diluc_E_3"].time_remaining = 3
            self.triggerable_buffs["Diluc_E_3"].source = self
            self.triggerable_buffs.pop("Diluc_E_2")
            self.e_stacks = 3

    def diluc_e_3(self, _, sim, ___):
        if self.e_stacks == 3:
            self.e_stacks = 0
            self.triggerable_buffs.pop("Diluc_E_3")
            self.current_skill_cd = self.live_skill_cd - (sim.encounter_duration - self.start_time)
            self.active_buffs.pop("Diluc_E")

    def diluc_q(self, _, __):
        self.live_normal_type = "Pyro"
        self.live_charged_type = "Pyro"
        self.live_pyro_dmg += 0.2

    # Diluc C2 ## Duration ## Any
    def diluc_c2(self):
        pass

    # Diluc C4 1 ## Duration ## Onhit ## Skill
    def diluc_c4_1(self, _, __, ___):
        self.active_buffs["Diluc_C4_2"] = copy.deepcopy(buff_dict["Diluc_C4_2"])
        self.active_buffs["Diluc_C4_2"].source = self
        self.active_buffs["Diluc_C4_3"] = copy.deepcopy(buff_dict["Diluc_C4_3"])
        self.active_buffs["Diluc_C4_3"].source = self

    # Diluc C4 2 ## Duration ##
    def diluc_c4_2(self, _, __):
        self.live_skill_dmg -= 0.4

    # All this was done to give Diluc a skill buff but only for 2s after NOT using his skill
    # Diluc C4 3 ## Duration ##
    def diluc_c4_3(self, _, __):
        self.live_skill_dmg += 0.4

    ## Diluc C6 ## Duration ## Postcast # Burst
    def diluc_c6_1(self, _, __, ___):
        self.triggerable_buffs["Diluc_C6_2"] = copy.deepcopy(buff_dict["Diluc_C6_2"])
        self.triggerable_buffs["Diluc_C6_2"].time_remaining = 6

        self.c6_stacks = 2

        if self.c6_stacks > 0:
            self.live_normal_speed += 0.3
            self.live_normal_dmg += 0.3

    def diluc_c6_2(self, _, __, ___):
        self.c6_stacks -= 1
        if self.c6_stacks <= 0:
            self.active_buffs.pop("Diluc_C6_1")
            self.triggerable_buffs.pop("Diluc_C6_2")


DilucArtifact = Artifact("Crimson Witch", "pct_atk", "pyro_dmg", "crit_rate", 30)
DilucTest = Diluc(90, 6, "Harbinger of Dawn", 5, DilucArtifact, [6, 6, 6])


def main():
    Test = Sim({DilucTest}, Monster, 60)
    Test.turn_on_sim()


if __name__ == '__main__':
    main()
