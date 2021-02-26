from math import sqrt


def calculate_crit_atk_ratio(unit):
    g = unit.live_pct_atk / 0.0495 + (unit.live_crit_rate - 0.05) / 0.033 + (unit.live_crit_dmg - 0.5) / 0.066 + unit.artifact.subs
    f = unit.live_flat_atk
    b = unit.live_base_atk

    y = (9801*b*b*g*g) + (396000*b*f + 574200*b*b)*g + (4000000*f*f) + (11600000*b*f) - (45590000*b*b)

    if y > 0:
        z = (sqrt(y) + (99*b*g) + (2000*f) + (200*b)) / (297 * b)
        if z > (20 / 3.3):
            cr = 0.25 + (z - (20 / 3.3)) * 0.0165
            cd = 2 * cr
            atk = (g - z) * 0.0495
        else:
            cr = 0.05
            cd = 0.5
            atk = g * 0.0495
    else:
        cr = 0.05
        cd = 0.5
        atk = g * 0.0495

    if cr > 1:
        cr = 1
        cd = ((((99*b*g) + (2000*f) + (2600*b)) / (198*b)) - (20/3.3 + 75/1.65)) * 0.066 + 2
        atk = (g - (((99*b*g) + (2000*f) + (2600*b)) / (198*b))) * 0.0495

    return {"crit_rate": cr, "crit_dmg": cd, "pct_atk": atk}
