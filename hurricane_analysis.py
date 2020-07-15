from hurricane_database import *

# Codecademy Project: Hurricane Analysis
# Jul 2020
# Agnes Bi

################################################################################
############################# Clean up the input ###############################
################################################################################
# Reformating how the damages (USD($)) data is stored

def update_damages(lst):
    """
    returns a new list of updated damages where the recorded data is converted to float values and the missing data is retained as "Damages not recorded"
    """
    newlst = []
    for entry in lst:
        if entry == 'Damages not recorded':
            newlst.append(entry)
        else:
            value = 0
            if entry[-1] == 'B':
                value = float(entry[:-1]) * 1000000000
            elif entry[-1] == 'M':
                value = float(entry[:-1]) * 1000000
            newlst.append(value)
    return newlst

damages = update_damages(damages)
#print(damages)

################################################################################
# Categorize damages and mortality in scales

def convert_to_damage_scale(lst):
    scales = []
    for i in lst:
        if not i == 'Damages not recorded':
            if not float(i) > 0:
                scales.append('0')
            elif not float(i) > 100000000:
                scales.append('1')
            elif not float(i) > 1000000000:
                scales.append('2')
            elif not float(i) > 10000000000:
                scales.append('3')
            elif not float(i) > 50000000000:
                scales.append('4')
            else:
                scales.append('5')
        else:
            scales.append('Damages not recorded')
    return scales

def convert_to_mortality_scale(lst):
    scales = []
    for i in lst:
        if not i > 0:
            scales.append(0)
        elif not i > 100:
            scales.append(1)
        elif not i > 500:
            scales.append(2)
        elif not i > 1000:
            scales.append(3)
        elif not i > 10000:
            scales.append(4)
        else:
            scales.append(5)
    return scales

damage_in_scales = convert_to_damage_scale(damages)
deaths_in_scales = convert_to_mortality_scale(deaths)

################################################################################
# Construct a dictionary containing all the data

def construct_record(names, months, years, max_sustained_winds, areas_affected, damages, damage_in_scales, deaths, deaths_in_scales):
    """
    returns a dictionary, where
        keys = the names of the hurricanes
        values = dictionaries themselves containing all the information about the hurricane
    """
    records= {}
    for i in range(len(names)):
        records[names[i]] = {}
        alias = records[names[i]]
        alias['Name'] = names[i]
        alias['Month'] = months[i]
        alias['Year'] = years[i]
        alias['Max Sustained Wind'] = max_sustained_winds[i]
        alias['Areas Affected'] = areas_affected[i]
        alias['Damage'] = damages[i]
        alias['Damage Scale'] = damage_in_scales[i]
        alias['Deaths'] = deaths[i]
        alias['Mortality Scale'] = deaths_in_scales[i]
    return records

AtlanticHurricanes = construct_record(names, months, years, max_sustained_winds, areas_affected, damages, damage_in_scales, deaths, deaths_in_scales)

################################################################################
# Construct a dictionary recording how many times the areas are hit by hurricanes

def affected_areas_frequency(records):
    dict = {}
    for hurricane in records.keys():
        regions = records[hurricane]['Areas Affected']
        for region in regions:
            if not region in dict.keys():
                dict[region] = {'Frequency': 1}
            else:
                dict[region]['Frequency'] += 1
    return dict

AffectedRegions = affected_areas_frequency(AtlanticHurricanes)
#print(AffectedRegions)

################################################################################
###################### Abstract information as needed ##########################
################################################################################

class organize_by_attribute(object):
    """
    arg1: a dictionary of hurricane records
    arg2: the attribute to organize the hurricanes by
    """

    def __init__(self, dict, string):
        self.records = dict
        self.attribute = string

    def get_record(self):
        return self.records.copy()

    def get_key_attribute(self):
        return self.attribute

    def sorting(self):
        result = {}
        database = self.get_record()
        keyattr = self.get_key_attribute()
        for hurricane in database.keys():
            info = database[hurricane]
            value = str(info[keyattr])  # converted into string format cause ideally we do not want the keys of a dictionary be of mutable types
            if not value in result.keys():
                result[value] = [info['Name']]
            else:
                result[value].append(info['Name'])
        return result

    def find_highest(self):
        database = self.get_record()
        keyattr = self.get_key_attribute()
        max = 0
        lst = []
        for hurricane in database.keys():
            value = database[hurricane][keyattr]
            if ( not isinstance(value, str) ) and ( value > max ):
                max = value
        for hurricane in database.keys():
            if database[hurricane][keyattr] == max:
                lst.append(hurricane)
        return (lst, max)

################################################################################
########################## Put in practice #####################################
################################################################################

# organize the hurricanes by year
organized_by_year = organize_by_attribute(AtlanticHurricanes, 'Year').sorting()
print("Hurricanes categorized by year: \n", organized_by_year)
print("-" * 25)


# organize the hurricanes by mortality scale
organized_by_mortality = organize_by_attribute(AtlanticHurricanes, 'Mortality Scale').sorting()
print("Hurricanes categorized by mortality scale: \n", organized_by_mortality)
print("-" * 25)


# organize the hurricanes by damage scale
organized_by_damage = organize_by_attribute(AtlanticHurricanes, 'Damage Scale').sorting()
print("Hurricanes categorized by damage scale: \n", organized_by_damage)
print("-" * 25)


# Find a list of the hurricane(s) causing the greatest number of deaths, and the specific number deaths they caused
highest_fatality = organize_by_attribute(AtlanticHurricanes, 'Deaths').find_highest()
print("Highest fatality:", highest_fatality)


# Find a list of the hurricane(s) causing the greatest damage, and how costly they were
greatest_damage = organize_by_attribute(AtlanticHurricanes, 'Damage').find_highest()
print("Greatest damage in US$:", greatest_damage)


# Find a list of the area(s) affected by the most hurricanes, and how often they were hit
highest_freq = organize_by_attribute(AffectedRegions, 'Frequency').find_highest()
print("Most affected area:", highest_freq)
