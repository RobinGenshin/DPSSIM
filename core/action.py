from core.scaling import ratio_type
from copy import deepcopy, copy
from core.read_data import ele_ratio_dict
from core.read_data import phys_ratio_dict


class ComboList:

    @staticmethod
    def create(unit, sim):
        combo_dict = dict()
        if sim.stamina_toggle:
            ac = (21 / 60)
        else:
            ac = (31 / 60)

        # Normal Combos #
        for i in range(unit.live_normal_ticks):
            normal_damage = 0
            for j in range(i + 1):
                normal_damage += unit.live_normal_tick_damage[j]
            if i == (unit.normal_ticks - 1):
                ac = min(ac, unit.live_normal_at - max(unit.live_normal_tick_times))

            time = unit.live_normal_tick_times[i] + ac
            dps = normal_damage / time
            combo_dict["N" + str(i + 1)] = [dps, normal_damage, time, [i + 1, 0, 0], "N" + str(i + 1)]
            if "plunge" in unit.live_combo_options:
                normal_damage += unit.live_plunge_tick_damage[0]
                time = unit.live_normal_cancel[i] + min(unit.live_plunge_attack,
                                                        unit.live_plunge_tick_times[0] + 0.33)
                dps = normal_damage / time
                combo_dict["N" + str(i + 1) + "JP"] = [dps, normal_damage, time, [i + 1, 0, unit.live_plunge_ticks],
                                                       "N" + str(i + 1) + "JP"]

        # Charged #
        if len(unit.normal_attack) == 0:
            charged_damage = 0
            for k in range(unit.live_charged_ticks):
                charged_damage += unit.live_charged_tick_damage[k]
            time = min(unit.live_charged_attack, max(unit.live_charged_tick_times) + 0.33)
            dps = charged_damage / time
            combo_dict["C"] = [dps, charged_damage, time, [0, unit.live_charged_ticks, 0], "C"]

        # Charged Combos #
        for i in range(len(unit.live_normal_attack)):
            normal_damage = 0
            charged_damage = 0
            for j in range(i + 1):
                normal_damage += unit.live_normal_tick_damage[j]
            for k in range(unit.live_charged_ticks):
                charged_damage += unit.live_charged_tick_damage[k]
            time = unit.live_normal_attack[i] + min(unit.live_charged_attack,
                                                    max(unit.live_charged_tick_times) + 0.33)
            damage = normal_damage + charged_damage
            dps = damage / time
            combo_dict["N" + str(i + 1) + "C"] = [dps, damage, time, [i + 1, unit.live_charged_ticks, 0],
                                                  "N" + str(i + 1) + "C"]

            if "plunge" in unit.live_combo_options:
                damage += unit.live_plunge_tick_damage[0]
                time = unit.live_normal_attack[i] + unit.live_charged_cancel + min(unit.live_plunge_attack,
                                                                                   unit.live_plunge_tick_times[0]
                                                                                   + 0.33)
                dps = damage / time
                combo_dict["N" + str(i + 1) + "C" + "JP"] = [dps, damage, time, [i + 1, unit.live_charged_ticks,
                                                                                 unit.live_plunge_ticks, 0],
                                                             "N" + str(i + 1) + "C" + "JP"]

        # Plunge Spam #
        if "plunge" in unit.live_combo_options:
            damage = unit.live_plunge_tick_damage[0]
            time = min(unit.live_plunge_attack, unit.live_plunge_tick_times[0] + 0.33)
            dps = damage / time
            combo_dict["JP"] = [dps, damage, time, [0, 0, unit.live_plunge_ticks], "JP"]
        return combo_dict


