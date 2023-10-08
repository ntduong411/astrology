from kerykeion import AstrologicalSubject, KerykeionChartSVG
import csv
from pprint import pprint
from utils import *
from destiny import *

import logging
logging.getLogger().setLevel(logging.ERROR)

results = []


# Read samples
samples = []
with open('../database/samples.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        first = AstrologicalSubject(row["name_1"], int(row["year_1"]), int(row["month_1"]), int(row["day_1"]), int(row["hour_1"]), int(row["minute_1"]), row["place_1"])
        second = AstrologicalSubject(row["name_2"], int(row["year_2"]), int(row["month_2"]), int(row["day_2"]), int(row["hour_2"]), int(row["minute_2"]), row["place_2"])
        destiny = Destiny(first, second)
        pprint (destiny.report())
        exit()
    
# Exort file
with open('results.csv', mode='w', newline='') as results_file:
    writer = csv.writer(results_file, delimiter=',')
    writer.writerows(results)
