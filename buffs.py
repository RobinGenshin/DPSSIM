import csv

class Buff:
    def __init__(self,Buff,Share,Type,Character,Weapon,Rank,Artifact,Constellation,method,Duration,Trigger,Instant,Precast):
        self.name = Buff
        self.share = Share
        self.type = Type
        self.character = Character
        self.constellation = Constellation
        self.weapon = Weapon
        self.weapon_rank = Rank
        self.artifact = Artifact
        self.method = method
        self.duration = Duration
        self.trigger = Trigger
        self.instant = Instant
        self.precast = Precast
        self.time_remaining = self.duration

class Debuff:
    def __init__(self,Debuff,Character,Constellation,Weapon,Rank,Artifact,method,Duration,Trigger):
        self.name = Debuff
        self.character = Character
        self.constellation = Constellation
        self.weapon = Weapon
        self.weapon_rank = Rank
        self.artifact = Artifact
        self.method = method
        self.duration = Duration
        self.trigger = Trigger
        self.time_remaining = self.duration