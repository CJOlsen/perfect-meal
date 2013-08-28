## The Perfect Meal
## Author: Christopher Olsen
## Copyright: 2013
## License: GNU GPL v3
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## ************************************************************************

####Levels of The Program (this file):
####	Class Structure (data types)
####		Food(object)  ** moved to baseclasses.py
####		Meal(Food)    ** moved to baseclasses.py
####	
####	Data and Benchmarks (data moved to nutrient_subgroups.py)
####		daily_min, daily_max 
####		various data for the program
####	
####	JSON Considerations
####		Food_Group_Filter
####		Name_Filter
####		open JSON file
####		read in JSON objects (filtered and not)
####		
####	Making Food objects and lists of Food objects
####		(isolates the algorithms from JSON considerations)
####
####	Searching Algorithms (moved to meal_building.py)
####		brute force (to-do)
####		Greedy algorithms
####			based on Comparators (balance returns a "valid" result)
####
####    GUI Specific Methods (interface for perfectmeal_gui.py)
####            get_fields()
####

debugging = False

from baseclasses import Food, Meal
import ackpl # the Arbitrary Constraint Knapsack Problem Library
import json
import re
import os # to find current directory (to find the json database)
import sys # same, used if the os method fails




## Text display options (superceded by GUI capabilities)

def display_nutrients(food, min_meal, max_meal):
    """ Displays the nutritional contents of 3 meals.
        """
    ## you can put any three meals in here and they'll print in order
    ## ideal for food, min_meal, max_meal.  the GUI will do this now, but in
    ## case you want to see it in text...this is here
    print ''
    print 'Food/Meal Object: ', food.name
    for group in food.get_nutrgroups(): # nutrient groupings (elements, vitamins, etc)
        print '-------------------------------------------------------------------'
        print 'Group:', group   #, 'food.d(g):', food.d(g)
        print "%-35s %-10s %-10s %-10s" % ('Name', 'Meal', 'Min', 'Max')
        print '-------------------------------------------------------------------'
        for nutr in food.get_nutrgroup_members(group):
            print "%-35s %-10s %-10s %-10s" % (key,
                                               food.get_val(group, nutr),
                                               min_meal.get_val(group, nutr),
                                               max_meal.get_val(group, nutr))

def display_info(food):
    d_min = make_daily_min(food.get_nutrgroups())
    d_max = make_daily_max(food.get_nutrgroups())
    display_nutrients(food, d_min, d_max)

def info(name):
    food = get_food_with_name(name)
    display_info(food)
    print 'weight:', food.get_servingsize(), 'grams'

#############################################################################
############################ nutritional benchmarks #########################
#############################################################################
# *see nutrient_subgroups.py


def make_daily_min(groupings):
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    json_loc = current_dir + "/database/json/foods-2011-10-03.json"
    jsonfile = open(json_loc, "r")
    pmeal_db = json.load(jsonfile)
    min_vals = pmeal_db['nutritional_profiles']['min_values']
    pass

## ****
## **** This section will be changed to pull the data from perfmeal.json
## **** but unfortunately trying to do so exposed some problems in the 
## **** baseclasses so it's waiting on the Food and Meal refactors
## ****

