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

####Levels of The Program (this file, GUI only):


import wx
import wx.lib.scrolledpanel as scrolled
import perfectmeal as perfmeal

class InteractivePanel(scrolled.ScrolledPanel):
    ## Essentially everything except the menubar, menu items, etc.
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.parent = parent
        self.fields = perfmeal.get_fields() # list of *displayed* fields
        self.text_fields = {} # dict mapping names to TextCtrls
        self.text_labels = {}
        self.section_labels = {}
        self.current_meal = perfmeal.get_meal([])
        
        self.panel = scrolled.ScrolledPanel(parent=self)

        self.field_panel = wx.Panel(parent=self.panel)

        self.BuildUI()
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
        self.Show()

    def BuildUI(self):
        self.sizer = wx.GridBagSizer(hgap=5, vgap=5)

        self.AddListboxes()
        self.AddFields()
        self.BindButtonsEtc()
        
        self.SetSizer(self.sizer)
        self.sizer.Layout()
        self.panel.SetSizerAndFit(self.sizer)

    def BindButtonsEtc(self):
        self.Bind(wx.EVT_BUTTON, self.OnUseSelected, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnRemoveSelected, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnAddToMeal, id=3)
        self.Bind(wx.EVT_BUTTON, self.OnGo, id=4)
    
    def AddFields(self):
        self.field_sizer = wx.GridBagSizer(hgap=5,vgap=5)
        self.nutritional_groupings = self.GetNutrientGroups()
        self.min_vals, self.max_vals = \
                       perfmeal.get_benchmarks()
        print 'nutritional groupings --> perfmeal.py', self.nutritional_groupings
        self.fields = perfmeal.get_fields(self.nutritional_groupings)
        if type(self.field_panel) != wx._windows.Panel:
            ## this happens if the panel has been destroyed and needs recreating
            self.field_panel = wx.Panel(parent=self.panel)
        i=0 #row
        for key in self.fields.keys():
            # key is section name
            self.section_labels[key] = wx.StaticText(parent=self.field_panel,
                                                     label=key.upper())
            self.field_sizer.Add(self.section_labels[key],
                           pos=(i,0),
                           flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                           border=5)
            i+=1
            for item in self.fields[key]:
                # add label
                self.text_labels[item] = wx.StaticText(parent=self.field_panel,
                                                       label=item)
                self.field_sizer.Add(self.text_labels[item],
                       pos=(i,0),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                       border=1)
                # add textbox for actual values
                self.text_fields[item] = wx.TextCtrl(parent=self.field_panel,
                                                     id=500,
                                                     size=(60, -1))
                self.field_sizer.Add(self.text_fields[item],
                               pos=(i,1),
                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                               border=1)
                # add textboxes for max and min values
                min_value = wx.StaticText(parent=self.field_panel,
                                          label=str(self.min_vals.get_val(key,
                                                                          item)))
                max_value = wx.StaticText(parent=self.field_panel,
                                          label=str(self.max_vals.get_val(key,
                                                                          item)))
                self.field_sizer.Add(min_value,
                               pos=(i,2),
                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                               border=1)
                self.field_sizer.Add(max_value,
                               pos=(i,3),
                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                               border=1)
                i+=1
        # add column labels
        actual_label = wx.StaticText(parent=self.field_panel, label="Actual")
        min_label = wx.StaticText(parent=self.field_panel, label="Min")
        max_label = wx.StaticText(parent=self.field_panel, label="Max")
        self.field_sizer.Add(actual_label,
                       pos=(0,1),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                       border=5)
        self.field_sizer.Add(min_label,
                       pos=(0,2),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                       border=5)
        self.field_sizer.Add(max_label,
                       pos=(0,3),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                       border=5)
        # final setup
        self.field_panel.SetSizer(self.field_sizer)
        self.sizer.Add(self.field_panel,
                       pos=(0,0),
                       span=(100,4))

    def DisplayFieldValues(self):
        """ Displays values in the nutrient fields.
            """
        for key in self.fields.keys():
            for item in self.fields[key]:
                value = self.current_meal.get_val(key,item)
                #serv_size = self.current_meal.
                self.text_fields[item].SetValue(str(value))
        
    def DestroyFields(self):
        """ Destroys the panel containing the nutrient fields,
            reinitializes the field data.
            """
        self.field_panel.DestroyChildren()
        self.field_panel.Destroy()
        self.text_fields = {}
        self.text_labels = {}
        self.section_labels = {}
    
    def AddListboxes(self):
        ## current meal
        current_meal_label = wx.StaticText(parent=self.panel,
                                           label="Current Meal")
        self.current_meal_listbox = wx.ListBox(parent=self.panel,
                                               id=-1,
                                               pos=(3,5),
                                               size=(275,375),
                                               choices=[],
                                               style=wx.LB_MULTIPLE)
        self.current_meal_delete_button = wx.Button(parent=self.panel,
                                                    id=2,
                                                    label='Remove Selected')
        self.sizer.Add(current_meal_label,
                       pos=(0,5),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_LEFT,
                       border=5)
        self.sizer.Add(self.current_meal_listbox,
                       pos=(1,5),
                       span=(12,1),
                       flag=wx.TOP,
                       border=5)
        self.sizer.Add(self.current_meal_delete_button,
                       pos=(13,5),
                       flag=wx.ALIGN_RIGHT,
                       border=0)

        ## search boxes
        self.search_label = wx.StaticText(parent=self.panel, label="Search Database")
        self.search_textbox = wx.TextCtrl(parent=self.panel,
                                          id=-1,
                                          size=(275, -1))
        self.search_button = wx.Button(parent=self.panel, id=4, label="go")
        self.search_listbox = wx.ListBox(parent=self.panel,
                                         id=-1,
                                         size=(275,300),
                                         choices=[],
                                         style=wx.LB_MULTIPLE)
        self.search_addto_button = wx.Button(parent=self.panel,
                                             id=3,
                                             label="Add To Meal")
        self.sizer.Add(self.search_label,
                       pos=(0,6),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_LEFT,
                       border=5)
        self.sizer.Add(self.search_textbox,
                       pos=(1,6),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_LEFT,
                       border=5)
        self.sizer.Add(self.search_button,
                       pos=(2,6),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                       border=0)
        self.sizer.Add(self.search_listbox,
                       pos=(3,6),
                       span=(10,1),
                       flag=wx.TOP,
                       border=5)
        self.sizer.Add(self.search_addto_button,
                       pos=(13,6),
                       flag=wx.ALIGN_LEFT,
                       border=0)

        ## Nutrient Groupings Box
        self.nutrient_groups_label = wx.StaticText(parent=self.panel, id=-1,
                                                   label="Nutrient Groupings")
        self.nutrient_groups_listbox = wx.ListBox(parent=self.panel,
                                                  id=-1,
                                                  size=(275,155),
                                                  choices=['elements','vitamins',
                                                           'energy', 'sugars',
                                                           'amino_acids',
                                                           'other',
                                                           'composition'],
                                                  style=wx.LB_MULTIPLE)
        self.nutrient_groups_listbox.Select(0) # default selections
        self.nutrient_groups_listbox.Select(1) # default selections
        self.nutrient_groups_select_button = wx.Button(parent=self.panel,
                                                       id=1,
                                                       label="Use Selected")
        self.sizer.Add(self.nutrient_groups_label,
                       pos=(15,5),
                       flag=wx.ALIGN_LEFT,
                       border=5)
        self.sizer.Add(self.nutrient_groups_listbox,
                       pos=(16,5),
                       span=(5,1),
                       border=5)
        self.sizer.Add(self.nutrient_groups_select_button,
                       pos=(21,5),
                       flag=wx.ALIGN_RIGHT,
                       border=0)
    def OnGo(self, event):
        print 'OnGo'
        text = self.search_textbox.GetValue()
        names = perfmeal.search_like(text)
        self.search_listbox.Set(names)
        
    def OnRemoveSelected(self, event):
        print 'OnRemoveSelected'
        to_remove_indexes = self.current_meal_listbox.GetSelections()
        to_remove_strings = self.current_meal_listbox.GetStrings()
        names = [to_remove_strings[i] for i in to_remove_indexes]
        for food_name in names:
            new_food = perfmeal.get_food(food_name)
            self.current_meal.subtract(new_food)
        self.current_meal_listbox.Set(self.current_meal.get_foods())
        self.DisplayFieldValues()
            
    def OnAddToMeal(self, event):
        to_add_indexes = self.search_listbox.GetSelections()
        to_add_strings = self.search_listbox.GetStrings()
        names = [to_add_strings[i] for i in to_add_indexes]
        for food_name in names:
            new_food = perfmeal.get_food(food_name)
            self.current_meal.add(new_food)
        self.current_meal_listbox.Set(self.current_meal.get_foods())
        self.DisplayFieldValues()
            
    def OnUseSelected(self, event):
        #nutrient groupings
        if self.GetNutrientGroups() == self.nutritional_groupings:
            return # groupings haven't changed, do nothing
        self.DestroyFields()
        self.AddFields()
        self.sizer.Layout()
        self.DisplayFieldValues()
    def OnCurrentMealLBSelected(self, event):
        pass
    def OnSearchLBSelected(self, event):
        pass
    def OnNutrientLBSelected(self, event):
        pass

    def GetNutrientGroups(self):
        indexes = self.nutrient_groups_listbox.GetSelections()
        choices=['elements','vitamins','energy', 'sugars','amino_acids',
                 'other','composition']
        print 'get nutrient groups:', [choices[i] for i in indexes]
        return [choices[i] for i in indexes]

    def populate_fields(self, name=None, meal=None, foods=None):
        assert name is not None or meal is not None
        if name:
            meal = perfmeal.get_food(name)
        elif foods:
            meal = perfmeal.get_meal(foods)
        
