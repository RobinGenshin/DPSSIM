## Workaround for ModuleNotFoundError
import sys
from pathlib import Path
txt_working_directory = str(Path(__file__).parent.parent)
sys.path.append(txt_working_directory)

# pylint: disable=no-member
# from characters.TestChars import *
from core import enemy
from core.reactions import React
from core.action import ComboList, Ability, Combo
from effects.resonance import Resonance
import copy
from core.priority_list import PriorityList
from core.read_data import buff_dict, weapon_dict
import cProfile

from collections import deque # import for action overriding

glb_bool_stamina_toggle = True

# Creating a list of actions
class Sim:
    def __init__(self, units, enemy, time, action_override):
        self.units = units
        self.enemy = enemy
        self.encounter_limit = time
        self.encounter_duration = 0
        self.turn_time = 0
        self.time_into_turn = 0
        self.last_action_time = 0
        self.damage = 0
        self.action_order = 0
        self.chosen_unit = None
        self.last_unit = None
        self.chosen_action = None
        self.last_action = None
        self.action_list = set()
        self.floating_actions = []
        self.action_queue = []
        self.sorted_action_queue = []
        self.a_dict = dict()

        self.stamina = 250
        self.stamina_timer = 0
        self.stamina_toggle = glb_bool_stamina_toggle

        self.override_actions = action_override # deque for overriding actions taken

        for unit in self.units:
            unit.damage = 0

    # Team Comp Buffs (Resonance) #
    def resonance(self):
        if sum(1 for unit in self.units if unit.element == "Pyro") >= 2:
            for unit in self.units:
                unit.static_buffs = copy.copy(buff_dict["Pyro_Resonance"])
                getattr(Resonance(), "pyro_resonance")(unit, self)

        if sum(1 for unit in self.units if unit.element == "Hydro") >= 2:
            pass

        if sum(1 for unit in self.units if unit.element == "Geo") >= 2:
            for unit in self.units:
                unit.triggerable_buffs["Geo_Resonance"] = copy.copy(buff_dict["Geo_Resonance"])
                unit.triggerable_buffs["Geo_Resonance"].source = Resonance()
        if sum(1 for unit in self.units if unit.element == "Electro") >= 2:
            for unit in self.units:
                unit.triggerable_buffs["Electro_Resonance"] = copy.copy(buff_dict["Electro_Resonance"])

        if sum(1 for unit in self.units if unit.element == "Anemo") >= 2:
            for unit in self.units:
                unit.static_buffs = copy.copy(buff_dict["Anemo_Resonance"])
                getattr(Resonance(), "anemo_resonance")(unit, self)

        if sum(1 for unit in self.units if unit.element == "Cryo") >= 2:
            for unit in self.units:
                unit.triggerable_buffs["Cryo_Resonance"] = copy.copy(buff_dict["Cryo_Resonance"])

    # Starts the sim, adds 1 to the turn number and updates the previous unit
    def start_sim(self):
        self.action_order += 1
        self.last_unit = copy.copy(self.chosen_unit)
        self.last_action = copy.copy(self.chosen_action)
        self.time_into_turn = 0

    # Creates a new list of actions for the sim to base its choice off
    def update_action_list(self):
        self.action_list = {Ability(unit, k) for unit in self.units for k in {"skill", "burst"} if
                            Ability(unit, k).available(self) == True}
        self.action_list.update(
            Combo(unit, combo) for unit in self.units for combo in ComboList().create(unit, self).values() if
            Combo(unit, combo).available(self) == True)

    # Checks for buffs/triggers and updates stats
    def check_buff(self, type2, action, tick, extra):
        for key, buff in copy.copy(action.unit.triggerable_buffs).items():
            if buff.field == "Yes" and self.chosen_unit == action.unit and (action.tick_types[tick] in buff.trigger or 'any' in buff.trigger) and buff.live_cd == 0 and buff.type2 == type2:
                if buff.duration == "Instant":
                    if buff.share == "Yes":
                        for unit in self.units:
                            getattr(buff.source, buff.method)(unit, self, extra)
                    else:
                        getattr(buff.source, buff.method)(action.unit, self, extra)
                else:
                    if buff.share == "Yes":
                        for unit in self.units:
                            unit.active_buffs[key] = copy.copy(buff)
                    else:
                        if key in self.chosen_unit.active_buffs and buff.max_stacks > 0 and \
                                self.chosen_unit.active_buffs[key].stacks > 0:
                            self.chosen_unit.active_buffs[key].stacks = min(
                                self.chosen_unit.active_buffs[key].max_stacks,
                                self.chosen_unit.active_buffs[key].stacks + 1)
                            self.chosen_unit.active_buffs[key].time_remaining = self.chosen_unit.active_buffs[
                                key].duration
                        else:
                            if buff.max_stacks > 0:
                                self.chosen_unit.active_buffs[key] = copy.copy(self.chosen_unit.triggerable_buffs[key])
                                self.chosen_unit.active_buffs[key].stacks += 1
                            else:
                                self.chosen_unit.active_buffs[key] = copy.copy(buff)
            else:
                if (action.tick_types[
                        tick] in buff.trigger or 'any' in buff.trigger) and buff.live_cd == 0 and buff.type2 == type2:
                    if buff.duration == "Instant":
                        if buff.share == "Yes":
                            for unit in self.units:
                                getattr(buff.source, buff.method)(unit, self, extra)
                        else:
                            getattr(buff.source, buff.method)(action.unit, self, extra)
                    else:
                        if buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = copy.copy(buff)
                        else:
                            self.chosen_unit.active_buffs[key] = copy.copy(buff)

    ## Checks for debuffs/triggers and updates stats
    def check_debuff(self, type2, action, tick):
        for key, debuff in action.unit.triggerable_debuffs.items():
            if (action.tick_types[tick] in debuff.trigger or 'any' in debuff.trigger) and debuff.type2 == type2:
                self.enemy.active_debuffs[key] = debuff
        self.enemy.update_stats

    ## Check if buffs ended for units. If they did, remove them
    def check_buff_end(self):
        for unit in self.units:
            ## Tartaglia Stance Check ##
            if unit.character == "Tartaglia" and "Tartaglia_Stance" in unit.active_buffs:
                if unit.active_buffs["Tartaglia_Stance"].time_remaining <= 0:
                    unit.stance = "ranged"
                    if hasattr(unit, "c6_reset") == True:
                        if unit.c6_reset == True:
                            unit.current_skill_cd = 1
                            unit.c6_reset = False
                    else:
                        unit.current_skill_cd = 51
                    print("Tartaglia Stance Timed Out")

            unit.update_stats(self)
            unit.active_buffs = {k: unit.active_buffs[k] for k in unit.active_buffs if
                                 unit.active_buffs[k].time_remaining > 0}
            unit.update_stats(self)

            for buff in copy.copy(unit.triggerable_buffs):
                if unit.triggerable_buffs[buff].temporary == "Yes" and unit.triggerable_buffs[buff].time_remaining == 0:
                    del unit.triggerable_buffs[buff]

    # Check if debuff ends for enemies. If they did, remove them
    def check_debuff_end(self):
        self.enemy.update_stats(self)
        self.enemy.active_debuffs = {k: self.enemy.active_debuffs[k] for k in self.enemy.active_debuffs if
                                     self.enemy.active_debuffs[k].time_remaining > 0}
        self.enemy.update_stats(self)

    # Chooses the best action from the action list. Currently does so based on the highest dps
    def choose_action(self):
        ## Implement action override edit START ##
        if self.override_actions:
            self.chosen_action = self.override_actions.popleft()
        else:
        ## Implement action override edit END ##
            self.chosen_action = PriorityList().prioritise(self,self.action_list)

        self.chosen_unit = self.chosen_action.unit
        if self.action_order == 1:
            self.last_unit = self.chosen_unit
            self.last_action = self.chosen_action
            for unit in self.units:
                self.a_dict[unit] = [0, 0, 0]

        for unit in self.units:
            if self.chosen_action.unit == unit:
                if self.chosen_action.talent == "skill":
                    self.a_dict[unit][0] += 1
                if self.chosen_action.talent == "burst":
                    self.a_dict[unit][1] += 1
                if self.chosen_action.talent == "combo":
                    self.a_dict[unit][2] += 1

    ## Uses the action, adds either adds damage if it's instant or adds it to the dot_actions, puts action on cd
    def use_ability(self):
        self.check_buff("precast", self.chosen_action, 0, None)
        self.chosen_action.unit.update_stats(self)
        self.chosen_action.add_to_damage_queue(self)

        if self.chosen_action.particles > 0:
            self.chosen_action.add_to_energy_queue(self)

        if self.chosen_action.talent == "skill":
            if self.chosen_unit.current_skill_charges > 0:
                self.chosen_unit.current_skill_charges -= 1
            else:
                self.chosen_unit.current_skill_cd = self.chosen_unit.live_skill_cd
        if self.chosen_action.talent == "burst":
            self.chosen_unit.current_burst_cd = self.chosen_unit.live_burst_cd
            self.chosen_unit.current_energy = 0

        for unit in self.units:
            if hasattr(unit, "stance") == True:
                if unit.character == "Tartaglia" and unit.stance == "melee" and self.last_unit == unit and self.chosen_unit != unit:
                    if hasattr(unit, "c6_reset") == True:
                        if unit.c6_reset == True:
                            unit.current_skill_cd = 1
                            unit.c6_reset = False
                        else:
                            unit.current_skill_cd = (45 - copy.deepcopy(
                                unit.active_buffs["Tartaglia Stance"].time_remaining)) * 2 + 6
                            unit.stance = "ranged"

        self.check_buff("postcast", self.chosen_action, 0, None)

        self.floating_actions = [x for x in self.floating_actions if not (
                (x.unit.character == "Klee") and (x.talent == "burst") and (self.chosen_unit.character != "Klee"))]

    ## Check how long the action took
    def check_turn_time(self):

        self.turn_time = self.chosen_action.minimum_time
        if self.action_order == 1:
            pass
        else:
            if self.last_unit != self.chosen_unit:
                self.turn_time += 0.12
                self.turn_time += (self.last_action.time_to_swap - self.last_action.minimum_time)
            else:
                if self.chosen_action.type == "burst":
                    self.turn_time += (self.last_action.time_to_burst - self.last_action.minimum_time)
                elif self.chosen_action.type == "skill":
                    self.turn_time += (self.last_action.time_to_skill - self.last_action.minimum_time)
                elif self.chosen_action.type == "combo":
                    if self.last_action.type != "combo":
                        self.turn_time += (self.last_action.time_to_attack - self.last_action.minimum_time)
                    else:
                        ## Normal String ##
                        if self.last_action.combo[3][1] == 0 and self.last_action.combo[3][2] == 0:
                            ## Not full string ##
                            if self.last_action.combo[3][0] < self.chosen_unit.live_normal_ticks:
                                self.dash_or_jump()
                            ## Full string ##
                            else:
                                if (self.last_unit.live_normal_at - self.last_action.time_to_cancel) < 0.33:
                                    self.turn_time += (self.last_unit.live_normal_at - self.last_action.time_to_cancel)
                                else:
                                    self.dash_or_jump()
                        ## Charged Attack or Plunge ##
                        else:
                            if (self.last_action.time_to_normal_nc - self.last_action.time_to_cancel) < 0.33:
                                self.turn_time += (self.last_action.time_to_normal_nc - self.last_action.minimum_time)
                            else:
                                self.dash_or_jump()

    ## Check stamina ##
    def check_stamina(self):
        if self.stamina_toggle == True:
            if self.stamina < 50:
                self.stamina_toggle == False
                return False
            else:
                return True
        else:
            if self.stamina > 200:
                self.stamina_toggle == True
                return True

                ## Check dash/jump ##

    def dash_or_jump(self):
        if self.check_stamina() == True:
            ## Dash ##
            self.turn_time += 0.33
            self.stamina -= 18
            self.stamina_timer = -1.5
            self.chosen_action.delay(0.33)
        else:
            ## Jump ##
            self.turn_time += 0.52
            self.chosen_action.delay(0.52)

    ## Reduce triggerable CDs by time interval
    def reduce_buff_times_cds(self, time_interval):
        for unit in self.units:
            for _, trig_buff in unit.triggerable_buffs.items():
                trig_buff.live_cd = max(0, trig_buff.live_cd - time_interval)
                if trig_buff.temporary == "Yes":
                    trig_buff.time_remaining = max(0, trig_buff.time_remaining - time_interval)
            for _, buff in unit.active_buffs.items():
                buff.time_remaining = max(0, buff.time_remaining - time_interval)

        ## Stamina regen ##
        ## if 0.5 left on stamina timer, timer + interval, if timer = 0, interval + stamina timer * 25 
        initial_timer = copy.copy(self.stamina_timer)
        self.stamina_timer = min(0, time_interval + self.stamina_timer)
        if self.stamina_timer == 0:
            self.stamina = min(250, self.stamina + (time_interval + initial_timer) * 25)

        self.check_buff_end()

    ## Check which dot ticks occur in the turn time
    def create_action_queue_turn(self, time_into_turn):
        self.action_queue = []
        for action in self.floating_actions:
            times_till_ticks = []
            for i in range(action.ticks):
                times_till_ticks.append((i, action.tick_times[i] - (action.initial_time - action.time_remaining)))
            for i in range(action.ticks):
                if time_into_turn <= times_till_ticks[i][1] <= self.turn_time:
                    if action.tick_used[i] == "no":
                        self.action_queue.append((i, action, times_till_ticks[i][1]))

    ## Sort the dot ticks in order of when they tick
    def sort_action_turn(self):
        self.sorted_action_queue = sorted(self.action_queue, key=lambda i: i[2])

    ## Proccesses actions
    def process_action(self):
        new = self.sorted_action_queue.pop(0)
        if new[1].action_type == "damage":
            self.process_action_damage(new)
        elif new[1].action_type == "energy":
            self.process_action_energy(new)
        else:
            print("Error", new[1].unit.character)

    ## Attack Speed
    def attack_speed(self, action, tick):
        if tick < action.ticks - 1:
            atk_speed = (action.tick_times[tick + 1] - action.tick_times[tick]) * (
                    1 - (1 / (1 + getattr(action.unit, "live_" + action.tick_types[tick + 1] + "_speed"))))
            for time in action.tick_times:
                time -= atk_speed
            for time in action.times:
                time -= atk_speed
            self.turn_time -= atk_speed

    # Hitlag
    def hitlag(self, action, tick):
        hitlag = action.tick_hitlag[tick] * (3 / self.enemy.hitlag) * (1 / 60)
        for time in action.tick_times:
            time += hitlag
        for time in action.times:
            time += hitlag
        self.turn_time += hitlag

    # Processes damage actions (ticks)
    def process_action_damage(self, new):
        tick = new[0]
        damage_action = new[1]

        damage_action.tick_used[tick] = "yes"

        self.last_action_time = copy.copy(self.time_into_turn)
        self.time_into_turn = new[2]

        time_since_last_action = self.time_into_turn - self.last_action_time
        self.reduce_buff_times_cds(time_since_last_action)

        self.check_buff("pre_hit", damage_action, tick, None)
        self.check_buff("mid_hit", damage_action, tick, [damage_action, tick])

        damage_action_element_unit = damage_action.tick_units[tick]
        multiplier = 1
        if damage_action_element_unit > 0:
            reaction = getattr(React(), React().check(damage_action, tick, self.enemy))(damage_action, tick, self.enemy,
                                                                                        damage_action_element_unit,
                                                                                        self)
            reaction[1].append(damage_action)
            multiplier = reaction[0]
            self.check_buff("reaction", damage_action, tick, reaction[1])

        self.enemy.update_units()
        instance_damage = damage_action.calculate_tick_damage(tick, self) * multiplier
        self.damage += instance_damage

        for unit in self.units:
            if damage_action.unit == unit:
                unit.damage += instance_damage

        self.check_buff("on_hit", damage_action, tick, None)
        self.check_debuff("on_hit", damage_action, tick)

        self.check_buff_end()
        self.check_debuff_end()
        if damage_action.talent == "combo":
            self.attack_speed(damage_action, tick)
            self.hitlag(damage_action, tick)
            self.stamina -= damage_action.stamina_cost[tick]
            if damage_action.stamina_cost[tick] > 0:
                self.stamina_timer = -1.5

    # Proccesses the energy
    def process_action_energy(self, new):
        tick = new[0]
        energy_action = new[1]
        energy_action.tick_used[tick] = "yes"
        self.last_energy_action_time = copy.copy(self.time_into_turn)
        self.time_into_turn = new[2]

        time_since_last_action = self.time_into_turn - self.last_energy_action_time
        self.reduce_buff_times_cds(time_since_last_action)
        particles = energy_action.particles / energy_action.ticks

        for unit in self.units:
            if unit == self.chosen_unit:
                if self.chosen_unit.element == energy_action.unit.element:
                    self.chosen_unit.current_energy += particles * 3 * (1 + self.chosen_unit.recharge)
                else:
                    self.chosen_unit.current_energy += particles * 1 * (1 + self.chosen_unit.recharge)
            else:
                if unit.element == energy_action.unit.element:
                    unit.current_energy += particles * 1.8 * (1 + unit.recharge)
                else:
                    unit.current_energy += particles * 0.6 * (1 + unit.recharge)

        self.check_buff("particle", energy_action, tick, None)
        self.check_buff_end()
        self.check_debuff_end()

    # Loops damage queue processing
    def process_loop(self):
        self.create_action_queue_turn(self.time_into_turn)
        while len(self.action_queue) > 0:
            self.sort_action_turn()
            self.process_action()
            self.create_action_queue_turn(self.time_into_turn)

    # Lower cooldowns based on turn time
    def reduce_cd(self):
        for unit in self.units:
            unit.current_skill_cd = max(unit.current_skill_cd - self.turn_time, 0)
            unit.current_burst_cd = max(unit.current_burst_cd - self.turn_time, 0)

    # Passes time
    def pass_turn_time(self):
        self.encounter_duration += self.turn_time
        for action in self.floating_actions:
            action.time_remaining -= self.turn_time

        self.floating_actions = [x for x in self.floating_actions if x.time_remaining > 0]

        for unit in self.units:
            for _, trig_buff in unit.triggerable_buffs.items():
                trig_buff.live_cd = max(0, trig_buff.live_cd - (self.turn_time - self.time_into_turn))
                if trig_buff.temporary == "Yes":
                    trig_buff.time_remaining = max(0, trig_buff.time_remaining - (self.turn_time - self.time_into_turn))
            for _, buff in unit.active_buffs.items():
                buff.time_remaining = max(0, buff.time_remaining - (self.turn_time - self.time_into_turn))

        initial_timer = copy.copy(self.stamina_timer)
        self.stamina_timer = min(0, (self.turn_time - self.time_into_turn) + self.stamina_timer)
        if self.stamina_timer == 0:
            self.stamina = min(250, self.stamina + ((self.turn_time - self.time_into_turn) + initial_timer) * 25)

    # Print status
    def status(self):
        if hasattr(self.chosen_unit, "stance"):
            stance = " (" + self.chosen_unit.stance + ")"
        else:
            stance = ""
        if self.chosen_action.talent == "combo":
            action = self.chosen_action.combo[4]
        else:
            action = self.chosen_action.talent
        print("#" + str(self.action_order) + " Time:" + str(
            round(self.encounter_duration, 2)) + " " + self.chosen_unit.character + stance + " used "
              + action, "Stamina:", self.stamina)

    # Turns on the sim
    def turn_on_sim(self):
        self.resonance()
        ## Implement action override edit START
        if self.override_actions != None: # if user wants to simulate actions
           while self.override_actions: # loop as long as there are actions to simulate
                self.start_sim()
                self.choose_action() # update_action_list not needed as we use our own inputs
                self.use_ability()
                self.status()
                self.check_turn_time()
                self.process_loop()
                self.reduce_cd()
                self.pass_turn_time()
                self.check_buff_end()
                self.check_debuff_end()
        else:
        ## Implement action override edit END
            while self.encounter_duration < self.encounter_limit:
                self.start_sim()
                self.update_action_list()
                self.choose_action()
                self.use_ability()
                self.status()
                self.check_turn_time()
                self.process_loop()
                self.reduce_cd()
                self.pass_turn_time()
                self.check_buff_end()
                self.check_debuff_end()
        print("Time:" + str(round(self.encounter_duration, 2)),
                  "DPS:" + str(round(self.damage / self.encounter_duration, 2)))

    def brute_force_weapon(self, unit_obj, unit_artifact):
        self.units.remove(unit_obj)
        weapon_ranks = dict()

        def check_weapon(unit, artifact, weapon):
            units = copy.deepcopy(self.units)
            check = unit.__class__(90, 6, weapon, 5, artifact, [6, 6, 6])
            units.add(check)
            sim = Sim(units, Monster, 60)
            sim.turn_on_sim()
            units.remove(check)
            weapon_ranks[weapon] = sim.damage / sim.encounter_duration
            return [sim.damage / sim.encounter_duration, weapon]

        a = max(check_weapon(unit_obj, unit_artifact, weapon) for weapon, obj in weapon_dict.items() if obj.type == unit_obj.weapon_type)
        # return str(unit_obj.__class__.__name__) + "'s best weapon was " + a[1] + " at " + str(round(a[0]))
        return {k: v for k, v in sorted(weapon_ranks.items(), key=lambda item: item[1])}

    @classmethod
    def brute_force_recharge(cls, unit_obj, unit_artifact, *args):
        def check_recharge(unit, i):
            check = unit.__class__(90, 6, unit.weapon, 5, unit_artifact, [6, 6, 6])
            check.crit_rate -= 0.0165 * i
            check.crit_dmg -= 0.033 * i
            check.recharge += 0.0583 * i
            sim = cls({check, *args}, Monster, 200)
            sim.turn_on_sim()
            return [sim.damage / sim.encounter_duration, i]

        dmg = [0, 0]
        for i in range(unit_obj.artifact.initial_subs):
            if check_recharge(unit_obj, i)[0] > dmg[0]:
                dmg = check_recharge(unit_obj, i)
        return dmg


