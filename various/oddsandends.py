## a few odds and ends from perfectmeal.py

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



## this one from perfectmeal_gui.py
##    def _add_current_meal_lb(self):
##        current_meal_label = wx.StaticText(parent=self.panel,
##                                           label="Current Meal")
##        self.current_meal_listbox = wx.ListBox(parent=self.panel,
##                                               id=-1,
##                                               pos=(3,5),
##                                               size=(275,375),
##                                               choices=[],
##                                               style=wx.LB_MULTIPLE)
##        self.current_meal_delete_button = wx.Button(parent=self.panel,
##                                                    id=2,
##                                                    label='Remove Selected')
##        
##        self.current_meal_complete_button = wx.Button(parent=self.panel,
##                                                      id=500,
##                                                      label='Complete Meal (testing)')
