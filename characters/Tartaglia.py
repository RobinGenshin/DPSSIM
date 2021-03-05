from core.unit import Char
from core.read_data import buff_dict, debuff_dict, ele_ratio_dict, phys_ratio_dict
from core.action import Action, Ability
from core.artifact import Artifact
import copy


class Tartaglia(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Tartaglia", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.stance = "ranged"
        self.c6_reset = False

    def tartaglia_autolevel(self):
        self.normal_level += 1

    def tartaglia_c1(self):
        self.skill_cdr *= 0.8

    def tartaglia_stance_swap(self, _, __, ___):
        if self.stance == "ranged":
            self.stance = "melee"
            self.active_buffs["Tartaglia_Stance"] = copy.copy(buff_dict["Tartaglia_Stance"])
            self.active_buffs["Tartaglia_Stance"].time_remaining = 45
            self.active_buffs["Tartaglia_Stance"].source = self

        elif self.stance == "melee":
            self.stance = "ranged"
            if self.c6_reset == True:
                self.c6_reset = False
                self.live_skill_cd = 1
            else:
                self.live_skill_cd = (45 - copy.copy(self.active_buffs["Tartaglia_Stance"].time_remaining)) * 2 + 6
            del self.active_buffs["Tartaglia_Stance"]
        else:
            print("Error")

    def tartaglia_stance(self, _, __):
        if self.stance == "melee":

            self.live_normal_type = "Hydro"
            self.live_normal_at = 3.017
            self.live_normal_ac = "No"
            self.live_normal_ticks = 7
            self.live_normal_tick_times = [0.083, 0.417, 0.717, 1.083, 1.667, 2.017, 2.300]
            self.live_normal_tick_damage = [0.3887, 0.4162, 0.5633, 0.5994, 0.553, 0.3543, 0.3767]
            self.live_normal_tick_units = [1, 0, 0, 0, 0, 1, 0]
            self.live_normal_cancel = [0.083, 0.417, 0.717, 1.083, 1.667, 2.017, 2.300]
            self.live_normal_swap = [0.083, 0.417, 0.717, 1.083, 1.667, 2.017, 2.300]
            self.live_normal_skill = [0.083, 0.417, 0.717, 1.083, 1.667, 2.017, 2.300]
            self.live_normal_burst = [0.083, 0.417, 0.717, 1.083, 1.667, 2.017, 2.300]
            self.live_normal_attack = [0.083, 0.417, 0.717, 1.083, 1.667, 2.017, 2.300]
            self.live_normal_hitlag = [6, 6, 6, 6, 6, 6, 6]

            self.live_charged_type = "Hydro"
            self.live_charged_ticks = 2
            self.live_charged_tick_times = [0.583, 0.683]
            self.live_charged_tick_damage = [0.602, 0.7198]
            self.live_charged_tick_units = [1, 0]
            self.live_charged_stamina_cst = [20, 0]
            self.live_normal_cancel = [0.583, 0.683]
            self.live_normal_swap = [0.683]
            self.live_normal_skill = [0.683]
            self.live_normal_burst = [0.683]
            self.live_normal_attack = [0.9]  # FILLER

            self.live_burst_hits = 1
            self.live_burst_tick_times = [1.133]
            self.live_burst_tick_damage = [4.64]
            self.live_burst_tick_units = [2]
            self.live_burst_cancel = [1.7]
            self.live_burst_swap = [1.717]
            self.live_burst_skill = [1.750]
            self.live_burst_attack = [1.800]

    @staticmethod
    def riptide_apply(_, sim, __):
        sim.enemy.active_debuffs["Riptide"] = copy.copy(debuff_dict["Riptide_debuff"])

    def tartaglia_aimed_riptide_proc(self, _, sim, action):
        if action[0].loop:
            if self.stance == "ranged":
                riptide = RangedRiptide(self)
                riptide.add_to_damage_queue(sim)
                riptide.add_to_energy_queue(sim)
            if self.constellation >= 4:
                if any(type(x) == TartagliaC4 for x in sim.floating_actions):
                    pass
                else:
                    c4_proc = TartagliaC4(self)
                    c4_proc.add_to_damage_queue(sim)
                    c4_proc.add_to_energy_queue(sim)

    def tartaglia_melee_riptide_proc(self, _, sim, action):
        if action[0].loop:
            if self.stance == "melee":
                riptide = MeleeRiptide(self)
                riptide.add_to_damage_queue(sim)
                riptide.add_to_energy_queue(sim)
            if self.constellation >= 4:
                if any(type(x) == TartagliaC4 for x in sim.floating_actions):
                    pass
                else:
                    c4_proc = TartagliaC4(self)
                    c4_proc.add_to_damage_queue(sim)
                    c4_proc.add_to_energy_queue(sim)

    def tartaglia_burst_riptide_proc(self, _, sim, __):
        if self.stance == "melee":
            if "Riptide" in sim.enemy.active_debuffs:
                del sim.enemy.active_debuffs["Riptide"]
                burst_proc = BurstRiptide(self)
                burst_proc.add_to_damage_queue(sim)

    def tartaglia_c6(self, _, __, ___):
        if self.stance == "melee":
            self.c6_reset = True


class RangedRiptide(Action):
    def __init__(self, unit_obj):
        super().__init__(unit_obj)
        self.action_type = "damage"
        self.name = "Ranged Riptide"
        self.ticks = 3
        self.element = "Hydro"
        self.tick_element = ["Hydro"] * 3
        self.tick_times = [0.25, 0.3, 0.3]
        self.tick_damage = [0.123, 0.123, 0.123]
        self.tick_units = [1, 0, 0]
        self.tick_scaling = [ele_ratio_dict[unit_obj.normal_level]] * 3
        self.tick_types = ["normal"] * 3
        self.particles = 1
        self.tick_used = ["no"] * 3
        self.loop = False


class MeleeRiptide(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "skill")
        self.name = "Melee Riptide"
        self.ticks = 1
        self.element = "Hydro"
        self.tick_element = ["Hydro"]
        self.tick_times = [0.25]
        self.tick_damage = [0.602]
        self.tick_units = [1]
        self.tick_scaling = [phys_ratio_dict[unit_obj.skill_level]]
        self.particles = 1
        self.loop = False


class TartagliaC4(Action):
    def __init__(self, unit_obj):
        super().__init__(unit_obj)
        self.name = "Tartaglia C4"
        self.action_type = "damage"

        self.ticks = 5
        self.tick_element = ["Hydro"] * 5
        self.tick_times = [0.05, 4.05, 8.05, 12.05, 16.05]
        self.energy_times = [2.05, 6.05, 10.05, 14.05, 18.05]
        self.tick_damages = [0.602, 0.602, 0.602, 0.602, 0.602]
        self.tick_types = ["normal"] * 5
        self.tick_units = [1, 1, 1, 1, 1]
        self.tick_used = ["no", "no", "no", "no", "no"]
        self.snapshot = True
        self.particles = 5
        self.loop = False

    def calculate_tick_damage(self, tick, sim):
        defence = (100 + self.unit.level) / ((100 + self.unit.level) + sim.enemy.live_defence)
        tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
        res = getattr(sim.enemy, "live_" + self.tick_element[tick].lower() + "_res")

        if self.unit.stance == "melee":
            attack_multiplier = 0.602
            talent_level = phys_ratio_dict[self.unit.skill_level]
            damage = self.snapshot_tot_atk * tot_crit_mult * (1 - res) * defence * talent_level * attack_multiplier
            return damage

        elif self.unit.stance == "ranged":
            attack_multiplier = 0.123
            talent_level = ele_ratio_dict[self.unit.normal_level]
            damage = self.snapshot_tot_atk * tot_crit_mult * (1 - res) * defence * talent_level * attack_multiplier

            # Adding the other 2 ticks to the queue #
            charged_proc = Action(self.unit)
            charged_proc.action_type = "damage"
            charged_proc.ticks = 2
            charged_proc.element = "Hydro"
            charged_proc.tick_element = ["Hydro"] * 2
            charged_proc.tick_types = ["normal"] * 2
            charged_proc.tick_times = [0.1, 0.2]
            charged_proc.tick_damage = [0.123] * 2
            charged_proc.tick_units = [0, 0, 0]
            charged_proc.tick_used = ["no"] * 2
            charged_proc.tick_scaling = [ele_ratio_dict[self.unit.normal_level]] * 2
            charged_proc.add_to_damage_queue(sim)
            return damage


class BurstRiptide(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "burst")
        self.ticks = 1
        self.tick_damage = [1.2]
        self.tick_times = [0]
        self.loop = False


TartagliaArtifact = Artifact("Heart of Depth", "pct_atk", "hydro_dmg", "crit_rate", 30)

TartagliaF2P = Tartaglia(90, 0, "Prototype Crescent", 1, TartagliaArtifact, [6, 6, 6])


def main():
    print(TartagliaTest.live_base_atk)
    print(TartagliaTest.static_buffs)


if __name__ == '__main__':
    main()
