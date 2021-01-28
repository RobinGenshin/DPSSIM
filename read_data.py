import csv
import OOP
CHARACTER_FILENAME = 'Characters.csv'

# Converts percentage strings to decimals [0, 1]
def pctstr_to_float(pctstr):
    if pctstr == '':
        return 0

    pctstr = pctstr[:-1] # Remove % symbol
    f = float(pctstr)
    return f / 100

def str_to_int(s):
    if s == '':
        return 0
    return int(s)

# Reads character data
def read_character_data():
    with open(CHARACTER_FILENAME) as charfile:
        character_dict = {}
        reader = csv.DictReader(charfile, delimiter=',')
        for row in reader:
            name = row['Character']
            new_unit = OOP.Unit(name)
            character_dict[name] = new_unit

            # TODO may want to consider doing something like: https://stackoverflow.com/a/1305663
            new_unit.Element = row['Element']
            new_unit.Weapon = row['Weapon Type']
            new_unit.Constellation = 0
            new_unit.WeaponRank = 0
            new_unit.BaseATK = str_to_int(row['Base ATK'])
            new_unit.ATK = pctstr_to_float(row['ATK%'])
            new_unit.FlatATK = str_to_int(row['Flat ATK'])
            new_unit.CritRate = pctstr_to_float(row['Crit Rate%'])
            # TODO add the other fields

    return character_dict

def main():
    character_dict = read_character_data()
    print(character_dict['Amber'])


if __name__ == '__main__':
    main()