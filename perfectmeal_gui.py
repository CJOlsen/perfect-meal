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
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent)
        self.parent = parent
        self.fields = perfmeal.get_fields()
        self.min_vals, self.max_vals = perfmeal.get_benchmarks()
        self.text_fields = {} # dict to keep track of TextCtrl id's
        
        self.panel = scrolled.ScrolledPanel(self)
        self.BuildUI()
        self.SetAutoLayout(1)
        self.SetupScrolling()
        
        self.Show()

    def BuildUI(self):
        self.sizer = wx.GridBagSizer(5,5)

        self.AddFields()
        self.AddListboxes()
        
        self.SetSizer(self.sizer)
        self.sizer.Layout()
        self.panel.SetSizerAndFit(self.sizer)

    def AddFields(self):
        i=0 #row
        j=0 #column
        for key in self.fields.keys():
            # key is section name
            new_label = wx.StaticText(self.panel, label=key.upper())
            self.sizer.Add(new_label,
                           pos=(i,0),
                           flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                           border=5)
            i+=1
            for item in self.fields[key]:
                # add label
                new_label = wx.StaticText(self.panel,
                                          label=item)
                self.sizer.Add(new_label,
                       pos=(i,0),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                       border=1)
                # add textbox for actual values
                location = i # this could be row and column
                self.text_fields[item] = location
                new_textbox = wx.TextCtrl(self.panel,
                                          id=location,
                                          size=(60, -1))
                self.sizer.Add(new_textbox,
                               pos=(i,1),
                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_RIGHT,
                               border=1)
                # add textboxes for max and min values
                min_value = wx.StaticText(self.panel,
                                          label=str(self.min_vals.get_val(key,item)))
                max_value = wx.StaticText(self.panel,
                                          label=str(self.max_vals.get_val(key,item)))
                self.sizer.Add(min_value,
                               pos=(i,2),
                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                               border=1)
                self.sizer.Add(max_value,
                               pos=(i,3),
                               flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                               border=1)
                i+=1
        # add column labels
        actual_label = wx.StaticText(self.panel, label="Actual")
        min_label = wx.StaticText(self.panel, label="Min")
        max_label = wx.StaticText(self.panel, label="Max")
        self.sizer.Add(actual_label,
                       pos=(0,1),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                       border=5)
        self.sizer.Add(min_label,
                       pos=(0,2),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                       border=5)
        self.sizer.Add(max_label,
                       pos=(0,3),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_CENTER,
                       border=5)

    def AddListboxes(self):
        ## current meal
        current_meal_label = wx.StaticText(self.panel, label="Current Meal")
        self.current_meal_listbox = wx.ListBox(self.panel,
                                               id=-1,
                                               pos=(3,5),
                                               size=(275,375),
                                               choices=['dummy','list'],
                                               style=wx.LB_MULTIPLE)
        self.sizer.Add(current_meal_label,
                       pos=(0,5),
                       flag=wx.TOP|wx.LEFT|wx.BOTTOM|wx.ALIGN_LEFT,
                       border=5)
        self.sizer.Add(self.current_meal_listbox,
                       pos=(1,5),
                       span=(12,1),
                       flag=wx.TOP,
                       border=5)

        ## search
        self.search_label = wx.StaticText(self.panel, label="Search Database")
        self.search_textbox = wx.TextCtrl(self.panel,
                                          id=-1,
                                          size=(275, -1))
        self.search_button = wx.Button(self.panel, id=-1, label="go")
        self.search_listbox = wx.ListBox(self.panel,
                                         id=-1,
                                         size=(275,300),
                                         choices=['search','dummy','list'],
                                         style=wx.LB_MULTIPLE)
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
                       span=(12,1),
                       flag=wx.TOP,
                       border=5)
                       
                       
        
                       
                       
        
        
        

    def populate_fields(self, name=None, meal=None, foods=None):
        assert name is not None or meal is not None
        if name:
            meal = perfmeal.get_food(name)
        elif foods:
            meal = perfmeal.get_meal(foods)
        
        
        
        
class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(800,400))
        
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
