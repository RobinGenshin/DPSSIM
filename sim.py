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
        self.time_into_turn = 0
        self.last_action_time = 0
        self.action_time = 0
        self.damage = 0
        self.units = {main,sup1,sup2,sup3}
        self.enemy = enemy
        self.action_order = 0
        self.chosen_unit = None
        self.last_unit = None
        self.chosen_action = None
        self.last_action = None
        self.action_list = set()
        self.floating_actions= set()
        self.action_queue = []
        self.sorted_action_queue = []

    ### Starts the sim, adds 1 to the turn number and updates the previous unit
    def start_sim(self):
        self.action_order += 1
        self.last_unit = copy.deepcopy(self.chosen_unit)
        self.last_action = copy.deepcopy(self.chosen_action)
        self.time_into_turn = 0

    ## Creates a new list of actions for the sim to base its choice off
    def update_action_list(self):
        self.action_list = set()
        types = {"normal", "charged", "skill", "burst"}
        for unit in self.units:
            for k in types:
                self.action_list.add(Action(unit,k,self.enemy))
        
    ## Checks for buffs/triggers and updates stats
    def check_buff(self, type2, action):
        for key, trig_buff in copy.deepcopy(action.unit.triggerable_buffs).items():
            if trig_buff.field == "Yes" and self.chosen_unit == action.unit:
                if (action.type in trig_buff.trigger or 'any'in trig_buff.trigger) and trig_buff.live_cd == 0 and trig_buff.type2 == type2:
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(action.unit,self)
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = copy.deepcopy(trig_buff)
                                unit.update_stats(self)
                        else:
                            if key in self.chosen_unit.active_buffs and trig_buff.max_stacks > 0 and self.chosen_unit.active_buffs[key].stacks > 0:
                                self.chosen_unit.active_buffs[key].stacks = min(self.chosen_unit.active_buffs[key].max_stacks,self.chosen_unit.active_buffs[key].stacks + 1)
                                self.chosen_unit.active_buffs[key].time_remaining = self.chosen_unit.active_buffs[key].duration
                            else:
                                if trig_buff.max_stacks > 0:
                                    self.chosen_unit.active_buffs[key] = copy.deepcopy(self.chosen_unit.triggerable_buffs[key])
                                    self.chosen_unit.active_buffs[key].stacks += 1
                                    self.chosen_unit.update_stats(self)
                                else:
                                    self.chosen_unit.active_buffs[key] = copy.deepcopy(trig_buff)
                                    self.chosen_unit.update_stats(self)
            else:
                if (action.type in trig_buff.trigger or 'any' in trig_buff.trigger) and trig_buff.live_cd == 0 and trig_buff.type2 == type2:
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(action.unit,self)
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                    unit.active_buffs[key] = copy.deepcopy(trig_buff)
                                    unit.update_stats(self)
                        else:
                            self.chosen_unit.active_buffs[key] = copy.deepcopy(trig_buff)
                            self.chosen_unit.update_stats(self)   

    ## Dupe of above but for reactions (too lazy to integrate)
    def check_buff_reaction(self,type2,action,reaction):
        for key, trig_buff in copy.deepcopy(action.unit.triggerable_buffs).items():
            if trig_buff.field == "Yes" and self.chosen_unit == action.unit:
                if (action.type in trig_buff.trigger or 'any'in trig_buff.trigger) and trig_buff.live_cd == 0 and trig_buff.type == type2:
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self,reaction)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(action.unit,self,reaction)
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                unit.active_buffs[key] = copy.deepcopy(trig_buff)
                                unit.update_stats(self)
                        else:
                            if key in self.chosen_unit.active_buffs and trig_buff.max_stacks > 0 and self.chosen_unit.active_buffs[key].stacks > 0:
                                self.chosen_unit.active_buffs[key].stacks = min(self.chosen_unit.active_buffs[key].max_stacks,self.chosen_unit.active_buffs[key].stacks + 1)
                                self.chosen_unit.active_buffs[key].time_remaining = self.chosen_unit.active_buffs[key].duration
                            else:
                                if trig_buff.max_stacks > 0:
                                    self.chosen_unit.active_buffs[key] = copy.deepcopy(self.chosen_unit.triggerable_buffs[key])
                                    self.chosen_unit.active_buffs[key].stacks += 1
                                    self.chosen_unit.update_stats(self)
                                else:
                                    self.chosen_unit.active_buffs[key] = copy.deepcopy(trig_buff)
                                    self.chosen_unit.update_stats(self)
            else:
                if (action.type in trig_buff.trigger or 'any' in trig_buff.trigger) and trig_buff.live_cd == 0 and trig_buff.type2 == type2:
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self,reaction)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(action.unit,self,reaction)
                    else:
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                    unit.active_buffs[key] = copy.deepcopy(trig_buff)
                                    unit.update_stats(self)
                        else:
                            self.chosen_unit.active_buffs[key] = copy.deepcopy(trig_buff)
                            self.chosen_unit.update_stats(self) 

    def check_buff_particle(self,type2,action):
        for _, trig_buff in copy.deepcopy(action.unit.triggerable_buffs).items():
            if trig_buff.field == "Yes" and self.chosen_unit == action.unit:
                if (action.type in trig_buff.trigger or 'any'in trig_buff.trigger) and trig_buff.live_cd == 0 and trig_buff.type == type2:
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self,action)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(action.unit,self,action)

    def check_buff_specific_hit(self,type2,action,tick):
        for _, trig_buff in copy.deepcopy(action.unit.triggerable_buffs).items():
            if trig_buff.field == "Yes" and self.chosen_unit == action.unit:
                if (action.type in trig_buff.trigger or 'any'in trig_buff.trigger) and trig_buff.live_cd == 0 and trig_buff.type == type2:
                    if trig_buff.instant == "Instant":
                        if trig_buff.share == "Yes":
                            for unit in self.units:
                                getattr(a.ActiveBuff(),trig_buff.method)(unit,self,action,tick)
                        else:
                            getattr(a.ActiveBuff(),trig_buff.method)(action.unit,self,action,tick)

    ## Checks for debuffs/triggers and updates stats
    def check_debuff(self, type2, action):
        for key, trig_debuff in self.chosen_unit.triggerable_debuffs.items():
            if trig_debuff.trigger == self.chosen_action.type or trig_debuff.trigger == "any":
                if trig_debuff.type2 == type2:
                    self.enemy.active_debuffs[key] = trig_debuff
        self.enemy.update_stats

    ## Check if buffs ended for units. If they did, remove them
    def check_buff_end(self):
        for unit in self.units:
            unit.active_buffs = {k:unit.active_buffs[k] for k in unit.active_buffs if unit.active_buffs[k].time_remaining > 0}
            unit.update_stats(self)

            for buff in copy.deepcopy(unit.triggerable_buffs):
                if unit.triggerable_buffs[buff].temporary == "Yes":
                    if unit.triggerable_buffs[buff].time_remaining == 0:
                        del unit.triggerable_buffs[buff]

    ## Check if debuff ends for enemies. If they did, remove them
    def check_debuff_end(self):
        self.enemy.active_debuffs = {k:self.enemy.active_debuffs[k] for k in self.enemy.active_debuffs if self.enemy.active_debuffs[k].time_remaining > 0}
        self.enemy.update_stats(self)

    ## Chooses the best action from the action list. Currently does so based on the highest dps
    def choose_action(self):
        self.chosen_action = max(self.action_list, key=methodcaller('calculate_dps_snapshot',self.enemy))
        self.chosen_unit = self.chosen_action.unit
        if self.action_order == 1:
            self.last_unit = copy.deepcopy(self.chosen_unit)
            self.last_action = copy.deepcopy(self.chosen_action)

    ## Uses the action, adds either adds damage if it's instant or adds it to the dot_actions, puts action on cd
    def use_ability(self):
        self.chosen_action.action_type = "damage"
        self.floating_actions.add(self.chosen_action)
        energy_copy = copy.deepcopy(self.chosen_action)
        energy_copy.action_type = "energy"
        energy_copy.initial_time += 1.6
        energy_copy.time_remaining += 1.6
        self.floating_actions.add(energy_copy)
        if self.chosen_action.type == "skill":
            if self.chosen_unit.live_skill_charges > 0:
                self.chosen_unit.live_skill_charges -= 1
            else:
                self.chosen_unit.live_skill_CD = self.chosen_unit.skill_CD
        if self.chosen_action.type == "burst":
            self.chosen_unit.live_burst_CD = self.chosen_unit.burst_CD
            self.chosen_unit.live_burst_energy = 0
 
    ## Check how long the action took
    def check_turn_time(self):
        if self.chosen_unit == self.last_unit:
            self.turn_time = self.chosen_action.AT
        elif self.last_action.AT < 1:
            self.turn_time = (1-self.last_action.AT) + 0.12 + self.chosen_action.AT
        else:
            self.turn_time = 0.12 + self.chosen_action.AT
    
    ## Reduce triggerable CDs by time interval
    def reduce_buff_times_cds(self,time_interval):
        for unit in self.units:
            for _, trig_buff in unit.triggerable_buffs.items():
                trig_buff.live_cd = max(0, trig_buff.live_cd - time_interval)
                if trig_buff.temporary == "Yes":
                    trig_buff.time_remaining = max(0, trig_buff.time_remaining - time_interval)
            for _, buff in unit.active_buffs.items():
                buff.time_remaining = max(0, buff.time_remaining - time_interval)

    ## Check which dot ticks occur in the turn time
    def create_action_queue_turn(self,time_into_turn):
        self.action_queue = []
        for action in self.floating_actions:
            times_till_ticks = []
            for i in range(action.ticks):
                times_till_ticks.append((i,action.tick_times[i] - (action.initial_time - action.time_remaining)))
            for i in range(action.ticks):
                if time_into_turn <= times_till_ticks[i][1] <= self.turn_time:
                    if action.tick_used[i] == "no":
                        self.action_queue.append((i,action,times_till_ticks[i][1]))

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
            print("Error",new[1].unit.name)

    ## Processes damage actions (ticks)
    def process_action_damage(self,new):
        tick = new[0]
        damage_action = new[1]
        damage_action.tick_used[tick] = "yes"
        self.last_action_time = copy.deepcopy(self.time_into_turn)
        self.time_into_turn = new[2]

        time_since_last_action = self.time_into_turn - self.last_action_time
        self.reduce_buff_times_cds (time_since_last_action)

        self.check_buff("pre_hit",damage_action)
        self.check_buff_specific_hit("specific_hit",damage_action,tick)

        damage_action_element_unit = damage_action.tick_units[tick]
        multiplier = 1
        if damage_action_element_unit > 0:
            reaction = getattr(React(),React().check(damage_action,self.enemy))(self,damage_action,self.enemy,damage_action_element_unit)
            reaction.append(damage_action)
            multiplier = reaction[0]
            self.check_buff_reaction("reaction",damage_action,reaction[1])

        self.enemy.update_units()
        instance_damage = damage_action.calculate_tick_damage(tick,self.enemy) * multiplier
        self.damage += instance_damage

        self.check_buff("on_hit",damage_action)
        self.check_debuff("on_hit", damage_action)

        self.check_buff_end()
        self.check_debuff_end()

    ## Proccesses the energy
    def process_action_energy(self,new):
        tick = new[0]
        energy_action = new[1]
        energy_action.tick_used[tick] = "yes"
        self.last_action_time = copy.deepcopy(self.time_into_turn)
        self.time_into_turn = new[2]

        time_since_last_action = self.time_into_turn - self.last_action_time
        self.reduce_buff_times_cds (time_since_last_action)

        particles = energy_action.particles / energy_action.ticks
        for unit in self.units:
            if unit == self.chosen_unit:
                if self.chosen_unit.element == energy_action.element:
                    self.chosen_unit.live_burst_energy += particles * 3 * (1+self.chosen_unit.energy_recharge)
                else:
                    self.chosen_unit.live_burst_energy += particles * 1 * (1+self.chosen_unit.energy_recharge)
            else:
                if unit.element == energy_action.element:
                    unit.live_burst_energy += particles * 1.8 * (1+self.chosen_unit.energy_recharge)
                else:
                    unit.live_burst_energy += particles * 0.6 * (1+self.chosen_unit.energy_recharge)

        self.check_buff("particle",energy_action)
        self.check_buff_particle("specific_particle",energy_action)
        self.check_buff_end()
        self.check_debuff_end()
    
    ## Loops damage queue processing
    def process_loop(self):
        self.create_action_queue_turn(self.time_into_turn)
        while len(self.action_queue) > 0:
            self.sort_action_turn()
            self.process_action()
            self.create_action_queue_turn(self.time_into_turn)
               
    ## Lower cooldowns based on turn time
    def reduce_cd(self):
        for unit in self.units:
            unit.live_skill_CD = max(unit.live_skill_CD - self.turn_time,0)
            unit.live_burst_CD = max(unit.live_burst_CD - self.turn_time,0)

    ## Passes time
    def pass_turn_time(self):
        self.encounter_duration += self.turn_time

        for action in self.floating_actions:
            action.time_remaining -= self.turn_time
        self.floating_actions = {x for x in self.floating_actions if x.time_remaining > 0}

        for unit in self.units:
            for _, trig_buff in unit.triggerable_buffs.items():
                trig_buff.live_cd = max(0, trig_buff.live_cd - (self.turn_time-self.time_into_turn))
                if trig_buff.temporary == "Yes":
                    trig_buff.time_remaining = max(0, trig_buff.time_remaining - (self.turn_time-self.time_into_turn))
            for _, buff in unit.active_buffs.items():
                buff.time_remaining = max(0, buff.time_remaining - (self.turn_time-self.time_into_turn))

    ## Print status
    def status(self):
        print("#" + str(self.action_order) + " Time:" + str(round(self.encounter_duration,2)) + " " + self.chosen_unit.name + " used "
        + self.chosen_action.type)

    ## Turns on the sim (lol)
    def turn_on_sim(self):
        while self.encounter_duration < self.encounter_limit:
            self.start_sim()
            self.update_action_list()
            self.choose_action()
            self.status()
            self.check_buff("precast",self.chosen_action)
            self.use_ability()
            self.check_buff("postcast",self.chosen_action)
            self.check_turn_time()
            self.process_loop()
            self.reduce_cd()
            self.pass_turn_time()
            self.check_buff_end()
            self.check_debuff_end()
            
        print(round(self.damage /self.encounter_duration))