def make_daily_min(groupings):
    # not complete
    assert type(groupings) == list
    daily_min = Meal(groupings)
    if 'elements' in groupings:
        daily_min.elements['Sodium, Na'] =  (1500. / 3.)
        daily_min.elements['Phosphorus, P'] =  (700. / 3.)
        daily_min.elements['Manganese, Mn'] =  (2.3 / 3.)
        daily_min.elements['Iron, Fe'] =  (8. / 3.)
        daily_min.elements['Potassium, K'] =  (4700. / 3.)
        daily_min.elements['Fluoride, F'] = None #4. having troubles
        daily_min.elements['Selenium, Se'] = None #.055 having troubles...
        daily_min.elements['Magnesium, Mg'] =  (420. / 3.)
        daily_min.elements['Zinc, Zn'] =  (11. / 3.)
        daily_min.elements['Copper, Cu'] =  (.9 / 3.)
        daily_min.elements['Calcium, Ca'] =  (1000. / 3.)
    if 'vitamins' in groupings:
        daily_min.vitamins['Niacin'] =  (16. / 3.)
        daily_min.vitamins['Thiamin'] =  (1.2 / 3.)
        daily_min.vitamins['Vitamin B-6'] = None ## instead of zero?
        daily_min.vitamins['Pantothenic acid'] =  (5. / 3.)
        daily_min.vitamins['Vitamin C, total ascorbic acid'] = (90. / 3.)
        daily_min.vitamins['Vitamin A, IU'] =  (.9 / 3.)
        daily_min.vitamins['Vitamin E (alpha-tocopherol)'] = (15. / 3.)
        daily_min.vitamins['Vitamin D'] =  (.015 / 3.)
        daily_min.vitamins['Folate, total'] =  (.4 / 3.)
        daily_min.vitamins['Vitamin B-12'] =  (.0024 / 3.)
        daily_min.vitamins['Vitamin K (phylloquinone)'] = (.12 / 3.)
    if 'amino_acids' in groupings:
        # assumed to be per 100kg, source for Proof Of Concept from
        # http://en.wikipedia.org/wiki/Essential_amino_acid#Recommended_daily_amounts
        # Methionine+Cysteine and Phenylalanine+Tyrosine were broken up,
        # although they are substitutes for eachother.  These are in a sense
        # dummy values!!!
        daily_min.amino_acids['Lysine'] =  (3000 / 3.)
        daily_min.amino_acids['Phenylalanine'] =  (1250 / 3.)
        daily_min.amino_acids['Leucine'] =  (3900 / 3.)
        daily_min.amino_acids['Methionine'] =  (750 / 3.)
        daily_min.amino_acids['Histidine'] =  (1000 / 3.)
        daily_min.amino_acids['Valine'] =  (2600 / 3.)
        daily_min.amino_acids['Tryptophan'] =  (400 / 3.)
        daily_min.amino_acids['Isoleucine'] =  (2000 / 3.)
        daily_min.amino_acids['Threonine'] =  (1500 / 3.)
        daily_min.amino_acids['Cystine'] =  (750 / 3.)
        daily_min.amino_acids['Tyrosine'] =  (1250 / 3.)
        daily_min.amino_acids['Hydroxyproline'] =  (5 / 3.)
    return daily_min

def make_daily_max(groupings):
    assert type(groupings) == list
    daily_max = Meal(groupings)
    if 'elements' in groupings:
        daily_max.elements['Sodium, Na'] =  (2300. / 3.)
        daily_max.elements['Phosphorus, P'] =  (4000. / 3.)
        daily_max.elements['Manganese, Mn'] =  (211. / 3.)
        daily_max.elements['Iron, Fe'] =  (45. / 3.)
        daily_max.elements['Potassium, K'] = 999999. ## 999999.=no upper limit
        daily_max.elements['Fluoride, F'] = None #10.  having troubles
        daily_max.elements['Selenium, Se'] = None #.4 having troubles, units off?
        daily_max.elements['Magnesium, Mg'] = 999999.
        daily_max.elements['Zinc, Zn'] =  (40. / 3.)
        daily_max.elements['Copper, Cu'] =  (10. / 3.)
        daily_max.elements['Calcium, Ca'] =  (2500. / 3.)
    if 'vitamins' in groupings:
        daily_max.vitamins['Niacin'] =  (35. / 3.)
        daily_max.vitamins['Thiamin'] = 999999. 
        daily_max.vitamins['Vitamin B-6'] =   (100. / 3.)
        daily_max.vitamins['Pantothenic acid'] = 999999.
        daily_max.vitamins['Vitamin C, total ascorbic acid'] = (2000. / 3.)
        daily_max.vitamins['Vitamin A, IU'] =  (3. / 3.)
        daily_max.vitamins['Vitamin E (alpha-tocopherol)'] = (1000. / 3.)
        daily_max.vitamins['Vitamin D'] =  (.05 / 3.)
        daily_max.vitamins['Folate, total'] =  (1. / 3.)
        daily_max.vitamins['Vitamin B-12'] = 999999.
        daily_max.vitamins['Vitamin K (phylloquinone)'] = 999999. 
    return daily_max


amino_acid_per_mass = {'Lysine':  (3000 / 3.),
                       'Alanine': None,
                       'Glycine': None,
                       'Proline': None,
                       'Serine': None,
                       'Arginine': None,
                       'Glutamic acid': None,
                       'Phenylalanine':  (1250 / 3.),
                       'Leucine':  (3900 / 3.),
                       'Methionine':  (750 / 3.),
                       'Histidine':  (1000 / 3.),
                       'Valine':  (2600 / 3.),
                       'Tryptophan':  (400 / 3.),
                       'Isoleucine':  (2000 / 3.),
                       'Threonine':  (1500 / 3.),
                       'Aspartic acid': None,
                       'Cystine':  (750 / 3.),
                       'Tyrosine':  (1250 / 3.)}

