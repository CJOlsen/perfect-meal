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
####		Food(object)
####		Meal(Food)
####	
####	Data and Benchmarks
####		daily_min, daily_max 
####		various data for the program
####	
####	JSON Considerations (pseudo JSON, really)
####		Food_Group_Filter
####		Name_Filter
####		open JSON file
####		read in JSON objects (filtered and not)
####		
####	Making Food objects and lists of Food objects
####		(isolates the algorithms from JSON considerations)
####
####	Searching Algorithms
####		brute force (to-do)
####		Greedy algorithms
####			based on Comparators (balance returns a "valid" result)
####
####    GUI Specific Methods
####            get_fields()
####

#############################################################################
##################### class structure (data types) ##########################
#############################################################################

debugging = False

import copy
import string

class Food(object):
    def __init__(self, nutritional_groupings, json_obj=None, name=None):
        """ The Food object has standard attributes for:
            -name: name of the food, optional
            -nutritional_groupings: a subset of ['elements', 'vitamins', 'energy', 'sugars',
                                     'amino_acids', 'other', 'composition']
                       used to choose which dictionaries to initialize
            -the seven dictionaries listed in the nutritional_groupings list
            
            If a json_obj is included the dictionaries will be populated with
            the data (as filtered by the nutritional_groupings list)
            """
        ## For comparisons to work the nutritional_groupings list will need to be the
        ## same for all Foods being used (one *could* add try/excepts to
        ## the "add" method of the Meal class to "fix" this)
        self.name = name
        assert type(nutritional_groupings) is list
        self.nutritional_groupings = nutritional_groupings     
        for i in self.nutritional_groupings:
            assert i in ['elements', 'vitamins', 'energy', 'sugars',
                         'amino_acids', 'other', 'composition']
        if 'elements' in self.nutritional_groupings:
            self.elements = {'Sodium, Na': None, 'Phosphorus, P': None,
                              'Manganese, Mn': None, 'Iron, Fe': None,
                              'Potassium, K': None, 'Fluoride, F': None,
                              'Selenium, Se': None, 'Magnesium, Mg': None,
                              'Zinc, Zn': None, 'Copper, Cu': None,
                              'Calcium, Ca': None}
        if 'vitamins' in self.nutritional_groupings:
            self.vitamins = {'Niacin': None, 'Menaquinone-4': None, 'Thiamin': None,
                             'Folate, food': None, 'Vitamin B-6': None,
                             'Tocopherol, gamma': None, 'Carotene, beta': None,
                             'Pantothenic acid': None, 'Vitamin E, added': None,
                             'Tocopherol, beta': None,
                             'Vitamin C, total ascorbic acid': None,
                             'Tocopherol, delta': None, 'Cryptoxanthin, beta': None,
                             'Vitamin D3 (cholecalciferol)': None, 'Lycopene': None,
                             'Vitamin B-12, added': None, 'Vitamin A, IU': None,
                             'Retinol': None, 'Vitamin A, RAE': None,
                             'Dihydrophylloquinone': None,
                             'Vitamin E (alpha-tocopherol)': None,
                             'Lutein + zeaxanthin': None, 'Betaine': None,
                             'Riboflavin': None, 'Vitamin D': None,
                             'Vitamin D2 (ergocalciferol)': None,
                             'Carotene, alpha': None, 'Folic acid': None,
                             'Folate, total': None, 'Vitamin B-12': None,
                             'Choline, total': None,
                             'Vitamin K (phylloquinone)': None,
                             'Vitamin D (D2 + D3)': None, 'Folate, DFE': None}
        if 'energy' in self.nutritional_groupings:
            self.energy = {'Energy': None}
        if 'sugars' in self.nutritional_groupings:
            self.sugars = {'Galactose': None, 'Starch': None, 'Lactose': None,
                           'Sucrose': None, 'Maltose': None, 'Fructose': None,
                           'Glucose (dextrose)': None}
        if 'amino_acids' in self.nutritional_groupings:
            self.amino_acids = {'Lysine': None, 'Alanine': None,
                                'Glycine': None, 'Proline': None, 'Serine': None,
                                'Arginine': None, 'Glutamic acid': None,
                                'Phenylalanine': None, 'Leucine': None,
                                'Methionine': None, 'Histidine': None,
                                'Valine': None, 'Tryptophan': None,
                                'Isoleucine': None, 'Threonine': None,
                                'Aspartic acid': None, 'Cystine': None,
                                'Tyrosine': None}
        if 'other' in self.nutritional_groupings:
            self.other = {'Alcohol, ethyl': None, 'Stigmasterol': None,
                          'Fatty acids, total trans-monoenoic': None,
                          'Theobromine': None, 'Caffeine': None,
                          'Fatty acids, total trans': None,
                          'Fatty acids, total monounsaturated': None,
                          'Beta-sitosterol': None,
                          'Fatty acids, total saturated': None,
                          'Fatty acids, total trans-polyenoic': None,
                          'Campesterol': None, 'Cholesterol': None, 'Ash': None,
                          'Fatty acids, total polyunsaturated': None,
                          'Phytosterols': None}
        if 'composition' in self.nutritional_groupings:
            self.composition = {'Fiber, total dietary': None,
                                'Adjusted Protein': None, 'Water': None,
                                'Total lipid (fat)': None, 'Protein': None,
                                'Carbohydrate, by difference': None,
                                'Sugars, total': None}
        if json_obj is not None:
            self.populate_from_json(json_obj)
    def _portion_helper(self, json_object):
        """ Takes a json_object, writes the smallest serving size (in grams)
            and unit of measurement to memory.
            Returns nothing.
            """
        portions = sorted(json_object['portions'], key=lambda k: k['grams'])
        if len(portions) == 0:
            self.unit = "100g"
            self.serving_size = 100
        else:
            smallest = portions[0]
            self.unit = smallest['unit']
            self.serving_size = smallest['grams']
    def populate_from_json(self, json_object):
        ## **** THIS IS AT LIKE 40% FUNCTIONALITY ****
        ##
        ## ALL VALUES COMING IN FROM JSON ARE PER 100g SO THEY MUST BE SCALED
        ## TO THE SERVING SIZE *AFTER* BEING CONVERTED TO MG!!!
        """ This takes a json_object and populates the active groups from it
            """
        assert type(json_object) is dict
        self.name = json_object['description']
        self._portion_helper(json_object)
        serv_size_conv_fact = self.serving_size/100. # json data is per 100g
        converter = {'g':1000., 'mg': 1., 'mcg': (1/1000.)} # normalize to mg
        serving_size = json_object['portions']
        
        for nutr_group in self.nutritional_groupings:
            for nutrient in json_object['nutrients']:
                if nutrient['group'] == nutr_group.capitalize() and\
                   nutrient['units'] in ['g','mg', 'mcg']:
                    new_value = nutrient['value'] * converter[nutrient['units']]* \
                                serv_size_conv_fact
                    self.__dict__[nutr_group][nutrient['description']] = new_value
                else:
                    if nutr_group == "amino_acids" and\
                       nutrient['units'] in ['g','mg', 'mcg']:
                        new_value = nutrient['value'] * converter[nutrient['units']]* \
                                    serv_size_conv_fact
                        self.__dict__["amino_acids"][nutrient['description']] = new_value
                
        ## may need a lookup table for IU to mg conversion for different
        ## vitamins and elements
        ## measurements not in g, mg or mcg are being ignored!!!
                    
    def d(self, string):
        ## d is for dictionary
        ## this gets the __dict__'s out of the algorithm layer
        return self.__dict__[string]
    def display(self):
        print ''
        print 'Food Name:'
        print self.name
        print ''
        print 'Nutritional Groupings: '
        print self.nutritional_groupings
        print ''
    def display_value(self, name):
        for group in self.nutritional_groupings:
            for item_name in self.__dict__[group]:
                if item_name == name:
                    print "Name:", name, " Value: ", self.__dict__[group][name]
    def get_val(self, group, item):
        return self.__dict__[group][item]
    def get_name(self):
        return self.name
    def set_name(self, name):
        assert type(name) is str
        self.name = name
    def get_element(name):
        return self.elements[name]
    def get_vitamin(name):
        return self.vitamins[name]
    def get_energy(name):
        return self.energy[name]
    def get_sugar(name):
        return self.sugars[name]
    def get_amino_acid(name):
        return self.amino_acids[name]
    def get_other(name):
        return self.others[name]
    def get_composition(name):
        return self.composition[name]
       
