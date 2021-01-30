import csv

class ActiveCharBuff:
    def __init__(self,character,constellation,stat,value,duration,trigger,share):
        self.character = character
        self.constellation = constellation
        self.stat = stat
        self.value = value
        self.duration = duration
        self.trigger = trigger
        self.share = share
