from kerykeion import AstrologicalSubject, KerykeionChartSVG
import csv
from pprint import pprint

results = []

# Read Relationship Compability
rcs = []
with open('Relationship_Compability.csv', mode='r') as csv_file:
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
        pos_scores = []
        neg_scores = []
        for at in ats:
            for rc in rcs:
                if at["obj_1"] == rc["obj_1"] and at["obj_2"] == rc["obj_2"] and at["aspect"] == rc["aspect"]:
                    if rc["score"] > 0:
                        pos_scores.append(rc["score"]) 
                    if rc["score"] < 0:
                        neg_scores.append(rc["score"]) 

        results.append([first["name"], second["name"], sum(pos_scores), sum(neg_scores)])
    
# Exort file
with open('results.csv', mode='w', newline='') as results_file:
    writer = csv.writer(results_file, delimiter=',')
    writer.writerows(results)