class Action:
    def __init__(self, unit_obj):

        self.name = str()
        self.talent = str()
        self.infused = False
        self.unit = unit_obj
        self.action_type = str()
        self.combo = []

        self.ticks = int()
        self.tick_types = []
        self.tick_element = []
        self.tick_stat = []
        self.tick_scaling = []
        self.tick_times = []
        self.energy_times = []
        self.tick_damage = []
        self.tick_units = []
        self.tick_used = []
        self.tick_stamina_cost = []
        self.total_stamina = float()

        self.initial_time = float()
        self.time_remaining = float()

        self.times = set()
        self.action_time = float()
        self.minimum_time = float()

        self.loop = True
        self.greedy = False

        self.snapshot = True
        self.snapshot_tot_atk = float()
        self.snapshot_crit_rate = float()
        self.snapshot_crit_dmg = float()
        self.snapshot_dmg = float()

    def available(self, sim):
        if self.talent == "skill":
            if self.unit.current_skill_cd <= 0:
                return True
            else:
                return False

        elif self.talent == "burst":
            if self.unit.current_burst_cd <= 0 and self.unit.current_energy >= self.unit.live_burst_energy_cost:
                return True
            else:
                return False

        elif self.talent == "combo":
            if self.combo[3][1] > 0:
                if sim.stamina > self.total_stamina and sim.stamina_toggle:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def update_time(self):
        if self.talent == "damage":
            self.initial_time = max(self.tick_times)
            self.time_remaining = max(self.tick_times)
        elif self.action_type == "energy":
            self.energy_times = [x + 2 for x in self.tick_times]
            self.initial_time = max(self.energy_times)
            self.time_remaining = max(self.energy_times)

    def calculate_tick_damage(self, tick, sim):
        if self.snapshot:
            tot_atk = self.snapshot_tot_atk
            attack_multiplier = self.tick_damage[tick]
            defence = (100 + self.unit.level) / ((100 + self.unit.level) + sim.enemy.live_defence)
            tot_crit_rate = min(1, self.snapshot_crit_rate + self.unit.live_cond_crit_rate + getattr(self.unit,
                                                                                              "live_" + self.tick_types[
                                                                                                tick] + "_cond_crit_rate"))

            tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
            tot_dmg = self.snapshot_dmg + self.unit.live_cond_dmg
            scaling = self.tick_scaling[tick]
            res = getattr(sim.enemy, "live_" + self.tick_element[tick].lower() + "_res")
            return tot_atk * tot_crit_mult * tot_dmg * defence * (1 - res) * attack_multiplier * scaling

        else:
            tot_atk = self.unit.live_base_atk * (1 + self.unit.live_pct_atk) + self.unit.live_flat_atk
            attack_multiplier = self.tick_damage[tick]
            defence = (100 + self.unit.level) / ((100 + self.unit.level) + sim.enemy.live_defence)
            tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate + getattr(self.unit, "live_" +
                                                                                               self.tick_types[tick] +
                                                                                               "_cond_crit_rate")
            tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
            tot_dmg = 1 + self.unit.live_all_dmg + self.unit.live_cond_dmg + getattr(self.unit, "live_" + self.tick_types[
                tick] + "_dmg")
            tot_dmg += getattr(self.unit, "live_" + self.tick_element[tick].lower() + "_dmg")
            scaling = self.tick_scaling[tick]
            res = getattr(sim.enemy, "live_" + self.tick_element[tick].lower() + "_res")
            return tot_atk * tot_crit_mult * tot_dmg * defence * (1 - res) * attack_multiplier * scaling

    def calculate_damage_snapshot(self, sim):
        total_damage = 0
        for i in range(self.ticks):
            total_damage += self.calculate_tick_damage(i, sim)
        return total_damage

    def calculate_dps_snapshot(self, sim):
        return self.calculate_damage_snapshot(sim) / self.action_time

    def add_to_damage_queue(self, sim):
        self.tick_times = [x + sim.time_into_turn for x in self.tick_times]
        self.update_time()
        sim.floating_actions.append(self)

    def add_to_energy_queue(self, sim):
        energy = deepcopy(self)
        energy.action_type = "energy"
        energy.energy_times = [x + sim.time_into_turn + 2 for x in self.tick_times]
        energy.update_time()
        sim.floating_actions.append(energy)

