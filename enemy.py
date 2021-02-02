import read_data as rd
import buffs as c


#Enemy with stats
class Enemy:
    def __init__ (self, enemy, level):
        enemydict = rd.read_enemy_data()
        self.name = enemydict[enemy].name
        self.level = int(level)
        self.element = "None"
        self.units = 0
        self.defence = self.level + 100
        self.defence_debuff = float(0)
        self.live_defence = self.defence
        self.physical_res = enemydict[enemy].physical_res
        self.physical_res_debuff = 0
        self.live_physical_res = self.physical_res
        self.anemo_res = enemydict[enemy].anemo_res
        self.anemo_res_debuff = 0
        self.live_anemo_res = self.anemo_res
        self.cryo_res = enemydict[enemy].cryo_res
        self.cryo_res_debuff = 0
        self.live_cryo_res = self.cryo_res
        self.electro_res = enemydict[enemy].electro_res
        self.electro_res_debuff = 0
        self.live_electro_res = self.electro_res
        self.geo_res = enemydict[enemy].geo_res
        self.geo_res_debuff = 0
        self.live_geo_res = self.geo_res
        self.hydro_res = enemydict[enemy].hydro_res
        self.hydro_res_debuff = 0
        self.live_hydro_res = self.hydro_res
        self.pyro_res = enemydict[enemy].pyro_res
        self.pyro_res_debuff = 0
        self.live_pyro_res = self.pyro_res
        self.active_debuffs = {}
        self.hitlag = enemydict[enemy].hitlag
        self.stats = {"defence", "anemo_res", "cryo_res", "geo_res", "electro_res", "hydro_res", "pyro_res"}
        self.debuffs = {"defence_debuff", "anemo_res_debuff", "cryo_res_debuff", "geo_res_debuff", "electro_res_debuff", "hydro_res_debuff", "pyro_res"}
    
    def update_stats(self,sim):
        # resets live stats
        for stat in self.stats:
            setattr(self, "live_" + stat, getattr(self,stat))
        # clears stat debuffs
        for debuff in self.debuffs:
            setattr(self, debuff, 0)
        # adds up stat debuff
        for _, debuff in self.active_debuffs.items():
            if debuff.artifact == "Viridiscent Venerer":
                getattr(c.ActiveDebuff(),debuff.method)(self,sim)
            else:
                getattr(c.ActiveDebuff(),debuff.method)(self,sim)

        # applies stat debuffs to main stat
        self.live_defence = self.live_defence * ( 1 - self.defence_debuff )

        elements = {"anemo","cryo","electro","geo","hydro","pyro"}
        for element in elements:
            if getattr( self, element + "_res") <= 0:
                setattr(self, "live_" + element + "_res", getattr( self, element + "_res") - ( getattr( self, element + "_res_debuff") / 2 ))
            elif ( getattr( self, element + "_res") - getattr( self, element + "_res_debuff")) <= 0:
                setattr(self, "live_" + element + "_res", (getattr( self, element + "_res") - getattr( self, element + "_res_debuff")) / 2)
            else:
                setattr(self, "live_" + element + "_res", (getattr( self, element + "_res") - getattr( self, element + "_res_debuff")))

    def update_units(self):
        if self.units <= 0:
            self.element = "None"