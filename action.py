#Action Class
class Action:
    def __init__ (self,unit,type,enemy):
        self.unit = unit
        self.type = type
        self.dps = getattr(unit,self.type + "_dps")(enemy)
        self.damage = getattr(unit,self.type + "_damage")(enemy)
        self.AT = getattr(unit,self.type + "_action_time")(enemy)
        self.element = getattr(unit,self.type + "_element")
        if self.type == "skill":
            self.particles = getattr(unit, "skill_particles")
        else:
            self.particles = 0
        if self.type == "normal_attack" or self.type == "charged_attack":
            self.duration = "Instant"
        else:
            self.duration = getattr(unit,self.type + "_dur")
        self.time_remaining = self.duration

        if self.type == "skill" or self.type == "burst":
            self.ticks = getattr(unit,self.type + "_ticks")
        self.element_units = 0
        if self.type == "skill" or self.type == "burst":
            self.element_units = getattr(unit,self.type + "_U") 
    
    def recalc_dps(self,enemy):
        self.dps = getattr(self.unit,self.type + "_dps")(enemy)
