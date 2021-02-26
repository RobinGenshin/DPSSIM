from core.read_data import zhongli_q_ratio_dict
from core.read_data import razor_auto_ratio_dict
from core.read_data import ele_ratio_dict
from core.read_data import phys_ratio_dict


def ratio_type(unit, action_type):
    if unit.character == "Razor" and action_type == "normal":
        return razor_auto_ratio_dict
    elif unit.character == "Zhongli" and action_type == "burst":
        return zhongli_q_ratio_dict
    elif unit.weapon_type in {"Polearm", "Claymore", "Sword"} and action_type == "normal" or action_type == "charged":
        return phys_ratio_dict
    elif unit.weapon_type == "Bow" and action_type == "normal":
        return phys_ratio_dict
    else:
        return ele_ratio_dict
