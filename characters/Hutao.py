from core.unit import Char
from core.read_data import buff_dict, debuff_dict, ele_ratio_dict, phys_ratio_dict
from core.action import Action, Ability
from core.artifact import Artifact
import copy

# TODO Get Low HP working

class Hutao(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Hutao", level, constellation, weapon, weapon_rank, artifact, talent_levels)
        self.snapshot_buff = 0

    def hutao_e_cast(self, _, __, ___): # TODO How is losing on swap handled?
        #atk_buff_mult = ele_ratio_dict[self.burst_level] * 0.56
        #T1 .0835
        #T6 .11
        hp_to_atk = .11
        tot_hp = self.live_base_hp * (1 + self.live_pct_hp) + self.live_flat_hp
        self.snapshot_buff = hp_to_atk * tot_hp
        self.active_buffs["Hutao_E_Buff"] = copy.copy(buff_dict["Hutao_E_Buff"])
        self.active_buffs["Hutao_E_Buff"].source = self

    def hutao_e_buff(self, _, __):

        self.live_flat_atk += self.snapshot_buff

        self.live_normal_type = "Pyro"
        self.live_normal_tick_units = [1, 0, 0, 1, 0, 0, 1] # TODO fix ICD

        self.live_charged_type = "Pyro"
        self.live_charged_tick_units = [1]

    # TODO Does BB need to be handled specially?

HutaoArtifact = Artifact("Crimson Witch", "pct_hp", "pyro_dmg", "crit_rate", 30) # TODO makesure pct_hp is implememented

HutaoF2P = Hutao(90, 0, "Deathmatch", 1, HutaoArtifact, [6, 6, 6])


def main():
    #print(TartagliaTest.live_base_atk)
    #print(TartagliaTest.static_buffs)
    pass

if __name__ == '__main__':
    main()
