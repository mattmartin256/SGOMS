
'''
2014.05.12 Each time I create a unit task, I need to add its parent planning unit to the Unit Task's list,
and I need to add the Unit Task to a parent planning unit.

Somewhere, somehow, my new unit task is being added to both planning units, but not by any obvious means.
This probably takes place in the UnitTaskWindow.createUnitTask function

The Unit Task seems to get added to each Planning Unit, both when a new Unit Task is created, and when a new Planning Unit is Created.
Adding a second PU when there already is a UT automatically adds the UT to the new PU

2014.05.13 *Changing the default constructor seemed to help. Getting rid of the optional parameter of theUnitTaskList=[], in PlanningUnit
seems to solve the problem of adding each new unit task to each new Planning Unit by default,
And getting rid of theParentPlanningUnits=[] in UnitTask seems to stop the problem of assigning each PU to be the parent of every new UT

^Apparently this is a common Python thing which has to do with how the code is interpreted. 
Python only interprets the definition of the class once, which means that any variable defined in the parameters
will be the same for each instantiation of the class; hence why 'a' was appearing in both asdf and fads's lists.

Basically, don't use arrays/lists as default parameters

2014.05.15 Can't have unitTask.ID be the ID of the corresponding item on the tree
because each tree ID needs to be unique, which means that you can't have the same
unit task be represented twice on one tree - something which we need to be able to do.

At this point in the code, we can't assign the same Unit Task to multiple PUs, but it works otherwise

2014.05.16- Upon David's advice, I'm going to create a new class of PU/UT relationships
and maintain a list of these in the model. This will hopefully solve the tree problem,
since every relation will have a unique ID which I can stick directly into the tree.

End of Day 2014.05.16 - The relational stuff can initialize the tree, haven't tried updating yet.

2014.05.20 - The tree updates, seems to exhibit the behaviours I want, have done some testing.
Moving on to ACT-R stuff.
'''

import Tkinter as tk
import ttk

class PlanningUnit:
    '''An SGOMS Planning Unit that contains a list of Unit Tasks'''

    def __init__(self, theID="Planning Unit", theUnitTaskList=0.0):
        '''Creates a PlanningUnit

        theID should be a string that identifies the Planning Unit
        theUnitTaskList should be a list of UnitTasks'''

        self.ID = theID
        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == 0.0:
            self.unitTaskList = []

        print "(PlanningUnit.__init__) Planning Unit Created: ", self.ID
        self.printPlanningUnitContents()

    def addUnitTask(self, theUnitTask):
        '''Adds theUnitTask to the Planning Unit,
        and sets the current Planning Unit to be the parent Planning Unit of the Unit Task

        theUnitTask should be a UnitTask'''

        self.unitTaskList.append(theUnitTask)
        theUnitTask.setParentPlanningUnit(self)

        print "(PlanningUnit.addUnitTask); Unit Task ", theUnitTask.ID, " was added to Planning Unit ", self.ID  
        
    def printPlanningUnitContents(self):
        '''Prints the Planning Unit's ID, and the IDs of all the Unit Tasks it contains'''

        print "(printPlanningUnitContents) ", self.ID, " has ", len(self.unitTaskList), " Unit Tasks:"

        if len(self.unitTaskList) > 0:
            for item in self.unitTaskList:
                print item.ID, "; parent Planning Unit(s) ="
                item.printParentPlanningUnits()

        else:
            print self.ID, " has no unit tasks"
    