class Ability(Action):
    def __init__(self, unit_obj, talent):
        super().__init__(unit_obj)
        self.name = unit_obj.character + " " + talent
        self.action_type = "damage"
        self.ticks = getattr(self.unit, "live_" + talent + "_ticks")
        self.talent = talent
        self.element = unit_obj.element

        self.tick_types = [talent] * self.ticks
        self.tick_element = [self.unit.element] * self.ticks
        self.tick_scaling = [ratio_type(self.unit, talent)[getattr(unit_obj, talent + "_level")]] * self.ticks
        self.tick_times = getattr(self.unit, "live_" + talent + "_tick_times")
        self.tick_damage = getattr(self.unit, "live_" + talent + "_tick_damage")
        self.tick_units = getattr(self.unit, "live_" + talent + "_tick_units")
        self.tick_used = ["no" for _ in self.tick_times]
        self.tick_stamina_cost = [getattr(unit_obj, "live_" + talent + "_stam", 0)] * self.ticks

        self.particles = getattr(unit_obj, "live_" + talent + "_particles")

        self.time_to_cancel = getattr(self.unit, talent + "_cancel")
        self.time_to_attack = getattr(self.unit, talent + "_attack")
        self.time_to_swap = getattr(self.unit, talent + "_swap")
        self.times = {self.time_to_cancel, self.time_to_attack, self.time_to_swap}
        self.minimum_time = min(self.times)

        if self.talent == "skill":
            self.time_to_burst = getattr(self.unit, talent + "_burst")
            self.time_to_skill = getattr(self.unit, talent + "_burst")
            self.times.add(self.time_to_burst)

        if self.talent == "burst":
            self.time_to_skill = getattr(self.unit, talent + "_skill")
            self.times.add(self.time_to_skill)

        self.action_time = min(self.times)
        self.time_remaining = max(self.tick_times)
        self.initial_time = max(self.tick_times)

        self.snapshot = True
        self.snapshot_tot_atk = copy(self.unit.base_atk * (1 + self.unit.live_pct_atk) + self.unit.flat_atk)
        self.snapshot_crit_rate = copy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = copy(self.unit.live_crit_dmg)
        self.snapshot_dmg = copy(1 + self.unit.live_all_dmg + getattr(self.unit, "live_" + self.talent + "_dmg") +
                                     getattr(self.unit, "live_" + self.unit.element.lower() + "_dmg"))


