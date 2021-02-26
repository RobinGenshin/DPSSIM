from core.unit import Char
from core.read_data import buff_dict
from core.artifact import Artifact
import copy


class Mona(Char):
    def __init__(self, level, constellation, weapon, weapon_rank, artifact, talent_levels):
        super().__init__("Mona", level, constellation, weapon, weapon_rank, artifact, talent_levels)

    def mona_a4(self):
        self.hydro_dmg += self.recharge * 0.2

    def mona_q_cast(self, _,sim, __):
        for unit in sim.units:
            unit.triggerable_buffs["Mona_Q_Trigger"] = copy.deepcopy(buff_dict["Mona_Q_Trigger"])
            unit.triggerable_buffs["Mona_Q_Trigger"].time_remaining = 8
            unit.triggerable_buffs["Mona_Q_Trigger"].source = self
            unit.active_buffs["Mona_Q_Buff_1"] = copy.copy(buff_dict["Mona_Q_Buff_1"])
            unit.active_buffs["Mona_Q_Buff_1"].source = self
            unit.triggerable_buffs["Mona_Q_Buff_2"] = copy.copy(buff_dict["Mona_Q_Buff_2"])
            unit.triggerable_buffs["Mona_Q_Buff_2"].source = self

    def mona_q_trigger(self, _, sim, __):
        for action in sim.floating_actions:
            if action.unit.character == "Mona" and action.talent == "burst":
                action.tick_times[1] = sim.time_into_turn
                action.update_time()

                for unit in sim.units:
                    del unit.triggerable_buffs["Mona_Q_Trigger"]
                    unit.active_buffs["Mona_Q_Buff_1"] = copy.deepcopy(buff_dict["Mona_Q_Buff_1"])
                    unit.active_buffs["Mona_Q_Buff_1"].time_remaining = 5
                    unit.active_buffs["Mona_Q_Buff_1"].source = self

                    unit.triggerable_buffs["Mona_Q_Buff_2"].time_remaining = 5
                    unit.triggerable_buffs["Mona_Q_Buff_2"].source = self

    def mona_q_buff_1(self, unit_obj, __):
        unit_obj.live_cond_dmg += min(0.6, 0.42 + self.burst_level * 0.02)

        if self.constellation >= 4:
            unit_obj.live_cond_crit_rate += 0.15

    @staticmethod
    def mona_q_buff_2(unit_obj, sim):
        if "Omen" in sim.enemy.active_debuffs:
            unit_obj.live_electro_charged_dmg += 0.15
            unit_obj.live_vaporise_dmg += 0.15
            unit_obj.live_hydro_swirl_dmg += 0.15

    def mona_a2(self, unit_obj, sim, extra):
        pass

    def mona_c2(self, unit_obj, sim, extra):
        pass

    def mona_c6(self, unit_obj, sim, extra):
        pass


MonaArtifact = Artifact("Noblesse", "recharge", "hydro_dmg", "crit_rate", 30)
MonaF2P = Mona(90, 0, "Sacrificial Fragments", 1, MonaArtifact, [6, 6, 6])


def main():
    print(MonaF2P.live_base_atk)
    print(MonaF2P.static_buffs)


if __name__ == '__main__':
    main()