class UnitTask:
    '''An SGOMS Unit Task'''
    
    def __init__(self, theID="Unit Task", theParentPlanningUnits=0.0):
        '''Creates a Unit Task

        ID is a string that names the Unit Task
        theParentPlanningUnits should be a list of PlanningUnits'''

        self.ID = theID
        self.parentPlanningUnits = theParentPlanningUnits
        if theParentPlanningUnits == 0.0:
            self.parentPlanningUnits = []
        

        print "(UnitTask.__init__) Unit Task Created: ", self.ID,
        self.printParentPlanningUnits()

    def setParentPlanningUnit(self, thePlanningUnit):
        '''Adds thePlanningUnit to the list of parent Planning Units

        thePlanningUnit should be a PlanningUnit'''

        self.parentPlanningUnits.append(thePlanningUnit)

        print "(UnitTask.setParentPlanningUnit); Planning Unit ", thePlanningUnit.ID, " was added to Unit Task ", self.ID, "'s parentPlanningUnits list"
        
    def printParentPlanningUnits(self):
        '''Prints the parent Planning Unit(s) of the Unit Task.
        There is no requirement for the Unit Task to have a parent Planning Unit'''
        
        print "(UnitTask.printParentPlanningUnits) ", self.ID, "'s parentPlanningUnit(s) = "

        if len(self.parentPlanningUnits) > 0:
            for item in self.parentPlanningUnits:
                print item.ID

        else:
            print self.ID, " has no parent Planning Unit"

class PUxUTRelation:
    '''Represents the relationship between a PlanningUnit and a UnitTask'''

    def __init__(self, theID, thePlanningUnit, theUnitTask):
        '''Initializes the relationship between thePlanningUnit and theUnitTask

        theID should be a unique string (or possibly integer), each relation's ID must be unique
        thePlanningUnit should be a single PlanningUnit that contains theUnitTask in its unitTasklist
        theUnitTask should be a single UnitTask with thePlanningUnit as a parent Planning Unit'''

        self.ID = theID 
        self.planningUnit = thePlanningUnit
        self.unitTask = theUnitTask
        self.location = thePlanningUnit.unitTaskList.index(theUnitTask) ## The location of the unit task within the planning unit/tree
        ##^I'm not sure, but this line may be problematic if there are more than one of the same unit task in the list
        self.tuppleID = "PUxUTRelation", self.planningUnit.ID, self.unitTask.ID, self.location

        print "(PUxUTRelation.init) Created: ", self.tuppleID  
            
