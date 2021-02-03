import unit as u
from operator import methodcaller
import artifact_substats
import math
from reactions import React
import activeeffects as a
from action import Action
import enemy
import copy

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
        self.action_list = set()
        self.dot_actions = set()
        self.energy_actions = set()
        self.dot_queue = []
        self.sorted_dot_queue = []
        self.energy_queue = []
        self.sorted_energy_queue = []

    ### Starts the sim, adds 1 to the turn number and updates the previous unit
    def start_sim(self):
        self.action_order += 1
        self.last_unit = self.chosen_unit
        self.last_action = self.chosen_action

    ## Creates a new list of actions for the sim to base its choice off
    def update_action_list(self):
        self.action_list = set()
        types = {"normal", "charged", "skill", "burst"}
        for unit in self.units:
            for k in types:
                self.action_list.add(Action(unit,k,self.enemy))
    
    ## Chooses the best action from the action list. Currently does so based on the highest dps
    def choose_action(self):
        self.chosen_action = max(self.action_list, key=methodcaller('calculate_dps',self.enemy))
        self.chosen_unit = self.chosen_action.unit
        if self.action_order == 1:
            self.last_unit = self.chosen_unit
            self.last_action = self.chosen_action

    ## Based on the chosen action, updates the units stats if the action would buff their stats pre-cast
    def add_buff_precast(self):
        for key, trig_buff in self.chosen_unit.triggerable_buffs.items():
            if trig_buff.trigger == self.chosen_action.type or trig_buff.trigger == 'any':
                if trig_buff.precast == "Yes":
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(self.chosen_unit)                     
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = trig_buff
                        else:
                            self.chosen_unit.active_buffs[key] = trig_buff
        for unit in self.units:
            unit.update_stats(self)

    ## Uses the action, adds either adds damage if it's instant or adds it to the dot_actions, puts action on cd
    def use_ability(self):
        self.dot_actions.add(self.chosen_action)
        energy_copy = copy.deepcopy(self.chosen_action)
        energy_copy.initial_time += 1.6
        energy_copy.time_remaining += 1.6
        self.energy_actions.add(energy_copy)
        if self.chosen_action.type == "skill":
            if self.chosen_unit.live_skill_charges > 0:
                self.chosen_unit.live_skill_charges -= 1
            else:
                self.chosen_unit.live_skill_CD = self.chosen_unit.skill_CD
        if self.chosen_action.type == "burst":
            self.chosen_unit.live_burst_CD = self.chosen_unit.burst_CD
            self.chosen_unit.live_burst_energy = 0
    
    ## Adds a buff postcast if the action would trigger a buff
    def add_buff_postcast(self):
        for key, trig_buff in self.chosen_unit.triggerable_buffs.items():
            if trig_buff.trigger == self.chosen_action.type or trig_buff.trigger == 'any':
                if trig_buff.precast != "Yes":
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(self.chosen_unit,self)

                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = trig_buff
                        else:
                            self.chosen_unit.active_buffs[key] = trig_buff   

    ## Adds debuff to enemy
    def add_debuff(self):
        for key, trig_debuff in self.chosen_unit.triggerable_debuffs.items():
            if trig_debuff.trigger == self.chosen_action.type or trig_debuff.trigger == "any":
                    self.enemy.active_debuffs[key] = trig_debuff

    ## Check how long the action took
    def check_turn_time(self):
        if self.chosen_unit == self.last_unit:
            self.turn_time = self.chosen_action.AT
        elif self.last_action.AT < 1:
            self.turn_time = (1-self.last_action.AT) + 0.12 + self.chosen_action.AT
        else:
            self.turn_time = 0.12 + self.chosen_action.AT
    
    ## Check which dot ticks occur in the turn time
    def create_dot_turn(self):
        self.dot_queue = []
        for dot in self.dot_actions:
            times_till_ticks = []
            for i in range(dot.ticks):
                times_till_ticks.append((i,dot.tick_times[i] - (dot.initial_time - dot.time_remaining)))
            for i in range(dot.ticks):
                if 0 <= times_till_ticks[i][1] <= self.turn_time:
                    self.dot_queue.append((i,dot,times_till_ticks[i][1]))

    ## Sort the dot ticks in order of when they tick
    def sort_dot_turn(self):
        self.sorted_dot_queue = sorted(self.dot_queue, key=lambda i: i[2])

    ## Proccesses the dot ticks
    def process_dot_damage(self):
        while self.sorted_dot_queue:
            new = self.sorted_dot_queue.pop(0)
            action = new[1]
            tick = new[0]
            unit = action.tick_units[tick]
            multiplier = 1
            if unit > 0:
                multiplier = getattr(React(),React().check(action,self.enemy))(self,action,self.enemy,unit)
            self.enemy.update_units()
            instance_damage = action.calculate_tick_damage(tick,self.enemy) * multiplier
            # print(instance_damage, action.unit.name, action.type, multiplier)
            self.damage += instance_damage
            

    ## Calc which hits give energy on the turn
    def create_energy_turn(self):
        self.energy_queue = []
        for energy in self.energy_actions:
            times_till_ticks = []
            for i in range(energy.ticks):
                times_till_ticks.append((i,energy.energy_times[i] - (energy.initial_time - energy.time_remaining)))
            for i in range(energy.ticks):
                if 0 <= times_till_ticks[i][1] <= self.turn_time:
                    self.energy_queue.append(energy)

    ## Proccesses the energy
    def process_energy(self):
        for energy in self.energy_queue:
            particles = energy.particles / energy.ticks
            for unit in self.units:
                if unit == self.chosen_unit:
                    if self.chosen_unit.element == energy.element:
                        self.chosen_unit.live_burst_energy += particles * 3 * (1+self.chosen_unit.energy_recharge)
                    else:
                        self.chosen_unit.live_burst_energy += particles * 1 * (1+self.chosen_unit.energy_recharge)
                else:
                    if unit.element == energy.element:
                        unit.live_burst_energy += particles * 1.8 * (1+self.chosen_unit.energy_recharge)
                    else:
                        unit.live_burst_energy += particles * 0.6 * (1+self.chosen_unit.energy_recharge)
            
    ## Lower cooldowns based on turn time
    def reduce_cd(self):
        for unit in self.units:
            unit.live_skill_CD = max(unit.live_skill_CD - self.turn_time,0)
            unit.live_burst_CD = max(unit.live_burst_CD - self.turn_time,0)

    ## Check if buffs ended for units. If they did, remove them
    ## Update stats
    def check_buff_end(self):
        for unit in self.units:
            for key, _, in unit.active_buffs.items():
                unit.active_buffs[key].time_remaining -= self.turn_time
            unit.active_buffs = {k:unit.active_buffs[k] for k in unit.active_buffs if unit.active_buffs[k].time_remaining > 0}
            unit.update_stats(self)

    ## Check if debuff ends for enemies. If they did, remove them
    ## Update Stats
    def check_debuff_end(self):
        for _, debuff in self.enemy.active_debuffs.items():
            debuff.time_remaining -= self.turn_time
        self.enemy.active_debuffs = {k:self.enemy.active_debuffs[k] for k in self.enemy.active_debuffs if self.enemy.active_debuffs[k].time_remaining > 0}
        self.enemy.update_stats(self)
    
    ## Increase the encounter time based on the turn time
    ## Reduce time remaining on dots

    def pass_time(self):
        self.encounter_duration += self.turn_time

        for dot in self.dot_actions:
            dot.time_remaining -= self.turn_time
        self.dot_actions = {x for x in self.dot_actions if x.time_remaining > 0}

        for energy in self.energy_actions:
            energy.time_remaining -= self.turn_time
        self.energy_actions = {x for x in self.energy_actions if x.time_remaining > 0}

    ## Print status
    def status(self):
        print("#" + str(self.action_order) + " Time:" + str(round(self.encounter_duration,2)) + " " + self.chosen_unit.name + " used "
        + self.chosen_action.type)

    def turn_on_sim(self):
        while self.encounter_duration < self.encounter_limit:
            self.start_sim()
            self.update_action_list()
            self.choose_action()
            self.status()
            self.add_buff_precast()
            self.use_ability()
            self.add_buff_postcast()
            self.add_debuff()
            self.check_turn_time()
            self.create_dot_turn()
            self.create_energy_turn()
            self.sort_dot_turn()
            self.process_dot_damage()
            self.process_energy()
            self.reduce_cd()
            self.check_buff_end()
            self.check_debuff_end()
            self.pass_time()
        print(round(self.damage /self.encounter_duration))

PyroArtifact = artifact_substats.ArtifactStats("energy_recharge", "pyro", "crit_rate", "Perfect")
CryoArtifact = artifact_substats.ArtifactStats("energy_recharge", "cryo", "crit_rate", "Perfect")
ElectroArtifact = artifact_substats.ArtifactStats("energy_recharge", "electro", "crit_rate", "Perfect")
AnemoArtifact = artifact_substats.ArtifactStats("energy_recharge", "anemo", "crit_rate", "Perfect")

Main = u.Unit("Fischl", 90, "The Stringless", "Viridescent Venerer", 0, 1, 6, 6, 6, AnemoArtifact)
Support1 = u.Unit("Amber", 90, "The Stringless", "Noblesse", 0, 1, 6, 6, 6, PyroArtifact)
Support2 = u.Unit("Kaeya", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 6, 6, 6, CryoArtifact)
Support3 = u.Unit("Lisa", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 6, 6, 6, ElectroArtifact)
Monster = enemy.Enemy("Hilichurls", 90)

Test = Sim(Main,Support1,Support2,Support3,Monster,100)
Test.turn_on_sim()