class Meal(Food):
    ## identical to the Food superclass with the addition of combination
    ## and comparison methods, and a self.foods attribute to keep a list of
    ## foods contained in the meal
    ## self.foods is optional since benchmark meals (daily min and max, etc)
    ## are also of this class
    def __init__(self, nutritional_groupings, food=None):
        Food.__init__(self, nutritional_groupings)
        self.foods = []
        if food is not None:
            self.add(food)
    def _add_helper(self, first, second):
        # needed to deal with the default None's
        # used by add (only)
        if second is None:
            if first is None:
                return None
            else:
                return first
        elif first is None:
            return second
        else:
            return first + second
    def add(self, food):
        ## this can be looped using __dict__'s but it isn't very clear
        ## variable name "food" is unclear, maybe change
        self.foods.append(food) ## (!) now keeping the entire food object (!)
        if 'elements' in self.nutritional_groupings:
            for key in self.elements:
                self.elements[key] = self._add_helper(self.elements[key],
                                                     food.elements[key])
        if 'vitamins' in self.nutritional_groupings:
            for key in self.vitamins:
                self.vitamins[key] = self._add_helper(self.vitamins[key],
                                                     food.vitamins[key])
        if 'energy' in self.nutritional_groupings:
            for key in self.energy:
                self.energy[key] = self._add_helper(self.energy[key],
                                                   food.energy[key])
        if 'sugars' in self.nutritional_groupings:
            for key in self.sugars:
                self.sugars[key] = self._add_helper(self.sugars[key],
                                                   food.sugars[key])
        if 'amino_acids' in self.nutritional_groupings:
            for key in self.amino_acids:
                self.amino_acids[key] = self._add_helper(self.amino_acids[key],
                                                        food.amino_acids[key])
        if 'other' in self.nutritional_groupings:
            for key in self.other:
                self.other[key] = self._add_helper(self.other[key],
                                                  food.other[key])
        if 'composition' in self.nutritional_groupings:
            for key in self.composition:
                self.composition[key] = self._add_helper(self.composition[key],
                                                         food.composition[key])
    def with_(self, food):
        """ with_ is a non-mutating version of add that returns a new Meal
            object.  The underscore avoids conflicts with the "with" built-in.
            """
        new_obj = copy.deepcopy(self)
        new_obj.add(food)
        return new_obj

    def _subtract_helper(self, first, second):
        # needed to deal with all the default None's floating around
        # used by _sub_diff_helper (only)
        if first is None:
            if second is None:
                return None
            else:
                return 0 - second
        else:
            if second is None:
                return first
            else:
                if first - second > .000000001:
                    return first - second
                else:
                    return 0
    def _sub_diff_helper(self, food):
        # used by the subtract() and difference() methods
        if 'elements' in self.nutritional_groupings:
            for key in self.elements:
               self.elements[key] = self._subtract_helper(self.elements[key],
                                                          food.elements[key])
        if 'vitamins' in self.nutritional_groupings:
            for key in self.vitamins:
               self.vitamins[key] = self._subtract_helper(self.vitamins[key],
                                                          food.vitamins[key])
        if 'energy' in self.nutritional_groupings:
            for key in self.energy:
               self.energy[key] = self._subtract_helper(self.energy[key],
                                                        food.energy[key])
        if 'sugars' in self.nutritional_groupings:
            for key in self.sugars:
               self.sugars[key] = self._subtract_helper(self.sugars[key],
                                                        food.sugars[key])
        if 'amino_acids' in self.nutritional_groupings:
            for key in self.amino_acids:
               self.amino_acids[key] = self._subtract_helper(self.amino_acids[key],
                                                             food.amino_acids[key])
        if 'other' in self.nutritional_groupings:
            for key in self.other:
               self.other[key] = self._subtract_helper(self.other[key],
                                                       food.other[key])
        if 'composition' in self.nutritional_groupings:
            for key in self.composition:
               self.composition[key] = self._subtract_helper(self.composition[key],
                                                             food.composition[key])
    def subtract(self, food_name):
        """ Subtracts a food and its nutrients from the current meal.
            Unlike "difference()" this method causes data mutatation
            """
        assert food_name in [f.name for f in self.foods]
        for food in self.foods:
            if food.get_name() == food_name:
                self._sub_diff_helper(food)
                self.foods.remove(food)
                break
    
    def difference(self, food):
        """ Returns a Meal object that represents the DIFFERENCE between
            the meal (self) and another meal, which may just be a benchmark.
            """
        diff = copy.deepcopy(self)
        diff._sub_diff_helper(food)
        diff.foods = None # because this list is meaningless now 
        return diff
    def greater_than(self, food):
        """ Compares this meal to another meal, returns True iff every nutrient
            in this meal is greater than (or wins by default against) every
            nutrient in the meal passed in as an argument.

            In other words, the inputted meal must have at least one nutrient
            in its dictionaries with a value greater than this meal to return
            False.
            """
        assert type(food) in [Food, Meal]
        assert sorted(self.nutritional_groupings) == \
               sorted(food.nutritional_groupings)
        ## this also could use a looping construct
        ## --check for logic error possibilities with None's--
        if 'elements' in self.nutritional_groupings:
            for key in self.elements:
                if self.elements[key] < food.elements[key]:
                    if self.elements[key] is not None and\
                       food.elements[key] is not None: ## throw out None's
                        return False
        if 'vitamins' in self.nutritional_groupings:
            for key in self.vitamins:
                if self.vitamins[key] < food.vitamins[key]:
                    if self.vitamins[key] is not None and\
                       food.vitamins[key] is not None:
                        return False
        if 'energy' in self.nutritional_groupings:
            for key in self.energy:
                if self.energy[key] < food.energy[key]:
                    return False
        if 'sugars' in self.nutritional_groupings:
            for key in self.sugars:
                if self.sugars[key] < food.sugars[key]:
                    return False
        if 'amino_acids' in self.nutritional_groupings:
            for key in self.amino_acids:
                if self.elements[key] < food.elements[key]:
                    return False
        if 'other' in self.nutritional_groupings:
            for key in self.other:
                if self.other[key] < food.other[key]:
                    return False
        return True
    def display_foods(self):
        if self.foods == []:
            return False
        print ''
        print 'Component Foods'
        print '-------------------------------------------------------------------------------'
        print "%-60s %15s" % ('Food Name', 'No. Servings')
        print '-------------------------------------------------------------------------------'
        for member in set(self.foods):
            if len(member) < 60:
                print "%-60s %15s" % (member,
                                      str(self.foods.count(member)).ljust(8))
            if len(member) > 59:
                print "%-60s %15s" % ((member[:57]+"..."),
                                      str(self.foods.count(member)).ljust(8))
        print '-------------------------------------------------------------------------------'
    def get_foods(self):
        return [food.get_name() for food in self.foods]

    def get_food_by_name(self, name):
        for food in self.foods:
            if food.get_name(name) == name:
                return food
        return False

