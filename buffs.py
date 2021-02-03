import csv

class Buff:
    def __init__(self, name):
        self.name = name
        self.share = ""
        self.type = ""
        self.type2 = ""
        self.trigger = ""
        self.character = ""
        self.constellation = 0
        self.weapon = ""
        self.artifact = ""
        self.method = ""
        self.duration = 0
        self.instant = ""
        self.cd = 0
        self.live_cd = 0
        self.max_stacks = 0
        self.stacks = 0
        self.temporary = ""

class Debuff:
    def __init__(self,name):
        self.name = name
        self.type2 = ""
        self.character = ""
        self.constellation = 0
        self.weapon = ""
        self.weapon_rank = 0
        self.artifact = ""
        self.method = ""
        self.duration = 0
        self.trigger = ""
        self.time_remaining = 0
        self.field = ""