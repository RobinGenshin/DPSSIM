class StaticBuff:


    # Character

    # Albedo

    def albedo_a2(self,unit_obj):
        unit_obj.skill_dmg += 0.125


    # Amber

    def amber_a2(self,unit_obj):
        unit_obj.skill_crit_rate += 0.1

    def amber_c1(self,unit_obj):
        unit_obj.charged_tick_times.append(unit_obj.charged_tick_times[0]+0.1)
        unit_obj.charged_tick_damage.append(1.24*0.2)
        unit_obj.charged_tick_units.append(1)

    def amber_c4(self,unit_obj):
        unit_obj.skill_charges += 1
        unit_obj.skill_cdr *= 0.8

    ## Barbara ##

    def barbara_c2_1(self,unit_obj):
        unit_obj.skill_cdr *= 0.85

    ## Bennett ##

    def bennett_a2(self,unit_obj):
        unit_obj.skill_cdr *= 0.8

    ## Chongyun ##

    def chongyun_c6(self,unit_obj):
        pass

    ## Diluc ##

    def diluc_c1(self,unit_obj):
        unit_obj.all_dmg += 0.075

    ## Diona ##

    def diona_c2(self,unit_obj):
        unit_obj.skill_dmg += 0.075

    ## Ganyu ##

    def ganyu_c2(self,unit_obj):
        unit_obj.skill_charges += 1

    ## Kaeya ##

    def kaeya_c6_1(self,unit_obj):
        unit_obj.burst_tick_times.extend([8.217+0.666,8.217+0.666*2,8.217+0.666*3,8.217*4])
        unit_obj.burst_tick_times = [x*(3/4) for x in unit_obj.burst_tick_times]
        unit_obj.burst_tick_damage.extend([0.776,0.776,0.776,0.776])
        unit_obj.burst_tick_units.extend([0,1,0,1])

    ## Lisa ##

    def lisa_c4(self,unit_obj):
        pass

    def lisa_c5(self,unit_obj):
        pass

    ## Mona ##

    def mona_a4(self,unit_obj):
        unit_obj.hydro_dmg += unit_obj.live_recharge * 0.2

    ## Noelle ##

    def noelle_c2(self,unit_obj):
        unit_obj.charged_dmg += 0.15
        unit_obj.charged_stam_save += 0.15

    def noelle_c6(self,unit_obj):
        unit_obj.triggerable_buffs["Noelle Q 2"].duration += 5

    ## Razor ##

    def razor_a2_1(self,unit_obj):
        unit_obj.skill_cd *= 0.82
    
    def razor_c2(self,unit_obj):
        unit_obj.crit_rate += 0.03

    ## Sucrose ##

    def sucrose_c1(self,unit_obj):
        unit_obj.skill_charges += 1

    def sucrose_c2(self,unit_obj):
        unit_obj.burst_hits += 1
        unit_obj.burst_tick_times.append(unit_obj.burst_tick_times[2]+2)
        unit_obj.burst_tick_damage.append(1.48)
        unit_obj.burst_tick_units.append(1)

    ## Tartaglia ##

    def tartaglia_autolevel(self,unit_obj):
        unit_obj.normal_level += 1
        unit_obj.charged_level += 1

    def tartaglia_c1(self,unit_obj):
        pass

    def tartaglia_c4(self,unit_obj):
        pass

    ## Venti ##

    def venti_c1(self,unit_obj):
        unit_obj.charged_hits += 2
        unit_obj.charged_tick_times.append(unit_obj.burst_tick_times[0]+0.1)
        unit_obj.charged_tick_times.append(unit_obj.burst_tick_times[0]+0.15)
        unit_obj.charged_tick_damage.append(124/3,124/3)
        unit_obj.charged_tick_units.append(0,0)

    ## Xiangling ##

    def xiangling_c4(self,unit_obj):
        pass

    ## Xiao ##

    def xiao_c1(self,unit_obj):
        unit_obj.skill_charges += 1

    ## Xingqiu ##

    def xingqiu_a4(self,unit_obj):
        unit_obj.hydro_dmg += 0.2

    def xingqiu_c4(self,unit_obj):
        unit_obj.skill_tick_damage = [x*1.5 for x in unit_obj.skill_tick_damage]

    def xingqiu_c6(self,unit_obj):
        pass

    ## Xinyan ##
    def xinyan_c1(self,unit_obj):
        pass

    def xinyan_c6(self,unit_obj):
        pass

    



    def burst_level_plus_3(self,unit_obj):
        unit_obj.burst_level += 3
    def skill_level_plus_3(self,unit_obj):
        unit_obj.skill_level += 3

    ## Weapons

    # Bows

    def amos_bow(self,unit_obj):
        unit_obj.normal_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03
        unit_obj.charged_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03
    
    def skyward_harp(self,unit_obj):
        unit_obj.crit_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05
    
    def rust(self,unit_obj):
        unit_obj.normal_dmg += 0.4 + (unit_obj.weapon_rank-1)*0.1
        unit_obj.charged_dmg -= 0.1

    def stringless(self,unit_obj):
        unit_obj.skill_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.6
        unit_obj.burst_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.6

    def sharpshooter(self,unit_obj):
        unit_obj.charged_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.6

    def slingshot(self,unit_obj):
        unit_obj.charged_dmg += 0.36 + (unit_obj.weapon_rank-1)*0.6

    # Catalyst

    def skyward_atlas(self,unit_obj):
        unit_obj.ele_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03

    # Claymore

    def wolfs_gravestone(self,unit_obj):
        unit_obj.pct_atk += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def skyward_pride(self,unit_obj):
        unit_obj.all_dmg += 0.8 + (unit_obj.weapon_rank-1)*0.02

    # Polearm

    def prim_cutter(self,unit_obj):
        unit_obj.pct_hp += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.flat_atk += (0.012 + (unit_obj.weapon_rank-1)*0.003) * (unit_obj.base_hp * unit_obj.hp_pct + unit_obj.flat_hp)

    def skyward_spine(self,unit_obj):
        unit_obj.crit_rate += 0.8 + (unit_obj.weapon_rank-1)*0.02

    def deathmatch(self,unit_obj):
        unit_obj.pct_atk += 0.24 + (unit_obj.weapon_rank-1)*0.05 

    def white_tassel(self,unit_obj):
        unit_obj.normal_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.06


    # Sword

    def aquila_favonia(self,unit_obj):
        unit_obj.pct_atk += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def skyward_blade(self,unit_obj):
        unit_obj.crit_rate += 0.04 + (unit_obj.weapon_rank-1)*0.01

    def black_sword(self,unit_obj):
        unit_obj.normal_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.charged_dmg += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def festering_desire(self,unit_obj):
        unit_obj.skill_crit_rate += 0.06 + (unit_obj.weapon_rank-1)*0.015
        unit_obj.skill_dmg += 0.16 + (unit_obj.weapon_rank-1)*0.04

    # Misc

    def blackcliff(self,unit_obj):
        unit_obj.pct_atk += 0.12 + (unit_obj.weapon_rank-1)*0.03