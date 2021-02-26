import copy

class Artifact:
    def __init__(self, artifact_set, sands, goblet, circlet, subs):
        self.set = artifact_set
        self.subs = subs  # Number of substats
        self.sands = sands
        self.goblet = goblet
        self.circlet = circlet
        self.pct_atk = 0
        self.flat_atk = 311
        self.crit_rate = 0
        self.crit_dmg = 0
        self.physical_dmg = 0
        self.anemo_dmg = 0
        self.cryo_dmg = 0
        self.electro_dmg = 0
        self.geo_dmg = 0
        self.hydro_dmg = 0
        self.pyro_dmg = 0
        self.ele_m = 0
        self.recharge = 0
        self.pct_hp = 0
        self.flat_hp = 4780
        self.pct_def = 0
        self.flat_def = 0
        a_dict = {'pct_atk': 0.466, 'pct_def': 0.583, 'pct_hp': 0.466, 'crit_rate': 0.311, 'crit_dmg': 0.622,
                  'anemo_dmg': 0.466, 'physical_dmg': 0.583,
                  'cryo_dmg': 0.466, 'electro_dmg': 0.466, 'geo_dmg': 0.466, 'hydro_dmg': 0.466, 'pyro_dmg': 0.466,
                  'ele_m': 187, 'recharge': 0.583}
        setattr(self, sands, getattr(self, sands) + a_dict[sands])
        setattr(self, goblet, getattr(self, goblet) + a_dict[goblet])
        setattr(self, circlet, getattr(self, circlet) + a_dict[circlet])

        if self.circlet == "crit_rate":
            self.crit_rate += 4 * 0.033
            self.subs -= 4
        else:
            self.crit_rate += 5 * 0.033
            self.subs -= 5
        if self.circlet == "crit_dmg":
            self.crit_dmg += 4 * 0.066
            self.subs -= 4
        else:
            self.crit_dmg += 5 * 0.066
            self.subs -= 5
        if self.sands == "recharge":
            self.recharge += 4 * 0.066
            self.subs -= 4
        else:
            self.recharge += 5 * 0.066
            self.subs -= 5
        if self.sands == "pct_atk":
            self.pct_atk += 4 * 0.066
            self.subs -= 4
        else:
            self.pct_atk += 5 * 0.066
            self.subs -= 5
        self.initial_subs = copy.copy(self.subs)


DilucArtifact = Artifact("Crimson Witch", "pct_atk", "pyro_dmg", "crit_rate", 30)


def main():
    pass


if __name__ == '__main__':
    main()