PyroArtifact = artifact_substats.ArtifactStats("energy_recharge", "pyro", "crit_rate", "Perfect")
CryoArtifact = artifact_substats.ArtifactStats("energy_recharge", "cryo", "crit_rate", "Perfect")
ElectroArtifact = artifact_substats.ArtifactStats("energy_recharge", "electro", "crit_rate", "Perfect")
AnemoArtifact = artifact_substats.ArtifactStats("energy_recharge", "anemo", "crit_rate", "Perfect")
HydroArtifact = artifact_substats.ArtifactStats("atk_pct", "hydro", "crit_rate", "Perfect")

Main = u.Unit("Tartaglia", 90, "Skyward Harp", "Heart of Depth", 6, 5, 6, 10, 6, HydroArtifact)
Support1 = u.Unit("Amber", 1, "Skyward Harp", "Crimson Witch", 2, 1, 1, 1, 1, PyroArtifact)
Support2 = u.Unit("Kaeya", 1, "Skyward Blade", "Wanderer's Troupe", 6, 1, 1, 1, 1, CryoArtifact)
Support3 = u.Unit("Lisa", 1, "Skyward Atlas", "Wanderer's Troupe", 0, 1, 1, 1, 1, ElectroArtifact)
Monster = enemy.Enemy("Hilichurls", 90)

Test = Sim(Main,Support1,Support2,Support3,Monster,15)
Test.turn_on_sim()