import csv

class Buff:
    def __init__(self,Buff,Share,Type,Character,Weapon,Rank,Constellation,method,Duration,Trigger,Instant,Precast):
        self.name = Buff
        self.share = Share
        self.type = Type
        self.character = Character
        self.constellation = Constellation
        self.weapon = Weapon
        self.weapon_rank = Rank
        self.method = method
        self.duration = Duration
        self.trigger = Trigger
        self.instant = Instant
        self.precast = Precast
        self.time_remaining = self.duration

class Debuff:
    def __init__(self,Debuff,Character,Constellation,Weapon,Rank,Artifact,method,Duration,Trigger):
        self.name = Debuff
        self.character = Character
        self.constellation = Constellation
        self.weapon = Weapon
        self.weapon_rank = Rank
        self.artifact = Artifact
        self.method = method
        self.duration = Duration
        self.trigger = Trigger
        self.time_remaining = self.duration

class StaticBuff:
    def skill_ratio_20pct(self,unit_obj):
        unit_obj.skill_ratio *= 1.2
    def skill_cdr_20pct(self,unit_obj):
        unit_obj.skill_CDR *= 0.8
    def burst_crit_rate_10pct(self,unit_obj):
        unit_obj.burst_crit_rate += 0.1
    def charged_ratio_20pct(self,unit_obj):
        unit_obj.charged_attack_ratio *= 1.2
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

class ActiveBuff:
    def atk_15pct(self,unit_obj):
        unit_obj.live_atk_pct += 0.15
    def cryo_dmg_20pct(self,unit_obj):
        unit_obj.live_cryo += 0.2
    def dmg_15pct(self,unit_obj):
        unit_obj.live_all_dmg += 0.15
    def em_200(self,unit_obj):
        unit_obj.live_elemental_mastery += 200
    def melee_pyro_15pct(self,unit_obj):
        if unit_obj.weapon_type in ("Polearm,","Claymore","Sword"):
            unit_obj.live_pyro += 0.15
    def ben_q(self,unit_obj):
        pass
    def ganyu_charged_reset(self,unit_obj):
        unit_obj.live_charged_speed = 0
    def charged_speed_60pct(self,unit_obj):
        pass
    def skill_cdr_50pct(self,unit_obj):
        pass

class ActiveDebuff:
    def def_15pct(self,unit_obj):
        unit_obj.defence_debuff += 0.15

