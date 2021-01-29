import csv
import OOP
import read_data as rd
import unit as un
import operator
import actionlist as a

Main = un.Unit("Amber","Prototype Crescent", 0, 1, 1, 1, 1)
sup1 = un.Unit("Diona","Prototype Crescent", 0, 1, 1, 1, 1)
sup2 = un.Unit("Fischl","Prototype Crescent", 0, 1, 1, 1, 1)
sup3 = un.Unit("Ganyu","Prototype Crescent", 0, 1, 1, 1, 1)
enemy = un.Enemy("Hilichurls")
time = 0
limit = 60

class Sim:
    def __init__(self, Main,sup1,sup2,sup3,enemy,time):
        self.mainskillcd = un.UnitStats(Main).skill_CD
        self.mainburstcd = un.UnitStats(Main).burst_CD
        self.mainenergy = un.UnitStats(Main).burst_energy
        self.sup1skillcd = un.UnitStats(sup1).skill_CD
        self.sup1burstcd = un.UnitStats(sup1).burst_CD
        self.sup1energy = un.UnitStats(sup1).burst_energy
        self.sup2skillcd = un.UnitStats(sup2).skill_CD
        self.sup2burstcd = un.UnitStats(sup2).burst_CD
        self.sup2energy = un.UnitStats(sup2).burst_energy
        self.sup3skillcd = un.UnitStats(sup3).skill_CD
        self.sup3burstcd = un.UnitStats(sup3).burst_CD
        self.sup3energy = un.UnitStats(sup3).burst_energy
        # ActionListSim = a.ActionList(Main,sup1,sup2,sup3,enemy).asdict()

        # while time < limit:
        #     best_action = max(ActionListSim, key=ActionListSim.get)
        #     time += 10
        #     if time > limit:
        #         print('Done')
        #         break
        #     pass

        # for i = 10:
            

# TestSim = Sim(Main,sup1,sup2,sup3,enemy,time)
# print(TestSim.best_action)