##Button and listbox ID's:
##  Current Meal Listbox:
##  Search Listbox:
##  Search Text Field: 
##  Search Text "Go" Button: id=4
##  
##  Add To Meal Button: id=3
##  Remove Selected Button: id=2
##  Use Selected (Nutrient Groupings)Button: id=1 
##  Nutrient Value Textboxes: id=500
##
            
        
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(1000,750))
        
        # setting up the file menu
        filemenu = wx.Menu()
        #wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxwidgets
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = filemenu.Append(wx.ID_EXIT, "&Exit", " Terminate the program.")
        # Creating the Menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        self.Show(True)
        # create event bindings
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        # display the notebook
        self.sizer = wx.BoxSizer()
        self.sizer.Add(InteractivePanel(self), 1, wx.EXPAND, border=15)
        self.SetSizer(self.sizer)
        self.Layout()
        self.Show()

    def OnAbout(self, e):
        """ Bound to the 'About' menu item.  Displays a dialog box with an OK
            button.

            """
        text = "Perfect Meal is an in-progress application by Christopher "\
               "Olsen.\n\ngithub.com/cjolsen\n\nIt's best to assume that "\
               "nothing in this app is sound dietary advice, because it "\
               "probably isn't."
        dialog = wx.MessageDialog(self,
                                  text,
                                  "About Payable Hours",
                                  wx.OK)
        dialog.ShowModal()
        dialog.Destroy()

    def OnExit(self, e):
        self.Close(True)

app = wx.App()
MainWindow(None, title="Perfect Meal")
app.MainLoop()





## **** this is a way to add the fields in columns (i.e. without min/max benchmarks)
####    def AddFields(self):
####        i=0 #row
####        j=0 #column
####        for key in self.fields.keys():
####            # key is section name
####            new_label = wx.StaticText(self.panel, label=key.upper())
####            self.sizer.Add(new_label,
####                           pos=(i,j),
####                           flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
####                           border=5)
####            i+=1
####            for item in self.fields[key]:
####                new_label = wx.StaticText(self.panel, label=item)
####                self.sizer.Add(new_label,
####                       pos=(i,j),
####                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
####                       border=1)
####                new_textbox = wx.TextCtrl(self.panel, size=(140, -1))
####                self.sizer.Add(new_textbox,
####                               pos=(i,j+1),
####                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
####                               border=1)  
####                i+=1
####            j+=2
####            i=0
