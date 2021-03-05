from core.action import WeaponAction
from core.read_data import buff_dict
import copy


class StaticBuff:

    @staticmethod
    def amos_bow(unit):
        unit.normal_dmg += 0.12 + (unit.weapon_rank - 1) * 0.03
        unit.charged_dmg += 0.12 + (unit.weapon_rank - 1) * 0.03

    @staticmethod
    def skyward_harp(unit):
        unit.crit_dmg += 0.2 + (unit.weapon_rank - 1) * 0.05

    @staticmethod
    def rust(unit):
        unit.normal_dmg += 0.4 + (unit.weapon_rank - 1) * 0.1
        unit.charged_dmg -= 0.1

    @staticmethod
    def stringless(unit):
        unit.skill_dmg += 0.24 + (unit.weapon_rank - 1) * 0.06
        unit.burst_dmg += 0.24 + (unit.weapon_rank - 1) * 0.06

    @staticmethod
    def sharpshooter(unit):
        unit.charged_dmg += 0.24 + (unit.weapon_rank - 1) * 0.06

    @staticmethod
    def slingshot(unit):
        unit.charged_dmg += 0.36 + (unit.weapon_rank - 1) * 0.06

    # Catalyst
    @staticmethod
    def skyward_atlas(unit):
        unit.ele_dmg += 0.12 + (unit.weapon_rank - 1) * 0.03

    # Claymore
    @staticmethod
    def wolfs_gravestone(unit):
        unit.pct_atk += 0.2 + (unit.weapon_rank - 1) * 0.05

    @staticmethod
    def skyward_pride(unit):
        unit.all_dmg += 0.08 + (unit.weapon_rank - 1) * 0.02

    # Polearm
    @staticmethod
    def skyward_spine(unit):
        unit.crit_rate += 0.08 + (unit.weapon_rank - 1) * 0.02

    @staticmethod
    def staff_of_homa(unit):
        unit.pct_hp += 0.2 + (unit.weapon_rank - 1) * 0.05
        unit.flat_atk += (0.008 + (unit.weapon_rank - 1) * 0.002) * (unit.base_hp * (1 + unit.pct_hp) + unit.flat_hp)

    @staticmethod
    def staff_of_homa_a(unit):
        unit.pct_hp += 0.2 + (unit.weapon_rank - 1) * 0.05
        unit.flat_atk += (0.018 + (unit.weapon_rank - 1) * 0.004) * (unit.base_hp * (1 + unit.pct_hp) + unit.flat_hp)

    @staticmethod
    def deathmatch(unit):
        unit.pct_atk += 0.24 + (unit.weapon_rank - 1) * 0.05

    @staticmethod
    def white_tassel(unit):
        unit.normal_dmg += 0.24 + (unit.weapon_rank - 1) * 0.06

    # Sword
    @staticmethod
    def aquila_favonia(unit):
        unit.pct_atk += 0.2 + (unit.weapon_rank - 1) * 0.05

    @staticmethod
    def skyward_blade(unit):
        unit.crit_rate += 0.04 + (unit.weapon_rank - 1) * 0.01

    @staticmethod
    def prim_cutter(unit):
        unit.pct_hp += 0.2 + (unit.weapon_rank - 1) * 0.05
        unit.flat_atk += (0.012 + (unit.weapon_rank - 1) * 0.003) * (unit.base_hp * unit.pct_hp + unit.flat_hp)

    @staticmethod
    def black_sword(unit):
        unit.normal_dmg += 0.2 + (unit.weapon_rank - 1) * 0.05
        unit.charged_dmg += 0.2 + (unit.weapon_rank - 1) * 0.05

    @staticmethod
    def festering_desire(unit):
        unit.skill_crit_rate += 0.06 + (unit.weapon_rank - 1) * 0.015
        unit.skill_dmg += 0.16 + (unit.weapon_rank - 1) * 0.04

    @staticmethod
    def harbinger_of_dawn(unit):
        unit.crit_rate += 0.014 + (unit.weapon_rank - 1) * 0.035

    # Misc
    @staticmethod
    def blackcliff(unit):
        unit.pct_atk += 0.12 + (unit.weapon_rank - 1) * 0.03

    @staticmethod
    def lithic(unit, sim):
        liyue_units = sum(1 for unit in sim.units if unit.region == "Liyue")
        unit.pct_atk += (0.07 + (unit.weapon_rank - 1) * 0.01) * liyue_units
        unit.crit_rate += (0.03 + (unit.weapon_rank - 1) * 0.01) * liyue_units

