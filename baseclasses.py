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



#############################################################################
##################### class structure (data types) ##########################
#############################################################################

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
        ## For comparisons to work the nutritional_groupings list will need to
        ## be the same for all Foods being used - problematic
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
                                'Tyrosine': None, 'Hydroxyproline': None}
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
        self.food_group = json_object['group']
        serv_size_conv_fact = self.serving_size/100. # json data is per 100g
        converter = {'g':1000., 'mg': 1., 'mcg': (1/1000.)} # normalize to mg
        serving_size = json_object['portions']
        #print 'serving_size, self.serving_size', serving_size, self.serving_size
        
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
                        new_value = nutrient['value'] * \
                                    converter[nutrient['units']]* \
                                    serv_size_conv_fact
                        self.__dict__["amino_acids"][nutrient['description']] = new_value
                
        ## may need a lookup table for IU to mg conversion for different
        ## vitamins and elements
        ## measurements not in g, mg or mcg are being ignored!!!

    def create_json_object(self):
        # this creates a new json object (from self) that is compatible with
        # the main json dictionary, so populate_from_json() will work with it

        ## **** in progress ****
        new_obj = {'portions':None, 'description':None, 'tags':None, 'id':None,
                   'nutrietns':None, 'group':None, 'manufacturer':None}
        new_obj['description'] = self.name
        #new_obj.['portions'] = ...
        new_obj['group'] = self.food_group
        for ngroup in self.nutritional_groupings:
            for member in ngroup.keys():
                # double check this
                if ngroup in ['elements', 'vitamins', 'sugars', 'amino_acids']:
                    pass
                    new_obj['nutrients']
                    ## **** in progress ****
                    
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

    def flatten(self):
        """ Flattens the active nutritional groupings into one dictionary."""
        flat = {}
        for group in self.nutritional_groupings:
            first_dict = flat.items()
            second_dict = self.__dict__[group].items()
            flat = dict(first_dict + second_dict)
            #flat = dict(flat.items() + self[group].items())
        return flat
    
    @classmethod
    def unflatten(cls, dictionary, name):
        """ Unflattens the food.  Actually creates a new Food object and populates
            its values from the provided dictionary. """
        ## ** this needs to be cleaned up
        keys = dictionary.keys()
        # create the food with all nutritional groups
        new_food = Food(['elements', 'vitamins', 'energy', 'sugars',
                         'amino_acids', 'other', 'composition'], name=name)
        # populate the nutritional groups
        for group in new_food.nutritional_groupings:
            for item_name in new_food.__dict__[group]:
                if item_name in dictionary.keys():
                    new_food.__dict__[group][item_name] = dictionary[item_name]
        # remove the extra nutritional groups (not clear or efficient)
        for group in new_food.nutritional_groupings:
            if set(new_food.__dict__[group].keys()) <= set(dictionary.keys()):
                # the nutritional group's keys are all in the dictionary
                pass
            else:
                del new_food.__dict__[group]
        return new_food
            
    def get_val(self, group, item):
        """ Takes group and item, returns value
            """
        ## hacky way to deal with the 'null' meal
        try:
            return self.__dict__[group][item]
        except:
            return None
    def get_nutrgroups(self):
        return self.nutritional_groupings
    def get_nutrgroup_members(self, group):
        return self.__dict__[group]
    def get_servingsize(self):
        return self.serving_size
    def set_servingsize(self, size):
        self.serving_size = size
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
    def __init__(self, nutritional_groupings, foods=None):
        Food.__init__(self, nutritional_groupings)
        self.foods = []
        if foods is not None:
            for food in foods:
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
        for group in self.nutritional_groupings:
            for key in self.__dict__[group]:
                new_val = self._add_helper(self.get_val(group,key),
                                           food.get_val(group,key))
                self.__dict__[group][key] = new_val
                
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

        for group in self.nutritional_groupings:
            for key in self.__dict__[group]:
                new_val = self._subtract_helper(self.get_val(group,key),
                                                food.get_val(group,key))
                self.__dict__[group][key] = new_val

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
        ## --check for logic error possibilities with None's--
        for group in self.nutritional_groupings:
            for key in self.__dict__[group]:
                this, that = self.get_val(group, key), food.get_val(group, key)
                if this < that:
                    if this is not None and that is not None:
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
        return self.foods
    def get_food_names(self):
        return [food.get_name() for food in self.foods]

    def get_servings_and_foods(self):
        return [str(food.get_servingsize())+'g'+'--'+ food.get_name()
                for food in self.foods]

    def get_food_by_name(self, name):
        for food in self.foods:
            if food.get_name(name) == name:
                return food
        return False
