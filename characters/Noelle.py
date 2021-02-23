from core.unit import Char
from core.read_data import ele_ratio_dict, buff_dict
from core.action import Ability
import copy


class Noelle(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Noelle", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.snapshot_buff = 0

    # Static
    def noelle_c2(self):
        self.charged_dmg += 0.15
        self.charged_stam_save += 0.15

    def noelle_c6(self):
        pass
        # unit_obj.triggerable_buffs["Noelle Q 2"].duration += 5

    # Active
    def noelle_q_1(self, _, __, ___):
        mult = ele_ratio_dict[self.burst_level] * 0.4
        if self.constellation >= 6:
            mult += 0.5

        buff = mult * (1+copy.copy(self.base_def) * (1+copy.copy(self.live_pct_def)) + copy.copy(self.live_flat_def))
        self.snapshot_buff = buff
        self.active_buffs["Noelle_Q_2"] = copy.copy(buff_dict["Noelle_Q_2"])
        self.active_buffs["Noelle_Q_2"].source = self

    def noelle_q_2(self, _, __):
        self.live_normal_type = "Geo"
        self.live_charged_type = "Geo"
        self.live_flat_atk += self.snapshot_buff

    def noelle_e(self, _, sim, ___):
        damage = NoelleE(self)
        damage.add_to_damage_queue(sim)

        if self.constellation >= 4:
            c4_proc = NoelleC4(self)
            c4_proc.add_to_damage_queue()

    def noelle_a4(self, _, __, ___):
        self.live_skill_cd -= 0.25

    def noelle_c1(self, unit_obj, sim, extra):
        pass

class NoelleE(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "skill")
        self.ticks = 1
        self.tick_damage = [1.2]
        self.tick_units = [1]
        self.tick_times = [0]

    def calculate_tick_damage(self, tick, sim):
        attack_multiplier = self.tick_damage[tick]
        tot_def = self.unit.base_def * (1 + self.unit.live_pct_def) + self.unit.live_flat_def
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        dmg = 1 + self.unit.live_all_dmg + self.unit.live_geo_dmg + self.unit.live_skill_dmg + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_geo_res")
        defence = (100 + self.unit.level) / ((100 + self.unit.level) + sim.enemy.live_defence)
        damage = attack_multiplier * tot_def * tot_crit_mult * dmg * (1 - res) * defence * self.tick_scaling
        return damage


class NoelleC4(Ability):
    def __init__(self, unit_obj):
        super().__init__(unit_obj, "skill")
        self.ticks = 1
        self.tick_damage = [4]
        self.tick_scaling = [1]


NoelleTest = Noelle(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(NoelleTest.live_base_atk)
    print(NoelleTest.static_buffs)


if __name__ == '__main__':
    main()
