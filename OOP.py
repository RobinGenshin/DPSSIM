import csv

# AC: 
#General class for team members

class GeneralObject:
    def __init__(self):
        self.name = ""
        self.element = ""
        self.weapon = ""
        self.constellation = 0
        self.weapon_rank = 0
        self.base_atk = 0
        self.atk_pct = 0
        self.flat_atk = 0
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical = 0
        self.anemo = 0
        self.cryo = 0
        self.electro = 0
        self.geo = 0
        self.hydro = 0
        self.pyro = 0
        self.elemental_dmg = 0
        self.elemental_mastery = 0
        self.energy_recharge = 0
        self.base_hp = 0
        self.hp_pct = 0
        self.flat_hp = 0
        self.base_def = 0
        self.def_pct = 0
        self.flat_def = 0
        self.all_dmg = 0
        self.def_red = 0
        self.normal_dmg = 0
        self.normal_speed = 0
        self.charged_dmg = 0
        self.skill_dmg = 0
        self.burst_dmg = 0
        self.healing_bonus = 0
        self.ele_res_red = 0
        self.swirl_res_red = 0
        self.normal_attack_type = ""
        self.normal_attack_ratio = 0
        self.normal_AT = ""
        self.normal_AC = 0
        self.normal_hits = 0
        self.normal_RP = 0
        self.passive_hits = 0
        self.charged_attack_type = 0
        self.charged_attack_ratio = 0
        self.charged_AT = 0
        self.charged_AC = ""
        self.charged_hits = 0
        self.charged_RP = 0
        self.charged_stam = 0
        self.skill_ratio = 0
        self.skill_AT = 0
        self.skill_CD = 0
        self.skill_hits = 0
        self.skill_dur = 0
        self.skill_charges = 0
        self.skill_RP = 0
        self.skill_particles = 0
        self.burst_ratio = 0
        self.burst_AT = 0
        self.burst_CD = 0
        self.burst_energy = 0
        self.burst_hits = 0
        self.burst_dur = 0
        self.burst_charges = 0
        self.burst_RP = 0

    def get_name(self):
        return self.name

    def __str__(self):
        s = ''
        for k, v in self.__dict__.items():
            s += f'{k}: {v}\n'
        return s

def main():
    Test = GeneralObject()
    print(GeneralObject.__str__(Test))

if __name__ == '__main__':
    main()