class Combo(Action):
    def __init__(self, unit_obj, combo):
        super().__init__(unit_obj)

        self.name = str(unit_obj.character) + " " + str(combo[4])
        self.combo = combo
        self.action_type = "damage"
        self.talent = "combo"
        self.tick_types = ["normal"] * self.combo[3][0]
        self.tick_types.extend(["charged"] * self.combo[3][1])
        self.tick_types.extend(["plunge"] * self.combo[3][2])

        self.tick_element = [getattr(self.unit, "live_normal_type").lower()] * self.combo[3][0]
        self.tick_element.extend([getattr(self.unit, "live_charged_type").lower()] * self.combo[3][1])
        if self.combo[3][2] > 0:
            self.tick_element.extend([getattr(self.unit, "live_plunge_type").lower()] * self.combo[3][2])

        self.tick_scaling = [ratio_type(self.unit, "normal")[getattr(unit_obj, "normal_level")]] * combo[3][0]
        self.tick_scaling.extend([ratio_type(self.unit, "charged")[getattr(unit_obj, "normal_level")]] * combo[3][1])
        self.tick_scaling.extend([ratio_type(self.unit, "normal")[getattr(unit_obj, "normal_level")]] * combo[3][2])

        self.tick = 0
        self.ticks = self.combo[3][0] + self.combo[3][1] + self.combo[3][2]
        self.tick_times = self.unit.live_normal_tick_times[:combo[3][0]]
        if not self.tick_times:
            self.tick_times = [0]
        self.tick_times.extend([x + max(self.tick_times) for x in self.unit.charged_tick_times[:combo[3][1]]])
        if self.combo[3][2] > 0:
            self.tick_times.extend([x + max(self.tick_times) for x in self.unit.plunge_tick_times[:combo[3][2]]])

        self.tick_damage = self.unit.live_normal_tick_damage[:combo[3][0]]
        self.tick_damage.extend(x for x in self.unit.live_charged_tick_damage[:combo[3][1]])
        if self.combo[3][2] > 0:
            self.tick_damage.extend(x for x in self.unit.live_plunge_tick_damage[:combo[3][2]])

        self.tick_units = self.unit.live_normal_tick_units[:combo[3][0]]
        self.tick_units.extend(self.unit.live_charged_tick_units[:combo[3][1]])
        if self.combo[3][2] > 0:
            self.tick_units.extend(self.unit.live_plunge_tick_units[:combo[3][2]])

        self.tick_hitlag = self.unit.live_normal_tick_hitlag[:combo[3][0]]
        self.tick_hitlag.extend(x for x in self.unit.live_charged_tick_hitlag[:combo[3][1]])
        if self.combo[3][2] > 0:
            self.tick_hitlag.extend(x for x in self.unit.live_plunge_tick_hitlag[:combo[3][2]])

        self.particles = 0
        self.tick_used = ["no"] * self.ticks

        if combo[3][1] > 0 and combo[3][0] > 0:
            self.time_to_normal_nc = self.unit.live_charged_attack + self.unit.live_normal_attack[combo[3][0] - 1]
            self.time_to_skill = self.unit.live_charged_skill + self.unit.live_normal_attack[combo[3][0] - 1]
            self.time_to_burst = self.unit.live_charged_burst + self.unit.live_normal_burst[combo[3][0] - 1]
            self.time_to_swap = self.unit.live_charged_swap + self.unit.live_normal_attack[combo[3][0] - 1]
            self.time_to_cancel = self.unit.live_charged_cancel + self.unit.live_normal_attack[combo[3][0] - 1]

        elif combo[3][1] > 0 and combo[3][0] == 0:
            self.time_to_normal_nc = self.unit.live_charged_attack
            self.time_to_skill = self.unit.live_charged_skill
            self.time_to_burst = self.unit.live_charged_burst
            self.time_to_swap = self.unit.live_charged_swap
            self.time_to_cancel = self.unit.live_charged_cancel
        else:
            self.time_to_normal_nc = self.unit.live_normal_at
            self.time_to_skill = max(self.tick_times)
            self.time_to_burst = max(self.tick_times)
            self.time_to_swap = max(self.tick_times)
            self.time_to_cancel = max(self.tick_times)

        self.times = [self.time_to_cancel, self.time_to_normal_nc, self.time_to_skill, self.time_to_burst,
                      self.time_to_swap]

        self.action_time = self.time_to_normal_nc

        if combo[3][2] > 0:
            if combo[3][0] == 0:
                self.time_to_normal_nc = self.unit.live_plunge_attack
                self.time_to_skill = self.unit.live_plunge_skill
                self.time_to_burst = self.unit.live_plunge_burst
                self.time_to_swap = self.unit.live_plunge_swap
                self.time_to_cancel = self.unit.live_plunge_cancel
            else:
                if combo[3][1] > 0:
                    for time in self.times:
                        time -= (self.unit.live_charged_attack - max(self.unit.live_charged_tick_times))
                    self.time_to_normal_nc += self.unit.live_plunge_attack
                    self.time_to_skill += self.unit.live_plunge_skill
                    self.time_to_burst += self.unit.live_plunge_burst
                    self.time_to_swap += self.unit.live_plunge_swap
                    self.time_to_cancel += self.unit.live_plunge_cancel
                else:
                    self.time_to_normal_nc = self.unit.live_plunge_attack
                    self.time_to_skill = self.unit.live_plunge_skill
                    self.time_to_burst = self.unit.live_plunge_burst
                    self.time_to_swap = self.unit.live_plunge_swap
                    self.time_to_cancel = self.unit.live_plunge_cancel

        atk_speed_0 = self.tick_times[0] * (1 - (1 / (1 + getattr(self.unit, "live_" + self.tick_types[0] + "_speed"))))
        for time in self.tick_times:
            time -= atk_speed_0

        for time in self.times:
            time -= atk_speed_0

        self.minimum_time = min(
            [self.time_to_cancel, self.time_to_normal_nc, self.time_to_skill, self.time_to_burst, self.time_to_swap])

        self.stamina_cost = [0 for _ in self.unit.live_normal_tick_times[:combo[3][0]]]
        self.stamina_cost.extend(x for x in self.unit.live_charged_stamina_cost[:combo[3][1]])
        if "plunge" in self.unit.live_combo_options:
            self.stamina_cost.extend(x for x in self.unit.live_plunge_stamina_cost[:combo[3][2]])
        self.total_stamina = sum(x for x in self.stamina_cost)

        self.snapshot = False
        self.initial_time = max(self.tick_times)
        self.time_remaining = max(self.tick_times)
        self.proc_type = "No"

    def delay(self, delay):
        for time in self.times:
            time += delay
        for hit_time in self.tick_times:
            hit_time += delay


