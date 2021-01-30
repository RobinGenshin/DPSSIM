import csv
import read_data as rd
import unit as u
import operator


# Creating a list of actions
class Sim:
    def __init__ (self, main,sup1,sup2,sup3,enemy,time):
        self.ActionList = set()
        self.EncounterTime = time
        self.EncounterDuration = 0
        self.Damage = 0
        self.units = {main,sup1,sup2,sup3}
        self.enemy = enemy
        self.action_order = 0
        self.chosen_unit = None
        self.last_unit = None
        self.action = None
        self.last_action = None

    def start_sim(self):
        self.action_order += 1
        self.last_unit = self.chosen_unit
        self.last_action = self.action

    def best_unit(self):
        self.chosen_unit = max(self.units, key=lambda obj: obj.highest_dps(self.enemy))
        if self.action_order == 1:
            self.last_unit = self.chosen_unit
            self.last_action = self.action

    def best_action(self):
        self.action = u.ChosenAction(self.chosen_unit,self.enemy)

    def use_ability(self):
        self.Damage += self.action.damage
        for unit in self.units:
            if unit == self.chosen_unit:
                if self.action.type == "skill":
                    unit.current_skill_CD = unit.skill_CD
                if self.action.type == "burst":
                    unit.current_burst_CD = unit.burst_CD
                    unit.current_burst_energy = unit.burst_energy

    def pass_time(self):
        if self.chosen_unit == self.last_unit:
            self.EncounterDuration += self.action.duration

        elif self.last_action.duration < 1:
            self.EncounterDuration += (1-self.last_action.duration) + 0.12 + self.action.duration

        else:
            self.EncounterDuration += 0.12 + self.action.duration
    
    def pass_turn(self):
        for unit in self.units:
            unit.current_skill_CD = max(unit.current_skill_CD - self.action.duration,0)
            unit.current_burst_CD = max(unit.current_burst_CD - self.action.duration,0)
            if unit == self.chosen_unit:
                unit.current_burst_energy = min((unit.current_burst_energy + self.action.particles * 3 * unit.energy_recharge),unit.burst_energy)
            else:
                unit.current_burst_energy = min((unit.current_burst_energy + self.action.particles * 1.6 * unit.energy_recharge),unit.burst_energy)

    def status(self):
        print("#" + str(self.action_order) + " Time:" + str(round(self.EncounterDuration,2)) + ", Action is " + self.chosen_unit.name + "'s "
        + self.action.type + ". It dealt " + str(int(self.action.damage)) + " damage. Total damage is " + str(int(self.Damage)) 
        + " and current DPS is " + str(int(self.Damage/self.EncounterDuration)))

    def turn_on_sim(self):
        while self.EncounterDuration < self.EncounterTime:
            self.start_sim()
            self.best_unit()
            self.best_action()
            self.use_ability()
            self.pass_time()
            self.pass_turn()
            self.status()

Main = u.Unit("Amber", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10)
Support1 = u.Unit("Diona", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10)
Support2 = u.Unit("Fischl", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10)
Support3 = u.Unit("Ganyu", 90, "Prototype Crescent", "Wanderer's Troupe", 6, 1, 10, 10, 10)
Monster = u.Enemy("Hilichurls", 90)

print(Support1.charged_AT)
print(Support1.charged_attack_dps(Monster))

Test = Sim(Main,Support1,Support2,Support3,Monster,60)
Test.turn_on_sim()