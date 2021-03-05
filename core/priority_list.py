
import re
from operator import methodcaller


class PriorityList:

    @staticmethod
    def q_after_e(sim, action_list):
        if sim.last_action != None:
            if any((action.talent == "burst" and (action.unit == sim.last_action.unit) and (sim.last_action.talent == "skill") and (sim.last_action.unit.current_skill_cd != 0)) for action in action_list):
                return [x for x in action_list if x.talent == "burst" and x.unit == sim.last_action.unit][0]

    @staticmethod
    def greedy_dps(sim, action_list):
        if sim.last_action is not None:
            for u in sim.units:
                if any([x.greedy == "Yes" for _, x in u.active_buffs.items()]):
                    return max([x for x in action_list if (x.unit == u)], key=methodcaller('calculate_dps_snapshot', sim))

    @staticmethod
    def pickup_particles(sim, action_list):
        a_dict = dict()
        for unit in sim.units:
            a_dict[unit] = 0
            if (unit.current_energy/unit.live_burst_energy_cost) < (unit.current_burst_cd / unit.live_burst_cd):
                for energy in {x for x in sim.floating_actions if x.action_type == "energy"}:
                    if 1 > energy.time_remaining > 0 and energy.element == unit.element:
                        a_dict[unit] += energy.particles * (1 + unit.recharge)
        if any(value > 0 for key, value in a_dict.items()):
            choose = max(a_dict,key=lambda x: a_dict[x])
            unit_actions = [x for x in action_list if x.unit == choose]
            return max(unit_actions, key=methodcaller('calculate_dps_snapshot', sim))

    @staticmethod
    def bennett_q(sim, action_list):
        for action in action_list:
            if action.unit.character == "Bennett" and action.talent == "burst":
                return action

    @staticmethod
    def e_before_q(sim, action_list):
        if any(action.talent == "skill" for action in action_list):
            skill_list = [x for x in action_list if (x.talent == "skill") and any(y.talent == "burst" and y.unit == x.unit for y in action_list)]
            pairs = [(x, y) for x in skill_list for y in action_list if y.unit == x.unit and y.talent == "burst" and x.unit.greedy == False]
            if pairs:
                return max(pairs, key=lambda x: (x[0].calculate_damage_snapshot(sim)+x[1].calculate_damage_snapshot(sim)))[0]
            else:
                pairs = [(x, y) for x in skill_list for y in action_list if
                         y.unit == x.unit and y.talent == "burst" and x.unit.greedy == True]
                if pairs:
                    return max(pairs, key=lambda x: (
                                x[0].calculate_damage_snapshot(sim) + x[1].calculate_damage_snapshot(sim)))[0]

    @staticmethod
    def use_greedy_burst(sim, action_list):
        for action in action_list:
            if action.talent == "burst" and action.greedy == True:
                return action

    @staticmethod
    def ning_combo(sim, action_list):
        for unit in sim.units:
            if unit.character == "Ningguang" and hasattr(unit,"jade_stacks") == True:
                if unit.jade_stacks >0:
                    return max([x for x in action_list if (x.unit.character == "Ningguang" and x.talent == "combo" and x.combo[4] == "N2C")], key=methodcaller('calculate_dps_snapshot',sim))

    @staticmethod
    def ning_burst(_, action_list):
        for action in action_list:
            if action.talent == "burst" and action.unit.character == "Ningguang":
                if action.unit.jade_wall:
                    return action

    @staticmethod
    def xing_trigger(sim, action_list):
        for unit in sim.units:
            if "Xingqiu_Q_Trigger" in unit.triggerable_buffs:
                if unit.triggerable_buffs["Xingqiu_Q_Trigger"].live_cd == 0:
                    return max([x for x in action_list if (x.talent == "combo")], key=methodcaller('calculate_dps_snapshot', sim))

    @staticmethod
    def bei_trigger(sim, action_list):
        for unit in sim.units:
            if "Beidou_Q_Trigger" in unit.triggerable_buffs:
                if unit.triggerable_buffs["Beidou_Q_Trigger"].live_cd == 0:
                    return max([x for x in action_list if (x.talent == "combo")], key=methodcaller('calculate_dps_snapshot', sim))

    @staticmethod
    def max_dps(sim, action_list):
        return max(action_list, key=methodcaller('calculate_dps_snapshot', sim))

    def prioritise(self, sim, action_list):
        if self.q_after_e(sim, action_list):
            return self.q_after_e(sim, action_list)
        if self.greedy_dps(sim, action_list):
            return self.greedy_dps(sim, action_list)
        if self.e_before_q(sim, action_list):
            return self.e_before_q(sim, action_list)
        if self.pickup_particles(sim, action_list):
            return self.pickup_particles(sim, action_list)
        if self.bennett_q(sim, action_list):
            return self.bennett_q(sim, action_list)
        if self.ning_burst(sim, action_list):
            return self.ning_burst(sim, action_list)
        if self.ning_combo(sim, action_list):
            return self.ning_combo(sim, action_list)
        if self.bei_trigger(sim, action_list):
            return self.bei_trigger(sim, action_list)
        if self.xing_trigger(sim, action_list):
            return self.xing_trigger(sim, action_list)
        return self.max_dps(sim, action_list)
