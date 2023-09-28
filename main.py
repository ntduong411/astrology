from kerykeion import AstrologicalSubject, KerykeionChartSVG
import csv
from pprint import pprint

import logging
logging.getLogger().setLevel(logging.ERROR)

# Const
POS_LV_1 = 20
POS_LV_2 = 26
POS_LV_3 = 32
POS_LV_4 = 38
POS_LV_5 = 44
POS_LV_6 = 50
POS_LV_7 = 70
POS_LV_8 = 90
POS_LV_9 = 115
POS_LV_10 = 116

NEG_LV_1 = -120
NEG_LV_2 = -74
NEG_LV_3 = -54
NEG_LV_4 = -34
NEG_LV_5 = -28
NEG_LV_6 = -22
NEG_LV_7 = -16
NEG_LV_8 = -10
NEG_LV_9 = -4

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

def check_planet_in_house(first, second, planet, house, is_asc = False):
    first_planets = first.planets_degrees_ut
    second_houses = second.houses_degree_ut

    if is_asc:
        planet_point = first.houses_degree_ut[0]
    else:
        planet_point = first_planets[planet]
    house_range = [second_houses[divmod(house, 12)[1]], second_houses[divmod(house + 1, 12)[1]]]
    
    if house_range[1] < house_range[0]:
        return planet_point >= house_range[0] or planet_point <= house_range[1]
    else:
        return house_range[0] <= planet_point <= house_range[1]

def score_houses(first, second):
    # planet of first mapping to house of second
    score = check_planet_in_house(first, second, SUN, FIRST_HOUSE)         * 3 + \
            check_planet_in_house(first, second, SUN, SEVENTH_HOUSE)       * 4 + \
            check_planet_in_house(first, second, MOON, FIRST_HOUSE)        * 3 + \
            check_planet_in_house(first, second, MOON, SEVENTH_HOUSE)      * 3 + \
            check_planet_in_house(first, second, VENUS, FIRST_HOUSE)       * 2 + \
            check_planet_in_house(first, second, VENUS, SEVENTH_HOUSE)     * 3 + \
            check_planet_in_house(first, second, JUPITER, SEVENTH_HOUSE)   * 2 + \
            check_planet_in_house(first, second, SUN, SEVENTH_HOUSE, True) * 3

    # planet of second mapping to house of first
    score += check_planet_in_house(second, first, SUN, FIRST_HOUSE)         * 3 + \
             check_planet_in_house(second, first, SUN, SEVENTH_HOUSE)       * 4 + \
             check_planet_in_house(second, first, MOON, FIRST_HOUSE)        * 3 + \
             check_planet_in_house(second, first, MOON, SEVENTH_HOUSE)      * 3 + \
             check_planet_in_house(second, first, VENUS, FIRST_HOUSE)       * 2 + \
             check_planet_in_house(second, first, VENUS, SEVENTH_HOUSE)     * 3 + \
             check_planet_in_house(second, first, JUPITER, SEVENTH_HOUSE)   * 2 + \
             check_planet_in_house(second, first, SUN, SEVENTH_HOUSE, True) * 3

    return score

