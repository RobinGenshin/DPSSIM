#Action Class
from scaling import ratio_type
from copy import deepcopy

class Action:
    def __init__ (self,unit,atype,enemy):
        self.action_type = "damage"
        self.unit = unit
        self.type = atype
        self.AT = getattr(unit,"live_" + self.type + "_AT")
        self.element = getattr(self.unit,"live_" + self.type + "_type")
        self.scaling = ratio_type(self)[getattr(unit,self.type + "_level")]

        self.tick = 0
        self.ticks = getattr(self.unit,"live_" + self.type + "_hits")
        self.tick_times = getattr(self.unit,"live_" + self.type + "_tick_times")
        self.energy_times = [ x + 1.6 for x in self.tick_times]
        self.tick_damage = getattr(self.unit,"live_" + self.type + "_tick_damage")
        self.tick_units = getattr(self.unit,"live_" + self.type + "_tick_units")
        self.tick_used = ["no" for i in self.tick_times]
        self.snapshot = ""
        self.particles = 0
        if self.type == "skill":
            self.particles = getattr(unit, "skill_particles")
        else:
            self.particles = 0

        self.infused = ""
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time

        self.snapshot = True
        self.snapshot_totatk = deepcopy(self.unit.base_atk * ( 1 + self.unit.live_atk_pct) + self.unit.flat_atk)
        self.snapshot_crit_rate = deepcopy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = deepcopy(self.unit.live_crit_dmg)
        self.snapshot_dmg = deepcopy(1 + self.unit.live_all_dmg + getattr(self.unit, "live_" + self.type + "_dmg") + 
                            getattr(self.unit, "live_" + self.element.lower()))


    def available(self):
        if self.type == "skill":
            if self.unit.live_skill_CD <= 0:
                return True
            else:
                return False

        elif self.type == "burst":
            if self.unit.live_burst_CD <= 0 and self.unit.live_burst_energy >= self.unit.burst_energy:
                return True
            else:
                return False

        else:
            return True

    def update_time(self):
        self.initial_time = max(self.tick_times)
        self.time_remaining = self.initial_time

    def calculate_damage_snapshot(self,enemy):
        if self.available() == False:
            return 0
        else:
            unit = self.unit
            tot_atk = self.snapshot_totatk
            crit_mult = 1 + (self.snapshot_crit_rate * self.snapshot_crit_dmg)
            dmg_bon = self.snapshot_dmg
            scaling = self.scaling
            defence = ( 100 + unit.level ) / (( 100 + unit.level ) + (enemy.live_defence))
            enemy_res = 1 - getattr(enemy, "live_" + self.element.lower() + "_res")
            mult = tot_atk * crit_mult * dmg_bon * scaling * defence * enemy_res
            damage = 0
            for i in range(self.ticks):
                damage += mult * self.tick_damage[i]
            self.snapshotted_mult = mult
            return damage

    def calculate_dps_snapshot(self,enemy):
        return self.calculate_damage_snapshot(enemy) / self.AT

    def calculate_tick_damage(self,tick,enemy):
        if self.snapshot == True:
            attack_multiplier = self.tick_damage[tick]
            tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
            tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
            tot_dmg = self.snapshot_dmg + self.unit.live_cond_dmg
            scaling = self.scaling
            res = getattr(enemy, "live_" + self.element.lower() + "_res")
            defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (enemy.live_defence))
            return self.snapshot_totatk * tot_crit_mult * tot_dmg * defence * (1-res) * attack_multiplier * scaling

        else:
            unit = self.unit
            tot_atk = unit.base_atk * (1 + unit.live_atk_pct) + unit.flat_atk
            crit_mult = 1 + (unit.live_crit_rate + unit.live_cond_crit_rate) * unit.live_crit_dmg
            dmg_bon = 1 + unit.live_all_dmg + unit.live_cond_dmg + getattr(unit, "live_ " + self.type + "_dmg") + getattr(unit, "live_" + self.element.lower())
            scaling = self.scaling
            defence = ( 100 + unit.level ) / (( 100 + unit.level ) + (enemy.live_defence))
            res = getattr(enemy, "live_" + self.element.lower() + "_res")
            attack_multiplier = self.tick_damage[tick]
            damage = tot_atk * crit_mult * dmg_bon * scaling * defence * (1-res) * attack_multiplier
            return damage

