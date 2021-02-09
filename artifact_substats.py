class ArtifactStats:
    def __init__(self,sands,goblet,circlet,grade):
        if grade == "Perfect":
            self.mult = 1
        elif grade == "Amazing":
            self.mult = 0.8
        elif grade == "Good":
            self.mult = 0.6
        self.grade = "grade"
        self.pct_atk = 0
        self.flat_atk = 311
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical_dmg = 0
        self.anemo_dmg = 0
        self.cryo_dmg = 0
        self.electro_dmg = 0
        self.geo_dmg = 0
        self.hydro_dmg = 0
        self.pyro_dmg = 0
        self.ele_m = 0
        self.recharge = 0
        self.pct_hp = 0
        self.flat_hp = 4780
        self.pct_def = 0
        self.flat_def = 0
        a_dict = {'pct_atk':0.466,'pct_def':0.583,'pct_hp':0.466,'crit_rate':0.311,'crit_dmg':0.622,'anemo_dmg':0.466,'physical_dmg':0.583,
                'cryo_dmg':0.466,'electro_dmg':0.466,'geo_dmg':0.466,'hydro_dmg':0.466,'pyro_dmg':0.466,'ele_m':187,'recharge':0.583}
        setattr(self,sands,getattr(self,sands)+ a_dict[sands])
        setattr(self,goblet,getattr(self,goblet)+ a_dict[goblet])
        setattr(self,circlet,getattr(self,circlet)+ a_dict[circlet])
        self.crit_rate += 0.033*10*self.mult
        self.crit_dmg += 0.066*10*self.mult
        self.pct_atk += 0.0495*10*self.mult