class SGOMS_Model:
    '''The underlying model that the GUI runs on'''

    def __init__(self, thePlanningUnitList=0.0, theUnitTaskList=0.0):
        '''The initializing method for the model

        planningUnitList should be a list of Planning Units
        unitTaskList should be a list of Unit Tasks'''

        print "SGOMS_Model initiated"

        self.planningUnitList = thePlanningUnitList
        if thePlanningUnitList == 0.0:
            self.planningUnitList = []
        self.planningUnitCounter = len(self.planningUnitList)

        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == 0.0:
            self.unitTaskList = []
        self.unitTaskCounter = len(self.unitTaskList)

        self.pUxUTRelationList = []

    def addPlanningUnit(self, thePlanningUnit):
        '''Adds thePlanningUnit to the planningUnitList,
        and updates the planningUnitCounter to be the length of the Planning Unit list.

        thePlanningUnit should be a PlanningUnit'''

        self.planningUnitList.append(thePlanningUnit)
        self.planningUnitCounter = len(self.planningUnitList)

        print "(Model.addPlanningUnit): ", thePlanningUnit.ID, " added. Total number of Planning Units in the model = ", len(self.planningUnitList)

    def addUnitTask(self, theUnitTask, theParentPlanningUnit=None):
        '''Adds theUnitTask to self.unitTaskList,
        and updates the unitTaskCounter to be the length of the Unit Task list.
        Also sets theParentPlanningUnit to be the parent Planning Unit of theUnitTask, if supplied
        There is no requirement for the Unit task to belong to a PlanningUnit

        theUnitTask should be a UnitTask
        thePlanningUnit should be a PlanningUnit'''

        if theParentPlanningUnit == None:
            self.unitTaskList.append(theUnitTask)
            self.unitTaskCounter = len(self.unitTaskList)

        else:
            self.unitTaskList.append(theUnitTask)
            self.unitTaskCounter = len(self.unitTaskList)
            #theParentPlanningUnit.addUnitTask(theUnitTask)

        print "(Model.addUnitTask): ", theUnitTask.ID, " added. Total number of Unit Tasks in the model = ", len(self.unitTaskList)

    def addPUxUTRelationReturnSelf(self, thePlanningUnit, theUnitTask):
        '''Creates a relationship between thePlanningUnit and theUnitTask,
        and adds it to the list of relationships. 

        thePlanningUnit should be a PlanningUnit
        theUnitTask should be a UnitTask'''

        tempID = len(self.pUxUTRelationList) ## The ID for the relation will just be its index in the model's list

        r = PUxUTRelation(tempID, thePlanningUnit, theUnitTask)

        self.pUxUTRelationList.append(r)
        return r

        print "(Model.addPUxUTRelation) Adding to list : ", r.tuppleID

    def printModelContentsBasic(self):
        '''Print the IDs of all Planning Units and Unit Tasks in the Model'''

        ## Planning Units
        print "(printModelContentsBasic), Planning Units:"
        if len(self.planningUnitList) > 0:
            print "There are ", self.planningUnitCounter, " Planning Units in the Model:"
            for item in self.planningUnitList:
                print item.ID
        else:
            print "There are no Planning Units in the Model"

        ## Unit Tasks
        print "(printModelContents), Unit Tasks:"
        if len(self.unitTaskList) > 0:
            print "There are ", self.unitTaskCounter, " Unit Tasks in the Model:"
            for item in self.unitTaskList:
                print item.ID
        else:
            print "There are no Unit Tasks in the Model"

        print "End of (printModelContentsBasic)"

    def printModelContentsAdvanced(self):
        '''Prints the entire contents of the model,
        including each Planning Unit and its contents,
        and each Unit Task and their parent Planning Unit(s)'''

        print "==== (printModelContentsAdvanced) ===="
        print "Planning Units:"
        if len(self.planningUnitList) > 0:
            print "There are ", self.planningUnitCounter, " Planning Units in the Model:"
            for item in self.planningUnitList:
                item.printPlanningUnitContents()
        else:
            print "There are no Planning Units in the Model"

        print "Unit Tasks:"
        if len(self.unitTaskList) > 0:
            print "There are ", len(self.unitTaskList), " Unit Tasks in the Model:"
            for item in self.unitTaskList:
                item.printParentPlanningUnits()
        else:
            print "There are no Unit Tasks in the model"

        print "(printModelContents), PUxUTRelations:"
        if len(self.pUxUTRelationList) > 0:
            print "There are ", len(self.pUxUTRelationList), " PUxUTRelationships in the Model:"
            for item in self.pUxUTRelationList:
                print item.tuppleID
        else:
            print "There are no PUxUTRelationships in the Model"

        print "==== End of (printModelContentsAdvanced) ===="    
                