def add_amino_acids_to_min(daily_min, body_weight):
    # body_weight is assumed to be in kilograms
                              ##**** this is gettinng factored out anyway
    for element in daily_min.amino_acids:
        daily_min.amino_acids[element] = amino_acid_per_mass[element] * \
                                         (body_weight / 100)
    return daily_min
    
def add_amino_acids_to_max(daily_max, body_weight):
    # no max info at this time
    pass
    

#############################################################################
########################### JSON considerations #############################
#############################################################################

## JSON (list)
##  -objects (dictionary)
##      -'portions' (key)
##          -list
##              -'amount' (key)
##              -'grams' (key)
##              -'units' (key)
##      -'description' (key)
##          string value (value)
##      -'tags' (key)
##          bunch of random stuff, *could* be useful for search? (list)
##      -'nutrients'
##          * see nutrient subgroups
##      -'group' (key)
##          food group string (value)
##      -'id' (key)
##          integer (value)
##      -'manufacturer' (key)
##          string (68 in total for the entire db) (value)

##
## JSON filters (these filter foods *before* they're mapped into the custom
##               Food objects)

class Food_Group_Filter(object):
    def __init__(self, name_list=None):
        ## to use initialize with a list of some or all of the keys from
        ## the dictionary below
        ## ** this needs to be deprecated or implemented more fully
        self.d = {'Dairy and Egg Products':0, 'Spices and Herbs':0,\
             'Baby Foods':0, 'Fats and Oils':0, 'Poultry Products':0,\
             'Soups, Sauces, and Gravies':0, 'Sausages and Luncheon Meats':0,\
             'Breakfast Cereals':0,'Fruits and Fruit Juices':0,\
             'Pork Products':0, 'Vegetables and Vegetable Products':0,\
             'Nut and Seed Products':0,'Beef Products':0, 'Beverages':0,\
             'Finfish and Shellfish Products':0,\
             'Legumes and Legume Products':0, 'Lamb, Veal, and Game Products':0,\
             'Baked Products':0, 'Snacks':0, 'Sweets':0,
             'Cereal Grains and Pasta':0,'Fast Foods':0,\
             'Meals, Entrees, and Sidedishes':0, 'Ethnic Foods':0,\
             'Restaurant Foods':0}
        if name_list is not None:
            for name in name_list:
                self.d[name] = 1
        else:
            # default to all groups included if no groups supplied
            for k in self.d:
                self.d[k] = 1
    def check(self, group):
        if self.d[group] == 1:
            return True
        else:
            return False
    def get_groups(self):
        return [x for x in self.d if self.d[x] == 1]

class Name_Filter(object):
    def __init__(self, name_list=None):
        if name_list is not None:
            self.n = name_list
        else:
            self.n = []
    def check(self, name):
        # if no names supplies filter defaults to True
        if self.n == []:
            return True
        elif name in self.n:
            return True
        else:
            return False


## 1441 objects skipped, but from the rest the groups were:
## will need to investigate those 1441 objects (ascii errors? i.e. 2% milk)
the_groups = ['Dairy and Egg Products', 'Spices and Herbs', 'Baby Foods',\
              'Fats and Oils', 'Poultry Products', 'Soups, Sauces, and Gravies',\
              'Sausages and Luncheon Meats', 'Breakfast Cereals',\
              'Fruits and Fruit Juices', 'Pork Products',\
              'Vegetables and Vegetable Products', 'Nut and Seed Products',\
              'Beef Products', 'Beverages', 'Finfish and Shellfish Products',\
              'Legumes and Legume Products', 'Lamb, Veal, and Game Products',\
              'Baked Products', 'Snacks', 'Sweets', 'Cereal Grains and Pasta',\
              'Fast Foods', 'Meals, Entrees, and Sidedishes', 'Ethnic Foods',\
              'Restaurant Foods']


def get_food_from_group_by_name(group_filter, name):
    """ Given a name and a filter of the group that name is in, returns the
        single corresponding object.
        """
    ## this should be optimized later (should terminate when object is found)
    assert type(group_filter) is Food_Group_Filter and type(name) is str
    return get_foods_by_group_and_name(group_filter, Name_Filter([name]))[0]


