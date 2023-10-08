from utils import *

class Planet_House_Rel:
    def __init__(self, planet, house):
        self.planet = planet
        self.house = house

        self.adapt_planet()
        self.adapt_house()

    def is_planet_in_house(self, first_person, second_person):
        first_planets = first_person.planets_degrees_ut
        second_houses = second_person.houses_degree_ut

        if self.planet == ASC:
            planet_point = first_person.houses_degree_ut[0]
        else:
            planet_point = first_planets[self.planet]
        house_range = [
            second_houses[divmod(self.house, 12)[1]], 
            second_houses[divmod(self.house + 1, 12)[1]]
        ]
        
        if house_range[1] < house_range[0]:
            return planet_point >= house_range[0] or planet_point <= house_range[1]
        else:
            return house_range[0] <= planet_point <= house_range[1]
    
    def is_house_has_planet(self, first_person, second_person):
        return self.is_planet_in_house(second_person, first_person)

    def adapt_planet(self):
        if isinstance(self.planet, str):
            if self.planet == "Sun": self.planet = SUN
            elif self.planet == "Moon": self.planet = MOON
            elif self.planet == "Mecury": self.planet = MERCURY
            elif self.planet == "Venus": self.planet = VENUS
            elif self.planet == "Mars": self.planet = MARS
            elif self.planet == "Jupiter": self.planet = JUPITER
            elif self.planet == "Saturn": self.planet = SATURN
            elif self.planet == "Uranus": self.planet = URANUS
            elif self.planet == "Neptune": self.planet = NEPTUNE
            elif self.planet == "Pluto": self.planet = PLUTO
            elif self.planet == "Ascendant": self.planet = ASC

    def adapt_house(self):
        if isinstance(self.house, str):
            if self.house == "1st house": self.house = FIRST_HOUSE
            elif self.house == "2nd house": self.house = SECOND_HOUSE
            elif self.house == "3rd house": self.house = THIRD_HOUSE
            elif self.house == "4th house": self.house = FORTH_HOUSE
            elif self.house == "5th house": self.house = FIFTH_HOUSE
            elif self.house == "6th house": self.house = SIXTH_HOUSE
            elif self.house == "7th house": self.house = SEVENTH_HOUSE
            elif self.house == "8th house": self.house = EIGHTH_HOUSE
            elif self.house == "9th house": self.house = NINTH_HOUSE
            elif self.house == "10th house": self.house = TENTH_HOUSE
            elif self.house == "11th house": self.house = ELEVENTH_HOUSE
            elif self.house == "12th house": self.house = TWELFTH_HOUSE

    def __eq__(self, obj):
        return isinstance(obj, Planet_House_Rel)    \
            and self.planet == obj.planet           \
            and self.house == obj.house             \

SUN_FIRST_HOUSE_REL = Planet_House_Rel(SUN, FIRST_HOUSE)
SUN_SEVENTH_HOUSE_REL = Planet_House_Rel(SUN, SEVENTH_HOUSE)
MOON_FIRST_HOUSE_REL = Planet_House_Rel(MOON, FIRST_HOUSE)
MOON_SEVENTH_HOUSE_REL = Planet_House_Rel(MOON, SEVENTH_HOUSE)
VENUS_FIRST_HOUSE_REL = Planet_House_Rel(VENUS, FIRST_HOUSE)
VENUS_SEVENTH_HOUSE_REL = Planet_House_Rel(VENUS, SEVENTH_HOUSE)
JUPITER_SEVENTH_HOUSE_REL = Planet_House_Rel(JUPITER, SEVENTH_HOUSE)
ASC_SEVENTH_HOUSE_REL = Planet_House_Rel(ASC, SEVENTH_HOUSE)