def cal_matching_percent(pos_score, neg_score):
    result = 0
    if   pos_score <= POS_LV_1  and neg_score <= NEG_LV_1:     result = 1
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_2:     result = 3
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_3:     result = 8
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_4:     result = 12
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_5:     result = 22
    elif pos_score <= POS_LV_1  and neg_score >  NEG_LV_6:     result = 35
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_7:     result = 47
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_8:     result = 56
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_9:     result = 59
    elif pos_score <= POS_LV_1  and neg_score >  NEG_LV_9:     result = 61
   
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_1:     result = 2
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_2:     result = 5
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_3:     result = 10
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_4:     result = 15
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_5:     result = 24
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_6:     result = 37
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_7:     result = 51
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_8:     result = 58
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_9:     result = 62
    elif pos_score <= POS_LV_2  and neg_score >  NEG_LV_9:     result = 65

    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_1:     result = 4
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_2:     result = 7
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_3:     result = 13
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_4:     result = 18
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_5:     result = 28
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_6:     result = 40
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_7:     result = 55
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_8:     result = 63
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_9:     result = 68
    elif pos_score <= POS_LV_3  and neg_score >  NEG_LV_9:     result = 71

    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_1:     result = 6
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_2:     result = 11
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_3:     result = 17
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_4:     result = 23
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_5:     result = 30
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_6:     result = 43
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_7:     result = 57
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_8:     result = 66
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_9:     result = 70
    elif pos_score <= POS_LV_4  and neg_score >  NEG_LV_9:     result = 76

    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_1:     result = 9
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_2:     result = 16
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_3:     result = 20
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_4:     result = 27
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_5:     result = 34  
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_6:     result = 45
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_7:     result = 64
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_8:     result = 73
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_9:     result = 77
    elif pos_score <= POS_LV_5  and neg_score >  NEG_LV_9:     result = 80

    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_1:     result = 14
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_2:     result = 21
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_3:     result = 25
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_4:     result = 31
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_5:     result = 39
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_6:     result = 49
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_7:     result = 69
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_8:     result = 75
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_9:     result = 79
    elif pos_score <= POS_LV_6  and neg_score >  NEG_LV_9:     result = 85

    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_1:     result = 19
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_2:     result = 29
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_3:     result = 33
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_4:     result = 38
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_5:     result = 48
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_6:     result = 67
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_7:     result = 74
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_8:     result = 84
    elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_9:     result = 86
    elif pos_score <= POS_LV_7  and neg_score >  NEG_LV_9:     result = 91

    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_1:     result = 26
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_2:     result = 36
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_3:     result = 42
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_4:     result = 46
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_5:     result = 54
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_6:     result = 78
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_7:     result = 83
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_8:     result = 90
    elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_9:     result = 93
    elif pos_score <= POS_LV_8  and neg_score >  NEG_LV_9:     result = 97

    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_1:     result = 32
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_2:     result = 44
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_3:     result = 50
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_4:     result = 52
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_5:     result = 72
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_6:     result = 82
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_7:     result = 88
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_8:     result = 92
    elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_9:     result = 95
    elif pos_score <= POS_LV_9  and neg_score >  NEG_LV_9:     result = 98

    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_1:     result = 41
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_2:     result = 53
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_3:     result = 60
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_4:     result = 81
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_5:     result = 87
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_6:     result = 89
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_7:     result = 94
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_8:     result = 96
    elif pos_score > POS_LV_10  and neg_score <= NEG_LV_9:     result = 99
    elif pos_score > POS_LV_10  and neg_score >  NEG_LV_9:     result = 100

    return result / 100

results = []

# Read Relationship Compability
rcs = []
with open('relationship_compatibility.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        rcs.append({
            "obj_1": row["Obj1"],
            "obj_2": row["Obj2"],
            "aspect": int(row["Aspect"]),
            "score": int(row["Score"]),
        })


# Read samples
samples = []
with open('samples.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        first = AstrologicalSubject(row["name_1"], int(row["year_1"]), int(row["month_1"]), int(row["day_1"]), int(row["hour_1"]), int(row["minute_1"]), row["place_1"])
        second = AstrologicalSubject(row["name_2"], int(row["year_2"]), int(row["month_2"]), int(row["day_2"]), int(row["hour_2"]), int(row["minute_2"]), row["place_2"])
        name = KerykeionChartSVG(first, chart_type="Synastry", second_obj=second)

        # Read Aspect Table
        ats = []
        for item in name.aspects_list:
            obj_1 = item["p1_name"]
            obj_2 = item["p2_name"]
            ignore_objs = ["Chiron", "True_Node"]
            if obj_1 in ignore_objs or obj_2 in ignore_objs: continue

            ats.append({
                "obj_1": item["p1_name"],
                "obj_2": item["p2_name"],
                "aspect": int(item["aspect_degrees"])
            })

        # Mapping and Calculating

        # score types: 0, 1, 2, 3, 4, -4, -3, -2, -1
        num_score_types = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for at in ats:
            for rc in rcs:
                if at["obj_1"] == rc["obj_1"] and at["obj_2"] == rc["obj_2"] and at["aspect"] == rc["aspect"]:
                    num_score_types[rc["score"]] += 1
                    # if rc["score"] > 0:
                    #     pos_scores.append(rc["score"]) 
                    # if rc["score"] < 0:
                    #     neg_scores.append(rc["score"]) 
        pos_sum = num_score_types[1] + num_score_types[2] * 2 + num_score_types[3] * 3 + num_score_types[4] * 4 + score_houses(first, second)
        neg_sum = num_score_types[-1] + num_score_types[-2] * 2 + num_score_types[-3] * 3 + num_score_types[-4] * 4
        results.append([
            first["name"], second["name"], 
            pos_sum, -neg_sum,
            num_score_types[1], num_score_types[2], num_score_types[3], num_score_types[4],
            num_score_types[-1], num_score_types[-2], num_score_types[-3], num_score_types[-4], 
            cal_matching_percent(pos_sum, -neg_sum)])
    
# Exort file
with open('results.csv', mode='w', newline='') as results_file:
    writer = csv.writer(results_file, delimiter=',')
    writer.writerows(results)
