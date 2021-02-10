#Action Class
from scaling import ratio_type
from copy import deepcopy
from read_data import ele_ratio_dict
from read_data import phys_ratio_dict
import pprint
import operator
import copy

class Action:
    def __init__ (self,unit,atype):

        self.action_type = "damage"
        self.unit = unit
        self.type = atype

        self.element = self.unit.element
        self.scaling = ratio_type(self.unit,self.type)[getattr(unit,self.type + "_level")]

        self.ticks = getattr(self.unit,"live_" + self.type + "_ticks")
        self.tick_times = getattr(self.unit,"live_" + self.type + "_tick_times")
        self.tick_damage = getattr(self.unit,"live_" + self.type + "_tick_damage")
        self.tick_units = getattr(self.unit,"live_" + self.type + "_tick_units")

        self.tick_used = ["no" for i in self.tick_times]
        self.snapshot = ""

        self.particles = getattr(unit, "live_" + atype + "_particles")
        self.stamina_cost = getattr(unit, "live_" + atype + "_stam",0)

        self.infused = ""
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time

        self.snapshot = True
        self.snapshot_totatk = deepcopy(self.unit.base_atk * ( 1 + self.unit.live_pct_atk) + self.unit.flat_atk)
        self.snapshot_crit_rate = deepcopy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = deepcopy(self.unit.live_crit_dmg)
        self.snapshot_dmg = deepcopy(1 + self.unit.live_all_dmg + getattr(self.unit, "live_" + self.type + "_dmg") + 
                                    getattr(self.unit, "live_" + self.element.lower() + "_dmg"))
        
        self.times = set()
        self.time_to_cancel = getattr(self.unit,atype+"_cancel")
        self.time_to_attack = getattr(self.unit,self.type+"_attack")
        self.time_to_swap = getattr(self.unit,self.type+"_swap")
        self.times.update([self.time_to_cancel,self.time_to_attack,self.time_to_swap])
        if self.type == "skill":
            self.time_to_burst = getattr(self.unit,self.type+"_burst")
            self.times.add(self.time_to_burst)
        if self.type == "burst":
            self.time_to_skill = getattr(self.unit,self.type+"_skill")
            self.times.add(self.time_to_skill)
        self.minimum_time = min(self.times)
        

    def available(self,sim):
        if self.type == "skill":
            if self.unit.current_skill_cd <= 0:
                return True
            else:
                return False

        elif self.type == "burst":
            if self.unit.current_burst_cd <= 0 and self.unit.current_energy >= self.unit.live_burst_energy_cost:
                return True
            else:
                return False

        elif self.type == "charged":
            if sim.stamina >= self.stamina_cost:
                return True
            else:
                return False

        else:
            return True

    def update_time(self):
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time
        self.energy_times = [x+2 for x in self.tick_times]

    def calculate_dps_snapshot(self,sim):
        if self.available(sim) == False:
            return 0
        else:
            unit = self.unit
            tot_atk = self.snapshot_totatk
            crit_mult = 1 + (self.snapshot_crit_rate * self.snapshot_crit_dmg)
            dmg_bon = self.snapshot_dmg
            scaling = self.scaling
            defence = ( 100 + unit.level ) / (( 100 + unit.level ) + (sim.enemy.live_defence))
            enemy_res = 1 - getattr(sim.enemy, "live_" + self.element.lower() + "_res")
            mult = tot_atk * crit_mult * dmg_bon * scaling * defence * enemy_res
            damage = 0
            for i in range(self.ticks):
                damage += mult * self.tick_damage[i]
            self.snapshotted_mult = mult
            return damage

    # def calculate_dps_snapshot(self,enemy,sim):
    #     return self.calculate_damage_snapshot(enemy,sim) / self.AT

    def calculate_tick_damage(self,tick,sim):
        if self.snapshot == True:
            attack_multiplier = self.tick_damage[tick]
            tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
            tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
            tot_dmg = self.snapshot_dmg + self.unit.live_cond_dmg
            scaling = self.scaling
            res = getattr(sim.enemy, "live_" + self.element.lower() + "_res")
            defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
            return self.snapshot_totatk * tot_crit_mult * tot_dmg * defence * (1-res) * attack_multiplier * scaling

        else:
            unit = self.unit
            tot_atk = unit.base_atk * (1 + unit.live_atk_pct) + unit.flat_atk
            crit_mult = 1 + (unit.live_crit_rate + unit.live_cond_crit_rate) * unit.live_crit_dmg
            dmg_bon = 1 + unit.live_all_dmg + unit.live_cond_dmg + getattr(unit, "live_ " + self.type + "_dmg") + getattr(unit, "live_" + self.element.lower())
            scaling = self.scaling
            defence = ( 100 + unit.level ) / (( 100 + unit.level ) + (sim.enemy.live_defence))
            res = getattr(sim.enemy, "live_" + self.element.lower() + "_res")
            attack_multiplier = self.tick_damage[tick]
            damage = tot_atk * crit_mult * dmg_bon * scaling * defence * (1-res) * attack_multiplier
            return damage

