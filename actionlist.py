import csv
import read_data as rd
import unit as u
import operator

Main = u.Unit("Amber", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 1, 1, 1)
Support1 = u.Unit("Diona", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 1, 1, 1)
Support2 = u.Unit("Fischl", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 1, 1, 1)
Support3 = u.Unit("Ganyu", 90, "Prototype Crescent", "Wanderer's Troupe", 0, 1, 1, 1, 1)
Monster = u.Enemy("Hilichurls", 90)

# Creating a list of actions
class Sim:
    def __init__ (self, main,sup1,sup2,sup3,enemy):
        self.ActionList = {}

    def Actions(self,main,sup1,sup2,sup3,enemy):
        self.ActionList['main_normal'] = main.normal_attack_dps(enemy)
        self.ActionList['main_charged'] = main.charged_attack_dps(enemy)
        if main.current_skill_CD == 0:
            self.ActionList['main_skill'] = main.skill_dps(enemy)
        if sup3.current_burst_CD == 0 and sup3.current_burst_energy == 0:
            self.ActionList['main_burst'] = main.burst_dps(enemy)
        if sup1.current_skill_CD == 0:
            self.ActionList['sup1_skill'] = sup1.skill_dps(enemy)
        if sup1.current_burst_CD == 0 and sup1.current_burst_energy == 0:
            self.ActionList['sup1_burst'] = sup1.burst_dps(enemy)        
        if sup2.current_skill_CD == 0:
            self.ActionList['sup2_skill'] = sup2.skill_dps(enemy)
        if sup2.current_burst_CD == 0 and sup2.current_burst_energy == 0:
            self.ActionList['sup2_burst'] = sup2.burst_dps(enemy)        
        if sup3.current_skill_CD == 0:
            self.ActionList['sup3_skill'] = sup3.skill_dps(enemy)
        if sup3.current_burst_CD == 0 and sup3.current_burst_energy == 0:
            self.ActionList['sup3_burst'] = sup3.burst_dps(enemy)
    
    def max_dps(self):
        return(max(self.ActionList, key=self.ActionList.get))
    
    def Rotation(self,main,sup1,sup2,sup3,enemy):
        self.Actions(main,sup1,sup2,sup3,enemy)
        print(self.max_dps())

Test = Sim(Main,Support1,Support2,Support3,Monster)
print(Main.current_skill_CD)
Test.Rotation(Main,Support1,Support2,Support3,Monster)

# print(Test.ActionList)