class Particle(Action):
    def __init__(self, unit_obj, element, amount, sim):
        super().__init__(unit_obj)
        self.ticks = 1
        self.tick_times = [sim.time_into_turn]
        self.element = element
        self.particles = amount
        self.tick_used = ["no"]
        self.tick_types = ["particle"]


class WeaponAction(Action):
    def __init__(self, unit_obj, ticks):
        super().__init__(unit_obj)
        self.name = "weapon"
        self.action_type = "damage"
        self.unit = unit_obj
        self.ticks = ticks
        self.type = "weapon"
        self.tick_types = ["weapon"] * self.ticks
        self.tick_element = ["physical"] * self.ticks
        self.tick_times = [0] * self.ticks
        self.tick_units = [0] * self.ticks
        self.tick_used = ["no"] * self.ticks
        self.tick_scaling = [1] * self.ticks

        self.snapshot = True
        self.particles = 0

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot = True
        self.snapshot_tot_atk = copy(self.unit.base_atk * (1 + self.unit.live_pct_atk) + self.unit.flat_atk)
        self.snapshot_crit_rate = copy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = copy(self.unit.live_crit_dmg)
        self.snapshot_dmg = copy(1 + self.unit.live_all_dmg + getattr(self.unit, "live_physical_dmg"))


class ElectroCharged(Action):
    def __init__(self, unit_obj, sim):
        super().__init__(unit_obj)
        self.ticks = 1
        self.action_type = "damage"
        self.name = str(unit_obj.character) + "Electrocharged"
        self.tick_times = [sim.time_into_turn]
        self.tick_used = ["no"]
        self.tick_types = ["electrocharged"]
        self.tick_units = [0]

    def calculate_tick_damage(self, tick, sim):
        if "Hydro" in sim.enemy.elements and "Electro" in sim.enemy.elements:
            if sim.enemy.elements["Hydro"] > 0 and sim.enemy.elements["Electro"] > 0:
                sim.enemy.elements["Hydro"] -= 0.4
                sim.enemy.elements["Electro"] -= 0.4
                if sim.enemy.elements["Hydro"] > 0 and sim.enemy.elements["Electro"] > 0:
                    ec = ElectroCharged(self.unit, sim)
                    ec.tick_times = [1]
                    ec.add_to_damage_queue(sim)
                dmg = 1443 * (1 + ((4.44 * self.unit.live_ele_m) / (1400 + self.unit.live_ele_m))) * (1 - sim.enemy.live_electro_res)
                print(self.unit.character + " proced electro_charged")
                return dmg
            else:
                return 0
        else:
            return 0

class ManualAction:
    def __init__(self, unit_obj, talent="", combo=""):
        self.unit = unit_obj
        self.talent = talent
        self.combo = combo
        if talent != "" and combo != "":
            raise RuntimeError(f'ManualAction cannot be a talent and a combo') 

    def find_action(self, action_list):
        for action in action_list:
            if action.unit == self.unit: 
                if type(action) == Ability and (self.talent == action.talent):
                    return action
                if type(action) == Combo:
                    combo_name = action.name.split(" ")[1] # action names in the form of "Bennett N4C"
                    if combo_name == self.combo:
                        return action

        raise RuntimeError(f'Could not find action: ({self.unit.character}, {self.talent + self.combo})') 