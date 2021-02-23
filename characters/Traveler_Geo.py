from core.unit import Char
from core.action import Combo
from core.read_data import buff_dict
import copy


class TravelerGeo(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Traveler (Geo)", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def traveler_geo_a2(self):
        pass

    def traveler_geo_a4(self, _,sim,action):
        if action[1] == 4 and action[0].loop == True:
            proc = TravelerGeoA4(self, action[0].combo)
            proc.add_to_damage_queue(sim)

    def traveler_geo_q_cast(self, _, sim, __):

        if self.constellation >6:
            time = 20
        else:
            time = 15

        if self.constellation >= 1:
            for unit in sim.units:
                unit.active_buffs["Traveler_(Geo)_Q_Buff"] = copy.deepcopy(buff_dict["Traveler_(Geo)_Q_Buff"])
                unit.active_buffs["Traveler_(Geo)_Q_Buff"].time_remaining = time
                unit.active_buffs["Traveler_(Geo)_Q_Buff"].source = self

    @staticmethod
    def traveler_geo_q_buff(unit_obj, sim):
        if unit_obj == sim.chosen_unit:
            unit_obj.live_crit_rate += 0.1

    def traveler_geo_c4(self, _, __, ___):
        self.current_energy += 5


class TravelerGeoA4(Combo):
    def __init__(self, unit_obj, combo):
        super().__init__(unit_obj, combo)
        self.name = "Traveler (Geo) A4"
        self.tick_element = ["Geo"]
        self.tick_times = [0]
        self.tick_damage = [0.6]
        self.tick_units = [1]
        self.tick_types = ["normal"]
        self.ticks = 1
        self.scaling = [1]
        self.loop = False


TravelerGeoTest = TravelerGeo(90, 6, "Harbinger of Dawn", 5, "Noblesse", [6, 6, 6])


def main():
    print(TravelerGeoTest.live_base_atk)
    print(TravelerGeoTest.static_buffs)


if __name__ == '__main__':
    main()