def test_subtract():
    pass

def display_nutrients(food, min_meal, max_meal):
    """ Displays the nutritional contents of 3 meals.
        """
    ## you can put any three meals in here and they'll print in order
    #print 'display nutrients method: food:', food
    print ''
    print 'Food/Meal Object: ', food.name
    for g in food.nutritional_groupings: # nutrient groupings (elements, vitamins, etc)
        print '-------------------------------------------------------------------'
        print 'Group:', g   #, 'food.d(g):', food.d(g)
        print "%-35s %-10s %-10s %-10s" % ('Name', 'Meal', 'Min', 'Max')
        print '-------------------------------------------------------------------'
        for key in food.d(g):
            print "%-35s %-10s %-10s %-10s" % (key,
                                               food.d(g)[key],
                                               min_meal.d(g)[key],
                                               max_meal.d(g)[key])

def display_info(food):
    d_min = make_daily_min(food.nutritional_groupings)
    d_max = make_daily_max(food.nutritional_groupings)
    display_nutrients(food, d_min, d_max)

def info(name):
    food = get_food_with_name(name)
    display_info(food)
    print 'weight:', food.serving_size, 'grams'

#############################################################################
################## some data and (nuritional) benchmarks ####################
#############################################################################

#IU_conversions:::: 'Vitamin A':  0.3 mcg retinol, 0.6 mcg beta-carotene

