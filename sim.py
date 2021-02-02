import csv
import read_data as rd
import unit as u
from operator import attrgetter
import artifact_substats
import math
import itertools
import reactions as r
import buffs as c
from action import Action
import enemy

# Creating a list of actions
class Sim:
    def __init__ (self, main,sup1,sup2,sup3,enemy,time):
        self.encounter_limit = time
        self.encounter_duration = 0
        self.turn_time = 0
        self.damage = 0
        self.units = {main,sup1,sup2,sup3}
        self.enemy = enemy
        self.action_order = 0
        self.chosen_unit = None
        self.last_unit = None
        self.chosen_action = None
        self.last_action = None
        self.dot_actions = set()
        self.action_list = set()
        self.reaction_queue = []
        self.sorted_queue = []

    def start_sim(self):
        self.action_order += 1
        self.last_unit = self.chosen_unit
        self.last_action = self.chosen_action

    def update_action_list(self):
        self.action_list = set()
        types = {"normal_attack", "charged_attack", "skill", "burst"}
        for unit in self.units:
            for k in types:
                self.action_list.add(Action(unit,k,self.enemy))
    
    def choose_action(self):
        self.chosen_action = max(self.action_list, key=attrgetter('dps'))
        self.chosen_unit = self.chosen_action.unit
        if self.action_order == 1:
            self.last_unit = self.chosen_unit
            self.last_action = self.chosen_action

    def add_buff_precast(self):
        for key, trig_buff in self.chosen_unit.triggerable_buffs.items():
            if trig_buff.trigger == self.chosen_action.type or trig_buff.trigger == 'any':
                if trig_buff.precast == "Yes":
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(c.ActiveBuff(),trig_buff.method)(unit)
                        else:
                            getattr(c.ActiveBuff(),trig_buff.method)(self.chosen_unit)                     
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = trig_buff
                        else:
                            self.chosen_unit.active_buffs[key] = trig_buff
        for unit in self.units:
            unit.update_stats(self)

    def use_ability(self):
        self.chosen_action.recalc_dps(self.enemy)
        if self.chosen_action.duration == "Instant":
            getattr(r.React(),r.React().check(self.chosen_action,self.enemy))(self,self.chosen_action,self.enemy)
            self.damage += self.chosen_action.damage
        else:
            self.dot_actions.add(self.chosen_action)
        for unit in self.units:
            if unit == self.chosen_unit:
                if self.chosen_action.type == "skill":
                    if self.chosen_unit.live_skill_charges > 0:
                        self.chosen_unit.live_skill_charges -= 1
                    else:
                        unit.live_skill_CD = unit.skill_CD
                if self.chosen_action.type == "burst":
                    if self.chosen_unit.live_burst_charges > 0:
                        self.chosen_unit.live_burst_charges -= 1
                    else:
                        unit.live_burst_CD = unit.burst_CD
                        unit.live_burst_energy = 0
    
    def add_buff_postcast(self):
        for key, trig_buff in self.chosen_unit.triggerable_buffs.items():
            if trig_buff.trigger == self.chosen_action.type or trig_buff.trigger == 'any':
                if trig_buff.precast != "Yes":
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(c.ActiveBuff(),trig_buff.method)(unit)
                        else:
                            getattr(c.ActiveBuff(),trig_buff.method)(self.chosen_unit)                     
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = trig_buff
                        else:
                            self.chosen_unit.active_buffs[key] = trig_buff                            

    def add_debuff(self):
        for key, trig_debuff in self.chosen_unit.triggerable_debuffs.items():
            if trig_debuff.trigger == self.chosen_action.type or trig_debuff.trigger == "any":
                    self.enemy.active_debuffs[key] = trig_debuff

    def check_turn_time(self):
        if self.chosen_unit == self.last_unit:
            self.turn_time = self.chosen_action.AT
        elif self.last_action.AT < 1:
            self.turn_time = (1-self.last_action.AT) + 0.12 + self.chosen_action.AT
        else:
            self.turn_time = 0.12 + self.chosen_action.AT
    
    def create_dot_reactions_turn(self):
        self.reaction_queue = []
        for dot in self.dot_actions:
            time_per_tick = dot.duration / dot.ticks
            times_till_ticks = list()
            times_for_turn = list()
            for i in range(int(dot.ticks)):
                times_till_ticks.append((i,(dot.time_remaining - i*time_per_tick)))
            for i in range(int(dot.ticks)):
                if 0 <= times_till_ticks[i][1] <= self.turn_time:
                    times_for_turn.append((i,(dot,times_till_ticks[i][1])))
            for i in times_for_turn:
                self.reaction_queue.append(i)

    def sort_dot_reactions_turn(self):
        self.sorted_queue = sorted(self.reaction_queue, key=lambda i: i[1][1])

    def process_dot(self):
        while self.sorted_queue:
            dot = self.sorted_queue.pop(0)[1][0]
            getattr(r.React(),r.React().check(dot,self.enemy))(self,dot,self.enemy)
            self.damage += dot.damage / dot.ticks
            particles = dot.particles / dot.ticks
            for unit in self.units:
                energy_gain = particles * 3 * ( 1 + unit.energy_recharge )
                if unit.element == dot.unit.element:
                    energy_gain *= 1
                else:
                    energy_gain *= 0.33
                if unit == self.chosen_unit:
                    energy_gain *= 1
                else:
                    energy_gain *= 0.6
                unit.live_burst_energy = min((unit.live_burst_energy + energy_gain),unit.burst_energy)
    
    def reduce_cd(self):
        for unit in self.units:
            unit.live_skill_CD = max(unit.live_skill_CD - self.turn_time,0)
            unit.live_burst_CD = max(unit.live_burst_CD - self.turn_time,0)

    def add_energy(self):
        if self.chosen_action.duration == "Instant":
            particles = self.chosen_action.particles
            for unit in self.units:
                energy_gain = particles * 3 * ( 1 + unit.energy_recharge )
                if unit.element == self.chosen_action.unit.element:
                    energy_gain *= 1
                else:
                    energy_gain /= 3
                if unit == self.chosen_unit:
                    energy_gain *= 1
                else:
                    energy_gain *= 0.6
                unit.live_burst_energy = min((unit.live_burst_energy + energy_gain),unit.burst_energy)
        else:
            pass

    def check_buff_end(self):
        for unit in self.units:
            for key, _, in unit.active_buffs.items():
                unit.active_buffs[key].time_remaining -= self.turn_time
            unit.active_buffs = {k:unit.active_buffs[k] for k in unit.active_buffs if unit.active_buffs[k].time_remaining > 0}
            unit.update_stats(self)

    def check_debuff_end(self):
        for _, debuff in self.enemy.active_debuffs.items():
            debuff.time_remaining -= self.turn_time
        self.enemy.active_debuffs = {k:self.enemy.active_debuffs[k] for k in self.enemy.active_debuffs if self.enemy.active_debuffs[k].time_remaining > 0}
        self.enemy.update_stats(self)
    
    def pass_time(self):
        self.encounter_duration += self.turn_time
        for dot in self.dot_actions:
            dot.time_remaining -= self.turn_time
        self.dot_actions = {x for x in self.dot_actions if x.time_remaining > 0}


    def status(self):
        print("#" + str(self.action_order) + " Time:" + self.chosen_unit.name + " used "
        + self.chosen_action.type)

    def turn_on_sim(self):
        while self.encounter_duration < self.encounter_limit:
            self.start_sim()
            self.update_action_list()
            self.choose_action()
            self.add_buff_precast()
            self.use_ability()
            self.add_buff_postcast()
            self.add_debuff()
            self.check_turn_time()
            self.create_dot_reactions_turn()
            self.sort_dot_reactions_turn()
            self.process_dot()
            self.reduce_cd()
            self.check_buff_end()
            self.check_debuff_end()
            self.add_energy()
            self.pass_time()
            self.status()
        print(round(self.damage /self.encounter_duration))

PyroArtifact = artifact_substats.ArtifactStats("energy_recharge", "pyro", "crit_rate", "Perfect")
CryoArtifact = artifact_substats.ArtifactStats("energy_recharge", "cryo", "crit_rate", "Perfect")
ElectroArtifact = artifact_substats.ArtifactStats("energy_recharge", "electro", "crit_rate", "Perfect")

Main = u.Unit("Amber", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, PyroArtifact)
Support1 = u.Unit("Diona", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, CryoArtifact)
Support2 = u.Unit("Fischl", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, ElectroArtifact)
Support3 = u.Unit("Ganyu", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, CryoArtifact)
Monster = enemy.Enemy("Hilichurls", 90)

Test = Sim(Main,Support1,Support2,Support3,Monster,10)
Test.turn_on_sim()
