from kerykeion import AstrologicalSubject, KerykeionChartSVG
import csv
from pprint import pprint

import logging
logging.getLogger().setLevel(logging.ERROR)

# Const
POS_LV_1 = 25
POS_LV_2 = 30
POS_LV_3 = 50
POS_LV_4 = 80
POS_LV_5 = 100
POS_LV_6 = 116

NEG_LV_1 = -116
NEG_LV_2 = -80
NEG_LV_3 = -60
NEG_LV_4 = -36
NEG_LV_5 = -8

def cal_matching_percent(pos_score, neg_score):
    result = 0
    if   pos_score <= POS_LV_1  and neg_score <= NEG_LV_1:     result = 1
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_2:     result = 5
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_3:     result = 20
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_4:     result = 25
    elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_5:     result = 45
    elif pos_score <= POS_LV_1  and neg_score >  NEG_LV_5:     result = 50

    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_1:     result = 10
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_2:     result = 15
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_3:     result = 25
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_4:     result = 40
    elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_5:     result = 50
    elif pos_score <= POS_LV_2  and neg_score >  NEG_LV_5:     result = 55

    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_1:     result = 15
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_2:     result = 20
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_3:     result = 35
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_4:     result = 50
    elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_5:     result = 60
    elif pos_score <= POS_LV_3  and neg_score >  NEG_LV_5:     result = 60

    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_1:     result = 30
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_2:     result = 35
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_3:     result = 40
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_4:     result = 55
    elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_5:     result = 70
    elif pos_score <= POS_LV_4  and neg_score >  NEG_LV_5:     result = 75

    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_1:     result = 35
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_2:     result = 45
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_3:     result = 55
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_4:     result = 65
    elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_5:     result = 80
    elif pos_score <= POS_LV_5  and neg_score >  NEG_LV_5:     result = 90

    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_1:     result = 45
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_2:     result = 50
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_3:     result = 60
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_4:     result = 70
    elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_5:     result = 90
    elif pos_score <= POS_LV_6  and neg_score >  NEG_LV_5:     result = 95

    elif pos_score >  POS_LV_6  and neg_score <= NEG_LV_1:     result = 50
    elif pos_score >  POS_LV_6  and neg_score <= NEG_LV_2:     result = 55
    elif pos_score >  POS_LV_6  and neg_score <= NEG_LV_3:     result = 65
    elif pos_score >  POS_LV_6  and neg_score <= NEG_LV_4:     result = 75
    elif pos_score >  POS_LV_6  and neg_score <= NEG_LV_5:     result = 99
    elif pos_score >  POS_LV_6  and neg_score >  NEG_LV_5:     result = 99

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
        pos_sum = num_score_types[1] + num_score_types[2] * 2 + num_score_types[3] * 3 + num_score_types[4] * 4
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