class WeaponAction:
    def __init__(self,unit_obj,enemy):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = "weapon"
        self.element = "physical"
        self.tick = 0
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
        self.snapshot_totatk = deepcopy(self.unit.base_atk * ( 1 + self.unit.live_atk_pct) + self.unit.flat_atk)
        self.snapshot_crit_rate = deepcopy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = deepcopy(self.unit.live_crit_dmg)
        self.snapshot_dmg = deepcopy(1 + self.unit.live_all_dmg + getattr(self.unit, "live_physical"))

    def calculate_tick_damage(self,tick,enemy):
        attack_multiplier = self.tick_damage[tick]
        tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
        tot_dmg = self.snapshot_dmg + self.unit.live_cond_dmg
        res = getattr(enemy, "live_" + self.element.lower() + "_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (enemy.live_defence))
        return self.snapshot_totatk * tot_crit_mult * tot_dmg * defence * (1-res) * attack_multiplier

class AlbedoTrigger:
    def __init__(self,unit_obj,enemy):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = "skill"
        self.element = "Geo"
        self.tick = 0
        self.ticks = 1
        self.tick_times = [0.05]
        self.energy_times = [0.05]
        self.tick_damage = [1.34]
        self.tick_used = ["no"]
        self.tick_units = [1]
        self.snapshot = True
        self.particles = (2/3)
        self.scaling = ratio_type(self)[getattr(unit_obj,self.type + "_level")]

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot = False

    def calculate_tick_damage(self,tick,enemy):
        attack_multiplier = self.tick_damage[tick]
        tot_def = self.unit.base_def * ( 1 + self.unit.live_def_pct ) + self.unit.live_flat_def
        tot_crit_rate = self.unit.live_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.unit.live_crit_dmg)
        tot_dmg = 1 + self.unit.live_all_dmg + self.unit.live_geo + self.unit.live_skill_dmg + self.unit.live_cond_dmg
        res = getattr(enemy, "live_geo_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (enemy.live_defence))
        damage = attack_multiplier * tot_def * tot_crit_mult * tot_dmg * ( 1 - res ) * defence * self.scaling
        return damage

class BeidouQ:
    def __init__(self,unit_obj,enemy):
        self.action_type = "damage"
        self.unit = unit_obj
        self.type = "burst"
        self.element = "Electro"
        self.tick = 0
        self.ticks = 1
        self.tick_times = [0.05]
        self.energy_times = [0.05]
        self.tick_damage = [0.96]
        self.tick_used = ["no"]
        self.tick_units = [1]
        self.snapshot = True
        self.particles = 0
        self.scaling = ratio_type(self)[getattr(unit_obj,self.type + "_level")]

        self.initial_time = 0
        self.time_remaining = 0
        self.snapshot = True
        self.snapshot_totatk = deepcopy(self.unit.base_atk * ( 1 + self.unit.live_atk_pct) + self.unit.flat_atk)
        self.snapshot_crit_rate = deepcopy(self.unit.live_crit_rate)
        self.snapshot_crit_dmg = deepcopy(self.unit.live_crit_dmg)
        self.snapshot_dmg = 1 + deepcopy(self.unit.live_all_dmg) + deepcopy(self.unit.live_electro) + deepcopy(self.unit.live_burst_dmg)

    def calculate_tick_damage(self,tick,enemy):
        attack_multiplier = 0.96
        tot_crit_rate = self.snapshot_crit_rate + self.unit.live_cond_crit_rate
        tot_crit_mult = 1 + (tot_crit_rate * self.snapshot_crit_dmg)
        tot_dmg = self.snapshot_dmg + self.unit.live_cond_dmg
        res = getattr(enemy, "live_" + self.element.lower() + "_res")
        defence = ( 100 + self.unit.level ) / (( 100 + self.unit.level ) + (enemy.live_defence))
        damage = self.snapshot_totatk * tot_crit_mult * tot_dmg * defence * (1-res) * attack_multiplier * self.scaling
        return damage

