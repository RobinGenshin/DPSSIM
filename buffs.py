import csv

class Buff:
    def __init__(self, name):
        self.name = name
        self.share = ""
        self.type = ""
        self.character = ""
        self.constellation = 0
        self.weapon = ""
        self.artifact = ""
        self.method = ""
        self.duration = 0
        self.on_hit = ""
        self.trigger = ""
        self.instant = ""
        self.precast = ""
        self.time_remaining = 0
        self.stacks = 0

class Debuff:
    def __init__(self,name):
        self.name = name
        self.character = ""
        self.constellation = 0
        self.weapon = ""
        self.weapon_rank = 0
        self.artifact = ""
        self.method = ""
        self.duration = 0
        self.trigger = ""
        self.time_remaining = 0