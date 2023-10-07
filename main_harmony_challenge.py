from kerykeion import AstrologicalSubject, KerykeionChartSVG
import csv, json
from pprint import pprint

import logging
logging.getLogger().setLevel(logging.ERROR)

# Const

def harmony_challenge_result(aspects):
    pprint (aspects)

categories = {
    "Commitment": 0,
    "Communication": 0,
    "Emotional": 0,
    "Intellectual": 0,
    "Lifestyle": 0,
    "Physical": 0,
}

results = []
results_json = []

# Read Harmony Challenge
hcs = []
with open('harmony_challenge.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        hcs.append({
            "obj_1": row["Person1"],
            "obj_2": row["Person2"],
            "aspect": int(row["Aspect"]),
            "harmony": row["Harmony"],
            "compatibility": row["Compatibility"],
            "challenge": row["Challenge"],
            "incompatibility": row["Incompatibility"],
        })


# Read samples
samples = []
with open('samples.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        first = AstrologicalSubject(row["name_1"], int(row["year_1"]), int(row["month_1"]), int(row["day_1"]), int(row["hour_1"]), int(row["minute_1"]), row["place_1"])
        second = AstrologicalSubject(row["name_2"], int(row["year_2"]), int(row["month_2"]), int(row["day_2"]), int(row["hour_2"]), int(row["minute_2"]), row["place_2"])
        name = KerykeionChartSVG(first, chart_type="Synastry", second_obj=second)

        harmonies = {}
        compatibilities = categories.copy()
        challenges = {}
        incompatibilities = categories.copy()

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

        for at in ats:
            for hc in hcs:
                if at["obj_1"] == hc["obj_1"] and at["obj_2"] == hc["obj_2"] and at["aspect"] == hc["aspect"]:
                    if hc["harmony"] != "":
                        harmonies[hc["harmony"]] = harmonies.get(hc["harmony"], 0) + 1
                    if hc["compatibility"] != "":
                        compatibilities[hc["compatibility"]] = compatibilities.get(hc["compatibility"], 0) + 1
                    if hc["challenge"] != "":
                        challenges[hc["challenge"]] = challenges.get(hc["challenge"], 0) + 1
                    if hc["incompatibility"] != "":
                        incompatibilities[hc["incompatibility"]] = incompatibilities.get(hc["incompatibility"], 0) + 1
        
        harmonies = sorted(harmonies.items(), key=lambda x:x[1], reverse=True)
        compatibilities = sorted(compatibilities.items(), key=lambda x:x[1], reverse=True)
        challenges = sorted(challenges.items(), key=lambda x:x[1], reverse=True)
        incompatibilities = sorted(incompatibilities.items(), key=lambda x:x[1], reverse=True)
        
        results.append([
            first["name"], second["name"], 
            harmonies[0], harmonies[1], harmonies[2], harmonies[3], harmonies[4], harmonies[5], 
            compatibilities[0], compatibilities[1], compatibilities[2], compatibilities[3], compatibilities[4], compatibilities[5], 
            challenges[0], challenges[1], challenges[2], challenges[3], challenges[4], challenges[5], 
            incompatibilities[0], incompatibilities[1], incompatibilities[2], incompatibilities[3], incompatibilities[4], incompatibilities[5]
        ])



        results_json.append({
            "first_person": first["name"],
            "second_person": second["name"],
            "harmonies": harmonies[0:6],
            "compatibilities": dict(compatibilities[0:6]),
            "challenges": challenges[0:6],
            "incompatibilities": dict(incompatibilities[0:6]),
        })
    
# Exort file
with open('hc_results.csv', mode='w', newline='') as results_file:
    writer = csv.writer(results_file, delimiter=',')
    writer.writerows(results)


# Serializing json
json_object = json.dumps(results_json, indent=4)
 
# Writing to sample.json
with open("hc_results.json", "w") as outfile:
    outfile.write(json_object)