## this isn't being used right now but it's nice to have around
## came from running through the JSON database and saving the results
nutrient_subgroups = {'Elements': set(['Sodium, Na', 'Phosphorus, P',
                                       'Manganese, Mn', 'Iron, Fe',
                                       'Potassium, K', 'Fluoride, F',
                                       'Selenium, Se', 'Magnesium, Mg',
                                       'Zinc, Zn', 'Copper, Cu', 'Calcium, Ca']),
                      'Vitamins': set(['Niacin', 'Menaquinone-4', 'Thiamin',
                                       'Folate, food', 'Vitamin B-6',
                                       'Tocopherol, gamma', 'Carotene, beta',
                                       'Pantothenic acid', 'Vitamin E, added',
                                       'Tocopherol, beta',
                                       'Vitamin C, total ascorbic acid',
                                       'Tocopherol, delta',
                                       'Cryptoxanthin, beta',
                                       'Vitamin D3 (cholecalciferol)',
                                       'Lycopene', 'Vitamin B-12, added',
                                       'Vitamin A, IU', 'Retinol',
                                       'Vitamin A, RAE', 'Dihydrophylloquinone',
                                       'Vitamin E (alpha-tocopherol)',
                                       'Lutein + zeaxanthin', 'Betaine',
                                       'Riboflavin', 'Vitamin D',
                                       'Vitamin D2 (ergocalciferol)',
                                       'Carotene, alpha', 'Folic acid',
                                       'Folate, total', 'Vitamin B-12',
                                       'Choline, total',
                                       'Vitamin K (phylloquinone)',
                                       'Vitamin D (D2 + D3)', 'Folate, DFE']),
                      'Energy': set(['Energy']),
                      'Sugars': set(['Galactose', 'Starch', 'Lactose', 'Sucrose',
                                     'Maltose', 'Fructose', 'Glucose (dextrose)']),
                      'Amino Acids': set(['Lysine', 'Alanine', 'Glycine',
                                          'Proline', 'Serine', 'Arginine',
                                          'Glutamic acid', 'Phenylalanine',
                                          'Leucine', 'Methionine', 'Histidine',
                                          'Valine', 'Tryptophan', 'Isoleucine',
                                          'Threonine', 'Aspartic acid',
                                          'Cystine', 'Tyrosine']),
                      'Other': set(['Alcohol, ethyl', 'Ash', 'Beta-sitosterol',
                                    'Stigmasterol',
                                    'Fatty acids, total trans-monoenoic',
                                    'Theobromine', 'Caffeine',
                                    'Fatty acids, total trans',
                                    'Fatty acids, total trans-polyenoic',
                                    'Fatty acids, total polyunsaturated',
                                    'Fatty acids, total saturated',
                                    'Campesterol', 'Cholesterol',
                                    'Fatty acids, total monounsaturated',
                                    'Phytosterols']),
                      'Composition': set(['Fiber, total dietary',
                                          'Adjusted Protein', 'Water',
                                          'Total lipid (fat)', 'Protein',
                                          'Carbohydrate, by difference',
                                          'Sugars, total'])}