class SGOMS_GUI(tk.Frame):
    '''An interface for creating Planning Units and Unit Tasks,
    and having them compile into ACT-R code''' 
    
    def __init__(self, theModel, master=None):
        '''The initializing method that creates the frame'''

        print "SGOMS_GUI initiated"
        tk.Frame.__init__(self, master)
        self.master = master
        self.pack()
        
        self.model = theModel

        self.createWidgets()   

        self.updateCounter = 0  ##Keeps track of the number of updates, for testing purposes
        
    def createWidgets(self):
        '''The method that defines the main window'''

        print "(SGOMS_GUI.createWidgets)"
        ##Define the Planning Unit Button
        self.planningUnitButton = tk.Button(self)
        self.planningUnitButton["text"] = "Create new Planning Unit"
        self.planningUnitButton["command"] = self.createPlanningUnitWindow

        #self.planningUnit.pack({"side": "bottom"})  ##Add it to the frame
        self.planningUnitButton.grid(row=0, column=0)

        ##Define the Unit Task Button
        self.unitTaskButton = tk.Button(self)
        self.unitTaskButton["text"] = "Create new Unit Task"
        self.unitTaskButton["command"] = self.createUnitTaskWindow

        #self.unitTaskButton.pack({"side": "bottom"})  ##Add it to the frame
        self.unitTaskButton.grid(row=1, column=0)

        ##Define the quit button
        self.quitButton = tk.Button(self)            
        self.quitButton["text"] = "QUIT"
        self.quitButton["fg"]   = "red"
        self.quitButton["command"] =  self.quit

        #self.QUIT.pack({"side": "bottom"})
        self.quitButton.grid(row=2, column=0)    ## Add the quit button to the frame

        ##Define the Label for the list of Planning Units
        self.pLabel = tk.Label(self, text = "Planning Units: -->")
        self.pLabel.grid(row=0, column=1)

        ##Define the Label for the list of unit tasks
        self.uLabel = tk.Label(self, text = "Unit Tasks:")
        self.uLabel.grid(row=1, column=1)

        self.createTree()

    def createTree(self):
        '''Creates the Treeview widget'''


        ## Original version
        '''
        self.tree = ttk.Treeview(self, height=6, selectmode="browse")
        
        dataColumns = ["Planning Units", "Unit Tasks"]
        
        self.tree.heading('#0', text='Model', anchor='w')
        self.tree.columns = dataColumns
        self.tree.displaycolumns = '#all'

        self.tree.grid(row=0, column=2)
        '''
        

        ## Testing out columns for the tree
        self.tree = ttk.Treeview(self, columns=("Info"), height=6, selectmode="browse") ## 'Columns' specifies the ID of the extra(?) column I want to have
        self.tree.column("#0",      stretch=True);
        self.tree.heading("#0",     text="Model",  anchor="w") #The column holding the tree can be accessed with the symbolic name "#0"
        self.tree.column("Info",   stretch=True); #"Info" is the ID of a particular column (specified in constructor above) 
        self.tree.heading("Info",  text="More Info",   anchor="w") 

        self.tree.displaycolumns = '#all'

        self.tree.grid(row=0, column=2)

        '''
        self.tree.insert('', 0, 'PU', text="Planning Unit X") #Insert <ID>'PU' as the first child of the root node, displaying the text "Planning Unit X"
        self.tree.insert('PU', 0, 'UT', text="Unit Task X") #Insert <ID>'UT' as the child of PU, at index 0
        self.tree.item('PU', open=True)
        '''
        planningUnitCounter = 0
        unitTaskCounter = 0

        '''
        ## Use the Planning Unit list and Unit Task list to populate the tree
        ## Add each initial Planning Unit and Unit Task (for testing purposes)
        for item in self.model.planningUnitList:
            self.tree.insert('', 'end', item.ID, text=item.ID) #Insert <ID>item.ID as the first child of the root node, displaying it's own ID as text
            ## Inserting something returns the ID of the newly created item, which can be used below
            self.tree.item(item.ID, open=True)

            for thing in item.unitTaskList:
                self.tree.insert(item.ID, 'end', thing.ID, text=thing.ID) #Insert <ID>thing.ID as the first child of <parent>pUID
                unitTaskCounter += 1

            planningUnitCounter += 1
        '''

        ##Use the Planning Unit list to populate the tree with Planning Units
        for item in self.model.planningUnitList:
            self.tree.insert('', 'end', item.ID, text=item.ID) 

        ##Use the relational list to populate the tree with Unit Tasks
        for item in self.model.pUxUTRelationList:
            self.tree.insert(item.planningUnit.ID, item.location, item.ID, text=item.unitTask.ID)              

    def createPlanningUnitWindow(self):
        '''A method for creating the window that pops up and takes user input
        when the 'Create Planning Unit' button is pressed'''
        
        print "(SGOMS_GUI.createPlanningUnitWindow) number of Planning Units in the model = %s" %self.model.planningUnitCounter

        ##Create a new window for user input, with the current SGOMS_GUI as the master
        w = PlanningUnitWindow(self)
        
    def createUnitTaskWindow(self):
        '''A method for creating the window that pops up and takes user input
        when the 'Create Unit Task' button is pressed'''
        
        print "(SGOMS_GUI.createUnitTaskWindow) number of unit tasks in model = %s" %self.model.unitTaskCounter

        w = UnitTaskWindow(self)

    def addPlanningUnitToTree(self, thePlanningUnit):
        '''Takes a PlanningUnit, and adds it to the tree

        thePlanningUnit should be a PlanningUnit'''

        print "(SGOMS_GUI.addPlanningUnitToTree)"
        
        self.tree.insert("", "end", thePlanningUnit.ID, text=thePlanningUnit.ID)
        self.tree.item(thePlanningUnit.ID, open=True)

    def addUnitTaskToTree(self, thePUxUTRelationship):
        '''Takes a UnitTask, and adds it to the tree

        thePUxUTRelationship should be a PUxUTRelationship that contains a unit task and planning unit'''

        print "(SGOMS_GUI.addUnitTaskToTree)"

        ## Insert unit task into the tree
        ## Each leaf must be unique, but point to the same underlying UT
        ## Somehow I must be able to access the tree ID of the parent PU
        ## If I had a global update function, I might be able to get around this problem
        ## Since I would be adding the planning units, I could have access to their IDs
        #for item in theUnitTask.parentPlanningUnits:
        #    self.tree.insert(item.ID, "end", theUnitTask.ID, text=theUnitTask.ID)

        tempID = thePUxUTRelationship.ID
        pU = thePUxUTRelationship.planningUnit
        uT = thePUxUTRelationship.unitTask
        loc = thePUxUTRelationship.location

        self.tree.insert(pU.ID, loc, thePUxUTRelationship.ID, text=uT.ID)
            
    def update(self):   
        '''A method that updates the frame, based on the model'''

        print "***** (Update) ***** ", self.updateCounter
        self.model.printModelContentsAdvanced()

        #self.updateButtons()
        self.updateTree()
        
        self.updateCounter += 1     ## Counts the total number of updates    
        print "***** UPDATE COMPLETE *****"    

           
    def updateTree(self):
        '''Updates the contents of the tree based on the model'''

        '''2014.05.15- Functionality of tree is different than buttons,
        You can't just clobber everything at update, and can't override what's already in the tree.
        (You get exceptions if you do).
        Need to either nuke the tree on each update and start from scratch,
        or move functionality to the TopLevel windows

        Or I could just have an 'if' statement that checks whether or not the thing already
        exists, and if so, just pass.

        The nuking option seems like not the best option, I will move functionality elsewhere
        ^Actually, I could just create a new tree on update, and populate it every time

        Option 1: when update is called, delete everything in the tree manually, and repopulate
        Option 2: don't use update, and have the TopLevel window add to the tree directly
        Option 3: when update is called check if the item is already in the tree, and if so, pass  #This seems like the best option
        Option 4: when update is called, create a new tree, and populate it from scratch

        #David seems to do something like Option 2 with his linkWorld/unlinkWorld commands.
        '''

        '''
        print "(updateTree)"

        planningUnitCounter = 0
        unitTaskCounter = 0

        for item in self.model.planningUnitList:
            self.tree.insert('', 'end', item.ID, text=item.ID) #Insert <ID>item.ID as the first child of the root node, displaying it's own ID as text
            self.tree.item(item.ID, open=True)

            for thing in item.unitTaskList:
                self.tree.insert(item.ID, 'end', thing.ID, text=thing.ID) #Insert <ID>thing.ID as the first child of <parent>item.ID
                unitTaskCounter += 1

            planningUnitCounter += 1
        '''

        ##Use the Planning Unit list to populate the tree with Planning Units
        for item in self.model.planningUnitList:
            self.tree.insert('', 'end', item.ID, text=item.ID) 

        ##Use the relational list to populate the tree with Unit Tasks
        for item in self.model.pUxUTRelationList:
            self.tree.insert(item.planningUnit.ID, item.location, item.ID, text=item.unitTask.ID) 


    def updateButtons(self):
        '''Updates the buttons for the PlanningUnits, Unit Tasks etc, bassed on the model'''

        print "(updateButtons)"

        planningUnitButtonLoopCounter = 0

        for item in self.model.planningUnitList:
            
            print "(Update): creating planning unit button for: ", item.ID, ", planningUnitButtonLoopCounter = ", planningUnitButtonLoopCounter
            ## Create a button for each entry in the planningUnitList
            pLButton = tk.Button(self)
            pLButton["text"] = item.ID
            pLButton.grid(row=0, column=2+planningUnitButtonLoopCounter)

            if len(item.unitTaskList) > 0:
                ##Create a button below each Planning Unit, for each Unit Task it contains
                print "Length of ", item.ID, "'s unitTaskList was greater than zero. Len = ", len(item.unitTaskList)
                uTCounter = 0
                for thing in item.unitTaskList:
                    print "(Update): creating Unit Task button for: ", thing.ID, "uTCounter = ", uTCounter
                    uTButton = tk.Button(self)
                    uTButton["text"] = thing.ID
                    uTButton.grid(row = 1+uTCounter, column = 2+planningUnitButtonLoopCounter)
                    uTCounter +=1

            else:
                print "Length of ", item.ID, "'s unitTaskList was zero. Len = ", len(item.unitTaskList)

            planningUnitButtonLoopCounter += 1

