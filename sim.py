import csv
import read_data as rd
import unit as u
from operator import attrgetter
import artifact_substats

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
        self.dot_actions = ()
        self.action_list = set()

    def start_sim(self):
        self.action_order += 1
        self.last_unit = self.chosen_unit
        self.last_action = self.chosen_action

    def update_action_list(self):
        self.action_list = set()
        types = {"normal_attack", "charged_attack", "skill", "burst"}
        for unit in self.units:
            for k in types:
                self.action_list.add(u.Action(unit,k,self.enemy))
    
    def choose_action(self):
            self.chosen_action = max(self.action_list, key=attrgetter('dps'))
            self.chosen_unit = self.chosen_action.unit
            if self.action_order == 1:
                self.last_unit = self.chosen_unit
                self.last_action = self.chosen_action

    def use_ability(self):
        self.damage += self.chosen_action.damage
        for unit in self.units:
            if unit == self.chosen_unit:
                if self.chosen_action.type == "skill":
                    unit.current_skill_CD = unit.skill_CD
                if self.chosen_action.type == "burst":
                    unit.current_burst_CD = unit.burst_CD
                    unit.current_burst_energy = 0
    
    def add_buff(self):
        for key, trig_buff in self.chosen_unit.triggerable_buffs.items():
            if trig_buff.trigger == self.chosen_action.type:
                if trig_buff.share == "Yes":
                    for unit in self.units:
                        unit.active_buffs[key] = trig_buff
                else:
                    self.chosen_unit.active_buffs[key] = trig_buff
    
    def add_debuff(self):
        for key, trig_debuff in self.chosen_unit.triggerable_debuffs.items():
            if trig_debuff.trigger == self.chosen_action.type:
                    self.enemy.active_debuffs[key] = trig_debuff

    def pass_time(self):
        if self.chosen_unit == self.last_unit:
            self.turn_time = self.chosen_action.AT
        elif self.last_action.AT < 1:
            self.turn_time = (1-self.last_action.AT) + 0.12 + self.chosen_action.AT
        else:
            self.turn_time = 0.12 + self.chosen_action.AT
        self.encounter_duration += self.turn_time
    
    def reduce_cd(self):
        for unit in self.units:
            unit.current_skill_CD = max(unit.current_skill_CD - self.turn_time,0)
            unit.current_burst_CD = max(unit.current_burst_CD - self.turn_time,0)

    def add_energy(self):
        particles = self.chosen_action.particles
        for unit in self.units:
            if unit == self.chosen_unit:
                unit.current_burst_energy = min((unit.current_burst_energy + particles * 3 * unit.energy_recharge),unit.burst_energy)
            else:
                unit.current_burst_energy = min((unit.current_burst_energy + particles * 1.6 * unit.energy_recharge),unit.burst_energy)

    def check_buff_end(self):
        for unit in self.units:
            for buff in unit.active_buffs.values():
                buff.time_remaining -= self.turn_time
            unit.update_stats()
            unit.active_buffs = {k:unit.active_buffs[k] for k in unit.active_buffs if unit.active_buffs[k].time_remaining > 0}
            unit.update_stats()

    def check_debuff_end(self):
        for debuff in self.enemy.active_debuffs.values():
            debuff.time_remaining -= self.turn_time
        self.enemy.active_debuffs = {k:self.enemy.active_debuffs[k] for k in self.enemy.active_debuffs if self.enemy.active_debuffs[k].time_remaining > 0}
        self.enemy.update_stats()

    def status(self):
        print("#" + str(self.action_order) + " Time:" + str(round(self.encounter_duration,2)) + ", Action is " + self.chosen_unit.name + "'s "
        + self.chosen_action.type + ". It dealt " + str(int(self.chosen_action.damage)) + " damage. Total damage is " + str(int(self.damage)) 
        + " and current DPS is " + str(int(self.damage/self.encounter_duration)))

    def turn_on_sim(self):
        while self.encounter_duration < self.encounter_limit:
            self.start_sim()
            self.update_action_list()
            self.choose_action()
            self.use_ability()
            self.add_buff()
            self.add_debuff()
            self.pass_time()
            self.reduce_cd()
            self.check_buff_end()
            self.check_debuff_end()
            self.status()


PyroArtifact = artifact_substats.ArtifactStats("atk_pct", "pyro", "crit_rate", "Perfect")
CryoArtifact = artifact_substats.ArtifactStats("atk_pct", "cryo", "crit_rate", "Perfect")
ElectroArtifact = artifact_substats.ArtifactStats("atk_pct", "electro", "crit_rate", "Perfect")

Main = u.Unit("Amber", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, PyroArtifact)
Support1 = u.Unit("Diona", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, CryoArtifact)
Support2 = u.Unit("Fischl", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, ElectroArtifact)
Support3 = u.Unit("Ganyu", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10, CryoArtifact)
Monster = u.Enemy("Hilichurls", 90)

Test = Sim(Main,Support1,Support2,Support3,Monster,100)
Test.turn_on_sim()