## these are max/min values from the USDA (find link, put it here)
## all values in mg !!!!
## http://www.iom.edu/Global/News%20Announcements/~/media/Files/Activity%20Files/Nutrition/DRIs/DRI_Summary_Listing.pdf
## http://iom.edu/Activities/Nutrition/SummaryDRIs/~~/media/Files/Activity%20Files/Nutrition/DRIs/RDA%20and%20AIs_Vitamin%20and%20Elements.pdf
#
## ******** (are some of these actually in GRAMS????????) ********
##daily_min_content = Nutrients(vitamin_a=.9, vitamin_c=90., vitamin_d=.015,
##                              vitamin_e=15., vitamin_k=.12, thiamin=1.2,
##                              riboflavin=1.3, niacin=16., vitamin_b6=0,
##                              folate=.4, vitamin_b12=.0024, pantothenic_acid=5.,
##                              biotin=30., choline=550., calcium=1000.,
##                              chromium=.035, copper=.9, fluoride=4.,
##                              iodine=.15, iron=8., magnesium=420.,
##                              manganese=2.3, molybdenum=.045, phosphorus=700.,
##                              selenium=.055, zinc=11., potassium=4700.,
##                              sodium=1500., chloride=2300.)
##
##daily_max_content = Nutrients(vitamin_a=3., vitamin_c=2000., vitamin_d=.05,
##                              vitamin_e=1000., vitamin_k=999999, thiamin=999999,
##                              riboflavin=999999, niacin=35., vitamin_b6=100,
##                              folate=1., vitamin_b12=999999, pantothenic_acid=999999,
##                              biotin=999999, choline=3500., calcium=2500.,
##                              chromium=999999, copper=10., fluoride=10,
##                              iodine=1.1, iron=45., magnesium=999999,
##                              manganese=11., molybdenum=2., phosphorus=4000.,
##                              selenium=.4, zinc=40., potassium=999999,
##                              sodium=2300., chloride=3600.)


## Vitamin A IU --> mg  (1000 IU == 300 mcg == .3 mg, 1 IU = 3/10,000 mg)
## the considerations of various Vitamin A measurements is beyond me...
## vitamin E is broken up between 'added' and 'alpha-tocopherol' (why?)
## is Iodine not in the database?  (that can't be...)
## Biotin not in the database?
#
## ******** THIS WILL NEED CLEAN-UP LATER!!!!  FOR NOW 23 VITAMINS AND
## ******** AND MINERALS IS ENOUGH FOR A PROOF OF CONCEPT 
#
## These represent the benchmark meals used to determine if a given meal
## falls within acceptable boundaries.
## ** these keys must match exactly the keys in the JSON databse **

def make_daily_min(groupings):
    # not complete
    assert type(groupings) == list
    daily_min = Meal(groupings)
    if 'elements' in groupings:
        daily_min.elements['Sodium, Na'] = 1500.
        daily_min.elements['Phosphorus, P'] = 700.
        daily_min.elements['Manganese, Mn'] = 2.3
        daily_min.elements['Iron, Fe'] = 8. 
        daily_min.elements['Potassium, K'] = 4700.
        daily_min.elements['Fluoride, F'] = None #4. having troubles
        daily_min.elements['Selenium, Se'] = None #.055 having troubles, units off?
        daily_min.elements['Magnesium, Mg'] = 420.
        daily_min.elements['Zinc, Zn'] = 11.
        daily_min.elements['Copper, Cu'] = .9
        daily_min.elements['Calcium, Ca'] = 1000.
    if 'vitamins' in groupings:
        daily_min.vitamins['Niacin'] = 16.
        daily_min.vitamins['Thiamin'] = 1.2
        daily_min.vitamins['Vitamin B-6'] = None ## instead of zero?
        daily_min.vitamins['Pantothenic acid'] = 5.
        daily_min.vitamins['Vitamin C, total ascorbic acid'] = 90.
        daily_min.vitamins['Vitamin A, IU'] =.9
        daily_min.vitamins['Vitamin E (alpha-tocopherol)'] = 15.
        daily_min.vitamins['Vitamin D'] = .015
        daily_min.vitamins['Folate, total'] = .4 
        daily_min.vitamins['Vitamin B-12'] = .0024
        daily_min.vitamins['Vitamin K (phylloquinone)'] = .12
    return daily_min

