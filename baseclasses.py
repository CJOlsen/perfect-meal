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

import os
import sys
import json

debug = True

# open the custom JSON file as a global readonly
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
json_loc = current_dir + "/pmeal.json"
pmeal_json = open(json_loc, "r")
pmeal_json_dict = json.load(pmeal_json)

class Food(object):
    def __init__(self, json_obj=None, name=None):
        """ The Food object has standard attributes for:
            -name: name of the food, optional
            If a json_obj is included the dictionaries will be populated with
            the data (as filtered by the nutritional_groupings list)
            """

        self.name = name
        self.nutritional_groupings = ['elements', 'vitamins', 'energy',
                                      'amino_acids', 'other', 'composition']                         
        self._initialize_fields()
        if json_obj:
            self._populate_from_json(json_obj)

    def _initialize_fields(self):
        self.nutrients = {group:None
                          for group
                          in self.nutritional_groupings}
        ## initialize all fields to None
        ## this is a little different than the json db, but the advantage is
        ## things can be found by:
        ## self.nutrients[*group*][*nutrient*][*attribute*]
        self.nutrients = {}
        for group in pmeal_json_dict['nutritional_groups']:
            sub_dict = {}
            for nutrient in self.nutrients[group]:
                sub_dict[nutrient] = {'units':None,
                                      'description':None,
                                      'value':None}
            self.nutrients[group] = sub_dict
                
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

    def _populate_from_json(self, json_object):
        assert type(json_object) is dict
        self.name = json_object['description']
        self.food_group = json_object['group']
        ## deal wit
        self._portion_helper(json_object)
        serving_size = json_object['portions']
        serv_size_conv_fact = self.serving_size/100. # json data is per 100g      

        for nutrient in json_object['nutrients']:
            self.nutrients[nutrient['group']]['units'] = nutrient['units']
            self.nutrients[nutrient['group']]['description'] = \
                                                        nutrient['description']
            # data comes in per 100g serving, needs to be converted to the
            # smallest serving size 
            try:
                self.nutrients[nutrient['group']]['value'] = \
                                                nutrient['value'] * \
                                                serv_size_conv_fact
            except:
                if debug: print 'value conversion failed'
                self.nutrients[nutrient['group']]['value'] = None

    ## **** in progress ****
    def _create_json_object(self):
        # this creates a new json object (from self) that is compatible with
        # the main json dictionary, so populate_from_json() will work with it
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


    ## **** flatten and unflatten still need to be refactored
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
        """ Unflattens the food.  Actually creates a new Food object and 
            populates its values from the provided dictionary. 
            """
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

    def get_val(self, group, item):
        """ Takes group and item, returns value
            """
        ## hacky way to deal with the 'null' meal
        try:
            return self.nutrients[group][name]['value']
        except:
            print 'Food().get_val try/except loop - exception'
            return None
    def set_val(self, group, item, value):
        self.nutrients[group][name]['value'] = value

    def get_element_val(name):
        return self.nutrients['elements'][name]['value']
    def get_vitamin_val(name):
        return self.nutrients['vitamins'][name]['value']
    def get_energy_val(name):
        return self.nutrients['energy'][name]['value']
    def get_sugar_val(name):
        return self.nutrients['sugars'][name]['value']
    def get_amino_acid_val(name):
        return self.nutrients['amino_acids'][name]['value']
    def get_other_val(name):
        return self.nutrients['other'][name]['value']
    def get_composition_val(name):
        return self.nutrients['composition'][name]['value']

    def set_element_val(name, value):
        return self.nutrients['elements'][name]['value'] = value
    def set_vitamin_val(name, value):
        return self.nutrients['vitamins'][name]['value'] = value
    def set_energy_val(name, value):
        return self.nutrients['energy'][name]['value'] = value
    def set_sugar_val(name, value):
        return self.nutrients['sugars'][name]['value'] = value
    def set_amino_acid_val(name, value):
        return self.nutrients['amino_acids'][name]['value'] = value
    def set_other_val(name, value):
        return self.nutrients['other'][name]['value'] = value
    def set_composition_val(name, value):
        return self.nutrients['composition'][name]['value'] = value
       
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
