import OOP

class Const(OOP.GeneralObject):
    def __init__(self):
        super(Const, self).__init__()

    def AmberConst(self):
        if self.constellation >= 1:
            self.charged_attack_ratio *= 1.2
        if self.constellation >= 2:
            self.skill_ratio += 2
        if self.constellation >= 3:
            self.skill_level += 3
        if self.constellation >= 4:
            self.skill_charges += + 1
        if self.constellation >= 5:
            self.burst_level += + 3
        if self.constellation >=6:
            self.base_atk += 0.15 #Need to change this to only happen in rotation
    
    def DionaConst(self):
        if self.constellation >= 1:
            self.burst_energy -= 15
        if self.constellation >= 2:
            self.skill_dmg += 0.15
        if self.constellation >= 3:
            self.burst_level += 3
        if self.constellation >= 4:
            self.charged_AT -= 0.7
        if self.constellation >= 5:
            self.skill_level += 3
        if self.constellation >= 6:
            pass
    
    def FischlConst(self):
        if self.constellation >= 1:
            pass
        if self.constellation >= 2:
            self.skill_flat_ratio += 2
        if self.constellation >= 3:
            self.skill_level += 3
        if self.constellation >= 4:
            self.burst_flat_ratio += 2.22
        if self.constellation >= 5:
            self.burst_level += 3
        if self.constellation >= 6:
            pass

    def GanyuConst(self):
        if self.constellation >= 1:
            pass
        if self.constellation >= 2:
            self.skill_charges += 1
        if self.constellation >= 3:
            self.burst_level += 3
        if self.constellation >= 4:
            pass
        if self.constellation >= 5:
            self.skill_level += 3
        if self.constellation >= 6:
            pass
    
    def asdict(self):
        return {'Amber': self.AmberConst, 'Diona': self.DionaConst, 'Fischl': self.FischlConst, 'Ganyu': self.GanyuConst}

if __name__ == '__main__':
    print(Const().asdict())