def make_daily_max(groupings):
    assert type(groupings) == list
    daily_max = Meal(groupings)
    if 'elements' in groupings:
        daily_max.elements['Sodium, Na'] = 2300.
        daily_max.elements['Phosphorus, P'] = 4000.
        daily_max.elements['Manganese, Mn'] = 211.
        daily_max.elements['Iron, Fe'] = 45.
        daily_max.elements['Potassium, K'] = 999999. ## 999999. means no upper limit
        daily_max.elements['Fluoride, F'] = None #10.  having troubles
        daily_max.elements['Selenium, Se'] = None #.4 having troubles, units off?
        daily_max.elements['Magnesium, Mg'] = 999999.
        daily_max.elements['Zinc, Zn'] = 40.
        daily_max.elements['Copper, Cu'] = 10.
        daily_max.elements['Calcium, Ca'] = 2500.
    if 'vitamins' in groupings:
        daily_max.vitamins['Niacin'] = 35.
        daily_max.vitamins['Thiamin'] = 999999. 
        daily_max.vitamins['Vitamin B-6'] =  100.
        daily_max.vitamins['Pantothenic acid'] = 999999.
        daily_max.vitamins['Vitamin C, total ascorbic acid'] = 2000. 
        daily_max.vitamins['Vitamin A, IU'] = 3.
        daily_max.vitamins['Vitamin E (alpha-tocopherol)'] = 1000.
        daily_max.vitamins['Vitamin D'] = .05
        daily_max.vitamins['Folate, total'] = 1. 
        daily_max.vitamins['Vitamin B-12'] = 999999.
        daily_max.vitamins['Vitamin K (phylloquinone)'] = 999999. 
    return daily_max

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

def get_all_groups():
    """ Gathers the different food groups from the database, only used for
        db exploration, i.e. making the group filter template.
        """
    global db_tuple
    groups = []
    error_count = 0
    for jdict in db_tuple:
        if jdict['group'] not in groups:
            groups.append(jdict['group'])
    if debugging: print error_count, "objects had troubles and were skipped"
    return groups


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

## a filter for groups (0 for discard, 1 for keep):
## ** this is used for filtering JSON objects before they get mapped in **

basic_filter = Food_Group_Filter(['Fats and Oils', 'Soups, Sauces, and Gravies',
                              'Breakfast Cereals', 'Fruits and Fruit Juices',
                              'Vegetables and Vegetable Products',
                              'Nut and Seed Products', 'Beverages',
                              'Legumes and Legume Products', 'Baked Products',
                              'Snacks', 'Sweets', 'Cereal Grains and Pasta',
                              'Meals, Entrees, and Sidedishes'])

all_groups_filter = Food_Group_Filter(the_groups)
        
veggie_filter = Food_Group_Filter(['Vegetables and Vegetable Products',
                              'Nut and Seed Products'])
veggie_beef_filter = Food_Group_Filter(['Vegetables and Vegetable Products',
                                   'Nut and Seed Products',
                                   'Beef Products'])
                                   
# this is a filter to pick a subset of the vegetable group, names are just
# copy/pasted from the output of the get_veggies funtion that output 872 veggies
# many of which are basically the same thing, so this narrows it down a bit
# ** this search could be done marginally more quickly using id's instead of
# descriptions, but descriptions make it so looking at the filter is more easily
# readable
veggie_name_filter = ['Alfalfa seeds, sprouted, raw', 'Amaranth leaves, raw',
                      'Artichokes, (globe or french), raw',
                      'Asparagus, raw', 'Bamboo shoots, raw', 'Beets, raw',
                      'Broccoli, raw', 'Brussels sprouts, raw',
                      'Lentils, sprouted, cooked, stir-fried, without salt',]

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

import json
jsonfile = open("/home/james/GitRepos/perfect_diet/database/json/foods-2011-10-03.json",
                "r")
db_tuple = tuple(json.load(jsonfile)) # tuple to prevent mutation

def get_filtered_object_count(the_filter):
    """ Counts the number of objects that can successfully be retrieved from
        the JSON database as constrained by the_filter
        """
    count = 0
    for jdict in db_tuple:
        if the_filter.check(jdict["group"]):
            count += 1
    return count

def get_filtered_object_names(the_filter):
    """ Gets the names of the objects that can be successfully retrieved from
        the JSON database as constrained by the_filter
        """
    food_names = []
    for jdict in db_tuple:
        if the_filter.check(jdict["group"]):
            food_names.append(jdict["description"])
    return food_names

