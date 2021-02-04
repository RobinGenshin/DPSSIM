from read_data import zhongli_q_ratio_dict
from read_data import razor_auto_ratio_dict
from read_data import ele_ratio_dict
from read_data import phys_ratio_dict
from read_data import razor_qas_ratio_dict


def ratio_type(action):
    if action.unit.name == "Razor" and action.type == "normal":
        return razor_auto_ratio_dict
    elif action.unit.name == "Zhongli" and action.type == "burst":
        return zhongli_q_ratio_dict
    elif action.unit.weapon_type in {"Polearm", "Claymore", "Sword"} and action.type == "normal" or action.type == "charged":
        return phys_ratio_dict
    elif action.unit.weapon_type == "Bow" and action.type == "normal":
        return phys_ratio_dict
    else:
        return ele_ratio_dict
