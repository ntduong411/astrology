from kerykeion import AstrologicalSubject, KerykeionChartSVG, SynastryAspects, NatalAspects
import csv
from pprint import pprint
from utils import *
from planet_house_rel import *
from pathlib import Path
from typing import Union
from swisseph import difdeg2n

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

class CustomNatalAspects(NatalAspects):
    def asp_calc(self, point_one, point_two):
        """
        Utility function.
        It calculates the aspects between the 2 points.
        Args: first point, second point.
        """

        distance = abs(difdeg2n(point_one, point_two))
        diff = abs(point_one - point_two)

        if distance <= self.aspects_settings[0]["orb"]:
            name = self.aspects_settings[0]["name"]
            aspect_degrees = self.aspects_settings[0]["degree"]
            color = self.aspects_settings[0]["color"]
            verdict = True
            aid = 0

        elif (
            (self.aspects_settings[1]["degree"] - self.aspects_settings[1]["orb"])
            <= distance
            <= (self.aspects_settings[1]["degree"] + self.aspects_settings[1]["orb"])
        ):
            name = self.aspects_settings[1]["name"]
            aspect_degrees = self.aspects_settings[1]["degree"]
            color = self.aspects_settings[1]["color"]
            verdict = True
            aid = 1

        elif (
            (self.aspects_settings[2]["degree"] - self.aspects_settings[2]["orb"])
            <= distance
            <= (self.aspects_settings[2]["degree"] + self.aspects_settings[2]["orb"])
        ):
            name = self.aspects_settings[2]["name"]
            aspect_degrees = self.aspects_settings[2]["degree"]
            color = self.aspects_settings[2]["color"]
            verdict = True
            aid = 2

        elif (
            (self.aspects_settings[3]["degree"] - self.aspects_settings[3]["orb"])
            <= distance
            <= (self.aspects_settings[3]["degree"] + self.aspects_settings[3]["orb"])
        ):
            name = self.aspects_settings[3]["name"]
            aspect_degrees = self.aspects_settings[3]["degree"]
            color = self.aspects_settings[3]["color"]
            verdict = True
            aid = 3

        elif (
            (self.aspects_settings[4]["degree"] - self.aspects_settings[4]["orb"])
            <= distance
            <= (self.aspects_settings[4]["degree"] + self.aspects_settings[4]["orb"])
        ):
            name = self.aspects_settings[4]["name"]
            aspect_degrees = self.aspects_settings[4]["degree"]
            color = self.aspects_settings[4]["color"]
            verdict = True
            aid = 4

        elif (
            (self.aspects_settings[5]["degree"] - self.aspects_settings[5]["orb"])
            <= distance
            <= (self.aspects_settings[5]["degree"] + self.aspects_settings[5]["orb"])
        ):
            name = self.aspects_settings[5]["name"]
            aspect_degrees = self.aspects_settings[5]["degree"]
            color = self.aspects_settings[5]["color"]
            verdict = True
            aid = 5

        elif (
            (self.aspects_settings[6]["degree"] - self.aspects_settings[6]["orb"])
            <= distance
            <= (self.aspects_settings[6]["degree"] + self.aspects_settings[6]["orb"])
        ):
            name = self.aspects_settings[6]["name"]
            aspect_degrees = self.aspects_settings[6]["degree"]
            color = self.aspects_settings[6]["color"]
            verdict = True
            aid = 6

        elif (
            (self.aspects_settings[7]["degree"] - self.aspects_settings[7]["orb"])
            <= distance
            <= (self.aspects_settings[7]["degree"] + self.aspects_settings[7]["orb"])
        ):
            name = self.aspects_settings[7]["name"]
            aspect_degrees = self.aspects_settings[7]["degree"]
            color = self.aspects_settings[7]["color"]
            verdict = True
            aid = 7

        elif (
            (self.aspects_settings[8]["degree"] - self.aspects_settings[8]["orb"])
            <= distance
            <= (self.aspects_settings[8]["degree"] + self.aspects_settings[8]["orb"])
        ):
            name = self.aspects_settings[8]["name"]
            aspect_degrees = self.aspects_settings[8]["degree"]
            color = self.aspects_settings[8]["color"]
            verdict = True
            aid = 8

        elif (
            (self.aspects_settings[9]["degree"] - self.aspects_settings[9]["orb"])
            <= distance
            <= (self.aspects_settings[9]["degree"] + self.aspects_settings[9]["orb"])
        ):
            name = self.aspects_settings[9]["name"]
            aspect_degrees = self.aspects_settings[9]["degree"]
            color = self.aspects_settings[9]["color"]
            verdict = True
            aid = 9

        elif (
            (self.aspects_settings[10]["degree"] - self.aspects_settings[10]["orb"])
            <= distance
            <= (self.aspects_settings[10]["degree"] + self.aspects_settings[10]["orb"])
        ):
            name = self.aspects_settings[10]["name"]
            aspect_degrees = self.aspects_settings[10]["degree"]
            color = self.aspects_settings[10]["color"]
            verdict = True
            aid = 10

        else:
            verdict = False
            name = None
            distance = 0
            aspect_degrees = 0
            color = None
            aid = None

        return (
            verdict,
            name,
            distance - aspect_degrees,
            aspect_degrees,
            color,
            aid,
            diff,
        )

