# Const
POS_LV_1 = 20
POS_LV_2 = 26
POS_LV_3 = 32
POS_LV_4 = 38
POS_LV_5 = 44
POS_LV_6 = 50
POS_LV_7 = 60
POS_LV_8 = 70
POS_LV_9 = 109
POS_LV_10 = 110

NEG_LV_1 = -100
NEG_LV_2 = -61
NEG_LV_3 = -51
NEG_LV_4 = -41
NEG_LV_5 = -34
NEG_LV_6 = -27
NEG_LV_7 = -20
NEG_LV_8 = -13
NEG_LV_9 = -6

SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6
URANUS = 7
NEPTUNE = 8
PLUTO = 9
ASC = 10

FIRST_HOUSE = 0
SECOND_HOUSE = 1
THIRD_HOUSE = 2
FORTH_HOUSE = 3
FIFTH_HOUSE = 4
SIXTH_HOUSE = 5
SEVENTH_HOUSE = 6
EIGHTH_HOUSE = 7
NINTH_HOUSE = 8
TENTH_HOUSE = 9
ELEVENTH_HOUSE = 10
TWELFTH_HOUSE = 11

def check_planet_in_house(first, second, planet, house):
    first_planets = first.planets_degrees_ut
    second_houses = second.houses_degree_ut

    if planet == ASC:
        planet_point = first.houses_degree_ut[0]
    else:
        planet_point = first_planets[planet]
    house_range = [second_houses[divmod(house, 12)[1]], second_houses[divmod(house + 1, 12)[1]]]
    
    if house_range[1] < house_range[0]:
        return planet_point >= house_range[0] or planet_point <= house_range[1]
    else:
        return house_range[0] <= planet_point <= house_range[1]