from core.unit import Char
from core.artifact import Artifact

class Xiao(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Xiao", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    # Static
    def xiao_plunge(self):
        self.plunge_type = "Anemo"
        self.plunge_ticks = 1
        self.plunge_tick_times = list([0.900])
        self.plunge_tick_damage = list([2.0439])
        self.plunge_tick_units = list([1])
        self.plunge_cancel = 0.900
        self.plunge_skill = 0.900
        self.plunge_burst = 0.900
        self.plunge_attack = 1.200
        self.plunge_swap = 1.200
        self.plunge_tick_hitlag = [0]
        self.plunge_stamina_cost = [0]

    def xiao_c1(self):
        self.skill_charges += 1

    # Active
    def xiao_q(self, _, sim):
        if self != sim.chosen_unit:
            del self.active_buffs["Xiao_Q"]

        self.live_normal_type = "Anemo"
        self.live_charged_type = "Anemo"
        self.live_combo_options.add("plunge")
        self.live_normal_dmg += 0.55 + self.burst_level*0.035
        self.live_charged_dmg += 0.55 + self.burst_level*0.035
        self.live_plunge_dmg += 0.55 + self.burst_level*0.035

    def xiao_a2(self, _, __):
        self.live_all_dmg += 0.15

    def xiao_a4(self, _, __):
        self.live_skill_dmg += self.active_buffs["Xiao_A4"].stacks

    def xiao_c2(self, _, sim):
        if self != sim.chosen_unit:
            self.live_recharge += 0.25
            self.active_buffs["Xiao_C2"].time_remaining = sim.encounter_limit

    def xiao_c6(self,unit_obj,sim,extra):
        pass


XiaoArtifact = Artifact("Viridiscent Venerer", "pct_atk", "anemo_dmg", "crit_rate", 30)

XiaoF2P = Xiao(90, 0, "Deathmatch", 1, XiaoArtifact, [6, 6, 6])


def main():
    print(XiaoTest.live_base_atk)
    print(XiaoTest.static_buffs)


if __name__ == '__main__':
    main()
