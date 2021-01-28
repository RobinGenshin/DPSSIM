import csv


#General class for team members
class Unit:
    def __init__(self, name):
        self.name = name
        self.Element = ""
        self.Weapon = ""
        self.Constellation = 0
        self.WeaponRank = 0
        self.BaseATK = 0
        self.ATK = 0
        self.FlatATK = 0
        self.CritRate = 0
        self.CritDMG = 0
        self.Physical = 0
        self.Anemo = 0
        self.Cryo = 0
        self.Electro = 0
        self.Geo = 0
        self.Hydro = 0
        self.Pyro = 0
        self.ElementalDMG = 0
        self.ElementalMastery = 0
        self.EnergyRecharge = 0
        self.BaseHP = 0
        self.HP = 0
        self.FlatHP = 0
        self.BaseDEF = 0
        self.DEF = 0
        self.FlatDEF = 0
        self.DMG = 0
        self.DEFRed = 0
        self.NormalDMG = 0
        self.NormalSpeed = 0
        self.ChargedDMG = 0
        self.SkillDMG = 0
        self.BurstDMG = 0
        self.HealingBonus = 0
        self.EleResRed = 0
        self.SwirlResRed = 0
        self.NormalAttackType = ""
        self.NormalAttackRatio = 0
        self.NormalAT = ""
        self.NormalAC = 0
        self.NormalHits = 0
        self.NormalRP = 0
        self.PassiveHits = 0
        self.ChargedAttackType = 0
        self.ChargedAttackRatio = 0
        self.ChargedAT = 0
        self.ChargedAC = ""
        self.ChargedHits = 0
        self.ChargedRP = 0
        self.ChargedStam = 0
        self.SkillRatio = 0
        self.SkillAT = 0
        self.SkillCD = 0
        self.SkillHits = 0
        self.SkillDur = 0
        self.SkillCharges = 0
        self.SkillRP = 0
        self.SkillParticles = 0
        self.BurstRatio = 0
        self.BurstAT = 0
        self.BurstCD = 0
        self.BurstEnergy = 0
        self.BurstHits = 0
        self.BurstDur = 0
        self.BurstCharges = 0
        self.BurstRP = 0

    def get_name(self):
        return self.name

Main = "Amber"
Unit2 = "Kaeya"
Unit3 = "Lisa"
Unit4 = "Noelle"

MainDPS = Unit(Main)

print(Unit.get_name(MainDPS))