class CustomSynastryAspects(CustomNatalAspects):
    """
    Generates an object with all the aspects between two persons.
    """

    def __init__(
        self,
        kr_object_one: AstrologicalSubject,
        kr_object_two: AstrologicalSubject,
        new_settings_file: Union[Path, None] = None,
    ):
        self.first_user = kr_object_one
        self.second_user = kr_object_two

        self.new_settings_file = new_settings_file
        self._parse_json_settings()

        self.first_init_point_list = self.first_user.planets_list + self.first_user.houses_list
        self.second_init_point_list = self.second_user.planets_list + self.second_user.houses_list

    def get_all_aspects(self):
        """
        Return all the aspects of the points in the natal chart in a dictionary,
        first all the individual aspects of each planet, second the aspects
        whiteout repetitions.
        """

        f_1 = self.filter_by_settings(self.first_init_point_list)
        f_2 = self.filter_by_settings(self.second_init_point_list)

        self.all_aspects_list = []

        for first in range(len(f_1)):
            # Generates the aspects list whitout repetitions
            for second in range(len(f_2)):
                verdict, name, orbit, aspect_degrees, color, aid, diff = self.asp_calc(
                    f_1[first]["abs_pos"], f_2[second]["abs_pos"]
                )

                if verdict == True:
                    d_asp = {
                        "p1_name": f_1[first]["name"],
                        "p1_abs_pos": f_1[first]["abs_pos"],
                        "p2_name": f_2[second]["name"],
                        "p2_abs_pos": f_2[second]["abs_pos"],
                        "aspect": name,
                        "orbit": orbit,
                        "aspect_degrees": aspect_degrees,
                        "color": color,
                        "aid": aid,
                        "diff": diff,
                        "p1": self.p_id_decoder(f_1[first]["name"]),
                        "p2": self.p_id_decoder(
                            f_2[second]["name"],
                        ),
                    }

                    self.all_aspects_list.append(d_asp)

        return self.all_aspects_list
    
    def get_relevant_aspects(self):
        """
        Filters the aspects list with the desired points, in this case
        the most important are hardcoded.
        Set the list with set_points and creating a list with the names
        or the numbers of the houses.
        """

        self.get_all_aspects()

        aspects_filtered = []
        for a in self.all_aspects_list:
            if self.aspects_settings[a["aid"]]["is_active"] == True:
                aspects_filtered.append(a)

        axes_list = [
            "First_House",
            "Tenth_House",
            "Seventh_House",
            "Fourth_House",
        ]
        counter = 0

        aspects_list_subtract = []
        for a in aspects_filtered:
            counter += 1
            name_p1 = str(a["p1_name"])
            name_p2 = str(a["p2_name"])

            if name_p1 in axes_list:
                if abs(a["orbit"]) >= self.axes_orbit_settings:
                    aspects_list_subtract.append(a)

            elif name_p2 in axes_list:
                if abs(a["orbit"]) >= self.axes_orbit_settings:
                    aspects_list_subtract.append(a)

        self.aspects = [item for item in aspects_filtered if item not in aspects_list_subtract]

        return self.aspects

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
        
        aspects = CustomSynastryAspects(self.first_person, self.second_person, Path("../kr.config.json"))
        
        ats = []
        # for item in aspects.aspects_list:
        for item in aspects.get_relevant_aspects():
            person_1 = item["p1_name"]
            person_2 = item["p2_name"]
            ignore_objs = ["Chiron", "True_Node"]
            if person_1 in ignore_objs or person_2 in ignore_objs: continue

            ats.append(Aspect(person_1, person_2, int(item["aspect_degrees"])))

            # print (f'{item["p1_name"]}, {item["p2_name"]}, {round(item["aspect_degrees"], 2)}, {round(item["p1_abs_pos"], 2)}, {round(item["p2_abs_pos"], 2)}, {round(item["diff"], 2)}, {round(item["orbit"], 2)} ')
            
        return ats

    def get_planet_in_houses(self):
        phs = []
        if SUN_FIRST_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_FIRST_HOUSE_REL)

        if SUN_FORTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_FORTH_HOUSE_REL)

        if SUN_FIFTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_FIFTH_HOUSE_REL)

        if SUN_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_SEVENTH_HOUSE_REL)

        if SUN_EIGHTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_EIGHTH_HOUSE_REL)

        if SUN_ELEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_ELEVENTH_HOUSE_REL)
        
        if SUN_TWELFTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(SUN_TWELFTH_HOUSE_REL)

        if MOON_FIRST_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_FIRST_HOUSE_REL)
        
        if MOON_FORTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_FORTH_HOUSE_REL)

        if MOON_FIFTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_FIFTH_HOUSE_REL)

        if MOON_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_SEVENTH_HOUSE_REL)
        
        if MOON_ELVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_ELVENTH_HOUSE_REL)
        
        if MOON_TWELFTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MOON_TWELFTH_HOUSE_REL)

        if MERCURY_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MERCURY_SEVENTH_HOUSE_REL)
        
        if MERCURY_ELVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(MERCURY_ELVENTH_HOUSE_REL)

        if VENUS_FIFTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_FIFTH_HOUSE_REL)

        if VENUS_SEVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_SEVENTH_HOUSE_REL)

        if VENUS_EIGHTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_EIGHTH_HOUSE_REL)
        
        if VENUS_ELVENTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_ELVENTH_HOUSE_REL)

        if VENUS_TWELFTH_HOUSE_REL.is_planet_in_house(self.first_person, self.second_person):
            phs.append(VENUS_TWELFTH_HOUSE_REL)

        return phs

    def get_house_has_planets(self):
        phs = []

        if SUN_FIRST_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_FIRST_HOUSE_REL)

        if SUN_FORTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_FORTH_HOUSE_REL)

        if SUN_FIFTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_FIFTH_HOUSE_REL)

        if SUN_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_SEVENTH_HOUSE_REL)

        if SUN_EIGHTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_EIGHTH_HOUSE_REL)

        if SUN_ELEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_ELEVENTH_HOUSE_REL)
        
        if SUN_TWELFTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(SUN_TWELFTH_HOUSE_REL)

        if MOON_FIRST_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_FIRST_HOUSE_REL)
        
        if MOON_FORTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_FORTH_HOUSE_REL)

        if MOON_FIFTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_FIFTH_HOUSE_REL)

        if MOON_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_SEVENTH_HOUSE_REL)
        
        if MOON_ELVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_ELVENTH_HOUSE_REL)
        
        if MOON_TWELFTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MOON_TWELFTH_HOUSE_REL)

        if MERCURY_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MERCURY_SEVENTH_HOUSE_REL)
        
        if MERCURY_ELVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(MERCURY_ELVENTH_HOUSE_REL)

        if VENUS_FIFTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_FIFTH_HOUSE_REL)

        if VENUS_SEVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_SEVENTH_HOUSE_REL)

        if VENUS_EIGHTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_EIGHTH_HOUSE_REL)
        
        if VENUS_ELVENTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_ELVENTH_HOUSE_REL)

        if VENUS_TWELFTH_HOUSE_REL.is_house_has_planet(self.first_person, self.second_person):
            phs.append(VENUS_TWELFTH_HOUSE_REL)

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
        report["aspect"]["pos_house_score"] = self.cal_pos_house_score()
        report["aspect"]["neg_house_score"] = self.cal_neg_house_score()
        report["aspect"]["pos_planet_score"] = self.cal_pos_planet_score()
        report["aspect"]["neg_planet_score"] = self.cal_neg_planet_score()
        report["harmony_challenge"] = self.cal_aspect_harmony_challenge()
        report["harmony_challenge"]["house_harmonies"] = self.cal_house_harmony()
        report["harmony_challenge"]["planet_harmonies"] = self.cal_planet_harmony()
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
            "Emotional_Connection": 0,
            "Intellectual_Connection": 0,
            "Interaction": 0,
            "Respect": 0,
            "Sincerity": 0,
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
    
    def cal_pos_house_score(self):
        house_score = 0

        for h in self.house_has_planets:
            for hs in self.house_scores:
                if h == hs["house_has_planet"]:
                    house_score += hs["score"] if hs["score"] > 0 else 0
        
        return house_score
    
    def cal_neg_house_score(self):
        house_score = 0

        for h in self.house_has_planets:
            for hs in self.house_scores:
                if h == hs["house_has_planet"]:
                    house_score += hs["score"] if hs["score"] < 0 else 0
        
        return house_score

    def cal_house_harmony(self):
        harmonies = {}
        challenges = {}
        compas = {
            "Commitment": 0,
            "Communication": 0,
            "Emotional": 0,
            "Intellectual": 0,
            "Lifestyle": 0,
            "Physical": 0,
        }
        incompas = compas.copy()

        for h in self.house_has_planets:
            for hh in self.house_harmony:
                if h == hh["house_has_planet"]:
                    if hh["harmony"] != "":
                        harmonies[hh["harmony"]] = harmonies.get(hh["harmony"], 0) + 1
                    if hh["compa"] != "":
                        compas[hh["compa"]] = compas.get(hh["compa"], 0) + 1
                    if hh["challenge"] != "":
                        challenges[hh["challenge"]] = challenges.get(hh["challenge"], 0) + 1
                    if hh["incompa"] != "":
                        incompas[hh["incompa"]] = incompas.get(hh["incompa"], 0) + 1
        
        return {
            "harmonies": harmonies,
            "compas": compas,
            "challenges": challenges,
            "incompas": incompas
        }

    def cal_planet_score(self):
        planet_score = 0

        for p in self.planet_in_houses:
            for ps in self.planet_scores:
                if p == ps["planet_in_house"]:
                    planet_score += ps["score"]
        
        return planet_score
    
    def cal_pos_planet_score(self):
        planet_score = 0

        for p in self.planet_in_houses:
            for ps in self.planet_scores:
                if p == ps["planet_in_house"]:
                    planet_score += ps["score"] if ps["score"] > 0 else 0
        
        return planet_score

    def cal_neg_planet_score(self):
        planet_score = 0

        for p in self.planet_in_houses:
            for ps in self.planet_scores:
                if p == ps["planet_in_house"]:
                    planet_score += ps["score"] if ps["score"] < 0 else 0
        
        return planet_score

    def cal_planet_harmony(self):
        harmonies = {}
        challenges = {}
        compas = {
            "Commitment": 0,
            "Communication": 0,
            "Emotional": 0,
            "Intellectual": 0,
            "Lifestyle": 0,
            "Physical": 0,
        }

        incompas = compas.copy()

        for p in self.planet_in_houses:
            for ph in self.planet_harmony:
                if p == ph["planet_in_house"]:
                    if ph["harmony"] != "":
                        harmonies[ph["harmony"]] = harmonies.get(ph["harmony"], 0) + 1
                    if ph["compa"] != "":
                        compas[ph["compa"]] = compas.get(ph["compa"], 0) + 1
                    if ph["challenge"] != "":
                        challenges[ph["challenge"]] = challenges.get(ph["challenge"], 0) + 1
                    if ph["incompa"] != "":
                        incompas[ph["incompa"]] = incompas.get(ph["incompa"], 0) + 1
        
        return {
            "harmonies": harmonies,
            "compas": compas,
            "challenges": challenges,
            "incompas": incompas
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
                    "challenge": row["Challenges Keyword"],
                    "incompa": row["Incompatibility Category"],
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
                    "challenge": row["Challenges Keyword"],
                    "incompa": row["Incompatibility Category"],
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
        
        for key, value in aspect_data["aspect_challenges"].items():
            if key in house_data["challenges"].keys():
                value += house_data["challenges"][key]
            
            if key in planet_data["challenges"].keys():
                value += planet_data["challenges"][key]

            aspect_data["aspect_challenges"][key] = value
        
        for key, value in aspect_data["aspect_compas"].items():
            if key in house_data["compas"].keys():
                value += house_data["compas"][key]
            
            if key in planet_data["compas"].keys():
                value += planet_data["compas"][key]

            aspect_data["aspect_compas"][key] = value
        
        for key, value in aspect_data["aspect_incompas"].items():
            if key in house_data["incompas"].keys():
                value += house_data["incompas"][key]
            
            if key in planet_data["incompas"].keys():
                value += planet_data["incompas"][key]

            aspect_data["aspect_incompas"][key] = value


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
            + self.cal_pos_house_score() + self.cal_pos_planet_score()

        neg_score = num_score_types[-1] \
            + num_score_types[-2] * 2   \
            + num_score_types[-3] * 3   \
            + num_score_types[-4] * 4   \
            - self.cal_neg_house_score() - self.cal_neg_planet_score()
        neg_score = -neg_score

        result = 0
        if   pos_score <= POS_LV_1  and neg_score <= NEG_LV_1:     result = 1
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_2:     result = 2
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_3:     result = 9
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_4:     result = 18
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_5:     result = 19
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_6:     result = 23
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_7:     result = 34
        elif pos_score <= POS_LV_1  and neg_score <= NEG_LV_8:     result = 40
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
        elif pos_score <= POS_LV_3  and neg_score <= NEG_LV_6:     result = 39
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

        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_1:    result = 30
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_2:    result = 55
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_3:    result = 64
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_4:    result = 70
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_5:    result = 83
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_6:    result = 86
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_7:    result = 91
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_8:    result = 95
        elif pos_score >= POS_LV_10  and neg_score <= NEG_LV_9:    result = 98
        elif pos_score >= POS_LV_10  and neg_score >  NEG_LV_9:    result = 100

        refined_result = result         \
            + num_score_types[4] * 0    \
            - num_score_types[-4] * 5   \
            + num_score_types[3] * 0    \
            - num_score_types[-3] * 0

        return (pos_score, neg_score, round(result / 100, 2), round(refined_result / 100, 2))










    