class ActiveBuff:

    @staticmethod
    def skyward_harp_2(unit_obj, sim, _):
        skyward_harp = WeaponAction(unit_obj, 1)
        skyward_harp.tick_damage = [1.25]
        skyward_harp.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Skyward Harp 2"].live_cd = 4 - ((unit_obj.weapon_rank - 1) * 0.5)
        print(unit_obj.character + " proced Skyward Harp")

    @staticmethod
    def compound_bow_2(unit, _, __):
        unit.live_pct_atk += (0.04 + (unit.weapon_rank - 1) * 0.01) * unit.active_buffs["Compound Bow 2"].stacks
        unit.live_normal_speed += (0.012 + (unit.weapon_rank - 1) * 0.003) * unit.active_buffs["Compound Bow 2"].stacks
        unit.triggerable_buffs["Compound Bow 2"].live_cd = 0.3

    @staticmethod
    def compound_bow_3(unit, _, __):
        pass

    @staticmethod
    def viridescent_hunt_2(unit_obj, sim, __):
        viri_hunt = WeaponAction(unit_obj, 8)
        d = ((unit_obj.weapon_rank - 1) * 0.25 + 1) * 0.4
        viri_hunt.tick_damage = [d] * 8
        viri_hunt.tick_times = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
        viri_hunt.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["The Viridescent Hunt 2"].live_cd = 14 - (unit_obj.weapon_rank - 1)
        print(unit_obj.character + " proced The Viridescent Hunt")

    @staticmethod
    def prototype_crescent_2(unit_obj, _):
        unit_obj.live_charged_dmg += 0.36 + (unit_obj.weapon_rank - 1) * 0.09

    # Claymores
    @staticmethod
    def prototype_archaic_2(unit_obj, sim, _):
        archaic = WeaponAction(unit_obj, 1)
        d = 2.4 + (unit_obj.weapon_rank - 1) * 0.6
        archaic.tick_damage = [d]
        archaic.tick_times = [0.5]
        archaic.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Prototype Archaic 2"].live_cd = 15

    def wolfs_gravestone_2(self, unit_obj, sim, _):
        for unit in sim.units:
            unit.active_buffs["Wolf's Gravestone 3"] = copy.copy(buff_dict["Wolf's Gravestone 3"])
            unit.active_buffs["Wolf's Gravestone 3"].source = self
        print(unit_obj.character + " proced Wolf's Gravestone")
        unit_obj.triggerable_buffs["Wolf's Gravestone 2"].live_cd = 30

    @staticmethod
    def wolfs_gravestone_3(unit_obj, _):
        unit_obj.live_pct_atk += 0.4 + (unit_obj.weapon_rank - 1) * 0.1

    @staticmethod
    def rainslasher_2(unit_obj, sim, _):
        if "Hydro" in sim.enemy.elements or "Electro" in sim.enemy.elements:
            unit_obj.live_cond_dmg += 0.2 + (unit_obj.weapon_rank - 1) * 0.05

    @staticmethod
    def whiteblind_2(unit, _):
        unit.live_pct_atk += (0.06 + (unit.weapon_rank - 1) * 0.015) * unit.active_buffs["Whiteblind 2"].stacks
        unit.live_pct_def += (0.06 + (unit.weapon_rank - 1) * 0.015) * unit.active_buffs["Whiteblind 2"].stacks
        unit.triggerable_buffs["Whiteblind 2"].live_cd = 0.5

    @staticmethod
    def skyrider_2(unit, _, __):
        unit.livek_pct_at += (0.06 + (unit.weapon_rank - 1) * 0.01) * unit.active_buffs["Whiteblind 2"].stacks
        unit.triggerable_buffs["Skyrider 2"].live_cd = 0.5

    @staticmethod
    def serpent_2(self, unit_obj, sim, extra):
        pass

    def skyward_pride_2(self, unit_obj, _, __):
        unit_obj.triggerable_buffs["Skyward Pride 3"] = copy.copy(buff_dict["Skyward Pride 3"])
        unit_obj.triggerable_buffs["Skyward Pride 3"].time_remaining = 20
        unit_obj.triggerable_buffs["Skyward Pride 3"].stacks = 8
        unit_obj.triggerable_buffs["Skyward Pride 3"].source = self

    @staticmethod
    def skyward_pride_3(unit_obj, sim, _):
        if unit_obj.triggerable_buffs["Skyward Pride 3"].stacks > 0:
            sp = WeaponAction(unit_obj, 1)
            d = (unit_obj.weapon_rank - 1) * 0.2 + 0.8
            sp.tick_damage = [d]
            sp.tick_times = [0.1]
            sp.add_to_damage_queue(sim)
            unit_obj.triggerable_buffs["Skyward Pride 3"].stacks -= 1
        else:
            del unit_obj.triggerable_buffs["Skyward Pride 3"]

    # Catalysts
    @staticmethod
    def lost_prayers_2(unit_obj, _, __):
        unit_obj.live_ele_dmg += (0.04 * round(unit_obj.field_time / 4)) * (1 + (unit_obj.weapon_rank - 1) * 0.25)

    @staticmethod
    def skyward_atlas_2(unit_obj, sim, _):
        atlas = WeaponAction(unit_obj, 6)
        d = (unit_obj.weapon_rank - 1) * 0.4 + 1.6
        atlas.tick_damage = [d] * 6
        atlas.tick_times = [2.5, 5, 7.5, 10, 12.5, 15]
        atlas.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Skyward Atlas 2"].live_cd = 30
        print(unit_obj.character + " proced Skyward Atlas")

    @staticmethod
    def solar_pearl_normal_buff_2(unit_obj, _):
        unit_obj.live_normal_dmg += 0.2 + (unit_obj.weapon_rank - 1) * 0.05

    @staticmethod
    def solar_pearl_ability_buff_2(unit_obj, _):
        unit_obj.live_skill_dmg += 0.2 + (unit_obj.weapon_rank - 1) * 0.05
        unit_obj.live_burst_dmg += 0.2 + (unit_obj.weapon_rank - 1) * 0.05

    @staticmethod
    def eye_of_perception_2(unit_obj, sim, _):
        eop = WeaponAction(unit_obj, 1)
        eop.ticks = 1
        d = (unit_obj.weapon_rank - 1) * 0.3 + 2.4
        eop.tick_damage = [d]
        eop.tick_times = [0.1]
        eop.tick_units = [0]
        eop.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Eye of Perception 2"].live_cd = 12 - (unit_obj.weapon_rank - 1)

    @staticmethod
    def widsith_2(unit_obj, _, __):
        unit_obj.live_pct_atk += 0.2 + (unit_obj.weapon_rank - 1) * 0.05
        unit_obj.live_ele_dmg += 0.16 + (unit_obj.weapon_rank - 1) * 0.04
        unit_obj.live_ele_m += 80 + (unit_obj.weapon_rank - 1) * 20
        unit_obj.triggerable_buffs["Widsith 2"].live_cd = 30

    @staticmethod
    def prototype_amber_2(unit_obj, sim, _):
        energy_gain = (4 + (unit_obj.weapon_rank - 1) * 0.5) * 3
        for unit in sim.units:
            unit.current_energy = min(unit.live_burst_energy_cost, unit.current_energy + energy_gain)

    @staticmethod
    def mappa_marre_2(unit, _, __):
        unit.live_all_dmg += (0.08 + (unit.weapon_rank - 1) * 0.02) * unit.active_buffs["Mappa Marre 2"].stacks

    # Polearms
    @staticmethod
    def skyward_spine_2(unit_obj, sim, _):
        skyward_spine = WeaponAction(unit_obj, 1)
        d = 0.4 + (unit_obj.weapon_rank - 1) * 0.1
        skyward_spine.tick_damage = [d]
        skyward_spine.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Skyward Spine 2"].live_cd = 2

    @staticmethod
    def primordial_spear_2(unit, _):
        unit.live_pct_atk += (0.032 + (unit.weapon_rank - 1) * 0.007) * unit.active_buffs["Prim Spear 2"].stacks
        if unit.active_buffs["Prim Spear 2"].stacks == 7:
            unit.live_all_dmg += 0.24 + (unit.weapon_rank - 1) * 0.06

    @staticmethod
    def prototype_starglitter_2(unit, _):
        unit.live_normal_dmg += (0.08 + (unit.weapon_rank - 1) * 0.02) * unit.active_buffs["Prototype Starglitter 2"].stacks

    @staticmethod
    def crescent_pike_2(unit_obj, sim, _):
        cres = WeaponAction(unit_obj, 1)
        d = (unit_obj.weapon_rank - 1) * 0.05 + 0.2
        cres.tick_damage = [d]
        cres.add_to_damage_queue(sim)

    # Swords
    @staticmethod
    def lions_roar_2(unit_obj, sim, _):
        if "Pyro" in sim.enemy.elements or "Electro" in sim.enemy.elements:
            unit_obj.live_cond_dmg += 0.2 + (unit_obj.weapon_rank - 1) * 0.05

    @staticmethod
    def aquila_favonia_2(unit_obj, sim, _):
        aq = WeaponAction(unit_obj, 1)
        d = (unit_obj.weapon_rank - 1) * 0.3 + 2
        aq.tick_damage = [d]
        aq.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Aquila Favonia 2"].live_cd = 15

    @staticmethod
    def prototype_rancour_2(unit_obj, _):
        unit_obj.live_pct_atk += (0.04 + (unit_obj.weapon_rank - 1) * 0.01) * unit_obj.active_buffs["Prototype Rancour 2"].stacks
        unit_obj.live_pct_def += (0.04 + (unit_obj.weapon_rank - 1) * 0.01) * unit_obj.active_buffs["Prototype Rancour 2"].stacks
        unit_obj.triggerable_buffs["Prototype Rancour 2"].live_cd = 0.5

    def skyward_blade_2(self, unit_obj, _, __):
        unit_obj.live_normal_speed += 0.1
        unit_obj.triggerable_buffs["Skyward Blade 3"] = copy.copy(buff_dict["Skyward Blade 3"])
        unit_obj.triggerable_buffs["Skyward Blade 3"].time_remaining = 12
        unit_obj.triggerable_buffs["Skyward Blade 3"].source = self
        unit_obj.active_buffs["Skyward Blade 4"] = copy.copy(buff_dict["Skyward Blade 4"])
        unit_obj.active_buffs["Skyward Blade 4"].time_remaining = 12
        unit_obj.active_buffs["Skyward Blade 4"].source = self

    @staticmethod
    def skyward_blade_3(unit_obj, sim, _):
        sb = WeaponAction(unit_obj, 1)
        sb.ticks = 1
        d = (unit_obj.weapon_rank - 1) * 0.05 + 0.2
        sb.tick_damage = [d]
        sb.add_to_damage_queue(sim)

    @staticmethod
    def skyward_blade_4(unit_obj, _):
        unit_obj.live_normal_speed += 0.1

    @staticmethod
    def the_flute_2(unit_obj, sim, _):
        tf = WeaponAction(unit_obj, 1)
        tf.ticks = 1
        d = (unit_obj.weapon_rank - 1) * 0.05 + 0.2
        tf.tick_damage = [d]
        tf.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["The Flute 2"].live_cd = 0.5

    @staticmethod
    def iron_sting_2(unit, _):
        unit.live_all_dmg += (0.06 + (unit.weapon_rank - 1) * 0.015) * unit.active_buffs["Iron Sting 2"].stacks

    # Misc
    @staticmethod
    def favonius(unit_obj, sim, extra):
        from core.action import Particle
        particles = Particle(unit_obj, "Clear", 3, sim)
        particles.add_to_energy_queue(sim)
        unit_obj.triggerable_buffs["Favonius"].live_cd = 12 - (unit_obj.weapon_rank - 1) * 1.5

    @staticmethod
    def sacrificial(unit_obj, _, __):
        unit_obj.live_skill_cd = 0
        unit_obj.triggerable_buffs["Sacrificial"].live_cd = 30 - (unit_obj.weapon_rank - 1) * 4

    @staticmethod
    def geo_weapons(unit_obj, _):
        if "Shield" in unit_obj.active_buffs:
            mult = 2
        else:
            mult = 1
        unit_obj.live_pct_atk += (0.08 + (unit_obj.weapon_rank - 1) * 0.02) * unit_obj.active_buffs["Geo Weapon"].stacks * mult

    @staticmethod
    def dragonspine(unit_obj, sim, _):
        dragonspine = WeaponAction(unit_obj, 1)
        d = (unit_obj.weapon_rank - 1) * 0.15 + 0.8
        if "Cryo" in sim.enemy.elements or "Frozen" in sim.enemy.elements:
            d *= 2.5
        dragonspine.tick_damage = [d]
        dragonspine.add_to_damage_queue(sim)
        unit_obj.triggerable_buffs["Dragonspine"].live_cd = 10
        print("Dragonspine effect")