class PlanningUnitWindow(tk.Toplevel):
    '''A class to define the parameters of the window that pops up
    when 'create planning unit is pressed'''

    def __init__(self, theMaster):
        '''Initializes the PlanningUnitWindow

        master should be an SGOMS_GUI'''

        print "(PlanningUnitWindow initiated)"
        tk.Toplevel.__init__(self,theMaster)
        self.master = theMaster
        #t = tk.Toplevel(theMaster)
        #self.t = t

        #Frame.__init__(self)
        #self.pack()
        self.createWidgets()

    def createWidgets(self):
        '''Create the widgets for the PlanningUnitWindow'''

        print "(PlanningUnitWindow.createWidgets)"
        ##Create and place the text entry boxes
        self.eOne = tk.Entry(self)
        self.eOne.grid(row=0, column=1)

        #self.eTwo = tk.Entry(self)
        #self.eTwo.grid(row=1, column=1)
        print "(PlanningUnitWindow) text entries created"

        ##Create and place the labels
        self.lOne = tk.Label(self, text = "Name of Planning Unit")
        self.lOne.grid(row=0, column=0)

        #self.lTwo = tk.Label(self, text = "RHS")
        #self.lTwo.grid(row=1, column=0)
        print "(PlanningUnitWindow) labels created"

        ##Create and place the button
        self.bOne = tk.Button(self)
        self.bOne["text"] = "Create Planning Unit"
        self.bOne["command"] = self.createPlanningUnit #Call a function that will create a new planning unit
        self.bOne.grid(row=1, column=0)

    def createPlanningUnit(self):
        '''Takes the text input from the entry boxes and creates a new planning unit'''

        print "(PlanningUnitWindow.createPlanningUnit)"
        var1 = self.eOne.get()
        #var2 = self.eTwo.get()

        newPlanningUnit = PlanningUnit(var1)
        self.master.model.addPlanningUnit(newPlanningUnit)

        #self.master.model.planningUnitCounter +=1
        #self.master.update()

        #Add the new Planning Unit to the tree by calling a function (instead of update)
        self.master.addPlanningUnitToTree(newPlanningUnit)
        #self.master.update()
        self.destroy()
                