##
## JSON data
## 



try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
except:
    current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

json_loc = current_dir + "/database/json/foods-2011-10-03.json"
jsonfile = open(json_loc, "r")

## json needs to be loaded using multithreading/multiprocessing so it doesn't
## hold up the entire program.  The multithreading approach is being
## experimented with bnut my computer only has one processor so I can't run
## and debug the multithreaded solution

db_tuple = tuple(json.load(jsonfile)) # tuple to prevent mutation


## database in pieces, separated by food group
def make_database_by_foodgroup(full_db):
    """ Create a dictionary from the json database where the keys are food
        groups and the values are lists of their members.

        Useful for searching through part of the database.
        """
    food_groups = ['Dairy and Egg Products', 'Spices and Herbs', 'Baby Foods',\
                  'Fats and Oils', 'Poultry Products', 'Soups, Sauces, and Gravies',\
                  'Sausages and Luncheon Meats', 'Breakfast Cereals',\
                  'Fruits and Fruit Juices', 'Pork Products',\
                  'Vegetables and Vegetable Products', 'Nut and Seed Products',\
                  'Beef Products', 'Beverages', 'Finfish and Shellfish Products',\
                  'Legumes and Legume Products', 'Lamb, Veal, and Game Products',\
                  'Baked Products', 'Snacks', 'Sweets', 'Cereal Grains and Pasta',\
                  'Fast Foods', 'Meals, Entrees, and Sidedishes', 'Ethnic Foods',\
                  'Restaurant Foods']
    data_dict = {x:[] for x in food_groups}
    for item in full_db:
        data_dict[item['group']].append(item)
    return data_dict

db_by_foodgroup = make_database_by_foodgroup(db_tuple)

def get_partial_db(food_groups):
    total = []
    for key in food_groups:
        total += db_by_foodgroup[key]
    return total

########################################

def get_objects_by_group_and_name(food_group_filter, name_filter):
    """ Steps through the JSON database and keeps objects that satisfy the
        group and name filters' constraints.
        """
    ## TODO: fix this to work with get_partial_db()

    print ''
    print 'food_group_filter and name_filter', food_group_filter, name_filter
    print ''
    assert type(food_group_filter) is Food_Group_Filter
    # and type(name_filter) is Name_Filter
    objects = []

    partial = get_partial_db(food_group_filter.get_groups())
    
    for jdict in partial:
        if food_group_filter.check(jdict['group']) and\
           name_filter.check(jdict['description']):
            objects.append(jdict)
    return objects

def get_object_by_name(name):
    """ Steps through the JSON database and returns the first object that meets
        the name criteria.
        """
    for jdict in db_tuple:
        if name == jdict['description']:
            return jdict
    return False

def search_by_name(word, food_groups):
    matches = []
    # db_tuple is the 'global' database, (not mutated so not declared)
    partial_db = get_partial_db(food_groups)
    for jdict in partial_db:
        if re.search(word.lower(),
                     jdict['description'].lower()) is not None:
            matches.append(jdict['description'])
    return matches

def search_many(word_list, food_groups):
    # a fairly naive multiple term search algorithm (term grouping is not incl.)
    # counts the matches for each description, must match at least all but one
    # term in the word list
    partial_db = get_partial_db(food_groups)
    matches = {}
    for jdict in partial_db: # partial_db is the database, jdict is a json object
        for word in word_list:
            if re.search(word.lower(),
                      jdict['description'].lower()) is not None:
                if jdict['description'] not in matches.keys():
                    matches[jdict['description']] = 1
                else:
                    matches[jdict['description']] += 1
    intermediate = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    return [x[0]
            for x
            in intermediate
            if x[1] >= len(word_list) - 1
            and x[1] > 1]
            
 


#############################################################################
######################## From JSON to Food objects ##########################
#############################################################################

def get_food_objects(food_group_filter=Food_Group_Filter(),
                     name_filter=Name_Filter(),
                     nutrient_group_filter=['elements', 'vitamins']):
    """ Given group, name and nutrient group filters, finds corresponding
        objects from the JSON database and maps them into Food objects,
        returns a list of Food objects.
        """
    print 'get_food_objects, type(name_filter', type(name_filter)
    obj_list = get_objects_by_group_and_name(food_group_filter, name_filter)
    return [Food(nutrient_group_filter, obj) for obj in obj_list]

