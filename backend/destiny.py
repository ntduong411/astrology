from kerykeion import AstrologicalSubject, KerykeionChartSVG, SynastryAspects
import csv
from pprint import pprint
from utils import *
from planet_house_rel import *
from pathlib import Path

class Aspect:
    def __init__(self, person_1, person_2, aspect):
        self.person_1 = person_1
        self.person_2 = person_2
        self.aspect = aspect

    def __eq__(self, obj):
        return isinstance(obj, Aspect)          \
            and self.person_1 == obj.person_1   \
            and self.person_2 == obj.person_2   \
            and self.aspect == obj.aspect

class Destiny:
    def __init__(self, first_person, second_person):
        self.first_person = first_person
        self.second_person = second_person

        self.aspects = self.get_aspects()
        self.aspect_scores = self.read_aspect_score_data()
        self.aspect_harmony_challenges = self.read_harmony_challenge_data()

        self.planet_in_houses = self.get_planet_in_houses()
        self.planet_scores = self.read_planet_score_data()
        self.planet_harmony = self.read_planet_harmony_data()

        self.house_has_planets = self.get_house_has_planets()
        self.house_scores = self.read_house_score_data()
        self.house_harmony = self.read_house_harmony_data()

        self.msgs = self.read_messages()
        
        
    def get_aspects(self):
        
        aspects = SynastryAspects(self.first_person, self.second_person, Path("../kr.config.json"))
        # pprint (aspects.__dict__.keys())
        # pprint (aspects.new_settings_file)
        # pprint (aspects.planets_settings)
        # pprint (aspects.aspects_settings)
        # pprint (aspects.axes_orbit_settings)
        # pprint (aspects.first_init_point_list)
        # pprint (aspects.second_init_point_list)

        # exit()

        ats = []
        # for item in aspects.aspects_list:
        for item in aspects.get_relevant_aspects():
            person_1 = item["p1_name"]
            person_2 = item["p2_name"]
            ignore_objs = ["Chiron", "True_Node"]
            if person_1 in ignore_objs or person_2 in ignore_objs: continue

            ats.append(Aspect(person_1, person_2, int(item["aspect_degrees"])))
        return ats

    def get_planet_in_houses(self):
        phs = []
        if SUN_FIRST_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_FIRST_HOUSE_REL)

        if SUN_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_SEVENTH_HOUSE_REL)

        if MOON_FIRST_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_FIRST_HOUSE_REL)

        if MOON_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_SEVENTH_HOUSE_REL)

        if VENUS_FIRST_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_FIRST_HOUSE_REL)
        
        if VENUS_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_SEVENTH_HOUSE_REL)

        if JUPITER_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(JUPITER_SEVENTH_HOUSE_REL)

        if ASC_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(ASC_SEVENTH_HOUSE_REL)

        return phs

    def get_house_has_planets(self):
        phs = []
        if SUN_FIRST_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_FIRST_HOUSE_REL)

        if SUN_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_SEVENTH_HOUSE_REL)

        if MOON_FIRST_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_FIRST_HOUSE_REL)

        if MOON_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_SEVENTH_HOUSE_REL)

        if VENUS_FIRST_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_FIRST_HOUSE_REL)
        
        if VENUS_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_SEVENTH_HOUSE_REL)

        if JUPITER_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(JUPITER_SEVENTH_HOUSE_REL)

        if ASC_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(ASC_SEVENTH_HOUSE_REL)

        return phs

    def report(self):
        num_score_types = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for at in self.aspects:
            for a_score in self.aspect_scores:
                if at == a_score["aspect"]:
                    num_score_types[a_score["score"]] += 1
        
        report = self.cal_aspect_score()
        report["first_person"] = self.first_person.name
        report["second_person"] = self.second_person.name
        report["aspect"]["house_score"] = self.cal_house_score()
        report["aspect"]["planet_score"] = self.cal_planet_score()
        report["harmony_challenge"] = self.cal_aspect_harmony_challenge()
        report["harmony_challenge"]["house_harmonies"] = self.cal_house_harmony()
        report["harmony_challenge"]["plane_harmonies"] = self.cal_planet_harmony()
        report.update(self.cal_harmony_challenge_score())

        report["message"] = self.cal_message(report)
        report["compas"] = dict(report["compas"])
        report["incompas"] = dict(report["incompas"])
        
        return report

    def cal_aspect_score(self):
        num_score_types = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        for at in self.aspects:
            for a_score in self.aspect_scores:
                if at == a_score["aspect"]:
                    num_score_types[a_score["score"]] += 1
        
        (pos_score, neg_score, matching_score, destiny_score) = self.cal_matching_score(num_score_types)
        
        return {
            "aspect": {
                "pos_score": pos_score,
                "neg_score": neg_score,
                "num_score_p1": num_score_types[1],
                "num_score_p2": num_score_types[2],
                "num_score_p3": num_score_types[3],
                "num_score_p4": num_score_types[4],
                "num_score_n1": num_score_types[-1],
                "num_score_n2": num_score_types[-2],
                "num_score_n3": num_score_types[-3],
                "num_score_n4": num_score_types[-4],
                "matching_score": matching_score,
            },
            "destiny_score": destiny_score,
        }

    def cal_aspect_harmony_challenge(self):
        harmonies = {}
        compas = {
            "Commitment": 0,
            "Communication": 0,
            "Emotional": 0,
            "Intellectual": 0,
            "Lifestyle": 0,
            "Physical": 0,
        }
        challenges = {}
        incompas = compas.copy()

        for at in self.aspects:
            for ahc in self.aspect_harmony_challenges:
                if at == ahc["aspect"]:
                    if ahc["harmony"] != "":
                        harmonies[ahc["harmony"]] = harmonies.get(ahc["harmony"], 0) + 1
                    if ahc["compa"] != "":
                        compas[ahc["compa"]] = compas.get(ahc["compa"], 0) + 1
                    if ahc["challenge"] != "":
                        challenges[ahc["challenge"]] = challenges.get(ahc["challenge"], 0) + 1
                    if ahc["incompa"] != "":
                        incompas[ahc["incompa"]] = incompas.get(ahc["incompa"], 0) + 1

        return {
            "aspect_harmonies": harmonies,
            "aspect_challenges": challenges,
            "aspect_compas": compas,
            "aspect_incompas": incompas,
        }

    def cal_house_score(self):
        house_score = 0

        for h in self.house_has_planets:
            for hs in self.house_scores:
                if h == hs["house_has_planet"]:
                    house_score += hs["score"]
        
        return house_score

    def cal_house_harmony(self):
        harmonies = {}
        compas = {
            "Commitment": 0,
            "Communication": 0,
            "Emotional": 0,
            "Intellectual": 0,
            "Lifestyle": 0,
            "Physical": 0,
        }

        for h in self.house_has_planets:
            for hh in self.house_harmony:
                if h == hh["house_has_planet"]:
                    if hh["harmony"] != "":
                        harmonies[hh["harmony"]] = harmonies.get(hh["harmony"], 0) + 1
                    if hh["compa"] != "":
                        compas[hh["compa"]] = compas.get(hh["compa"], 0) + 1
        
        return {
            "harmonies": harmonies,
            "compas": compas,
        }

    def cal_planet_score(self):
        planet_score = 0

        for p in self.planet_in_houses:
            for ps in self.planet_scores:
                if p == ps["planet_in_house"]:
                    planet_score += ps["score"]
        
        return planet_score

    def cal_planet_harmony(self):
        harmonies = {}
        compas = {
            "Commitment": 0,
            "Communication": 0,
            "Emotional": 0,
            "Intellectual": 0,
            "Lifestyle": 0,
            "Physical": 0,
        }

        for p in self.planet_in_houses:
            for ph in self.planet_harmony:
                if p == ph["planet_in_house"]:
                    if ph["harmony"] != "":
                        harmonies[ph["harmony"]] = harmonies.get(ph["harmony"], 0) + 1
                    if ph["compa"] != "":
                        compas[ph["compa"]] = compas.get(ph["compa"], 0) + 1
        
        return {
            "harmonies": harmonies,
            "compas": compas,
        }

    def cal_message(self, report):
        destiny_score = round(report["destiny_score"] * 100)
        major_compa = report["compas"][0][0]
        
        for msg in self.msgs:
            if destiny_score > msg["destiny_score_min"] and destiny_score <= msg["destiny_score_max"] and major_compa == msg["compa"]:
                return msg["message_en"]

    def read_aspect_score_data(self):
        ass = []
        with open('../database/aspect_scores.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                ass.append({
                    "aspect": Aspect(row["Person1"], row["Person2"], int(row["Aspect"])),
                    "score": int(row["Score"]),
                })
        return ass

    def read_planet_score_data(self):
        ps = []
        with open('../database/planet_score.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                ps.append({
                    "planet_in_house": Planet_House_Rel(row["Planet"], row["House"]),
                    "score": int(row["Score"]),
                })
        return ps

    def read_planet_harmony_data(self):
        phs = []
        with open('../database/planet_harmony.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                phs.append({
                    "planet_in_house": Planet_House_Rel(row["Planet"], row["House"]),
                    "score": int(row["Score"]),
                    "harmony": row["Harmonious Keyword"],
                    "compa": row["Compatibility Category"],
                })
        return phs

    def read_house_score_data(self):
        hs = []
        with open('../database/house_score.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                hs.append({
                    "house_has_planet": Planet_House_Rel(row["Planet"], row["House"]),
                    "score": int(row["Score"]),
                })
        return hs

    def read_house_harmony_data(self):
        hps = []
        with open('../database/house_harmony.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                hps.append({
                    "house_has_planet": Planet_House_Rel(row["Planet"], row["House"]),
                    "score": int(row["Score"]),
                    "harmony": row["Harmonious Keyword"],
                    "compa": row["Compatibility Category"],
                })
        return hps

    def read_harmony_challenge_data(self):
        hcs = []
        with open('../database/harmony_challenge.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                hcs.append({
                    "aspect": Aspect(row["Person1"], row["Person2"], int(row["Aspect"])),
                    "harmony": row["Harmonious Keyword"],
                    "compa": row["Compatibility Category"],
                    "challenge": row["Challenges Keyword"],
                    "incompa": row["Incompatibility Category"],
                })
        return hcs

    def read_messages(self):
        msgs = []
        with open('../database/message.csv', mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                msgs.append({
                    "destiny_score_min": int(row["Destiny Score Min"]),
                    "destiny_score_max": int(row["Destiny Score Max"]),
                    "compa": row["Compatibility"],
                    "message_en": row["Message (Eng)"],
                    "message_vi": row["Message (Viet)"],
                })
        return msgs
    
    def cal_harmony_challenge_score(self):
        aspect_data = self.cal_aspect_harmony_challenge()
        house_data = self.cal_house_harmony()
        planet_data = self.cal_planet_harmony()

        for key, value in aspect_data["aspect_harmonies"].items():
            if key in house_data["harmonies"].keys():
                value += house_data["harmonies"][key]
            
            if key in planet_data["harmonies"].keys():
                value += planet_data["harmonies"][key]

            aspect_data["aspect_harmonies"][key] = value
        
        for key, value in aspect_data["aspect_compas"].items():
            if key in house_data["compas"].keys():
                value += house_data["compas"][key]
            
            if key in planet_data["compas"].keys():
                value += planet_data["compas"][key]

            aspect_data["aspect_compas"][key] = value


        harmonies = sorted(aspect_data["aspect_harmonies"].items(), key=lambda x:x[1], reverse=True)
        challenges = sorted(aspect_data["aspect_challenges"].items(), key=lambda x:x[1], reverse=True)

        compas = sorted(aspect_data["aspect_compas"].items(), key=lambda x:x[1], reverse=True)
        incompas = sorted(aspect_data["aspect_incompas"].items(), key=lambda x:x[1], reverse=True)

        return {
            "harmonies": harmonies,
            "challenges": challenges,
            "compas": compas,
            "incompas": incompas,
        }


    def cal_matching_score(self, num_score_types):
        pos_score = num_score_types[1]  \
            + num_score_types[2] * 2    \
            + num_score_types[3] * 3    \
            + num_score_types[4] * 4    \
            + self.cal_house_score() + self.cal_planet_score()

        neg_score = num_score_types[-1] \
            + num_score_types[-2] * 2   \
            + num_score_types[-3] * 3   \
            + num_score_types[-4] * 4
        neg_score = -neg_score

        result = 0
        if   pos_score <= POS_LV_1  and neg_score <= NEG_LV_1:     result = 1
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_2:     result = 2
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_3:     result = 9
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_4:     result = 18
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_5:     result = 19
        elif pos_score <= POS_LV_1  and neg_score >  NEG_LV_6:     result = 23
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_7:     result = 34
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_8:     result = 39
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_9:     result = 41
        elif pos_score <= POS_LV_1  and neg_score >  NEG_LV_9:     result = 44
    
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_1:     result = 3
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_2:     result = 4
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_3:     result = 14
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_4:     result = 24
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_5:     result = 33
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_6:     result = 36
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_7:     result = 38
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_8:     result = 47
        elif pos_score <= POS_LV_2  and neg_score <= NEG_LV_9:     result = 51
        elif pos_score <= POS_LV_2  and neg_score >  NEG_LV_9:     result = 61

        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_1:     result = 5
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_2:     result = 10
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_3:     result = 21
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_4:     result = 26
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_5:     result = 35
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_6:     result = 40
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_7:     result = 50
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_8:     result = 54
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_9:     result = 60
        elif pos_score <= POS_LV_3  and neg_score >  NEG_LV_9:     result = 65

        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_1:     result = 6
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_2:     result = 11
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_3:     result = 22
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_4:     result = 27
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_5:     result = 37
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_6:     result = 43
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_7:     result = 59
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_8:     result = 63
        elif pos_score <= POS_LV_4  and neg_score <= NEG_LV_9:     result = 66
        elif pos_score <= POS_LV_4  and neg_score >  NEG_LV_9:     result = 74

        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_1:     result = 7
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_2:     result = 12
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_3:     result = 25
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_4:     result = 42
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_5:     result = 46  
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_6:     result = 53
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_7:     result = 62
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_8:     result = 68
        elif pos_score <= POS_LV_5  and neg_score <= NEG_LV_9:     result = 77
        elif pos_score <= POS_LV_5  and neg_score >  NEG_LV_9:     result = 80

        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_1:     result = 8
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_2:     result = 13
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_3:     result = 28
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_4:     result = 48
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_5:     result = 52
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_6:     result = 58
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_7:     result = 71
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_8:     result = 76
        elif pos_score <= POS_LV_6  and neg_score <= NEG_LV_9:     result = 82
        elif pos_score <= POS_LV_6  and neg_score >  NEG_LV_9:     result = 87

        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_1:     result = 15
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_2:     result = 16
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_3:     result = 31
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_4:     result = 49
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_5:     result = 67
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_6:     result = 73
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_7:     result = 75
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_8:     result = 85
        elif pos_score <= POS_LV_7  and neg_score <= NEG_LV_9:     result = 89
        elif pos_score <= POS_LV_7  and neg_score >  NEG_LV_9:     result = 92

        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_1:     result = 17
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_2:     result = 29
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_3:     result = 45
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_4:     result = 56
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_5:     result = 72
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_6:     result = 78
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_7:     result = 84
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_8:     result = 90
        elif pos_score <= POS_LV_8  and neg_score <= NEG_LV_9:     result = 94
        elif pos_score <= POS_LV_8  and neg_score >  NEG_LV_9:     result = 96

        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_1:     result = 20
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_2:     result = 32
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_3:     result = 57
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_4:     result = 69
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_5:     result = 79
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_6:     result = 81
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_7:     result = 88
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_8:     result = 93
        elif pos_score <= POS_LV_9  and neg_score <= NEG_LV_9:     result = 97
        elif pos_score <= POS_LV_9  and neg_score >  NEG_LV_9:     result = 99

        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_1:     result = 30
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_2:     result = 55
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_3:     result = 64
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_4:     result = 70
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_5:     result = 83
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_6:     result = 86
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_7:     result = 91
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_8:     result = 95
        elif pos_score > POS_LV_10  and neg_score <= NEG_LV_9:     result = 98
        elif pos_score > POS_LV_10  and neg_score >  NEG_LV_9:     result = 100

        refined_result = result         \
            + num_score_types[4] * 0    \
            - num_score_types[-4] * 5   \
            + num_score_types[3] * 0    \
            - num_score_types[-3] * 0

        return (pos_score, neg_score, round(result / 100, 2), round(refined_result / 100, 2))










    