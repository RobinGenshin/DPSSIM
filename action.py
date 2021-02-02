#Action Class
from scaling import ratio_type

class Action:
    def __init__ (self,unit,atype,enemy):
        self.unit = unit
        self.type = atype
        self.AT = getattr(unit,self.type + "_AT")
        self.element = getattr(self.unit,self.type + "_type")
        self.scaling = ratio_type(self)

        self.tick = 0
        self.ticks = getattr(self.unit,self.type + "_hits")
        self.tick_times = getattr(self.unit,self.type + "_tick_times")
        self.energy_times = [ x + 1.6 for x in self.tick_times]
        self.tick_damage = getattr(self.unit,self.type + "_tick_damage")
        self.tick_units = getattr(self.unit,self.type + "_tick_units")
        self.snapshot = ""

        if self.type == "skill":
            self.particles = getattr(unit, "skill_particles")
        else:
            self.particles = 0

        self.time_remaining = max(self.tick_times)
        self.snapshotted_mult = 0

    def available(self):
        if self.type == "skill" and self.unit.live_skill_CD != 0:
            return False
        elif self.type == "burst" and self.unit.live_burst_CD != 0:
            if self.unit.live_burst_energy != self.unit.burst_energy:
                return False
            return True
        else:
            return True

    def calculate_damage_snapshot(self,enemy):
        if self.available() == False:
            return 0
        else:
            unit = self.unit
            tot_atk = unit.base_atk * (1 + unit.live_atk_pct) + unit.flat_atk
            crit_mult = 1 + unit.live_crit_rate * unit.live_crit_dmg
            dmg_bon = 1 + unit.live_all_dmg + getattr(unit,self.type + "_dmg") + getattr(unit, "live_" + self.element.lower())
            scaling = self.scaling[getattr(unit,self.type + "_level")]
            defence = ( 100 + unit.level ) / (( 100 + unit.level ) + (enemy.live_defence))
            enemy_res = 1 - getattr(enemy, "live_" + self.element.lower() + "_res")
            mult = tot_atk * crit_mult * dmg_bon * scaling * defence * enemy_res
            damage = 0
            for i in range(self.ticks):
                damage += mult * self.tick_damage[i]
            self.snapshotted_mult = mult
            return damage

    def calculate_dps(self,enemy):
        return self.calculate_damage_snapshot(enemy) / self.AT

    def calculate_tick_damage(self,tick,enemy):
        if self.snapshot == True:
            ratio = ratio = tick.tick_damage[tick]
            return ratio * self.snapshotted_mult
        else:
            unit = self.unit
            tot_atk = unit.base_atk * (1 + unit.live_atk_pct) + unit.flat_atk
            crit_mult = 1 + unit.live_crit_rate * unit.live_crit_dmg
            dmg_bon = 1 + unit.live_all_dmg + getattr(unit,self.type + "_dmg") + getattr(unit, "live_" + self.element.lower())
            scaling = self.scaling[getattr(unit,self.type + "_level")]
            defence = ( 100 + unit.level ) / (( 100 + unit.level ) + (enemy.live_defence))
            enemy_res = 1 - getattr(enemy, "live_" + self.element.lower() + "_res")
            ratio = tick.tick_damage[tick.tick]
            damage = tot_atk * crit_mult * dmg_bon * scaling * defence * enemy_res * ratio
            return damage

