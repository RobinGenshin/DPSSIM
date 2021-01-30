class ArtifactStats:
    def __init__(self,sands,goblet,circlet,grade):
        if grade == "Perfect":
            self.mult = 1
        elif grade == "Amazing":
            self.mult = 0.8
        elif grade == "Good":
            self.mult = 0.6
        self.grade = "grade"
        self.atk_pct = 0
        self.flat_atk = 311
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical = 0
        self.anemo = 0
        self.cryo = 0
        self.electro = 0
        self.geo = 0
        self.hydro = 0
        self.pyro = 0
        self.elemental_mastery = 0
        self.energy_recharge = 0
        self.base_hp = 0
        self.hp_pct = 0
        self.flat_hp = 4780
        self.base_def = 0
        self.def_pct = 0
        self.flat_def = 0
        a_dict = {'atk_pct':0.466,'def_pct':0.583,'hp_pct':0.466,'crit_rate':0.311,'crit_Dmg':0.622,'anemo':0.466,'cryo':0.466,'electro':0.466,'geo':0.466,'hydro':0.466,'pyro':0.466,'elemental_mastery':187,'energy_recharge':0.583}
        setattr(self,sands,getattr(self,sands)+ a_dict[sands])
        setattr(self,goblet,getattr(self,goblet)+ a_dict[goblet])
        setattr(self,circlet,getattr(self,circlet)+ a_dict[circlet])
        self.crit_rate += 0.033*10
        self.crit_dmg += 0.066*10
        self.atk_pct += 0.0495*10

Test = ArtifactStats("atk_pct","cryo","crit_rate","Perfect")