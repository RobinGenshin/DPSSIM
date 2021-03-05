from core.read_data import enemy_dict
from effects import debuffs
import copy


class Enemy:
    def __init__(self, enemy, level):
        self.name = enemy_dict[enemy].name
        self.level = int(level)
        self.elements = dict()
        self.defence = self.level + 100
        self.defence_debuff = float(0)
        self.live_defence = self.defence
        self.physical_res = enemy_dict[enemy].physical_res
        self.physical_res_debuff = 0
        self.live_physical_res = self.physical_res
        self.anemo_res = enemy_dict[enemy].anemo_res
        self.anemo_res_debuff = 0
        self.live_anemo_res = self.anemo_res
        self.cryo_res = enemy_dict[enemy].cryo_res
        self.cryo_res_debuff = 0
        self.live_cryo_res = self.cryo_res
        self.electro_res = enemy_dict[enemy].electro_res
        self.electro_res_debuff = 0
        self.live_electro_res = self.electro_res
        self.geo_res = enemy_dict[enemy].geo_res
        self.geo_res_debuff = 0
        self.live_geo_res = self.geo_res
        self.hydro_res = enemy_dict[enemy].hydro_res
        self.hydro_res_debuff = 0
        self.live_hydro_res = self.hydro_res
        self.pyro_res = enemy_dict[enemy].pyro_res
        self.pyro_res_debuff = 0
        self.live_pyro_res = self.pyro_res
        self.active_debuffs = {}
        self.hitlag = enemy_dict[enemy].hitlag
        self.stats = {"defence", "anemo_res", "cryo_res", "geo_res", "electro_res", "hydro_res", "pyro_res"}
        self.debuffs = {"defence_debuff", "anemo_res_debuff", "cryo_res_debuff", "geo_res_debuff", "electro_res_debuff",
                        "hydro_res_debuff", "pyro_res_debuff"}

    def update_stats(self, sim):
        # resets live stats

        for stat in self.stats:
            setattr(self, "live_" + stat, copy.copy(getattr(self, stat)))
        # clears stat debuffs

        for debuff in self.debuffs:
            setattr(self, debuff, 0)

        # adds up stat debuff
        for _, debuff in self.active_debuffs.items():
            getattr(debuffs.ActiveDebuff(), debuff.method)(self, sim)

        # applies stat debuffs to main stat
        self.live_defence = self.live_defence * (1 - self.defence_debuff)

        elements = {"anemo", "cryo", "electro", "geo", "hydro", "pyro"}
        for element in elements:
            if getattr(self, element + "_res") <= 0:
                setattr(self, "live_" + element + "_res",
                        getattr(self, element + "_res") - (getattr(self, element + "_res_debuff") / 2))
            elif (getattr(self, element + "_res") - getattr(self, element + "_res_debuff")) <= 0:
                setattr(self, "live_" + element + "_res",
                        (getattr(self, element + "_res") - getattr(self, element + "_res_debuff")) / 2)
            else:
                setattr(self, "live_" + element + "_res",
                        (getattr(self, element + "_res") - getattr(self, element + "_res_debuff")))

    def update_units(self):
        for element, unit in copy.copy(self.elements).items():
            if unit < 0:
                del self.elements[element]
