# pylint: disable=no-member
import copy
from core.read_data import character_dict, weapon_dict, artifact_dict, buff_dict, debuff_dict
from effects import weapons, artifacts
from core.calculations import calculate_crit_atk_ratio


# Unit/Character #
class Char:
    def __init__(self, char, level, constellation, weapon, weapon_rank, artifact, talent_levels):

        self.level = level
        self.element = character_dict[char].element
        self.weapon_type = character_dict[char].weapon_type
        self.character = char
        self.constellation = constellation
        self.weapon = weapon
        self.weapon_rank = weapon_rank
        self.artifact = artifact
        self.normal_level = talent_levels[0]
        self.skill_level = talent_levels[1]
        self.burst_level = talent_levels[2]

        self.actions = {"combo", "skill", "burst"}
        self.combo_options = {"normal", "charged"}

        for stat in {"atk", "hp", "def"}:
            for x in {"base_", "flat_", "pct_"}:
                setattr(self, x + stat,
                        getattr(character_dict[char], x + stat, 0) +
                        getattr(weapon_dict[weapon], x + stat, 0) +
                        getattr(artifact, x + stat, 0))

        for stat in {"anemo_dmg", "cryo_dmg", "electro_dmg", "geo_dmg", "hydro_dmg", "pyro_dmg", "ele_dmg",
                     "physical_dmg", "normal_dmg", "charged_dmg", "skill_dmg", "burst_dmg", "plunge_dmg", "all_dmg",
                     "ele_m", "recharge", "crit_rate", "crit_dmg", "heal_bonus",
                     "normal_speed", "charged_speed", "stam_save", "plunge_speed"}:
            setattr(self, stat,
                    getattr(character_dict[char], stat, 0) +
                    getattr(weapon_dict[weapon], stat, 0) +
                    getattr(artifact, stat, 0))

        for stat in {"crit_rate", "dmg"}:
            setattr(self, "cond_" + stat, 0)

        for action_type in {"normal", "charged", "skill", "burst", "plunge", "weapon"}:
            for x in {"_type", "_ticks", "_tick_times", "_tick_damage", "_tick_units", "_element", "_tick_hitlag",
                      "_cancel", "_swap", "_attack", "_skill", "_burst", "_crit_rate", "_cond_dmg",
                      "_cd", "_cdr", "_particles", "_charges", "_energy_cost", "_stamina_cost", "_stam_save", "_ac",
                      "_at", "_cond_crit_rate"}:
                setattr(self, action_type + x, getattr(character_dict[char], action_type + x, 0))

        for reaction in {"overload", "superconduct", "electro_charged", "swirl", "vaporise", "melt", "hydro_swirl"}:
            setattr(self, reaction + "_dmg", 0)

        self.static_buffs = {}
        self.triggerable_buffs = {}
        self.active_buffs = {}
        self.triggerable_debuffs = {}

        base_stats = copy.copy(self.__dict__)

        for x in base_stats:
            setattr(self, "live_" + x, copy.copy(getattr(self, x)))

        total_stats = copy.copy(self.__dict__)

        self.live_stats = copy.copy({k: total_stats[k] for k in set(total_stats) - set(base_stats)})

        self.current_skill_cd = 0
        self.current_burst_cd = 0
        self.current_energy = self.live_burst_energy_cost
        self.current_skill_charges = self.live_skill_charges

        self.add_effects()
        self.add_substats()

        self.greedy = False

    def add_effects(self):
        for key, buff in buff_dict.items():

            if buff.character == self.character:
                if buff.constellation <= self.constellation:
                    if buff.type == "Static":
                        self.static_buffs[key] = copy.deepcopy(buff)
                        getattr(self, buff.method)()
                    if buff.type == "Active":
                        self.triggerable_buffs[key] = copy.deepcopy(buff)
                        self.triggerable_buffs[key].source = self

            if self.weapon in buff.weapon:
                if buff.type == "Static":
                    self.static_buffs[key] = copy.deepcopy(buff)
                    getattr(weapons.StaticBuff, buff.method)(self)
                if buff.type == "Active":
                    self.triggerable_buffs[key] = copy.deepcopy(buff)
                    self.triggerable_buffs[key].source = weapons.ActiveBuff()

            if buff.artifact == self.artifact:
                if buff.type == "Static":
                    self.static_buffs[key] = copy.deepcopy(buff)
                    getattr(artifacts.StaticBuff(), buff.method)(self)
                if buff.type == "Active":
                    self.triggerable_buffs[key] = copy.deepcopy(buff)
                    self.triggerable_buffs[key].source = artifacts.ActiveBuff()

        for key, debuff in debuff_dict.items():
            if debuff.character == self.character:
                if debuff.constellation <= self.constellation:
                    self.triggerable_debuffs[key] = debuff
            if debuff.weapon == self.weapon:
                self.triggerable_debuffs[key] = debuff
            if debuff.artifact == self.artifact:
                self.triggerable_debuffs[key] = debuff

    def add_substats(self):
        optimal_stats = calculate_crit_atk_ratio(self)
        while optimal_stats["pct_atk"] > self.pct_atk and self.artifact.subs > 0:
            self.pct_atk += 0.0495
            self.artifact.subs -= 1
        while optimal_stats["crit_rate"] > self.crit_rate and self.artifact.subs > 0:
            self.crit_rate += 0.033
            self.artifact.subs -= 1
        while optimal_stats["crit_dmg"] > self.crit_dmg and self.artifact.subs > 0:
            self.crit_dmg += 0.066
            self.artifact.subs -= 1

    def update_stats(self, sim):
        # clears active buffs
        for stat in self.live_stats:
            setattr(self, stat, copy.copy(getattr(self, stat.removeprefix("live_"))))
        # call method to reactivate buff
        for _, buff in copy.copy(self.active_buffs).items():
            getattr(buff.source, buff.method)(self, sim)


    def skill_level_plus_3(self):
        self.skill_level += 3

    def burst_level_plus_3(self):
        self.burst_level += 3