class UnitTaskWindow(tk.Toplevel):
    '''A class to define the parameters of the window that pops up
    when 'Create Unit Task' is pressed'''

    def __init__(self, theMaster):
        '''Initializes the UnitTaskWindow

        master should be an SGOMS_GUI'''

        print "(UnitTaskWindow initiated)"
        tk.Toplevel.__init__(self,theMaster)
        self.master = theMaster

        self.checkList = [] ##The list to keep track of the checkboxes
        #t = tk.Toplevel(theMaster)
        #self.t = t

        #Frame.__init__(self)
        #self.pack()
        self.createWidgets()

    def createWidgets(self):
        '''Create the widgets for the UnitTaskWindow'''

        print "(UnitTaskWindow.createWidgets)"
        ##Create and place the text entry boxes
        self.eOne = tk.Entry(self)
        self.eOne.grid(row=0, column=1)

        print "(UnitTaskWindow) text entries created"

        ##Create and place the labels
        self.lOne = tk.Label(self, text = "Name of Unit Task")
        self.lOne.grid(row=0, column=0)

        self.lTwo = tk.Label(self, text = "Select Planning Unit(s):")
        self.lTwo.grid(row=1,column=0)

        print "(UnitTaskWindow) labels created"
       
        ##Create Check Buttons that display the currently created planning units
        counter = 0
        for item in self.master.model.planningUnitList:

            checkVar = tk.IntVar()
            c = tk.Checkbutton(self, text=self.master.model.planningUnitList[counter].ID, variable=checkVar)
            c.var = checkVar
            self.checkList.append(c)
            
            c.grid(row=counter+1, column=1)

            print "(UnitTaskWindow.createWidgets): create checkbutton for: ", item.ID

            counter += 1
            
        ##Create and place the 'Create Unit Task' button
        self.bOne = tk.Button(self)
        self.bOne["text"] = "Create Unit Task"
        self.bOne["command"] = self.createUnitTask #Call a function that will create a new unit task
        self.bOne.grid(row=0, column=counter+1)    

    def createUnitTask(self):
        '''Takes the text input from the entry boxes and creates a new Unit Task'''

        print "(UnitTaskWindow.createUnitTask) button pushed"
        #FDO self.master.model.printModelContentsAdvanced()
        
        textVar = self.eOne.get()

        newUnitTask = UnitTask(textVar) ## Initialize the basic new unit task here, but don't put it into the model yet

        self.master.model.printModelContentsAdvanced()
        
        ##Add the unit task to each selected Planning Unit, and to the master list of Planning Units
        counter = 0
        for item in self.master.model.planningUnitList: ##Each item in the planningUnitList should have a corresponding checkbutton
            print "XXXXX Create Unit Task Loop XXXXX, [counter] = ", counter, "(UnitTaskWindow.createUnitTask): Planning Unit ",\
                  item.ID, "'s unit task length = ", len(item.unitTaskList)
            if self.checkList[counter].var.get() == 1:  ##Right now the location of the checkbox corresponds to the index of the planning unit in the model's list
                print "(createUnitTask) checkList for ", self.master.model.planningUnitList[counter].ID, " was selected. [counter] = ",\
                      counter, " checkVar = ", self.checkList[counter].var.get()
                #item.unitTaskList.append(newUnitTask)

                #FDO print "State of the Model before explicitly adding the new Unit Task to ", item.ID, ":"
                #FDO self.master.model.printModelContentsAdvanced()
                item.addUnitTask(newUnitTask) ##This sets the current Planning Unit to be the new Unit Task's parent, by default

                newRelationship = self.master.model.addPUxUTRelationReturnSelf(item, newUnitTask) ## Creates a new relation, and appends to model's list

                self.master.addUnitTaskToTree(newRelationship) ## Update the GUI's tree, feed it a relationship

                #print "State of the Model after explicitly adding the new Unit Task to ", item.ID, ":"
                #FDO self.master.model.printModelContentsAdvanced() ##The problem is occuring before this point
                #newUnitTask.parentPlanningUnits.append(item)
                #newUnitTask.printParentPlanningUnits()
                counter += 1
            else:
                print "Else block tripped for ", self.master.model.planningUnitList[counter].ID, " [counter] = ", counter
                #FDOself.master.model.printModelContentsAdvanced()
                counter += 1
                continue
                

        ## If no Planning Unit is selected, add the new Unit Task to the Model's list anyways, without setting a parent Planning Unit
        ## Either way, the model should add the new Unit Task to the model's unitTaskList
        self.master.model.addUnitTask(newUnitTask)  ##Why do this here? - Because the Unit Task should be in the model even if it doesn't have a parent

        print "(UnitTaskWindow.createUnitTask) contents of the model: "
        self.master.model.printModelContentsAdvanced()

        #self.master.model.unitTaskCounter +=1
        #self.master.update()

        self.destroy()
        
        
root = tk.Tk()

model = SGOMS_Model()
testPU = PlanningUnit("TestPU")
testUT = UnitTask("TestUT")
testPU.addUnitTask(testUT)
model.addPlanningUnit(testPU)
model.addUnitTask(testUT, testPU)
model.addPUxUTRelationReturnSelf(testPU, testUT)

app = SGOMS_GUI(model, master=root)
app.mainloop()
root.destroy()


