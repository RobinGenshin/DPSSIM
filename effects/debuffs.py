class ActiveDebuff:

    @staticmethod
    def beidou_c6(enemy_obj, _):
        enemy_obj.electro_res_debuff += 0.15

    @staticmethod
    def chongyun_a4(enemy_obj, _):
        pass

    @staticmethod
    def jean_c4(enemy_obj, _):
        enemy_obj.anemo_res_debuff += 0.4

    @staticmethod
    def klee_c2(enemy_obj, _):
        enemy_obj.defence_debuff += 0.23

    @staticmethod
    def lisa_a4(enemy_obj, _):
        enemy_obj.defence_debuff += 0.15

    @staticmethod
    def razor_c4(enemy_obj, _):
        enemy_obj.defence_debuff += 0.15

    @staticmethod
    def riptide_debuff(enemy_obj, _):
        pass

    @staticmethod
    def venti_c2_1(enemy_obj, _):
        enemy_obj.anemo_res_debuff += 0.12
        enemy_obj.physical_res_debuff += 0.12

    @staticmethod
    def venti_c2_2(enemy_obj, _):
        enemy_obj.anemo_res_debuff += 0.12
        enemy_obj.physical_res_debuff += 0.12

    @staticmethod
    def venti_c6(enemy_obj, _):
        pass

    @staticmethod
    def xiangling_c1(enemy_obj, _):
        enemy_obj.pyro_res_debuff += 0.15

    @staticmethod
    def xinyan_c4(enemy_obj, _):
        enemy_obj.physical_res_debuff += 0.15

    @staticmethod
    def xingqiu_c2(enemy_obj, _):
        enemy_obj.hydro_res_debuff += 0.15

    @staticmethod
    def vv_cryo(enemy_obj, _):
        enemy_obj.cryo_res_debuff += 0.4

    @staticmethod
    def vv_hydro(enemy_obj, _):
        enemy_obj.hydro_res_debuff += 0.4

    @staticmethod
    def vv_pyro(enemy_obj, _):
        enemy_obj.pyro_res_debuff += 0.4

    @staticmethod
    def vv_electro(enemy_obj, _):
        enemy_obj.electro_res_debuff += 0.4

    @staticmethod
    def traveler_anemo_anemo(enemy_obj, _):
        enemy_obj.anemo_res_debuff += 0.2

    @staticmethod
    def traveler_anemo_hydro(enemy_obj, _):
        enemy_obj.hydro_res_debuff += 0.2

    @staticmethod
    def traveler_anemo_pyro(enemy_obj, _):
        enemy_obj.pyro_res_debuff += 0.2

    @staticmethod
    def traveler_anemo_electro(enemy_obj, _):
        enemy_obj.electro_res_debuff += 0.2

    @staticmethod
    def traveler_anemo_cryo(enemy_obj, _):
        enemy_obj.cryo_res_debuff += 0.2

    @staticmethod
    def geo_resonance_debuff(enemy_obj, _):
        enemy_obj.geo_res_debuff += 0.2
