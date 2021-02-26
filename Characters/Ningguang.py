from core.unit import Char
from core.action import Action, Ability
from core.scaling import ratio_type
from core.read_data import buff_dict
from core.artifact import Artifact
import copy


class Ningguang(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Ningguang", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.jade_stacks = 0
        self.jade_wall = False

    def ningguang_normal(self, _, __, ___):
        if self.jade_stacks < 3:
            self.jade_stacks += 1

    def ningguang_charged(self, _, sim, action):
        if self.jade_stacks > 0:
            jade_proc = JadeStar(self, self.jade_stacks)
            jade_proc.add_to_damage_queue(sim)
            self.jade_stacks = 0

    def ningguang_a2(self, _, __):
        if self.jade_stacks > 0:
            self.live_charged_stamina_cost = [0]

    def ningguang_e(self, _, sim, __):
        self.jade_wall = True

        for unit in sim.units:
            unit.triggerable_buffs["Ningguang_A4_Trigger"] = copy.copy(buff_dict["Ningguang_A4_Trigger"])
            unit.triggerable_buffs["Ningguang_A4_Trigger"].time_remaining = 30
            unit.triggerable_buffs["Ningguang_A4_Trigger"].source = self

    def ningguang_a4_trigger(self, unit_obj, sim, __):
        if unit_obj == sim.chosen_unit:
            unit_obj.active_buffs["Ningguang_A4_Buff"] = copy.copy(buff_dict["Ningguang_A4_Buff"])
            unit_obj.active_buffs["Ningguang_A4_Buff"].source = self

    @staticmethod
    def ningguang_a4_buff(unit_obj, _):
        unit_obj.live_geo_dmg += 0.1

    def ningguang_q(self, _, sim, __):
        if self.jade_wall:

            self.jade_wall = False

            for unit in sim.units:
                del unit.triggerable_buffs["Ningguang_A4_Trigger"]

            jade_stars_burst = Ability(self, "burst")
            jade_stars_burst.add_to_damage_queue(sim)

            if self.constellation >= 2:
                self.live_skill_cd = 0

        if self.constellation >= 6:
            self.jade_stacks = 7


class JadeStar(Action):
    def __init__(self, unit_obj, jade_stacks):
        super().__init__(unit_obj)
        self.action_type = "damage"
        self.ticks = jade_stacks
        self.tick_times = [0.25] * jade_stacks
        self.tick_damage = [0.496] * jade_stacks
        self.tick_scaling = [ratio_type(unit_obj, "charged")[unit_obj.normal_level]] * jade_stacks
        self.tick_types = ["charged"] * jade_stacks
        self.tick_units = [0] * jade_stacks
        self.tick_element = ["Geo"] * jade_stacks
        self.particles = 0
        self.tick_used = ["no"] * jade_stacks


NingguangArtifact = Artifact("Archaic Petra", "pct_atk", "geo_dmg", "crit_rate", 30)

NingguangF2P = Ningguang(90, 0, "Mappa Marre", 1, NingguangArtifact, [6, 6, 6])


def main():
    print(NingguangTest.live_base_atk)
    print(NingguangTest.static_buffs)


if __name__ == '__main__':
    main()