class WeaponAction:
    def __init__(self,unit_obj):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = "weapon"
        self.element = "physical"

        self.ticks = []
        self.tick_times = []
        self.energy_times = []
        self.tick_damage = []
        self.tick_units = []
        self.tick_used = ["no"]
        self.snapshot = True
        self.particles = 0

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot = True
        self.snapshot_totatk = deepcopy(self.unit.base_atk * ( 1 + self.unit.live_pct_atk) + self.unit.flat_atk)
        self.snapshot_crit_rate = deepcopy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = deepcopy(self.unit.live_crit_dmg)
        self.snapshot_dmg = deepcopy(1 + self.unit.live_all_dmg + getattr(self.unit, "live_physical_dmg"))

    def calculate_tick_damage(self,tick,sim):
        attack_multiplier = self.tick_damage[tick]
        tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
        tot_dmg = self.snapshot_dmg + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_" + self.element.lower() + "_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
        return self.snapshot_totatk * tot_crit_mult * tot_dmg * defence * (1-res) * attack_multiplier

class AlbedoTrigger:
    def __init__(self,unit_obj,enemy,sim):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = "skill"
        self.element = "Geo"

        self.ticks = 1
        self.tick_times = [0.1]
        self.energy_times = [0.1+2]
        self.tick_damage = [1.34]
        self.tick_used = ["no"]
        self.tick_units = [1]
        self.snapshot = True
        self.particles = (2/3)
        self.scaling = ratio_type(self.unit,self.type)[getattr(unit_obj,self.type + "_level")]

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot = False

    def update_time(self):
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time
        self.energy_times = [x+2 for x in self.tick_times]

    def calculate_tick_damage(self,tick,sim):
        attack_multiplier = self.tick_damage[tick]
        tot_def = self.unit.base_def * ( 1 + self.unit.live_def_pct ) + self.unit.live_flat_def
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        tot_dmg = 1 + self.unit.live_all_dmg + self.unit.live_geo + self.unit.live_skill_dmg + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_geo_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
        damage = attack_multiplier * tot_def * tot_crit_mult * tot_dmg * ( 1 - res ) * defence * self.scaling
        return damage

