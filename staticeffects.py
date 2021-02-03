class StaticBuff:


    # Character

    # Albedo

    def albedo_a2(self,unit_obj):
        unit_obj.skill_dmg += 0.125


    # Amber

    def amber_a2(self,unit_obj):
        unit_obj.skill_crit_rate += 0.1

    def skill_ratio_20pct(self,unit_obj):
        pass
    def skill_cdr_20pct(self,unit_obj):
        unit_obj.skill_CDR *= 0.8
    def burst_crit_rate_10pct(self,unit_obj):
        unit_obj.burst_crit_rate += 0.1
    def charged_ratio_20pct(self,unit_obj):
        pass
    def skill_flat_200pct(self,unit_obj):
        unit_obj.skill_flat_ratio += 2
    def burst_level_plus_3(self,unit_obj):
        unit_obj.burst_level += 3
    def skill_level_plus_3(self,unit_obj):
        unit_obj.skill_level += 3
    def skill_cd_minus_20pct(self,unit_obj):
        unit_obj.skill_CDR *= 0.8
    def q_on_use_atk_pct_10pct(self,unit_obj):
        unit_obj.atk_pct += 0
    def burst_refund_15(self,unit_obj):
        unit_obj.burst_energy -= 15
    def skill_dmg_15pct(self,unit_obj):
        unit_obj.skill_dmg += 0.15
    def aimed_shot_dur_minus_60pct(self,unit_obj):
        unit_obj.charged_AT *= 0.4
    def skill_charges_plus_1(self,unit_obj):
        unit_obj.skill_charges += 1
    def q_on_use_200em(self,unit_obj):
        pass
    def electro_on_hit_self_22pct(self,unit_obj):
        pass
    def burst_flat_222pct(self,unit_obj):
        unit_obj.burst_flat_ratio += 2.22
    def electro_on_hit_30pct(self,unit_obj):
        pass
    def charged_cryo_res_15pct(self,unit_obj):
        pass
    def q_on_hit_15_pct(self,unit_obj):
        pass
    def skill_skip_charge(self,unit_obj):
        pass

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
        unit_obj.elemental_dmg += 0.12 + (unit_obj.weapon_rank-1)*0.03

    # Claymore

    def wolfs_gravestone(self,unit_obj):
        unit_obj.atk_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05

    def skyward_pride(self,unit_obj):
        unit_obj.all_dmg += 0.8 + (unit_obj.weapon_rank-1)*0.02

    # Polearm

    def prim_cutter(self,unit_obj):
        unit_obj.hp_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05
        unit_obj.flat_atk += (0.012 + (unit_obj.weapon_rank-1)*0.003) * (unit_obj.base_hp * unit_obj.hp_pct + unit_obj.flat_hp)

    def skyward_spine(self,unit_obj):
        unit_obj.crit_rate += 0.8 + (unit_obj.weapon_rank-1)*0.02

    def deathmatch(self,unit_obj):
        unit_obj.atk_pct += 0.24 + (unit_obj.weapon_rank-1)*0.05 

    def white_tassel(self,unit_obj):
        unit_obj.normal_dmg += 0.24 + (unit_obj.weapon_rank-1)*0.06


    # Sword

    def aquila_favonia(self,unit_obj):
        unit_obj.atk_pct += 0.2 + (unit_obj.weapon_rank-1)*0.05

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
        unit_obj.atk_pct += 0.12 + (unit_obj.weapon_rank-1)*0.03