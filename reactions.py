#Turn dot reactions into damage/reactions

class React:
    def __init__(self):
        self.print = True

    def check(self,action,enemy):
        #Anemo
        if action.element == "Anemo":
            return "swirl"
        #Geo
        elif action.element == "Geo":
            return "crystallise"
        #Hydro
        elif action.element == "Hydro":
            if enemy.element == "None":
                return "enemyhydro"
            elif enemy.element == "Pyro":
                return "vaporise2"
            elif enemy.element == "Electro":
                return "electro_charged"
            elif enemy.element == "Cryo":
                return "frozen"
            else:
                return "no_reaction"
        #Cryo
        elif action.element == "Cryo":
            if enemy.element == "None":
                enemy.element = "Cryo"
                return "enemycryo"
            if enemy.element == "Hydro":
                return "frozen"
            if enemy.element == "Pyro":
                return "melt15"
            if enemy.element == "Electro":
                return "superconduct"
            else:
                return "no_reaction"
        #Electro
        elif action.element == "Electro":
            if enemy.element == "None":
                return "enemyelectro"
            if enemy.element == "Hydro":
                return "electro_charged"
            if enemy.element == "Pyro":
                return "overload"
            if enemy.element == "Cryo":
                return "superconduct"
            else:
                return "no_reaction"    
        #Pyro
        elif action.element == "Pyro":
            if enemy.element == "None":
                return "enemypyro"
            if enemy.element == "Hydro":
                return "vaporise15"
            if enemy.element == "Cryo":
                return "melt2"
            if enemy.element == "Electro":
                return "overload"
            else:
                return "no_reaction"

        else:
            return "no_reaction"
    
    def swirl(self,sim,action,enemy,unit):
        enemy.element -= unit*0.5
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proced swirl")

    def overload(self,sim,action,enemy,unit):
        enemy.units -= unit
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proced overload")

    def crystallise(self,sim,action,enemy,unit):
        enemy.element -= unit*0.5
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proced crystallise")

    def superconduct(self,sim,action,enemy,unit):
        enemy.units -= unit
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proced superconduct")

    def electro_charged(self,sim,action,enemy,unit):
        enemy.units -= unit
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proced electro_charged")

    def frozen(self,sim,action,enemy,unit):
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proced frozen")

    def vaporise2(self,sim,action,enemy,unit):
        action.damage *= 2 * (action.unit.elemental_mastery*25) / (9*(action.unit.elemental_mastery+1400))
        enemy.units -= unit*2
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " proc'd Vaporise Vaporise for 2x damage")

    def vaporise15(self,sim,action,enemy,unit):
        action.damage *= 2 * (action.unit.elemental_mastery*25) / (9*(action.unit.elemental_mastery+1400))
        enemy.units -= unit*0.5

    def melt2(self,sim,action,enemy,unit):
        action.damage *= 2 * (action.unit.elemental_mastery*25) / (9*(action.unit.elemental_mastery+1400))
        enemy.units -= unit*2

    def melt15(self,sim,action,enemy,unit):
        action.damage *= 1.5 * (action.unit.elemental_mastery*25) / (9*(action.unit.elemental_mastery+1400))
        enemy.units -= unit*0.5

    def enemyelectro(self,sim,action,enemy,unit):
        enemy.element = action.element
        enemy.units += unit*0.8
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " applied electro")
    
    def enemypyro(self,sim,action,enemy,unit):
        enemy.element = action.element
        enemy.units += unit*0.8
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " applied pyro")

    def enemycryo(self,sim,action,enemy,unit):
        enemy.element = action.element
        enemy.units += unit*0.8
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " applied cryo")

    def enemyhydro(self,sim,action,enemy,unit):
        enemy.element = action.element
        enemy.units += unit*0.8
        print("#" + str(sim.action_order) + " Time:" + str(round(sim.encounter_duration,2)) + " " + action.unit.name + " applied hydro")

    def no_reaction(self,sim,action,enemy,unit):
        pass