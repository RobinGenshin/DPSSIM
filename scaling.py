from read_data import zhongli_q_ratio_dict
from read_data import razor_auto_ratio_dict
from read_data import ele_ratio_dict
from read_data import phys_ratio_dict
from read_data import razor_qas_ratio_dict


def ratio_type(unit_obj,action_type):
    if unit_obj.name == "Razor" and action_type == "normal":
        return razor_auto_ratio_dict
    elif unit_obj.name == "Zhongli" and action_type == "burst":
        return zhongli_q_ratio_dict
    elif unit_obj.weapon_type in {"Polearm", "Claymore", "Sword"} and action_type == "normal" or action_type == "charged":
        return phys_ratio_dict
    elif unit_obj.weapon_type == "Bow" and action_type == "normal":
        return phys_ratio_dict
    else:
        return ele_ratio_dict