def get_objects_by_group_and_name(group_filter, name_filter):
    """ Steps through the JSON database and keeps objects that satisfy the
        group and name filters' constraints.
        """
    global db_tuple
    assert type(group_filter) is Food_Group_Filter and \
           type(name_filter) is Name_Filter
    objects = []
    
    for jdict in db_tuple:
        if group_filter.check(jdict['group']) and\
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

import re
def search_by_name(word):
    matches = []
    # db_tuple is the 'global' database, (not mutated so not declared)
    for jdict in db_tuple:
        if re.search(word.lower(),
                      jdict['description'].lower()) is not None:
            matches.append(jdict['description'])
    return matches

def search_many(word_list):
    # a fairly naive multiple term search algorithm (term grouping is not incl.)
    # counts the matches for each description, must match at least all but one
    # term in the word list
    matches = {}
    for jdict in db_tuple: # db_tuple is the database, jdict is a json object
        for word in word_list:
            if re.search(word.lower(),
                      jdict['description'].lower()) is not None:
                if jdict['description'] not in matches.keys():
                    matches[jdict['description']] = 1
                else:
                    matches[jdict['description']] += 1
    intermediate = sorted(matches.items(), key=lambda x: x[1], reverse=True)
    return [x[0] for x in intermediate if x[1] >= len(word_list) - 1
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
    obj_list = get_objects_by_group_and_name(food_group_filter, name_filter)
    return [Food(nutrient_group_filter, obj) for obj in obj_list]

def get_foods_for_objects(objects, nutrient_groups=['vitamins', 'elements']):
    return [Food(nutrient_groups, obj) for obj in objects]

def get_food_with_name(food_name, nutrient_groups=None):
    ######## rewrite
    if nutrient_groups == None:
        nutrient_groups = ['elements', 'vitamins']
    the_object = get_object_by_name(food_name)
    if the_object is not False:
        return Food(nutrient_groups, the_object)
    else:
        return False

#############################################################################
############################### FINDING MEALS ###############################
#############################################################################

def greedy_alg(min_meal, max_meal, servings, food_groups, nutrient_groups,
                   comparator, seed_name, names=None):
        """ 
            min_meal: benchmark Meal object
            max_meal: benchmark Meal object
            servings: integer
            food_groups: list, used to filter from the JSON database
            nutrient_groups: list, used as an argument for Food and Meal objects
            comparator: procedure, comparator used to measure objects
            seed_name: name of the first food used as a seed
            names: optional list of food names, filters the JSON objects
            """
        print 'Greedy Algorithm Beginning, comparator is:', comparator.__name__
        foods = get_food_objects(food_groups, Name_Filter(names),
                                 nutrient_groups)
        first_food = get_food_with_name(seed_name, nutrient_groups)
        current_foods = [first_food]
        #tries = [first_food]
        current_meal = Meal(nutrient_groups, first_food)
        counter = [0] # putting the counter in a list sidesteps namespace
                      # issues (nonlocal not implemented until Python 3.0)
        def _next_food_helper(current_meal, min_meal, max_meal, foods,
                              nutrient_groups, comparator):
            """
                current_meal: the meal so far
                min_meal, max_meal: the benchmark meals
                foods: list of Food objects from above
                nutrient_groups: i.e. ['vitamins', 'elements']
                comparator: function that takes a meal, the min_meal and an
                            optional argument
                            returns a unitless number, smaller = better
                """
            next_food = foods[0] # seed
            next_food_meal_score = comparator(min_meal,
                                              current_meal.with_(next_food),
                                              counter)
            for food in foods:
                prospective_meal_score = comparator(min_meal,
                                                    current_meal.with_(food),
                                                    counter)
                if not max_meal.greater_than(current_meal.with_(food)):
                    continue  ## where is the best place for this check???
                if prospective_meal_score < next_food_meal_score:
                    next_food = food
                    next_food_meal_score = prospective_meal_score
            counter[0] += 1
            #print 'next food is:', next_food.name
            return next_food
        
        while len(current_foods) < servings:
            if not max_meal.greater_than(current_meal):
                print "Dead end reached in search algorithm, one or more"
                print "maximum constraints have been violated"
                print "Current foods: ", [x.name for x in current_foods]
                return current_meal
            if current_meal.greater_than(min_meal):
                return current_meal
            current_foods.append(_next_food_helper(current_meal, min_meal,
                                                   max_meal, foods,
                                                   nutrient_groups, comparator))
            current_meal.add(current_foods[-1])
        return current_meal


## COMPARATORS (return a unitless number used to compare meals)
    ## the 'optional' argument can be used to pass whatever info may be needed
    ## it may be nice to include a lambda function with each comparator that
    ## will automatically gather whatever info that comparator may need
def finish_line(min_meal, meal, optional=None):
    """ This algorithm takes a meal and a min_meal (benchmark meal) and finds
        the total distance between the meal and meeting its min constraints.
        The bigger the distance the farther from the min-meal.
        """
    distance = 0
    for group in meal.groupings:
        for key in meal.d(group):
            if meal.d(group)[key] < min_meal.d(group)[key]:
                if meal.d(group)[key] is not None and\
                   min_meal.d(group)[key] is not None: ## temporary, better way?
                    distance += ((min_meal.d(group)[key] -
                                  meal.d(group)[key]) / min_meal.d(group)[key])
    return distance

def balance(min_meal, meal, optional=None):
    """ This algorithm focuses on the overall balance of a meal, the more
        evenly distributed the nutrients, the lower the b_factor.
        If every nutrient is at 80% of it's min value the b_factor would be
        zero, this only measures lopsidedness.
        The bigger the number the more lopsided the meal.
        """
    total = 0 # total distance from perfect balance
    count = 0
    # get the average level
    for group in meal.groupings:
        for key in meal.d(group):
            if meal.d(group)[key] is not None and\
                   min_meal.d(group)[key] is not None:
                total += meal.d(group)[key] / min_meal.d(group)[key]
                count += 1
    average = total/count
    b_factor = 0
    for g in meal.groupings:
        for key in meal.d(group):
            if meal.d(group)[key] is not None and\
                   min_meal.d(group)[key] is not None: ## temporary
                #b_factor += abs(average - (meal.d(group)[key] / min_meal.d(group)[key]))
                if meal.d(group)[key] < min_meal.d(group)[key]:
                    b_factor += 4 * abs(average - (meal.d(group)[key] / min_meal.d(group)[key]))
                else:
                    b_factor += abs(average - (meal.d(group)[key] / min_meal.d(group)[key]))
    return b_factor
    
def alternating_finish_line_balance(min_meal, meal, optional=None):
    if optional % 2 == 0:
        return balance(min_meal, meal, optional)
    else:
        return finish_line(min_meal, meal, optional)



def test_greedy_finish_line(seed='Alfalfa seeds, sprouted, raw'):
    groupings = ['elements', 'vitamins']
    d_min = make_daily_min(groupings)
    d_max = make_daily_max(groupings)
    the_meal = greedy_alg(d_min, d_max, 250, veggie_beef_filter,
                          groupings, finish_line,
                          seed)
    display_nutrients(the_meal, d_min, d_max)
    print "Meets minimum requirements? ", the_meal.greater_than(d_min)
    print "Meets maximum requirements? ", d_max.greater_than(the_meal) 
    return the_meal

def test_greedy_balance(seed='Alfalfa seeds, sprouted, raw'):
    ## this takes a very long time to run and doesn't return a valid solution
    ## for 1000 foods it still doesn't reach all minimum values
    ## perhaps some sort of weighting scheme will help?
    groupings = ['elements', 'vitamins']
    d_min = make_daily_min(groupings)
    d_max = make_daily_max(groupings)
    the_meal = greedy_alg(d_min, d_max, 10000, veggie_beef_filter,
                          groupings, balance,
                          seed)
    display_nutrients(the_meal, d_min, d_max)
    print "Meets minimum requirements? ", the_meal.greater_than(d_min)
    print "Meets maximum requirements? ", d_max.greater_than(the_meal) 
    return the_meal

def test_greedy_alternating(seed='Alfalfa seeds, sprouted, raw'):
    groupings = ['elements', 'vitamins']
    d_min = make_daily_min(groupings)
    d_max = make_daily_max(groupings)
    the_meal = greedy_alg(d_min, d_max, 250, veggie_beef_filter,
                          groupings, alternating_finish_line_balance,
                          seed)
    display_nutrients(the_meal, d_min, d_max)
    print "Meets minimum requirements? ", the_meal.greater_than(d_min)
    print "Meets maximum requirements? ", d_max.greater_than(the_meal) 
    return the_meal
            
def run_walk_greedy_alg():
    """ Uses the finish_line() comparator until half of the nutrients have met
        their min constraints, then switches to the balance() comparator.
        """
    pass

def balanced_walk_greedy_alg():
    """ Uses the finish_line() comparator unless the nutritional balance is
        too unbalanced, then uses balance() to balance the situation before
        switching back to finish_line()
        """
    pass


#############################################################################
############################## GUI Specific #################################
#############################################################################

def get_fields(nutritional_groupings=['elements', 'vitamins', 'energy',
                                      'sugars', 'amino_acids', 'other',
                                      'composition']):
    print 'get_fields groupings:', nutritional_groupings
    food = Food(nutritional_groupings)
    fields = dict()
    for group in food.nutritional_groupings:
        fields[group] = food.__dict__[group].keys()
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
    
def search_like(search_string):
    assert type(search_string) is unicode or type(search_string) is str
    search_list = search_string.split(' ')
    if len(search_list) == 1:
        return search_by_name(search_string)
    else:
        return search_many(search_list)