def get_foods_for_objects(objects, nutrient_groups=['vitamins', 'elements',
                                                    'amino_acids']):
    return [Food(nutrient_groups, obj) for obj in objects]

def get_food_with_name(food_name, nutrient_groups=None):
    ######## rewrite
    if nutrient_groups == None:
        nutrient_groups = ['elements', 'vitamins', 'amino_acids']
    the_object = get_object_by_name(food_name)
    if the_object is not False:
        return Food(nutrient_groups, the_object)
    else:
        return False


#############################################################################
############################## GUI Specific #################################
#############################################################################

## all GUI communication with what's above thie line takes place below this line
## (except for methods included in Meal and Food objects)

def get_fields(nutritional_groupings=['elements', 'vitamins', 'energy',
                                      'sugars', 'amino_acids', 'other',
                                      'composition']):
    print 'get_fields groupings:', nutritional_groupings
    food = Food(nutritional_groupings)
    fields = dict()
    for group in food.get_nutrgroups():
        fields[group] = food.__dict__[group].keys()
        fields[group] = food.get_nutrgroup_members()
    return fields

def get_fields_for_group(group):
    food = Food([group])
    fields = food.get_nutrgroup_members(group)
    return fields

def get_food(name, groupings=['elements', 'vitamins', 'energy', 'sugars',
                              'amino_acids', 'other', 'composition']):
    """ Takes a food name (string) and returns the corresponding Food object.
        """
    return get_food_with_name(name, groupings)

def get_meal(name_list, groupings=['elements', 'vitamins', 'energy',
                                      'sugars', 'amino_acids', 'other',
                                      'composition']):
    """ Takes a list of food names (strings) and returns a Meal object of
        those foods.
        """
    meal = Meal(groupings)
    for name in name_list:
        food = get_food_with_name(name)
        meal.add(food)
    return meal

def get_benchmarks(nutritional_groupings=['elements', 'vitamins', 'energy',
                                      'sugars', 'amino_acids', 'other',
                                      'composition']):
    """ Returns a two-tuple of the minimum and maximum daily allowances
        """
    return (make_daily_min(nutritional_groupings),
            make_daily_max(nutritional_groupings))
    
def search_like(search_string, food_groups):
    assert type(search_string) is unicode or type(search_string) is str
    assert type(food_groups) is list
    search_list = search_string.split(' ')
    if len(search_list) == 1:
        return search_by_name(search_string, food_groups)
    else:
        return search_many(search_list, food_groups)
    
def get_available_algs():
    """ Go-between for the GUI and ackpl """
    # this exists so perfectmeal_gui doesn't need to directy access ackpl.py
    return ackpl.algorithm_names()

def complete_meal(current_meal, min_meal, max_meal, algorithm, food_groups):
    """ Acts as a go-between for the GUI and ackpl.py
        Returns a "completed" meal, completed either because it violated a max
        constraint or because it satisfied all of its min constraints.
        """
    ## should this Name_Filter class be derprecated or just renamed?
    all_foods = get_food_objects(food_group_filter=Food_Group_Filter(food_groups),
                                 name_filter=Name_Filter(),
                                 nutrient_group_filter=current_meal.get_nutrgroups())
    possibilities = []
    serving_sizes = {}
    for food in all_foods:
        serving_sizes[food.get_name()] = food.get_servingsize()
        possibilities.append([food.get_name(), food.flatten()])
    minimums = ('minimums', min_meal.flatten())
    maximums = ('maximums', max_meal.flatten())
    currents = [[food.get_name(), food.flatten()]
                for food
                in current_meal.get_foods()]
    #algorithm = algorithm

    completed_flat = ackpl.ackp(possibilities, minimums, maximums, currents, 
                                algorithm)
    if completed_flat is None:
        return None
    if type(completed_flat) is not list:
        return completed_flat ## maybe?
    foods = []
    for food in completed_flat:
        new_food = Food.unflatten(food[1], food[0])
        new_food.set_servingsize(serving_sizes[new_food.get_name()])
        foods.append(new_food)
    print 'number foods', len(foods)
    new_meal = Meal(foods[0].get_nutrgroups(), foods)
    return new_meal

def get_all_foodgroups():
    # pulling from a global?  this could be better...
    return the_groups