Monster = enemy.Enemy("Ruin Guard", 100)


def main():
    from characters.Diluc import DilucF2P, DilucArtifact
    from characters.Xingqiu import XingqiuF2P, XingqiuArtifact
    from characters.Venti import VentiF2P
    from characters.Mona import MonaF2P
    from characters.Klee import KleeF2P
    from characters.Ningguang import NingguangF2P
    from characters.Albedo import AlbedoF2P, AlbedoArtifact
    from characters.Fischl import FischlF2P
    from characters.Bennett import BennettF2P
    from characters.Chongyun import ChongyunF2P
    from characters.Kaeya import KaeyaF2P
    from characters.Keqing import KeqingF2P

    from action import Ability
    from action import ComboList
    from action import Combo

    #Instantiate unit combos
    DilucCombos = ComboList().create(DilucF2P,glb_bool_stamina_toggle)

    #Define actions to simulate
    ActionsToSim = deque()
    ActionsToSim.append(Ability(XingqiuF2P,"skill"))
    ActionsToSim.append(Ability(XingqiuF2P,"burst"))
    ActionsToSim.append(Ability(DilucF2P,"burst"))
    ActionsToSim.append(Combo(DilucF2P,DilucCombos["N1"]))
    ActionsToSim.append(Ability(DilucF2P,"skill"))
    ActionsToSim.append(Combo(DilucF2P,DilucCombos["N1"]))
    ActionsToSim.append(Ability(DilucF2P,"skill"))
    ActionsToSim.append(Combo(DilucF2P,DilucCombos["N1"]))
    ActionsToSim.append(Ability(DilucF2P,"skill"))

    Test = Sim({DilucF2P, XingqiuF2P}, Monster, None, ActionsToSim)
    Test.turn_on_sim()
    # for key, dps in Test.brute_force_weapon(KeqingF2P, AlbedoArtifact).items():
    #     print("Weapon: " + key, "DPS:", round(dps))

    # print([(key, str(round(combo[0]*100,2)) + "%") for key, combo in ComboList.create(KaeyaF2P, Test).items()])

    # cProfile.runctx("Test.turn_on_sim()", None, locals())

    # for key, value in Test.a_dict.items():
    #     print(key.character, "Skills used:" + str(value[0]), "Bursts used:" + str(value[1]), "Combos used:" + str(value[2]))


if __name__ == '__main__':
    main()