class TartagliaC4:
    def __init__(self,unit_obj,enemy,sim):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = ""
        self.element = "Hydro"

        self.ticks = 4
        self.tick_times = [0.05, 4.05, 8.05, 12.05, 16.05]
        self.energy_times = [2.05, 6.05, 10.05, 14.05, 18.05]
        self.tick_damages = [0.602, 0.602, 0.602, 0.602, 0.602]
        self.tick_units = [1, 1, 1, 1, 1]
        self.tick_used = ["no", "no", "no", "no", "no"]
        self.snapshot = True
        self.particles = 5

        self.scaling = 0

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot_totatk = deepcopy(self.unit.base_atk * ( 1 + self.unit.live_atk_pct) + self.unit.flat_atk)
        self.snapshot_crit_rate = deepcopy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = deepcopy(self.unit.live_crit_dmg)
        self.snapshot_dmg = 1 + deepcopy(self.unit.live_all_dmg) + deepcopy(self.unit.live_hydro) + deepcopy(self.unit.live_burst_dmg)

    def update_time(self):
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time
        self.energy_times = [x+2 for x in self.tick_times]

    def calculate_tick_damage(self,tick,sim):
        res = getattr(sim.enemy, "live_" + self.element.lower() + "_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
        tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
        res = getattr(sim.enemy, "live_" + self.element.lower() + "_res")
        
        if self.unit.stance == "melee":
            attack_multiplier = 0.602
            talent_level = phys_ratio_dict[self.unit.skill_level]
            damage = self.snapshot_totatk * tot_crit_mult * (1-res) *  defence * talent_level * attack_multiplier
            return damage

        elif self.unit.stance == "ranged":
            attack_multiplier = 0.123
            talent_level = ele_ratio_dict[self.unit.normal_level]
            damage = self.snapshot_totatk * tot_crit_mult * (1-res) * defence * talent_level * attack_multiplier

            ## Adding the other 2 ticks to the queue ##
            charged_proc = Action(self.unit,"normal")
            charged_proc.ticks = 2

            charged_proc.tick_times = [sim.time_into_turn + 0.1, sim.time_into_turn + 0.2]
            charged_proc.tick_damage = [0.123]
            charged_proc.tick_units = [0,0,0]
            charged_proc.scaling = ele_ratio_dict[self.unit.normal_level]
            charged_proc.update_time()
            sim.floating_actions.add(charged_proc)
            energy_copy = deepcopy(charged_proc)
            energy_copy.action_type = "energy"
            energy_copy.particles = 1
            energy_copy.energy_times = [x+2 for x in energy_copy.tick_times]
            sim.floating_actions.add(energy_copy)

            return damage

class XinyanQ:
    def __init__(self,unit_obj,enemy,sim):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = "burst"
        self.element = "Physical"

        self.ticks = 1
        self.tick_times = [1.5]
        self.energy_times = [1.5+2]
        self.tick_damage = [3.404]
        self.tick_used = ["no"]
        self.tick_units = [0]
        self.snapshot = True
        self.particles = 0
        self.scaling = ratio_type(self.unit,self.type)[getattr(unit_obj,self.type + "_level")]

        self.initial_time = 2
        self.time_remaining = 2

    def update_time(self):
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time
        self.energy_times = [x+2 for x in self.tick_times]

    def calculate_tick_damage(self,tick,sim):
        attack_multiplier = self.tick_damage[tick]
        tot_atk = self.unit.base_atk * ( 1 + self.unit.live_atk_pct ) + self.unit.live_flat_atk
        if self.unit.constellation >= 2:
            crit_rate = 1
        else:
            crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (crit_rate * self.unit.live_crit_dmg)
        tot_dmg = 1 + self.unit.live_all_dmg + self.unit.live_physical + self.unit.live_skill_dmg + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_physical_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
        damage = attack_multiplier * tot_atk * tot_crit_mult * tot_dmg * ( 1 - res ) * defence * self.scaling
        return damage

class ZhongliA4:
    def __init__(self,unit_obj,atype,enemy,sim):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = atype
        self.element = getattr(self.unit,"live_" + self.type + "_type")

        self.ticks = 1
        self.tick_times = [0.1+sim.time_into_turn]
        if self.type == "skill":
            self.tick_damage = [0.019]
        elif self.type == "burst":
            self.tick_damage = [0.33]
        elif (self.type == "normal") or (self.type == "charged"):
            self.tick_damage = [0.0139]
        self.energy_times = [0.1+sim.time_into_turn+2]
        self.tick_damage = [0.0139]
        self.tick_used = ["no"]
        self.tick_units = [0]
        self.snapshot = True
        self.particles = 0
        self.scaling = 1

        self.initial_time = max(self.tick_damage)
        self.time_remaining = self.initial_time

    def calculate_tick_damage(self,tick,sim):
        attack_multiplier = self.tick_damage[tick]
        tot_hp = self.unit.base_atk * ( 1 + self.unit.hp_pct ) + self.unit.flat_hp
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        tot_dmg = 1 + self.unit.live_all_dmg + self.unit.live_geo + getattr(self.unit, "live_ " + self.type + "_dmg") + self.unit.live_cond_dmg
        res = getattr(sim.enemy, "live_geo_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
        damage = attack_multiplier * tot_hp * tot_crit_mult * tot_dmg * ( 1 - res ) * defence * self.scaling
        return damage


class Combos:
    def __init__(self):
        pass
    def _list(self,unit_obj):
        combo_dict = dict()

        ## Normal Combos ##
        for i in range(unit_obj.live_normal_ticks):
            normal_damage = 0
            for j in range(i+1):
                normal_damage += unit_obj.normal_tick_damage[j]
            if i < (unit_obj.normal_ticks - 1):
                AC = (21/60)
            else:
                AC = min(21/60,unit_obj.live_normal_at - max(unit_obj.live_normal_tick_times))
            time = unit_obj.live_normal_tick_times[i] + AC
            dps = normal_damage / time
            combo_dict["N"+str(i+1)] = [dps,normal_damage,time,[i+1,0]]

        ## Charged ##
        if len(unit_obj.normal_attack) == 0:

            charged_damage = 0
            for k in range(unit_obj.live_charged_ticks):
                charged_damage += unit_obj.live_charged_tick_damage[k]
            time = min(unit_obj.live_charged_attack,max(unit_obj.live_charged_tick_times)+0.33)
            dps = charged_damage/time
            combo_dict["C"] = [dps,charged_damage,time,[0,unit_obj.live_charged_ticks]]

        ## Charged Combos ##
        for l in range(len(unit_obj.live_normal_attack)):

            normal_damage = 0
            charged_damage = 0

            for j in range(l+1):
                normal_damage += unit_obj.normal_tick_damage[j]

            for k in range(unit_obj.live_charged_ticks):
                charged_damage += unit_obj.live_charged_tick_damage[k]
            
            time = unit_obj.live_normal_attack[l] + min(unit_obj.live_charged_attack,max(unit_obj.live_charged_tick_times)+0.33)
            damage = normal_damage + charged_damage
            dps = damage/time

            combo_dict["N"+str(l+1)+"C"] = [dps,damage,time,[l+1,unit_obj.live_charged_ticks]]
        return combo_dict

class ComboAction:
    def __init__(self,unit_obj,combo):
        self.action_type = "damage"
        self.unit = unit_obj
        self.combo = combo
        self.type = "combo"
        self.tick_types = ["normal"] * self.combo[3][0]
        self.tick_types.extend(["charged"]*self.combo[3][1])

        self.element = [getattr(self.unit,"live_normal_type").lower()]*self.combo[3][0]
        self.element.extend([getattr(self.unit,"live_charged_type").lower()]*self.combo[3][1])

        self.scaling = [ratio_type(self.unit,"normal")[getattr(unit_obj,"normal_level")]]*combo[3][0]
        self.scaling.extend([ratio_type(self.unit,"charged")[getattr(unit_obj,"normal_level")]]*combo[3][1])

        self.tick = 0
        self.ticks = self.combo[3][0] + self.combo[3][1]
        self.tick_times = self.unit.normal_tick_times[:combo[3][0]]
        if self.tick_times == []:
            self.tick_times = [0]
        self.tick_times.extend([ x + max(copy.deepcopy(self.tick_times)) for x in self.unit.charged_tick_times[:combo[3][1]]])

        self.tick_damage = self.unit.normal_tick_damage[:combo[3][0]]
        self.tick_damage.extend(x for x in self.unit.charged_tick_damage[:combo[3][1]])
        self.tick_units = self.unit.normal_tick_units[:combo[3][0]]
        self.tick_units.extend(self.unit.charged_tick_units[:combo[3][1]])

        self.tick_hitlag = self.unit.normal_tick_hitlag[:combo[3][0]]
        self.tick_hitlag.extend(x for x in self.unit.charged_tick_hitlag[:combo[3][1]])

        self.particles = 0 
        self.tick_used = ["no" for i in self.tick_times]

        if combo[3][1] > 0 and combo[3][0] > 0:
            self.time_to_normal_nc = self.unit.charged_attack + self.unit.normal_attack[combo[3][0]-1]
            self.time_to_skill = self.unit.charged_skill + self.unit.normal_attack[combo[3][0]-1]
            self.time_to_burst = self.unit.charged_burst + self.unit.normal_burst[combo[3][0]-1]
            self.time_to_swap = self.unit.charged_swap + self.unit.normal_attack[combo[3][0]-1]
            self.time_to_cancel = self.unit.charged_cancel + self.unit.normal_attack[combo[3][0]-1]

        elif combo[3][1] > 0 and combo[3][0] == 0:
            self.time_to_normal_nc = self.unit.charged_attack
            self.time_to_skill = self.unit.charged_skill
            self.time_to_burst = self.unit.charged_burst
            self.time_to_swap = self.unit.charged_swap
            self.time_to_cancel = self.unit.charged_cancel
        else:
            self.time_to_normal_nc = self.unit.normal_at
            self.time_to_skill = max(self.tick_times)
            self.time_to_burst = max(self.tick_times)
            self.time_to_swap = max(self.tick_times)
            self.time_to_cancel = max(self.tick_times)

        atk_speed_0 = copy.deepcopy(self.tick_times[0]*(1-(1/(1+getattr(self.unit,"live_" + self.tick_types[0]+"_speed")))))
        for time in self.tick_times:
            time -= atk_speed_0

        self.times = [self.time_to_cancel, self.time_to_normal_nc, self.time_to_skill, self.time_to_burst, self.time_to_swap]
        for time in self.times:
            time -= atk_speed_0

        self.minimum_time = min([self.time_to_cancel,self.time_to_normal_nc,self.time_to_skill,self.time_to_burst,self.time_to_swap])

        self.stamina_cost = [0 for x in self.unit.normal_tick_times[:combo[3][0]]]
        self.stamina_cost.extend(self.unit.charged_stamina_cost)
        self.total_stamina = sum(x for x in self.stamina_cost)

        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time

    def available(self,sim):
        if self.combo[3][1] > 0:
            if sim.stamina >= self.total_stamina:
                return True
            else:
                return False
        else:
            return True

    def calculate_tick_damage(self,tick,sim):
        tot_atk = self.unit.live_base_atk * ( 1 + self.unit.live_pct_atk ) + self.unit.live_flat_atk
        attack_multiplier = self.tick_damage[tick]
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (sim.enemy.live_defence))
        tot_dmg = self.unit.live_all_dmg + self.unit.live_cond_dmg + getattr(self.unit,"live_"+self.tick_types[tick]+"_dmg")
        tot_dmg += getattr(self.unit,"live_"+self.element[tick].lower()+"_dmg")
        scaling = self.scaling[tick]
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate + getattr(self.unit,"live_"+self.tick_types[tick]+"_cond_crit_rate")
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        res = getattr(sim.enemy, "live_" + self.element[tick].lower() + "_res")
        return tot_atk * tot_crit_mult * tot_dmg * defence * (1-res) * attack_multiplier * scaling

    def calculate_dps_snapshot(self,sim):
        total_damage = 0
        for i in range(self.ticks):
            total_damage += self.calculate_tick_damage(i,sim)
        return total_damage / self.combo[2]
    


