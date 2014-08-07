'''
Created on Jun 13, 2014

@author: Matthew Martin

This is an Extension of SimpleGraph1, where I include multiple JPanels into my Frame

I refactored the code on June 25, making the PUs and UTs 'dumber',
moving all the 'smart' functionality to SGOMS_Model to reduce moving parts. 
'''

'''
## Old Sloppy Import Statements
from java.lang import System
from java.awt import *
from java.awt.event import *
from java.util import *
from javax.swing import *
'''

## New Shiny Import Statements
from javax.swing import JFrame
from javax.swing import JPanel
from javax.swing import JButton
from javax.swing import JLabel
from javax.swing import JTextField
from javax.swing import BorderFactory
from javax.swing import JMenu
from javax.swing import JMenuBar
from javax.swing import JMenuItem
from javax.swing import JDialog

from java.awt import Point
from java.awt import Color
from java.awt import FlowLayout
from java.awt import GridLayout
from javax.swing import BoxLayout

from java.awt.event import KeyEvent
from java.awt.event import KeyListener
from java.awt.event import MouseListener
from java.awt.event import MouseMotionListener

import os

########
# The SGOMS-Related model stuff from ACT-R_GUI-2 (As of 2014.06.17)
########

class PlanningUnit:
    '''An SGOMS Planning Unit that contains a list of Unit Tasks'''

    def __init__(self, theID="Planning Unit", theUnitTaskList=None, theFiringConditions=None, theBehaviour=None):
        '''Creates a PlanningUnit

        theID should be a string that identifies the Planning Unit
        theUnitTaskList should be a list of UnitTasks
        theFiringConditions should be a list of strings representing the states of relevant buffers
            required to fire the PU
        theBehaviour should be a list of strings representing the effect of the PU on various buffers /
            the environment (optional, can be done entirely via UTs or methods)'''

        self.ID = theID
        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == None:
            self.unitTaskList = []
            
        self.firingConditions = theFiringConditions
        if theFiringConditions == None:
            self.firingConditions = []  ## By default the firingConditions is an empty list, 
                                        ## to be populated by strings later, representing relevant context buffer info
                                        ## that is required to fire the planning unit production
                                        
        self.behaviour = theBehaviour
        if theBehaviour == None:
            self.behaviour = []         ## By default the behaviour is an empty list, 
                                        ## to be populated by strings later, representing relevant context buffer info
            ## By default, the behaviour of a Unit Task should be pass (for python syntax reasons)
            self.behaviour.append("pass")

        print "(PlanningUnit.__init__) Planning Unit Created: ", self.ID
        self.printPlanningUnitContents()
        
    def __str__(self):
        '''Returns a string representation of the Planning Unit'''
        
        return "PU: " + self.ID + " # of Unit Tasks: " + len(self.unitTaskList)

    def addUnitTask(self, theUnitTask):
        '''Adds theUnitTask to the Planning Unit,
        does not set the current Planning Unit to be the parent Planning Unit of the Unit Task

        theUnitTask should be a UnitTask'''

        self.unitTaskList.append(theUnitTask)

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
    
    def __init__(self, theID="Unit Task", theParentPlanningUnits=None, theFiringConditions=None, theBehaviour=None):
        '''Creates a Unit Task

        ID is a string that names the Unit Task
        theParentPlanningUnits should be a list of PlanningUnits
        theFiringConditions should be a list of strings that represent the firing conditions of a production
        theBehaviour should be a list of strings that represent the behaviour of a production'''

        self.ID = theID
        self.parentPlanningUnits = theParentPlanningUnits
        if theParentPlanningUnits == None:
            self.parentPlanningUnits = []   
            
        self.firingConditions = theFiringConditions
        if theFiringConditions == None:
            self.firingConditions = []    
            
        self.behaviour = theBehaviour
        if theBehaviour == None:
            self.behaviour = []
            ## By default, the behaviour of a Unit Task should be pass (for python syntax reasons)
            self.behaviour.append("pass")

        print "(UnitTask.__init__) Unit Task Created: ", self.ID,
        #self.printParentPlanningUnits()
        
    def __str__(self):
        '''Returns a string representation of the Unit Task'''
        
        return "UT: " + str(self.ID) + ", # of Parent PUs: " + str(len(self.parentPlanningUnits))

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

    def __init__(self, theID=0, thePlanningUnit=None, theUnitTask=None, theLocation=0):
        '''Initializes the relationship between thePlanningUnit and theUnitTask

        theID should be a unique integer (or possibly string), each relation's ID must be unique
        thePlanningUnit should be a single PlanningUnit that contains theUnitTask in its unitTasklist
        (Or can be None by default, representing an unconnected Unit Task)
        theUnitTask should be a single UnitTask with thePlanningUnit as a parent Planning Unit
        theLocation represents the location/order of the Unit Task within the Planning Unit'''

        self.ID = theID 
        self.planningUnit = thePlanningUnit
        self.unitTask = theUnitTask
        self.location = theLocation ## The location of the unit task within the planning unit/tree
        if self.planningUnit == None:
            self.tuppleID = "PUxUTRelation", self.ID, None, self.unitTask.ID, self.location
        else:
            self.tuppleID = "PUxUTRelation", self.ID, self.planningUnit.ID, self.unitTask.ID, self.location

        print "(PUxUTRelation.init) Created: ", self.tuppleID
        
        #######################
        ## ACT-R related stuff
        #######################
        ## Each Planning Unit in SGOMS is represented by a series of chunks in DM that contains info about:
        ## The Planning Unit the Unit Task belongs to, the associated Unit Task, the cue to fire the Unit Task
        ## and the 'cuelag'- the cue of the previous Unit Task (following the Rooster's model)
        ## the cuelag is the previous cue ('none' if no previous cue)
        ## the cue is the previous unit_task ('start' if no previous unit_task). E.g.
        ## DM.add ('planning_unit:prep_wrap    cuelag:none          cue:start          unit_task:veggies')
        ## DM.add ('planning_unit:prep_wrap    cuelag:start         cue:veggies        unit_task:finished')
        ##
        ## The PUxUTRelations will each have a string representation of the DM chunk to be outputed to ACT-R
        #######################
        
        ## Maintain some variables to populate the DM string
        
        if self.planningUnit != None:
            self.planning_unit_DM = self.planningUnit.ID
        else:
            self.planning_unit_DM = ''     ## This will not work in ACT-R, it is equivalent to None 
        
        self.cuelag_DM = 'none'
        self.cue_DM = 'start'
        
        if self.unitTask != None:
            self.unit_task_DM = self.unitTask.ID
        else:
            self.unit_task_DM = ''
            
        self.DM_string = 'planning_unit:' + self.planning_unit_DM + ' cuelag:' + self.cuelag_DM \
                        + ' cue:' + self.cue_DM + ' unit_task:' + self.unit_task_DM 
        
    def updateTuppleID(self):
        '''Updates the tuppleID, based on any changes made to the PUxUTRelation'''
        
        if self.planningUnit == None:
            self.tuppleID = "PUxUTRelation", self.ID, None, self.unitTask.ID, self.location
        else:
            self.tuppleID = "PUxUTRelation", self.ID, self.planningUnit.ID, self.unitTask.ID, self.location
            
        print "(PUxUTRelation.updateTuppleID) new ID:", self.tuppleID
        
    def updateDM_string(self):
        '''Updates the DM_string, based on any changes made to the PUxUTRelation'''
        
        self.DM_string = 'planning_unit:' + self.planning_unit_DM + ' cuelag:' + self.cuelag_DM \
                        + ' cue:' + self.cue_DM + ' unit_task:' + self.unit_task_DM
                        
        print "(PUxUTRelation.updateDM_string) new DM_string:", self.DM_string
        
        
##### The Model #####
        
class SGOMS_Model:
    '''The underlying model that the GUI runs on'''

    def __init__(self, thePlanningUnitList=None, theUnitTaskList=None, thePUxUTRelationList=None, theBufferList=None):
        '''The initializing method for the model

        planningUnitList should be a list of Planning Units
        unitTaskList should be a list of Unit Tasks'''

        print "SGOMS_Model initiated"

        self.planningUnitList = thePlanningUnitList
        if thePlanningUnitList == None:
            self.planningUnitList = []

        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == None:
            self.unitTaskList = []

        if thePUxUTRelationList == None:   
            self.pUxUTRelationList = []
            
        if theBufferList == None:
            self.bufferList = []
            
        ## The default buffers that every SGOMS_Model must have
        self.bufferList.append("buffer_context")
        self.bufferList.append("buffer_DM")
        self.bufferList.append("buffer_planning_unit")
        self.bufferList.append("buffer_unit_task")
        self.bufferList.append("buffer_method")
        self.bufferList.append("buffer_operator")

        
        ## A counter to keep track of the number of relations in the model
        ## Is used as a unique ID of each relation
        self.relationCounter = 0
        
        ## The initial behaviour for ACT-R must be set somewhere
        ## This will be a list of strings
        self.initialBehaviour = []
        self.initialBehaviour.append("pass")
        
    def __str__(self):
        '''Prints a string representation of the SGOMS_Model'''
        
        return "SGOMS_Model with " + str(len(self.planningUnitList)) + " Planning Units, " + \
            str(len(self.unitTaskList)) + " Unit Tasks, and " + str(len(self.pUxUTRelationList)) + "PUxUT Relations"
            

    def addPlanningUnit(self, thePlanningUnit):
        '''Adds thePlanningUnit to the planningUnitList,
        and updates the planningUnitCounter to be the length of the Planning Unit list.

        thePlanningUnit should be a PlanningUnit'''

        self.planningUnitList.append(thePlanningUnit)

        print "(Model.addPlanningUnit): ", thePlanningUnit.ID, " added. Total number of Planning Units in the model = ", len(self.planningUnitList)

    def addUnitTask(self, theUnitTask, theParentPlanningUnit=None):
        '''Adds theUnitTask to self.unitTaskList,
        Adds the Unit Task to theParentPlanningUnit (if supplied)
        Also sets theParentPlanningUnit to be the parent Planning Unit of theUnitTask, if supplied
        (Function prevents adding of duplicate Parent Planning Units to the unit task's list)
        There is no requirement for the Unit task to belong to a PlanningUnit

        theUnitTask should be a UnitTask
        thePlanningUnit should be a PlanningUnit'''

        self.unitTaskList.append(theUnitTask)
        
        ## If there is a Parent Planning Unit supplied
        if theParentPlanningUnit != None:
            ## Append the unit task to the Parent Planning Unit (do not prevent duplicates)
            theParentPlanningUnit.unitTaskList.append(theUnitTask)
            
            ## Prevent duplicate entries of Parent PUs while adding the Parent to the list
            if theParentPlanningUnit not in theUnitTask.parentPlanningUnits:
                theUnitTask.parentPlanningUnits.append(theUnitTask)

        print "(Model.addUnitTask): ", theUnitTask.ID, " added. Total number of Unit Tasks in the model = ", len(self.unitTaskList)
        
    def addUnitTaskToPlanningUnit(self, theUnitTask, thePlanningUnit):
        '''Adds theUnitTask to thePlanningUnit's list of unit tasks, not preventing duplicates
        Adds thePlanningUnit to theUnitTask's list of Parent Planning Units, while preventing duplicates
        
        theUnitTask should be a UnitTask
        thePlanningUnit should be a PlanningUnit'''
        
        thePlanningUnit.unitTasks.append(theUnitTask)
        
        if thePlanningUnit not in theUnitTask.parentPlanningUnits:
            theUnitTask.parentPlanningUnits.append()
            
        print "(SGOMS_Model.addUnitTaskToPlanningUnit) ", theUnitTask.ID, " added to", thePlanningUnit.ID

    def addPUxUTRelationReturnSelf(self, theUnitTask, thePlanningUnit=None,  theLocation=0):
        '''Creates a relationship between thePlanningUnit and theUnitTask at the location given,
        and adds it to the list of relationships. 

        theUnitTask should be a UnitTask
        thePlanningUnit should be a PlanningUnit (but can be None by default)
        theLocation should be an Integer, representing the order of the UT within the PU'''

        ## self.relationCounter assigns a unique ID to each relation (the first parameter of a Relation)
        r = PUxUTRelation(self.relationCounter, thePlanningUnit, theUnitTask, theLocation)

        self.pUxUTRelationList.append(r)
        self.relationCounter += 1   

        print "(Model.addPUxUTRelation) Adding to list : ", r.tuppleID
        
        return r

    def printModelContentsBasic(self):
        '''Print the IDs of all Planning Units and Unit Tasks in the Model'''

        ## Planning Units
        print "(printModelContentsBasic), Planning Units:"
        if len(self.planningUnitList) > 0:
            print "There are ", len(self.planningUnitList), " Planning Units in the Model:"
            for item in self.planningUnitList:
                print item.ID
        else:
            print "There are no Planning Units in the Model"

        ## Unit Tasks
        print "(printModelContents), Unit Tasks:"
        if len(self.unitTaskList) > 0:
            print "There are ", len(self.unitTaskList), " Unit Tasks in the Model:"
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
            print "There are ", len(self.planningUnitList), " Planning Units in the Model:"
            for item in self.planningUnitList:
                item.printPlanningUnitContents()
        else:
            print "There are no Planning Units in the Model"

        print "Unit Tasks:"
        if len(self.unitTaskList) > 0:
            print "There are ", len(self.unitTaskList), " Unit Tasks in the Model:"
            for item in self.unitTaskList:
                print item
        else:
            print "There are no Unit Tasks in the model"

        print "(printModelContents), PUxUTRelations:"
        if len(self.pUxUTRelationList) > 0:
            print "There are ", len(self.pUxUTRelationList), " PUxUTRelationships in the Model:"
            for item in self.pUxUTRelationList:
                print item.tuppleID
                print item.DM_string
        else:
            print "There are no PUxUTRelationships in the Model"

        print "==== End of (printModelContentsAdvanced) ===="    
        
    def getPrecedingRelations(self, theRelation):
        '''Returns a list of PUxUTRelations that have a location of theRelation-1
        
        theRelation should be a PUxUTRelation contained in self.pUxUTRelationList'''
               
        returnList = []
        
        ## If they belong to the same planning unit, and item.location is theRelation-1, add to returnList
        for item in self.pUxUTRelationList:
            if item.planningUnit == theRelation.planningUnit and item.planningUnit !=None:
                if item.location == theRelation.location-1:
                    returnList.append(item)
        
        print "(SGOMS_Model.getPrecedingRelations)", theRelation.ID, "found ", len(returnList), "preceding relations"
        return returnList
    
    def getSucceedingRelations(self, theRelation):
        '''Returns a list of PUxUTRelations that have a location of theRelation+1
        
        theRelation should be a PUxUTRelation contained in self.pUxUTRelationList''' 
        
        returnList = []
        
        ## If they belong to the same planning unit, and item.location is theRelation-1, add to returnList
        for item in self.pUxUTRelationList:
            if item.planningUnit == theRelation.planningUnit and item.planningUnit !=None:
                if item.location == theRelation.location+1:
                    returnList.append(item)
        
        print "(SGOMS_Model.getSucceedingRelations)", theRelation.ID, "found ", len(returnList), "succeeding relations"
        return returnList
        
    def updateRelation(self, theRelation):
        '''Takes a relation and updates its planning_unit_DM, cuelag, cue, unit task, and DM string
        based on its preceding relation in self.pUxUTRelationList
        
        theRelation should be a PUxUTRelation that is contained within self.pUxUTRelationList'''
        
        print "(SGOMS_Model.updateRelation), update: ", theRelation.ID
        
        precedingRelations = self.getPrecedingRelations(self)   ## Returns a list of preceding relations
        
        ## Set the planning_unit_DM string, regardless if there are preceding relations
        if theRelation.planningUnit != None:
            theRelation.planning_unit_DM = theRelation.planningUnit.ID
        
        ## Set the unit_task_DM string, regardless if there are preceding relations
        if theRelation.unitTask != None:
            theRelation.unit_task_DM = theRelation.unitTask.ID
        
        ## Set the cue to be 'start' if theRelation's location is 0, and the culag to be 'none'
        if theRelation.location == 0:
            print "(SGOMS_Model.updateRelation) self.location == 0"
            ## Set the cuelag to 'none'
            self.pUxUTRelation.cuelag = 'none'
            ## Set the cue ('start' if location = 0)
            self.pUxUTRelation.cue_DM = 'start'
        
        if len(precedingRelations) > 0: ## If there are preceding relations...
            print "(SGOMS_Model.updateRelation) self.location is not 0, setting cue etc."
            #FDO print "(SGOMS_Model.updateRelation) preceding relation = ", precedingRelations[0]
            #FDO print "(SGOMS_Model.updateRelation) preceding relations's cue_DM = ", precedingRelations[0].cue_DM 
            self.pUxUTRelation.cuelag_DM = precedingRelations[0].cue_DM ## Pick an arbitrary node for now
            #FDO print "(UTNode.updateRelation) self.cuelag=", self.pUxUTRelation.cuelag_DM
            self.pUxUTRelation.cue_DM = precedingRelations[0].unitTask.ID
            
        theRelation.updateTuppleID()
        theRelation.updateDM_string()
        

    ########## Write to ACT-R ##########

    def outputToACTR(self):
        '''Takes what is in the model and outputs it into Python ACT-R readable code'''

        directory = os.getcwd()
        print "(SGOMS_Model.outputToACTR) Directory = " + directory

        f = open("TestWriting.py", "w")  ## Open a new file for writing

        ## Write the basic import statements
        f.write("import sys\n")
        f.write("sys.path.insert(0, 'C:/CCMSuite/CCMSuite/')\n")
        
        f.write("import ccm\n")
        f.write("log=ccm.log()\n")
        f.write("from ccm.lib.actr import *\n\n")

        ## Write the environment statements
        f.write("class MyEnvironment(ccm.Model):\n")
        f.write("   pass\n\n")

        ## Write the Agent
        f.write("class MyAgent(ACTR):\n")
        f.write("    b_context=Buffer()\n")
        f.write("    b_plan_unit=Buffer()\n")                        ## There is a planning unit buffer which keeps track of the relevant planning unit                       
        f.write("    b_unit_task=Buffer()\n")
        f.write("    b_DM=Buffer()\n")
        f.write("    DM=Memory(b_DM)\n\n")

        ## Write the init method, adding chunks to DM
        f.write("    def init():\n")
        for relation in self.pUxUTRelationList:
            f.write("        DM.add('" + relation.DM_string + "')\n")
        ## How to handle the final unit task?
        ## ^We are going to have default values for UT and cue that the user can change if they want
        
        ## For syntax reasons, there should be a pass by default at the end of each function
        #f.write("        pass    ## Required for Python syntax reasons when there are no Unit Tasks in the Model")
        
        ## Write the initial behaviour of the model
        
        f.write("\n\n##Initial Model Behaviours\n")
        
        if len(self.initialBehaviour) < 1:
            f.write("        pass\n")
        for behaviour in self.initialBehaviour:
            f.write("        " + behaviour + "\n")
            
        ## For syntax reasons, there should be a pass by default at the end of each function
        #f.write("        pass    ## Required for Python syntax reasons when there are no Unit Tasks in the Model")
        
                      
        ## Write the Planning Unit Productions
        f.write("    \n## Planning Units\n")
        for planningUnit in self.planningUnitList:
            f.write("\n    def " + planningUnit.ID + "(")
            for firingCondition in planningUnit.firingConditions:
                f.write(firingCondition + ",\n")
                
            f.write("):\n")
            for behaviour in planningUnit.behaviour:
                f.write("        " + behaviour + "\n")
                
        ## For syntax reasons, there should be a pass by default at the end of each function
        #f.write("        pass    ## Required for Python syntax reasons when there are no Planning Units in the Model")

        ## Write the Unit Task Productions
        f.write("    \n## Unit Tasks\n")
        for unitTask in self.unitTaskList:
            f.write("\n    def " + unitTask.ID + "(")
            for firingCondition in unitTask.firingConditions:
                f.write(firingCondition + ",\n") 
            f.write("):\n")
            for behaviour in unitTask.behaviour:
                f.write("        " + behaviour + "\n")
                
        ## Write the general productions that handle choosing 
        
        f.write("\n## Global productions for retrieving Unit Tasks from DM\n\n")
        
        ## Request Next Unit Task
        f.write("    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit " \
                + "cuelag:?cuelag cue:?cue unit_task:?unit_task state:running', " \
                + "b_unit_task='unit_task:?unit_task state:finished'):\n")
        f.write("        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')\n")
        f.write("        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag " \
                + "cue:?cue unit_task:?unit_task state:retrieve')\n\n")
        
        ## Retrive Next Unit Task
        f.write("    def retrieve_next_unit_task(b_plan_unit='state:retrieve', " \
                                + "b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):\n")
        f.write("        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag " \
                + "cue:?cue unit_task:?unit_task state:running')\n")
        f.write("        b_unit_task.set('unit_task:?unit_task state:start')\n\n")
        
        ## Last Unit Task
        f.write("    def last_unit_task(b_unit_task='unit_task:finished state:start', " \
                       + "b_plan_unit='planning_unit:?planning_unit'):\n")
        f.write("        b_unit_task.set('stop')\n\n")
        
        ########### Not sure what to do about setting the context at end of PU, how to make general?
        #f.write("        b_context.set('customer:new order:wrap status:prepped done:?planning_unit')\n\n")


        ## Write the code to run the model

        f.write("## Code to run the model\n")
        f.write("tim = MyAgent()\n")
        f.write("env = MyEnvironment()\n")
        f.write("env.agent = tim\n")
        f.write("ccm.log_everything(env)\n\n")

        f.write("env.run()\n")
        f.write("ccm.finished()\n")
        
        f.close()

#######
# The Graph-Related model stuff from the Java tutorial
#######

class Node:
    '''Defines the model node'''
    
    RADIUS = 15
    
    def __init__(self, aLabel = "Node", aLocation = None, theIncidentEdges = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string 
        aLocation should be a Point
        theIncidentEdges should be a list of Edges'''   
        
        self.label = aLabel
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
            
        self.rootNode = False  ## By default, a node is not the root
        self.selected = False  ## Indicates whether the node is selected or not
        self.recursed = False  ## A flag for using recursive functions such as getRootNode()
        
        ## Specifies the default order within the planning unit (distance from the root)
        orderVar = self.getHopsToRootNode()  ## Returns none if no root node
        if orderVar == None:    ## If can't find a root node, it's order is by default zero
            self.order = 0
        else:
            self.order = orderVar   
        #self.everyConnectedNode = []  ## A list for keeping track of nodes recursed over during getRootNode()
    
    def __str__(self):
        '''Returns a string representing the Node as label (x,y)'''
        
        return self.label + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
    
    def toggleSelected(self):
        '''Changes the selected boolean to True/False depending on previous state'''
        
        self.selected = not self.selected
        
        '''
        if self.selected == False: 
            self.selected = True
        else:
            self.selected = False
        '''
            
        print "(Node.toggleSelected) selected = ", self.selected
            
    def addIncidentEdge(self, theIncidentEdge):
        '''Adds theIncidentEdge to the list of incidentEdges'''
        
        self.incidentEdges.append(theIncidentEdge)
        
    def returnNeighbourNodes(self):
        returnList = []
        
        for edge in self.incidentEdges:
            returnList.append(edge.otherEndFrom(self))
            
        return returnList
    
    def returnUnvisitedNeighbourNodes(self):
        '''Returns each neighbour node where recursed == False
        Used in recursive functions such as getHopsToRootNode()'''
        
        returnList = []
        
        for edge in self.incidentEdges:
            if edge.otherEndFrom(self).recursed == False:
                returnList.append(edge.otherEndFrom(self))
        
        #for item in returnList:
        #    item.recursed = True
        return returnList
    
    def update(self):
        '''Updates the Node
        
        calls self.updateOrder()'''
        
        print "(Node.update)"
        self.updateOrder()
    
    def updateOrder(self):
        '''Updates self.order based on the distance to root node'''
        
        print "(Node.updateOrder)"
        orderVar = self.getHopsToRootNode() ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
    
    def getRootNode(self):
        '''Returns the root node of the hierarchy. 
        Returns None if there is no root node'''
        
        if self.rootNode == True:   ## If self is the root node, return self
            print "(Node.getRootNode) ", self.label, " (self is the root node)"
            return self
        
        nodes = self.getEveryConnectedNode()
        
        ## If there are no connected nodes, return none
        if len(nodes) < 1:
            print "(Node.getRootNode) There is no root node"
            return None
        
        for item in nodes:
            if item.rootNode == True:
                print "(Node.getRootNode) ", item.label, " is the root node"
                return item
        
        ## If the search did not find ahy root nodes, return none
        print "(Node.getRootNode) there are no root nodes connected to ", self.label
        return None

        
    '''def getRootNodeHelper(self, theNodeList, times=0):
        ##A recursive helper method for getRootNode

        for item in theNodeList:
            self.everyConnectedNode.append(item)
                
        ## Print the recursive level 
        print "---------- Level", times+1, "----------"

        ## This is the check for end state, if the root node is in theNodeList, return the Root Node
        for item in theNodeList:
            if item.rootNode == True:
                print "(Node.GetRootNodeHelper) Root node found: ", item.label
                return item
        
        ## This is the check for end state, if it has gone 20 times, the function ends and returns None
        if times > 19:
            print ("(Node.getRootNodeHelper) Recursed 20 times, returning False")
            return None
        
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been activated, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            for thing in tempList:
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        self.getRootNodeHelper(passList,times+1)
    '''
    
    def getHopsToRootNode(self):
        '''Returns the number of hops away from the root node the current node is (as an int)
        Calls getHopsToRootNodeHelper
        
        Returns 0 if self is the root
        Returns None if self is not the root, and self is not connected to anything
        Returns None if self is connected to other nodes, but none are the root (returns value from helper)
        Returns an int if self is connected to a root, int is how many hops away self is
        
        E.g. nodes a(root) --> b --> c
        c.getHopsToRootNode() --> returns 2'''
               
        #everyConnectedNode = [] ## The list to keep track of each connected node
        
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        everyConnectedNode = [] ## The list to keep track of each connected node
                
        ## Return zero if the self is the root
        if self.rootNode == True:
            print "(Node.getHopsToRootNode) ", self.label, " is the root node"
            return 0
        
        ## Return None if there are no neighbour nodes (i.e. throw an exception)
        if len(nodeList) < 1:
            print "(Node.getHopsToRootNode) ", self.label, " is not connected to anything"
            return None
        
        self.recursed = True  ## Prevent the function from finding itself
        
        ## This is the recursive call to the helper method, stores the return value in returnVar
        returnVar = self.getHopsToRootNodeHelper(nodeList, everyConnectedNode)
        
        print "(Node.getHopsToRootNode) hops to root node from", self.label, "=", returnVar
        self.recursed = False   ## Reset the recursed flag to False at the end
        return returnVar
        
        
        
    def getHopsToRootNodeHelper(self, theNodeList, everyConnectedNode, times=0):
        '''Helper method for getHopsToRootNode
        Returns the number of hops away from the root node the current node is
        Returns None if it exhausts the nodes connected to self, and finds no root
        
        theNodeList is basically a list of connected nodes to recurse over in order to find more nodes
        it is populated by the function returnUnvisitedNeighbourNodes()
        nodes that have been found by this function have their recursed flag set to true, to avoid recursing infinitely
        
        everyConnectedNode keeps track of every node found by the search,
        so that every node's 'recursed' flag can be reset at the end of the function
        
        times keeps track of the recursive level, and by proxy the distance from the initial node the function is'''

        ## Set every node in theNodeList's recursed flag to True, 
        ## in order to prevent nodes from finding previous nodes, and recursing infinitely
        for item in theNodeList:
            item.recursed = True
            ## Keep track of every node found by the function so that their flags can be reset at the end
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                    
        ## Print the recursive level 
        print "---------- Level", times+1, "----------"
       
        ## This is the check for end state, if it has gone 20 times, the function ends and returns None
        ## This function is for testing purposes only, it should not be tripped under normal circumstances
        ## This is basically like throwing an exception, it stops an infinite loop if something goes wrong
        if times > 19:
            ## Reset each recursed flag back to False before returning
            for thing in everyConnectedNode:
                    thing.recursed = False
            print ("(Node.getRootNodeHelper) Recursed 20 times, returning None")
            return None
        
        ## Another check for the end state, if it has found the root node, return the # of hops
        ## (each item in theNodeList is one hop away from the previous node, so hops = times +1)
        for item in theNodeList:
            if item.rootNode == True:   ## If it has found a root
                ## Reset each recursed flag back to False before returning
                for thing in everyConnectedNode:
                    thing.recursed = False
                return times+1      ## Return # of hops
        
        ## Now we get into the 'guts' of the function
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been activated, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            print "Length of tempList on times", times, len(tempList)
                       
            for thing in tempList:
                print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## and it has not found a root node, return None (throw an exception)
        if len(passList) < 1:
            print "(Node.getHopsToRootNodeHelper) passList is empty, returning None"
            ## Reset the recursed flags
            for item in everyConnectedNode:
                #print item.label
                item.recursed = False
                #if item not in returnList:
                #    returnList.append(item)
                #    print "appending happened ok"
            #FDO print "helper returnlist", str(returnList)
            return None
        
        #FDO print "hi"        
        return self.getHopsToRootNodeHelper(passList, everyConnectedNode, times+1)     
        
    def getEveryConnectedNode(self):
        '''Returns a list of all nodes that the current node is (indirectly) connected to
        Returns an empty list if there are no connected nodes
        
        Eg. Nodes a --> b --> c
        c.getEveryConnectedNode() --> returns [a, b]'''
       
        self.recursed = True  ## Prevent the function from finding itself
        
        everyConnectedNode = [] ## The list to keep track of each connected node
        
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        ## Return empty list if there are no neighbour nodes 
        if len(nodeList) < 1:
            print self.label, " is not connected to anything"
            self.recursed = False   ## Reset the recursed variable before returning
            return nodeList
       
        
        ## This is the recursive call, the helper should return a list of every connected node
        returnList = self.getEveryConnectedNodeHelper(nodeList, everyConnectedNode)
        
        ## (obsolete) Create a list to put non-duplicate connected nodes into
        #for item in self.getEveryConnectedNodeHelper(nodeList, everyConnectedNode):
        #    print "(getEveryConnectedNode) item in helper return:", item.label
        #    if item not in returnList:
        #        returnList.append(item)

        #print "last call", str(returnList)
        
        #returnList = self.getEveryConnectedNodeHelper(nodeList, everyConnectedNode)
        print "(Node.getEveryConnectedNode) returnlist = ", str(returnList)
        self.recursed = False   ## Reset the recursed variable before returning
        
        return returnList

    def getEveryConnectedNodeHelper(self, theNodeList, everyConnectedNode, times=0):
        '''A helper method for the recursive getEveryConnectedNode() method
        
        functions essentially the same as getHopsToRootNodeHelper(), except it returns
        everyConnectedNode, rather than the # of hops
        
        theNodeList is basically a list of connected nodes to recurse over in order to find more nodes
        it is populated by the function returnUnvisitedNeighbourNodes()
        nodes that have been found by this function have their recursed flag set to true, to avoid recursing infinitely
        
        everyConnectedNode keeps track of every node found by the search,
        so that they can be returned at the end of the function, and so that their recursed flags can be reset 
        
        times keeps track of the recursive level, and by proxy the distance from the initial node the function is'''
        
        for item in theNodeList:
            item.recursed = True    ## Prevent the function from finding itself
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                
        ## Print the recursive level 
        print "---------- Level", times+1, "----------"
       
        ## This is the check for end state, if it has gone 20 times, the function ends and returns None
        if times > 19:
            print "(Node.getRootNodeHelper) Recursed 20 times, returning False"
            return None
                
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been found, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            print "Length of tempList on times", times, len(tempList)
            
                       
            for thing in tempList:
                print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## return the list of every connected node
        if len(passList) < 1:
            print "passList is empty, returning everyConnectedNode:"
            for item in everyConnectedNode:
                print item.label
                item.recursed = False   ## Reset the recursed flag back to false for every node found
            
            return everyConnectedNode
            
        ##FDO print "hi"        
        return self.getEveryConnectedNodeHelper(passList, everyConnectedNode, times+1)
    
    def draw(self, aPen):
        '''Draws the node
        
        aPen should be a Graphics object'''
                        
        #Draw a black border around the circle
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - Node.RADIUS, self.location.y - Node.RADIUS, Node.RADIUS * 2,
                      Node.RADIUS * 2)
        
        #Draw a blue-filled circle around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.blue)
        aPen.fillOval(self.location.x - self.RADIUS, self.location.y - self.RADIUS, self.RADIUS * 2,
                      self.RADIUS * 2)
        
        # Draw a label at the top right corner of the node (including its label, and order)
        aPen.setColor(Color.black)
        stringVar = self.label + "," + str(self.order)
        aPen.drawString(stringVar, self.location.x + self.RADIUS, self.location.y - self.RADIUS)
        
    
    def printNode(self):
        '''Prints the node as: label(x,y)'''
        
        print self.label, "(", self.location.x, ",", self.location.y, ")" 
        
class PUNode(Node):
    '''Specifies the behaviour/appearance of a PlanningUnitNode (PUNode)
    
    PUNode inherits from Node
    Each PUNode will point to a unique underlying PlanningUnit'''
    
    HEIGHT = 40
    WIDTH = 50
    
    def __init__(self, aLabel = "PUNode", aLocation = None, theIncidentEdges = None, thePU = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string, by default it is the Label of thePU (if one is provided)
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        thePU should be a PlanningUnit
        
        A blank PU is not created by default, it should be passed in only'''
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
        
        ## 2014.06.26 - We are not going to create a blank PU on initialization,
        ## by default the PU will remain None
        ## when created by Graph.addPUNode, Graph will supply the PU and add to SGOMS_Model
        #if thePU == None:
            ## This needs to be added to the SGOMS_Model somehow!!!
        #    self.planningUnit = PlanningUnit()
        #else:
        #    self.planningUnit = thePU
        
        self.planningUnit = thePU
        
        if aLabel == "PUNode" and self.planningUnit != None:
            self.label = self.planningUnit.ID
        else:
            self.label = aLabel 

        self.selected = False   ## Indicates whether the node is selected or not
        self.rootNode = True    ## Specifies whether the node is the root node (PUs are by default the root)
        self.recursed = False
        self.order = 0
        
        
        print "(PUNode) initiated, ", self 
        
    def __str__(self):
        '''Returns a string representation of the PUNode
        
        looks like: PUNode: label PU: PU.ID (x,y)'''
        
        return "PUNode: " + self.label \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
                
    def update(self):
        '''Updates the PUNode, based on any changes to the graph
        Calls updateOrder() and updatePU()'''
        
        print "(", self.label, ".update)"
        
        self.updateOrder()
        self.updatePU()
         
    def updatePU(self):
        '''Updates the PUNode, based on which nodes are connected to it
        Adds the UT of each connected UTNode to the PU's list of UTs
        
        This basically resets the PU contents each time it is called
        based on the nodes the PUNode is connected to
        The function is primarily concerned with connecting UTNodes to PUNodes'''
        
        print "(PUNode: ",self.label,".updatePU)"
        
        ## I believe this is the syntax for clearing a list in python
        del self.planningUnit.unitTaskList[:]
        
        connectedNodes = self.getEveryConnectedNode()
        
        ## We are not adding anything to SGOMS model here, we are only modifying what already exists
        ## e.g. no UnitTasks or PlanningUnits are being deleted or added to the SGOMS lists
        ## We are also only worried about the PU contents, the relations can worry about themselves elsewhere
        ## The list of unit tasks in the PlanningUnit is 'semi-ordered', i.e. each instance of a UT is
        ## represented in the UnitTaskList, but the order is not important (order is represented by relations
        for node in connectedNodes:
            ## Check to make sure the connected node in question is a UTNode
            if isinstance(node, UTNode):
                ## Add the UTNode's UT to the PUNode's PU
                self.planningUnit.addUnitTask(node.pUxUTRelation.unitTask)
        
    def draw(self, aPen):
        '''Draws the PUNode
        
        aPen should be a Graphics object'''
                        
        #Draw a black border around the rectangle
        aPen.setColor(Color.black)
        aPen.fillRect(self.location.x - int(PUNode.WIDTH/2), self.location.y - int(PUNode.HEIGHT/2), PUNode.WIDTH,
                      PUNode.HEIGHT)
        
        #Draw a blue-filled rectangle around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.blue)
        aPen.fillRect(self.location.x - int(PUNode.WIDTH/2), self.location.y - int(PUNode.HEIGHT/2), PUNode.WIDTH,
                      PUNode.HEIGHT)
        
        # Draw a label at the top right corner of the node
        aPen.setColor(Color.black)
        aPen.drawString(self.label, self.location.x + int(PUNode.WIDTH/2), self.location.y - int(PUNode.HEIGHT/2))
        
class UTNode(Node):
    '''Specifies the behaviour/appearance of a UTNode
    
    UTNode inherits from Node
    Each UTNode points directly to a unique underlying PUxUTRelation'''
    
    RADIUS = 20
    
    def __init__(self, aLabel = "UTNode", aLocation = None, theIncidentEdges = None, thePUxUTRelation = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string, by default it is the Label of theUT  
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        thePUxUTRelation should be a PUxUTRelation
        
        A blank PUxUTRelation is not created by default, it should be passed in only'''
        
        self.selected = False  ## Indicates whether the node is selected or not
        self.rootNode = False  ## Indicates whether the node is the root node (false by default for UTNodes)
        self.recursed = False  ## A flag for recursive functions to use    
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
                
        self.label = aLabel
            
        ## Specifies the distance from the root (i.e. distance to connected PlanningUnitNode)
        orderVar = self.getHopsToRootNode() ## Returns none if no connected root node
        if orderVar == None:    ## If can't find a root node, order = 0
            self.order = 0
        else:
            self.order = orderVar
        
        ## An empty PUxUTRelation is created by default, to be populated later
        ## This needs to be added to the SGOMS_Model somehow
        self.pUxUTRelation = thePUxUTRelation
        
        ## We are assuming that the root is a PUNode
        #if thePUxUTRelation == None:    ## If there is no Relation specified
        #    root = self.getRootNode()
        #    if root != None or self:  ## And there is a rootNode (i.e. a PU)
        #        self.pUxUTRelation = PUxUTRelation("R",root.planningUnit,self.unitTask)
        
        print "(UTNode) initiated, ", self 
    
    def __str__(self):
        '''Returns a string representation of the UTNode'''
        
        return "UTNode: " + self.label \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
    
    def returnRelation(self):
        '''Returns the PUxUTRelation of the node, if it exists, returns None if none is specified'''
        
        return self.pUxUTRelation
    
    def returnUnitTask(self):
        '''Returns the UnitTask'''
        
        return self.pUxUTRelation.unitTask
    
    def getPrecedingUTNodes(self):
        '''Returns a list of nodes where the node's order is self.order -1
        '''
        
        connectedNodes = self.getEveryConnectedNode()
        returnList = []
        
        for node in connectedNodes:
            if isinstance(node, UTNode):
                if node.order == self.order-1:
                    returnList.append(node)
                    
        print "(UTNode.getPrecedingUTNodes), returning: "
        for item in returnList:
            print item.label
        return returnList
    
    def update(self):
        '''Updates the Node
        
        calls self.updateOrder()
        and self.updateRelation()'''
        
        print "(UTNode:", self.label, ".update)"
        self.updateOrder()
        self.updateRelation()
    
    def updateOrder(self):
        '''Updates self.order based on the distance to root node'''
        
        print "(UTNode.updateOrder)"
        orderVar = self.getHopsToRootNode() ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
            
    def updateRelation(self):
        '''Updates self.pUxUTRelation based on the node's distance to the PU root
        
        Sets the relation's PU to be that of the PUNode's, none if there is no PUNode root
        Sets the relation's location to be hops to root node - 1, 0 if there is not PUNode root
        Sets the relation's planning_unit_DM, cuelag_DM, cue_DM, and unit_task_DM, based on the location
        Does not worry about the UT or PU lists in SGOMS
        Updates the relation's tuppleID and DM_string'''
        
        print "(", self.label, ".updateRelation)"
        
        
        root = self.getRootNode()
        
        ## If the root is a PUNode, assign the PU to the relation, and the relation's location is order-1
        if isinstance(root, PUNode):
            print "(UTNode.updateRelation) root is a PUNode"
            self.pUxUTRelation.planningUnit = root.planningUnit
            self.pUxUTRelation.location = self.order-1
            
            ## I'm not going to worry about Parent Planning Units anymore - 2014.06.27
            
            ### ACT-R Stuff ###
            ## Set the planning_unit_DM string
            self.pUxUTRelation.planning_unit_DM = root.planningUnit.ID
            
            ## Set the cuelag (previous relation's cue, 'none' if location = 0), 
            ###### This should probably be changed in future versions #######
            if self.pUxUTRelation.location == 0:
                print "(UTNode.updateRelation) self.location == 0"
                self.pUxUTRelation.cuelag = 'none'
                ## Set the cue ('start' if location = 0)
                self.pUxUTRelation.cue_DM = 'start'
            else:   ## If the location is not 0:
                print "(UTNode.updateRelation) self.location is not 0, setting cuelag etc."
                precedingNodes = self.getPrecedingUTNodes() ## A list of nodes with an order of self.order-1
                #FDO print "(UTNode.updateRelation) preceding node = ", precedingNodes[0]
                #FDO print "(UTNode.updateRelation) preceding node's cue_DM = ", precedingNodes[0].pUxUTRelation.cue_DM 
                self.pUxUTRelation.cuelag_DM = precedingNodes[0].pUxUTRelation.cue_DM ## Pick an arbitrary node for now
                #FDO print "(UTNode.updateRelation) self.cuelag=", self.pUxUTRelation.cuelag_DM
                self.pUxUTRelation.cue_DM = precedingNodes[0].pUxUTRelation.unitTask.ID
        
        else:   ## If there is no PUNode as a root, set the attributes back to their defaults
            print "(UTNode.updateRelation) there is no PUNode Root"
            self.pUxUTRelation.planningUnit = None
            self.pUxUTRelation.location = 0
            
            self.pUxUTRelation.planning_unit_DM = ''
            self.pUxUTRelation.cuelag_DM = 'none'
            self.pUxUTRelation.cue_DM = 'start'
            
        self.pUxUTRelation.unit_task_DM = self.pUxUTRelation.unitTask.ID
        
        self.pUxUTRelation.updateTuppleID()
        self.pUxUTRelation.updateDM_string()
        
        
        
        
    def draw(self, aPen):
        '''Draws the UTNode
        
        aPen should be a Graphics object'''
        
        '''
        ## Node syntax
        aPen.fillOval(self.location.x - Node.RADIUS, self.location.y - Node.RADIUS, Node.RADIUS * 2,
                      Node.RADIUS * 2)
        '''
                 
        #Draw a black border around the oval
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - UTNode.RADIUS, self.location.y - UTNode.RADIUS, UTNode.RADIUS * 2,
                      UTNode.RADIUS * 2)
        
        #Draw a green-filled oval around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.green)
        
        aPen.fillOval(self.location.x - UTNode.RADIUS, self.location.y - UTNode.RADIUS, UTNode.RADIUS * 2,
                      UTNode.RADIUS * 2)
        
        # Draw a label at the top right corner of the node
        # Label looks like: UT.label, order within PU
        aPen.setColor(Color.black)
        stringVar = str(self.pUxUTRelation.unitTask.ID) + ", ID:" + str(self.pUxUTRelation.ID) + \
        ", loc:" + str(self.pUxUTRelation.location) 
        aPen.drawString(stringVar, self.location.x + self.RADIUS, self.location.y - self.RADIUS)

class Edge:
    '''Defines the model edge'''
    
    def __init__(self, theStartNode, theEndNode, theLabel="Edge"):
        '''Initializes the Edge with a startnode and end node
        
        theStartNode should be a Node
        theEndNode should be a Node'''
        
        self.startNode = theStartNode
        self.endNode = theEndNode
        if theLabel == None:
            self.label = theStartNode.label + " --> " + theEndNode.label 
        else:
            self.label = theLabel
        
        self.selected = False
        
    def __str__(self):
        '''Returns label, startNode --> endNode'''
        
        return str(self.label) + " " + str(self.startNode.label) + " --> " + str(self.endNode.label)
    
    def toggleSelected(self):
        '''Changes the selected boolean to True/False depending on previous state'''
        
        self.selected = not self.selected
        
        '''
        if self.selected == False: 
            self.selected = True
        else:
            self.selected = False
        '''
            
        print "(Edge.toggleSelected) selected = ", self.selected
        
    def otherEndFrom(self, aNode):
        '''If given a node that the edge is connected to, returns the other node
        
        aNode should be a Node that the Edge is connected to'''
        
        if self.startNode == aNode:
            return self.endNode
        else:
            return self.startNode
        
    def returnMidpoint(self):
        '''Returns a point as a midpoint between the startNode and endNode'''
        
        mX = (self.startNode.location.x +
              self.endNode.location.x) / 2
            
        mY = (self.startNode.location.y +
              self.endNode.location.y) / 2
              
        midPoint = Point(mX,mY)
        return midPoint
                
    def draw(self, aPen):
        '''Draws the edge
        
        aPen should be a Graphics object'''
        
        #Draw a line from the center of he startNode to the center of the endNode (red if selected, black otherwise)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.black)
        aPen.drawLine(self.startNode.location.x, self.startNode.location.y,
                      self.endNode.location.x, self.endNode.location.y)
        aPen.fillRect(self.returnMidpoint().x - 3, self.returnMidpoint().y - 3,
                      6, 6)
        
    def printEdge(self):
        '''Prints the Edge as sNode(x,y) --> eNode(x,y)'''
        
        print self.startNode.label, "(", self.startNode.location.x, ",", self.startNode.location.y, ")", \
        " --> ", self.endNode.label, "(", self.endNode.location.x, ",", self.endNode.location.y, ")"
       
class Graph:
    '''Defines a collection of Nodes, Edges, and their behaviour'''
    
    def __init__(self, theLabel = "Graph", theNodes = None, theSGOMS_Model = None):
        '''Initializes the Graph, with a set of nodes and edges, as well as an SGOMS_Model
        
        theLabel should be a string
        theNodes should be a list of Nodes
        theSGOMS_Model should be an SGOMS_Model
        '''
        
        self.label = theLabel 
        
        if theNodes == None:
            self.nodes = []
        else:
            self.nodes = theNodes
        
        if theSGOMS_Model == None:
            self.SGOMS = SGOMS_Model()
        else:
            self.SGOMS = theSGOMS_Model
            
        #if theEdges == None:
        #    self.edges = []
        #else:
        #    self.edges = theEdges
    
    def __str__(self):
        '''Returns the Graph as label, (#of Nodes, #of Edges)'''
        
        return self.label + " (" + str(len(self.nodes)) + " nodes, " + str(len(self.returnEdges())) + " edges)"
    
    def returnEdges(self):
        '''Returns all Nodes contained in self.nodes'''
        
        returnList = []
        
        for node in self.nodes:
            for edge in node.incidentEdges:
                if edge not in returnList:
                    returnList.append(edge)
                    
        return returnList
    
    def returnSelectedNodes(self):
        '''Returns a list of all currently selected nodes'''
        
        returnList = []
        
        for node in self.nodes:
            if node.selected == True:
                returnList.append(node)
        return returnList
    
    def returnSelectedEdges(self):
        '''Returns a list of all currently selected edges'''
        
        returnList = []
        
        for e in self.returnEdges():
            if e.selected == True:
                returnList.append(e)
        return returnList
    
    def addNode(self, aNode):
        '''Adds a node to self.nodes
        
        aNode should be a Node
        
        2014.06.27- This '''
        
        self.nodes.append(aNode)
        
        self.update()
        
    def addNodeAdvanced(self, aLabel, aPoint):
        '''Creates a new node, with aPoint as its location, and aLabel as its label
        and adds the node to self.nodes'''
        
        node = Node(aLabel, aPoint)
        
        self.nodes.append(node)
        
        self.update()
        
    def addPUNode(self, aPUNode):
        '''Adds aPUNode to self.nodes
        adds the PUNode's PU to the SGOMS_Model
        
        aPUNode should be a PUNode, with an instantiated planning unit'''
        
        self.nodes.append(aPUNode)
        self.SGOMS.addPlanningUnit(aPUNode.planningUnit)
        
        self.update()
        
        print "(Graph.addPUNode),", aPUNode 
        
    def addPUNodeAdvanced(self, aLabel, aPoint):
        '''Creates a new PUNode, with aLabel and aPoint as the label and point of the PUNode
        Creates a blank PlanningUnit, which it will feed to the PUNode and add to self.SGOMS
        
        aLabel should be a string
        aPoint should be a Point
        '''

        pU = PlanningUnit(aLabel)
        pUNode = PUNode(pU.ID, aPoint, None, pU)
        
        self.nodes.append(pUNode)
        self.SGOMS.addPlanningUnit(pU)
        
        self.update()
        
        print "(Graph.addPUNodeAdvanced)", pUNode
        
    def addUTNode(self, aUTNode):
        '''Adds aUTNode to self.nodes
        adds aUTNode's relation to the SGOMS_Model
        adds aUTNode's UT to the SGOMS_Model
        
        aUTNode should be a UTNode, with an instantiated relation'''
        
        self.nodes.append(aUTNode)
        self.SGOMS.pUxUTRelationList.append(aUTNode.pUxUTRelation)
        self.SGOMS.addUnitTask(aUTNode.pUxUTRelation.unitTask)
        
        self.update()
        
        print "(Graph.addUTNode)", aUTNode
        
    def addUTNodeAdvanced(self, aLabel, aPoint):
        '''Creates new UTNode, with aLabel and aPoint as the label and point of the UTNode
        Creates a blank UnitTask and PUxUTRelation, the Unit Task will be fed to the PUxUTRelation
        The PUxUTRelation will be fed to the UTNode, and added to SGOMS
        The UTNode will be added to self.nodes
        
        By default, this function creates a unique UT to be fed to the relation and SGOMS Model
        
        I should make a new function in SGOMS that takes a PUxUTRelation, and adds it to the list,
        and maybe also adds the unit task to the unitTaskList at the same time
        ^Nope, want to be able to have same pointers to same UT, for duplicate UTs'''
        
        
        unitTask = UnitTask(aLabel)
        relation = self.SGOMS.addPUxUTRelationReturnSelf(unitTask)  ##This returns the new relation and stores it
        
        self.SGOMS.addUnitTask(relation.unitTask)   ## Adds the new UT to the list of Unit Tasks
        
        ## Add the new node
        uTNode = UTNode(aLabel, aPoint, None, relation)
        
        self.nodes.append(uTNode)
        
        self.update()
        
        print "(Graph.addUTNodeAdvanced)", uTNode
    
    def addUTNodeAdvancedNew(self, aUnitTask, aPoint):
        '''Creates new UTNode, with aUnitTask aPoint as the UnitTask and point of the UTNode
        Creates a blank PUxUTRelation, the Unit Task will be fed to the PUxUTRelation
        The PUxUTRelation will be fed to the UTNode, and added to SGOMS
        The UTNode will be added to self.nodes
        
        By default, this function creates a unique UT to be fed to the relation and SGOMS Model
        
        I should make a new function in SGOMS that takes a PUxUTRelation, and adds it to the list,
        and maybe also adds the unit task to the unitTaskList at the same time
        ^Nope, want to be able to have same pointers to same UT, for duplicate UTs'''
        
        relation = self.SGOMS.addPUxUTRelationReturnSelf(aUnitTask)  ##This returns the new relation and stores it
        
        self.SGOMS.addUnitTask(relation.unitTask)   ## Adds the new UT to the list of Unit Tasks
        
        ## Add the new node
        uTNode = UTNode(aUnitTask.ID, aPoint, None, relation)
        
        self.nodes.append(uTNode)
        
        self.update()
        
        print "(Graph.addUTNodeAdvancedNew)", uTNode
    
    def addEdge(self, startNode, endNode):
        '''Adds an edge to the Nodes' incident edges
        
        startNode should be a Node
        endNode should be a Node'''
        
        print "(Graph.addEdge)"
        
        anEdge = Edge(startNode, endNode)
        
        startNode.addIncidentEdge(anEdge)
        endNode.addIncidentEdge(anEdge)
        
        ## The start node is the one where the dragging comes from (see GraphEditor.mouseReleased)
        ## but need to check both nodes if they are UT nodes (connection can come from either direction)
        
        ## Check if one of the nodes is a UTNode, if a UTNode has been connected to another node,
        ## it needs to figure out if it is now indirectly connected to a PUNode
        if isinstance(startNode, UTNode):
            self.addEdgeHelper(startNode)
            
        if isinstance(endNode, UTNode):
            self.addEdgeHelper(endNode)
        
        self.update()
    
    def addEdgeHelper(self, theUTNode):
        '''Specifies behaviour for connecting UTNodes to another node
        Checks to see if the UTNode has been (indirectly) connected to a PUNode.
        If so, update the PUNode and UTNode accordingly.
        SGOMS does not need to 'add' anything new, but needs to modify what is already created 
        If not, no need to do anything
        
        aNode should be a UTNode'''
        
        print "(Graph.addEdgeHelper),", theUTNode.label
        
        root = theUTNode.getRootNode()  ## Will return a PUNode, if theUTNode is indirectly connected to it
                                        ## Returns None if not connected to a 'root' node
        theUTNode.updateOrder() ## Make sure the order is correct
        
        ## If the root is a PUNode:
        if isinstance(root, PUNode):
            print "(Graph.addEdgeHelper) root node is a PUNode"
            
            ## For every connected UTNode to the PUNode, adjust the relations etc. accordingly
            for uTNode in root.getEveryConnectedNode():
                if isinstance(uTNode, UTNode):  ## Make sure the node in question is a UTNode
                    uTNode.update()
            
            ## Update the PUNode accordingly
            root.update()
            
            '''
            ## For every connected UTNode to the PUNode, adjust the relations etc. accordingly
            for uTNode in root.getEveryConnectedNode():
                if isinstance(uTNode, UTNode):  ## Make sure the node in question is a UTNode
                    uTNode.pUxUTRelation.update()
            
            ## Update the PUNode accordingly
            #root.update()
            
            ## Append the UT in the PU's list (don't insert, to account for branching, the list is 'semi-ordered')
            root.planningUnit.unitTaskList.append(theUTNode.pUxUTRelation.unitTask)
            ## Set the UT's parent Planning Unit
            theUTNode.pUxUTRelation.unitTask.setParentPlanningUnit(root.planningUnit)
            ## Set the UTNode's relation to have the PUNode's PU
            theUTNode.pUxUTRelation.planningUnit = root.planningUnit
            ## Set the UTNode's relation to have the correct location (order-1)
            theUTNode.pUxUTRelation.location = (theUTNode.order-1)
            ## Make sure the relation's tuppleID is up-to-date
            theUTNode.pUxUTRelation.updateTuppleID()
            '''
            
            self.SGOMS.printModelContentsAdvanced()
        ## If the root is not a PUNode, do nothing, just connect as a normal Node would
        else:
            pass
    
    '''    
    def updateRelation(self):
                
        print "(", self.label, ".updateRelation)"
        
        root = self.getRootNode()
        
        ## If the root is a PUNode, add a new relation, add self to PU list, and planning Parent Unit
        if isinstance(root, PUNode):
            self.pUxUTRelation = PUxUTRelation(self.label, root.planningUnit, self.unitTask)
            ## Inserts the UT in the correct location of the PU's list
            root.planningUnit.unitTaskList.insert(self.order-1, self.unitTask)
            self.unitTask.setParentPlanningUnit(root.planningUnit)
        else:
            pass
    '''
        
    def deleteEdge(self, theEdge):
        '''Deletes the parameter edge from self.edges
        
        theEdge should be an Edge'''
        
        theEdge.startNode.incidentEdges.remove(theEdge)
        theEdge.endNode.incidentEdges.remove(theEdge)
        
        self.update()
        
    def deleteNode(self, theNode):
        '''Deletes the parameter node, and all of its incident edges
        
        If theNode is a PUNode, delete the PU from the SGOMS model
        If theNode is a UTNode, delete the relation from the SGOMS model
        And if the UTNode was the only instance of a UT, delete the UT from the SGOMS model
        
        ^2014.07.02, for now, we will remove the UT from the SGOMS model regardless,
        i.e. we will assume that there are no duplicate UTs in the graph
        Also, we could in the future make the UTList in SGOMS to be semi-ordered,
        thus allowing for duplicates, and the current syntax will be ok'''
        
        if isinstance(theNode, PUNode):
            #self.deletePUNode()
            self.SGOMS.planningUnitList.remove(theNode.planningUnit)
            
        if isinstance(theNode, UTNode):
            #self.deleteUTNode()
            self.SGOMS.unitTaskList.remove(theNode.pUxUTRelation.unitTask)
            self.SGOMS.pUxUTRelationList.remove(theNode.pUxUTRelation)
        
        for edge in theNode.incidentEdges:
            edge.otherEndFrom(theNode).incidentEdges.remove(edge)
        self.nodes.remove(theNode)
        
        self.update()
        
    def nodeAt(self, p):
        '''Return the first node in which point p is contained, if none, return None
        
        p should be a Point'''

        for node in self.nodes:
            #FDO print "(Graph.nodeAt) Node: ", node.label
            c = node.location ##This returns a point
            
            ## Check to see what kind of node it is to determine whether the point is contained by the node
            ## (Different types of nodes have different dimensions)
            if isinstance(node, PUNode):
                ## We are calculating the square of the distance to avoid negatives
                dx = (p.x - c.x) * (p.x - c.x)
                dy = (p.y - c.y) * (p.y - c.y)
                if dx <= (int(PUNode.WIDTH/2) * int(PUNode.WIDTH/2)) and \
                    dy <= (int(PUNode.HEIGHT/2) * int(PUNode.HEIGHT/2)):
                    print "(Graph.nodeAt) returning PUNode ", node.label
                    return node
            
            ## Calculate the square of the distance from the node point and the click point
            d = (((p.x - c.x) * (p.x - c.x)) + ((p.y - c.y) * (p.y - c.y)))
            
            if isinstance(node, UTNode):                
                if d <= (UTNode.RADIUS * UTNode.RADIUS):
                    print "(Graph.nodeAt) returning UTNode ", node.label
                    return node

            if isinstance(node, Node):
                if d <= (Node.RADIUS * Node.RADIUS):  ##If some point is within the radius of the node:
                    print "(Graph.nodeAt) returning node ", node.label
                    return node
        #FDO print"(Graph.nodeAt) returning None"
        return None
    
    def edgeAt(self, p):
        '''Return the first edge in which point p is near the midpoint; if none, return null
        
        p should be a Point'''
        
        mX = 0
        mY = 0
        
        for e in self.returnEdges():
            #FDO print "(Graph.edgeAt) edges ", e.label
            mX = (e.startNode.location.x +
                  e.endNode.location.x) / 2
            
            mY = (e.startNode.location.y +
                  e.endNode.location.y) / 2
                  
            distance = (p.x - mX) * (p.x - mX) + (p.y - mY) * (p.y - mY)
            
            if distance <= (Node.RADIUS * Node.RADIUS):
                print "(Graph.edgeAt) click was near midpoint of edge ", e.label
                return e
            
            print "(Graph.edgeAt) click was not near midpoint of edge"
        return None
    
    def update(self):
        '''Update method for the graph
        
        calls update() on all nodes'''
        
        print "(Graph.update)"
        for node in self.nodes:
            node.update()
            
        self.SGOMS.printModelContentsAdvanced()
        
    def draw(self, aPen):
        '''Draws the graph
        
        aPen should be a Graphics object'''
        
        edges = self.returnEdges()
        
        for edge in edges:  #Draw the edges first
            edge.draw(aPen)
            
        for node in self.nodes: #Draw the nodes second
            node.draw(aPen)
            
    def printGraph(self):
        '''Prints the graph in the form of label(x nodes, y edges)'''
        
        print self.label, "(", len(self.nodes), ",", len(self.returnEdges()), ")"

class DialogClientInterface:
    '''An interface for dealing with custom dialog boxes'''
    
    def __init__(self):
        pass
    
    def dialogFinished(self):
        '''Specifies the behaviour for closing the dialog box when data is entered and should be kept
        Each implementation of a DialogClientInterface will overrite this method'''
        
        pass
    
    def dialogCancelled(self):
        '''Specifies the behaviour for closing the dialog box when data should be discarded
        Each implementation of a DialogClientInterface will overwrite this method'''
        
        pass 
            
class GraphEditor(JPanel, MouseListener, MouseMotionListener, KeyListener):
    '''The user interface for the graph example'''
    
    def __init__(self, aGraph = None):
        '''Initializes the GraphEditor
        
        aGraph should be a Graph'''
        
        super(GraphEditor, self).__init__()
        
        ##Store the Graph
        if aGraph == None:
            self.graph = Graph()
        else:
            self.graph = aGraph
            self.setBackground(Color.white)
            
        ##Store a variable to keep track of a node being dragged
        self.dragNode = None
        self.elasticEndLocation = None  ## Variable to store location for edge dragging
        
        ## Variables for handling dragging of edges
        self.dragEdge = None    
        self.dragPoint = None
        
        ## Sets the border to be a loweredBevelBorder
        self.setBorder(BorderFactory.createLoweredBevelBorder())
        
        #self.setLayout(None)
        #self.setSize(600, 400)
        
        ## Add the event handlers
        self.addEventHandlers()
        
    def addEventHandlers(self):
        '''Adds all event handlers to the GUI'''
        
        self.addMouseListener(self)
        self.addMouseMotionListener(self)
        self.addKeyListener(self)
        
    def removeEventHandlers(self):
        '''Removes all event handlers from the GUI'''
        
        self.removeMouseListener(self)
        self.removeMouseMotionListener(self)
        self.removeKeyListener(self)
            
    def mouseClicked(self, event):
        '''Defines what happens when the mouse is clicked'''
        
        ## On a double-click
        if (event.getClickCount() == 2):
            
            print "(mouseClicked) at (", event.getX(), ",", event.getY(), ")"
            aNode = self.graph.nodeAt(event.getPoint()) ##Find the node where the click happened
            
            if aNode == None:   ##If there was no node, check to see if it was an edge
                anEdge = self.graph.edgeAt(event.getPoint())
                if anEdge == None: ##If no edge and no node clicked, create a new node
                    self.graph.addUTNodeAdvanced("finished", event.getPoint())
                    #self.graph.addNode(Node("x",event.getPoint()))  
                else:
                    anEdge.toggleSelected() ##If there was an edge, select it
            else:   ## If there was a node that was clicked, select it
                aNode.toggleSelected()
                
            # We have changed the model, so now we update
            self.update()
            
    def mousePressed(self, event):
        '''Defines what happens when the mouse is pressed'''
        
        ## Find where the click occurred, return the node the click happened in
        aNode = self.graph.nodeAt(event.getPoint())
        print "(mousePressed) location = ", event.getX(), ",", event.getY()
        if aNode != None:
            #If we pressed on a node, store it in the dragNode variable
            self.dragNode = aNode
            print "(mousePressed) Node to be dragged = ", self.dragNode.label
        ##If the click was in an edge (i.e. not in a node), store the dragEdge variables
        else:
            self.dragEdge = self.graph.edgeAt(event.getPoint())
        
        ## Keep track of the eventPoint (for dragging edges, and multiple nodes)
        self.dragPoint = event.getPoint()
            
    def mouseDragged(self, event):
        '''Defines what happens when the mouse is dragged'''
        
        print "(mouseDragged)"
        ## Behaviour for dragging nodes
        if self.dragNode != None:   ## If there is a node to drag from (set in mousePressed)
            if self.dragNode.selected == True:  ## If the node is selected
                ## Drag each selected node
                for n in self.graph.returnSelectedNodes():
                    n.location.translate(event.getPoint().x - self.dragPoint.x,
                                         event.getPoint().y - self.dragPoint.y)
                self.dragPoint = event.getPoint()
                print "(mouseDragged) location of node = ", self.dragNode.location.x, ",", self.dragNode.location.y
            else:   ## If no node, store the point for edge creation
                self.elasticEndLocation = event.getPoint()
        
        ##Behaviour for dragging Edges (moves both attached nodes)
        if self.dragEdge != None:
            if self.dragEdge.selected == True:
                ##Translate the startNode and endNode
                self.dragEdge.startNode.location.translate(event.getPoint().x - self.dragPoint.x, 
                                                           event.getPoint().y - self.dragPoint.y)
                self.dragEdge.endNode.location.translate(event.getPoint().x - self.dragPoint.x,
                                                         event.getPoint().y - self.dragPoint.y)
                self.dragPoint = event.getPoint()
        ##We have changed the model, so now update
        self.update()
            
    def mouseReleased(self, event):
        '''Defines what happens when the mouse is released'''
        
        print "(mouseReleased)"
        
        ##Check to see if we have let go on a node
        aNode = self.graph.nodeAt(event.getPoint())
        
        if aNode != None and aNode != self.dragNode:
            self.graph.addEdge(self.dragNode, aNode);
        
        ##Refresh the panel either way
        self.dragNode = None
        self.update()
            
    def keyPressed(self, event):
        '''Defines what happens when a keyboard key is pressed'''
        
        if event.getKeyCode() == KeyEvent.VK_DELETE:
            print "(GraphEditor.keyPressed) DELETE pressed"
            
            ## Remove selected edges
            for e in self.graph.returnSelectedEdges():
                self.graph.deleteEdge(e)
            
            ## Remove selected nodes
            for n in self.graph.returnSelectedNodes():
                self.graph.deleteNode(n)
                for node in self.graph.nodes:
                    print node.label
            self.update()       
    
    def paintComponent(self, aPen):
        '''This is the method responsible for displaying the graph
        
        aPen should be a Graphics object'''
                
        #######
        #This is the workaround for a Jython bug which doesn't allow
        #for calling super(...) directly for the paintComponent method
        #The syntax normally would be: super(GraphEditor, self).paintComponent(aPen)
        #But this throws an exception, because the paintComponent method is protected in Java
        #See: http://sourceforge.net/p/jython/mailman/message/9129532/
        #Also see: http://bugs.jython.org/issue1540
        #######
        
        self.super__paintComponent(aPen)    ## This is the workaround here (note weird syntax)
        
        self.graph.draw(aPen)
        
        ##If you are dragging from an unselected node, draw a line
        if self.dragNode != None:
            if self.dragNode.selected == False:
                print "(paintComponent) draw elastic line"               
                aPen.drawLine(self.dragNode.location.x, self.dragNode.location.y,
                              self.elasticEndLocation.location.x, self.elasticEndLocation.location.y)
        
    def update(self):
        '''Repaints the GraphEditor based on the model (graph)'''
        
        print "(GraphEditor.update) Begin Update"
        self.requestFocus()
        self.removeEventHandlers()
        self.repaint()
        self.addEventHandlers()

class UnitTaskSimpleDialogPanel(JPanel):
    '''A panel that specifies the text fields etc. for creating/editing a new Unit Task
    (This panel contains fields for )
    Used by UnitTaskDialog'''
    
    def __init__(self, aGraph):
        '''Initializes the UnitTaskPanel with aGraph as a model that can feed it inputs
        
        aGraph should be a Graph'''
        
        super(UnitTaskSimpleDialogPanel, self).__init__()
        
        self.graph = aGraph
        
        self.components = []
        
        ## Create the Labels and store them in the components list
        
    def reinitialize(self, aGraph):
        '''Reinitializes the panel when a new field is created
        
        for each component in self.components, add the component'''
        

class UnitTaskDialogPanel(JPanel):
    '''A panel that specifies the text fields etc. for creating/editing a new Unit Task
    (This panel contains fields for specifying ACT-R behaviour)
    Used by UnitTaskDialog'''
    
    def __init__(self, aGraph):
        '''Initializes the UnitTaskPanel with aGraph as a model that can feed it inputs
        
        aGraph should be a Graph'''
        
        super(UnitTaskDialogPanel, self).__init__()
        
        self.graph = aGraph
        
        ## Create the Labels
        self.nameLabel = JLabel("Enter Name of Unit Task")
        self.firingConditionsLabel = JLabel("Specify Firing Conditions:")
        self.setFiringBufferLabel = JLabel("Set Buffer:")
        self.setFiringSlotNameLabel = JLabel("Set Slot Name:")
        self.setFiringSlotValueLabel = JLabel("Set Slot Value:")
        self.behavioursLabel = JLabel("Specify Behaviours:")
        self.setBehaviourBufferLabel = JLabel("Set Buffer:")
        self.setBehaviourSlotNameLabel = JLabel("Set Slot Name:")
        self.setBehaviourSlotValueLabel = JLabel("Set Slot Value:")
        
        ## Create an empty label as a filler
        self.emptyLabel1 = JLabel()
        self.emptyLabel2 = JLabel()
        
        ## Create the text entry fields
        self.nameEntry = JTextField()
        self.firingBufferEntry = JTextField()
        self.firingSlotNameEntry = JTextField()
        self.firingSlotValueEntry = JTextField()
        self.behaviourBufferEntry = JTextField()
        self.behaviourSlotNameEntry = JTextField()
        self.behaviourSlotValueEntry = JTextField()
        
        ## Set the layout manager and add the components
        self.setLayout(GridLayout(9,2,5,5)) ## Rows, Cols, hgap, vgap
        
        ## Add components in order, starting from top-left to top-right
        self.add(self.nameLabel)
        self.add(self.nameEntry)
        
        self.add(self.firingConditionsLabel)
        self.add(self.emptyLabel1)
        
        self.add(self.setFiringBufferLabel)
        self.add(self.firingBufferEntry)
        
        self.add(self.setFiringSlotNameLabel)
        self.add(self.firingSlotNameEntry)
        
        self.add(self.setFiringSlotValueLabel)
        self.add(self.firingSlotValueEntry)
        
        self.add(self.behavioursLabel)
        self.add(self.emptyLabel2)
        
        self.add(self.setBehaviourBufferLabel)
        self.add(self.behaviourBufferEntry)
        
        self.add(self.setBehaviourSlotNameLabel)
        self.add(self.behaviourSlotNameEntry)
        
        self.add(self.setBehaviourSlotValueLabel)
        self.add(self.behaviourSlotValueEntry)
        
class UnitTaskDialog(JDialog):
    '''A Dialog Box that pops up for creating a new Unit Task'''
    
    def __init__(self, theOwner = None, theTitle = "Create New Unit Task", isModal = True, theGraph = None):
        '''Initializes a UnitTaskDialog
        
        theOwner is the client application that caused the dialog to open, must be a Frame of some sort
        theTitle specifies the title of the pop-up window
        isModal specifies whether the window must be dealt with before other actions can happen 
        (True = must be dealt with)
        aGraph is the model to be changed, it should be a Graph
        '''
        
        print "##### Unit Task Dialog Initiated #####"
        
        #super(theOwner, "Create New Unit Task", True, windowClosing=self.cancelButtonPressed).__init__() ## The title and modal value should be hard-coded
        super(UnitTaskDialog, self).__init__(theOwner, theTitle, isModal, windowClosing=self.cancelButtonPressed)
        
        self.dialogOwner = theOwner
        self.title = theTitle
        self.modal = isModal
        self.graph = theGraph
        
        self.okButton = JButton("OK", actionPerformed=self.okButtonPressed)
        self.cancelButton = JButton("Cancel", actionPerformed=self.cancelButtonPressed)
        
        self.buttonPanel = JPanel()
        self.buttonPanel.setLayout(FlowLayout(FlowLayout.RIGHT))
        self.buttonPanel.add(self.okButton)
        self.buttonPanel.add(self.cancelButton)
        
        self.unitTaskPanel = UnitTaskDialogPanel(theGraph)
        
        self.setLayout(BoxLayout(self.getContentPane(), BoxLayout.Y_AXIS))
        
        self.add(self.unitTaskPanel)
        self.add(self.buttonPanel)
        
        ## Prevent the window from being resized
        self.setResizable(False)
        
        ## Set the size of the dialog box
        self.setSize(400, 300)
        
        self.setVisible(True)
            
    def okButtonPressed(self, event):
        '''Defines what happens when the ok button is pressed
        
        Creates a new UnitTask, based on the info entered into the dialog box,
        and passes the newly created UnitTask to the owner'''
        
        print "(UnitTaskDialog.okButtonPressed())"
        
        ##theID="Unit Task", theParentPlanningUnits=None, theFiringConditions=None, theBehaviour=None):
        newUnitTask = UnitTask(self.unitTaskPanel.nameEntry.getText())  ## Set the ID
        
        newUnitTask.firingConditions.append(self.unitTaskPanel.firingBufferEntry.getText())   ## Add the firing conditions
        newUnitTask.behaviour.append(self.unitTaskPanel.behaviourBufferEntry.getText())
        
        self.owner.dialogFinished(newUnitTask)
        self.dispose()
        
    def cancelButtonPressed(self, event):
        '''Defines what happens when the cancel button is pressed'''
        
        print "(UnitTaskDialog.cancelButtonPressed())"      
        self.owner.dialogCancelled()
        self.dispose()

class ButtonPanel(JPanel):
    '''A panel that contains a few buttons for creating PUs, UTs, etc.'''
    
    def __init__(self, aGraph = None, aFrame = None):
        '''Initializes the ButtonPanel
        
        aGraph should be a Graph
        aFrame should be a JFrame, the owner of the ButtonPanel as a reference'''
        
        super(ButtonPanel, self).__init__()
        
        ##Store the Graph
        if aGraph == None:
            self.graph = Graph()
        else:
            self.graph = aGraph
            self.setBackground(Color.white)
        
        ## Store the owner frame
        self.frame = aFrame
        
        ##Set the layout
        self.setLayout(FlowLayout())
        
        self.createButtons()
        
        #self.setSize(100,400)
        
    def createButtons(self):
        '''Creates and places the buttons onto the JPanel'''
        
        pUButton = JButton("Create New \nPlanning Unit")
        #pUButton.setLocation(10,10)
        pUButton.setSize(60,40)
        self.add(pUButton)
        
        uTButton = JButton("Create New \nUnitTask", actionPerformed=self.createNewUnitTask)
        #uTButton.setLocation(220,120)
        uTButton.setSize(60,40)
        self.add(uTButton)
        
    def createNewUnitTask(self, event):
        '''Defines what happens when the Create New Unit Task button is pushed
        
        brings up a UnitTaskDialog pop-up window for the user to enter info'''
        
        ## Note, this method is primarily used for testing purposes,
        ## And will likely not appear in the final code (2014.07.21)
        
        dialog = UnitTaskDialog(self.frame, "Create New Unit Task", True, self.graph) ## theOwner, theTitle, isModal, theGraph
        
        
class GraphEditorFrame(JFrame, DialogClientInterface):
    '''A simple view which holds a GraphEditor panel'''
    
    def __init__(self, theTitle = "Title", theGraph = None):
        '''Initializes the GraphEditorFrame
        
        theTitle should be a string
        theGraph should be a Graph'''
        
        if theGraph == None:
            self.graph = Graph()
        else:
            self.graph = theGraph
        
        ## These are the JPanels
        self.editor = GraphEditor(theGraph)
        self.buttonPannel = ButtonPanel(theGraph, self)
        
        ## Set the layout of the Frame (Border Layout)
        #self.setLayout(BorderLayout())        
        #self.add(BorderLayout.EAST, self.editor)
        #self.add(BorderLayout.WEST, self.buttonPannel)
        
        self.setLayout(None)
        
        self.buttonPannel.setSize(200,400)
        self.buttonPannel.setLocation(5,10)
        self.add(self.buttonPannel)
        
        self.editor.setSize(600,400)
        self.editor.setLocation(210,10)
        self.add(self.editor)
        
        #self.buttonPannel.setSize(600, 400)
        
        ## Add the menu Items
        menubar = JMenuBar()
        fileMenu = JMenu("File")
        
        fileExport = JMenuItem("Export To ACT-R",
            actionPerformed=self.exportToACTR)
        
        fileExport.setToolTipText("Convert Current Graph Into an ACT-R Readable Model")

        fileMenu.add(fileExport)

        menubar.add(fileMenu)

        self.setJMenuBar(menubar)


        ## Add the title and other basic operations
        self.setTitle(theTitle)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setSize(1000, 600)
        self.setVisible(True)
    
    def dialogFinished(self, theUnitTask):
        '''Specifies what to do when the Create Unit Task Dialog box ends successfully
        
        theUnitTask should be a UnitTask passed from the UnitTaskDialog'''
        
        print "(GraphEditorFrame.dialogFinished())"
        
        ## Add the Unit Task to the Model and GUI (at some location)
                
        self.graph.addUTNodeAdvancedNew(theUnitTask, Point(200,200))    ## For now, the location is arbitrary
        self.editor.update()
    
    def exportToACTR(self, e):
        '''Exports the Graph to an ACT-R readable python file
        
        Calls SGOMS_Model.outputToACTR()'''
        
        print "(GraphEditorFrame.exportToACTR) Called"
        
        self.graph.SGOMS.outputToACTR()
       
     
'''
## Node Test Code
point1 = Point(1,2)
point2 = Point(3,4)        
node1 = Node("node1", point1)
node2 = Node("node2", point2)
edge1 = Edge(node1, node2, "edge1")
#print node1
#print edge1

map1 = Graph("Ontario and Quebec")
ottawa = Node("Ottawa", Point(250,100))
toronto = Node("Toronto", Point(100,170))
kingston = Node("Kingston", Point(200, 150))
montreal = Node("Montreal", Point(300,90))
quebec = Node("Quebec", Point(350, 80))
halifax = Node("Halifax", Point(400, 80))
map1.addNode(ottawa)
map1.addNode(toronto)
map1.addNode(kingston)
map1.addNode(montreal)
map1.addNode(quebec)
map1.addNode(halifax)

map1.addEdge(ottawa, toronto)
map1.addEdge(ottawa, montreal)
map1.addEdge(ottawa, kingston)
map1.addEdge(kingston, toronto)
map1.addEdge(montreal, quebec)
map1.addEdge(quebec, halifax)

toronto.rootNode = True
map1.update()


#toronto.getEveryConnectedNode()
#montreal.getEveryConnectedNode()
#quebec.getHopsToRootNode()
#halifax.getHopsToRootNode()
'''
        
'''
print "number of connected nodes to toronto = " 
connected = toronto.getEveryConnectedNode()
print len(connected)
for item in connected:
    print item.label, ",", item.recursed
    
print "number of connected nodes to halifax = " 
connected = halifax.getEveryConnectedNode()
print len(connected)
for item in connected:
    print item.label, ",", item.recursed
    
print "number of connected nodes to montreal = " 
connected = montreal.getEveryConnectedNode()
print len(connected)
for item in connected:
    print item.label, ",", item.recursed
'''

'''
## SGOMS Test Code 3 (Testing OutputToACT-R without Frame)
## This will not use any features of the GUI
## The PUs and UTs are taken from SGOMS-ACT-R-BasicModel2

## Create the Model
## Create the PUs and assign them behaviour etc.
## Create the UTs and assign them behaviour etc.
## Add the UTs to the PUs
## Create the relations and add the PUs and UTs
## Add the PUs, UTs and Relations to the model
## Output to ACT-R

SGOMS = SGOMS_Model()
SGOMS.initialBehaviour.append("b_context.set('area:not_clear cover:not_taken status:not_started completed:no')")

## The Planning Units
take_area = PlanningUnit("take_area")
hold_ground = PlanningUnit("hold_ground")

take_area.firingConditions.append("b_context='area:not_clear status:not_started'")
take_area.behaviour.append("b_plan_unit.set('planning_unit:take_area cuelag:none cue:start unit_task:advance state:running')")
take_area.behaviour.append("b_unit_task.set('unit_task:advance state:running')")
take_area.behaviour.append("b_context.set('area:not_clear status:started')")

hold_ground.firingConditions.append("b_context='area:clear cover:not_taken status:not_started'")
hold_ground.behaviour.append("b_plan_unit.set('planning_unit:hold_area cuelag:none cue:start unit_task:find_cover state:running')")
hold_ground.behaviour.append("b_unit_task.set('unit_task:find_cover state:start')")
hold_ground.behaviour.append("b_context.set('area:clear status:started')")

## The Unit Tasks
advance_unit_task = UnitTask("advance_unit_task")
kill_enemies_unit_task = UnitTask("kill_enemies_unit_task")
find_cover_unit_task = UnitTask("find_cover_unit_task")
finished = UnitTask("finished")

advance_unit_task.firingConditions.append("b_unit_task='unit_task:advance state:running'")
advance_unit_task.behaviour.append("b_unit_task.set('unit_task:advance state:finished')")

kill_enemies_unit_task.firingConditions.append("b_unit_task='unit_task:kill_enemies state:start'")
kill_enemies_unit_task.behaviour.append("b_unit_task.set('unit_task:kill_enemies state:finished')")
kill_enemies_unit_task.behaviour.append("b_context.set('area:clear cover:not_taken status:not_started')")

find_cover_unit_task.firingConditions.append("b_unit_task='unit_task:find_cover state:start'")
find_cover_unit_task.behaviour.append("b_unit_task.set('unit_task:find_cover state:finished')")
find_cover_unit_task.behaviour.append("b_context.set('area:clear cover:taken status:completed')")

finished.firingConditions.append("")
finished.behaviour.append("pass")

## Add the UTs to the PUs
take_area.unitTaskList.append(advance_unit_task)
take_area.unitTaskList.append(kill_enemies_unit_task)
hold_ground.unitTaskList.append(find_cover_unit_task)


## Create the Relations
## Should create a method in SGOMS_Model that updates the relations automatically
relation1 = PUxUTRelation(1, take_area, advance_unit_task, 0)
relation2 = PUxUTRelation(2, take_area, kill_enemies_unit_task, 1)
relation3 = PUxUTRelation(3, take_area, finished, 2)

relation4 = PUxUTRelation(4, hold_ground, find_cover_unit_task, 0)
relation5 = PUxUTRelation(5, hold_ground, finished, 1)

## Change the DM strings manually
relation1.DM_string = "planning_unit:take_area    cuelag:none          cue:start          unit_task:advance"
relation2.DM_string = "planning_unit:take_area    cuelag:start         cue:advance        unit_task:kill_enemies"
relation3.DM_string = "planning_unit:take_area    cuelag:advance       cue:kill_enemies   unit_task:finished"
relation4.DM_string = "planning_unit:hold_area    cuelag:none          cue:start          unit_task:find_cover"
relation5.DM_string = "planning_unit:hold_area    cuelag:start         cue:find_cover     unit_task:finished"

## Add the Relations
SGOMS.pUxUTRelationList.append(relation1)
SGOMS.pUxUTRelationList.append(relation2)
SGOMS.pUxUTRelationList.append(relation3)
SGOMS.pUxUTRelationList.append(relation4)
SGOMS.pUxUTRelationList.append(relation5)

## Add the UTs and PUs to the model (do not add "finished"
SGOMS.unitTaskList.append(advance_unit_task)
SGOMS.unitTaskList.append(kill_enemies_unit_task)
SGOMS.unitTaskList.append(find_cover_unit_task)

SGOMS.planningUnitList.append(take_area)
SGOMS.planningUnitList.append(hold_ground)

## Add The PUxUTRelations
#SGOMS.addPUxUTRelationReturnSelf(advance_unit_task, take_area, 0)
#SGOMS.addPUxUTRelationReturnSelf(kill_enemies_unit_task, take_area, 1)
#SGOMS.addPUxUTRelationReturnSelf(find_cover_unit_task, hold_ground, 0)

## Print Model Contents, and export to ACT-R
SGOMS.printModelContentsAdvanced()
SGOMS.outputToACTR()
'''


## SGOMS Test Code 2

## The procedure for adding PUNodes and UTNodes
## 1. Create map (creates a blank SGOMS_Model)
## 2. map.addPUNode(label, point) adds a PU to SGOMS and a PUNode to Graph.nodes
## 3. map.addUTNode(label, point) adds a UT to SGOMS, a relation to SGOMS, and a UTNode to Graph.nodes

## Then add the edges

map1 = Graph("SGOMS Test")
map1.addPUNodeAdvanced("PU1", Point(100,100))
map1.addUTNodeAdvanced("UT1", Point(100,200))
map1.addUTNodeAdvanced("UT2", Point(100,300))

#map1.addEdge()

map1.SGOMS.printModelContentsAdvanced()


'''
## SGOMS Test Code 1
## The Planning Units and UTs
pu1 = PlanningUnit("PU1")
ut1 = UnitTask("UT1")
ut2 = UnitTask("UT2")
s = SGOMS_Model()

s.addUnitTask(ut1,pu1)
s.addUnitTask(ut2,pu1)

s.printModelContentsAdvanced()

pun1 = PUNode("PUNode", Point(100,100))
pun1.planningUnit = pu1

utn1 = UTNode("UTNode1", Point(100,200))
utn1.unitTask = ut1
utn2 = UTNode("UTNode2", Point(100,300))
utn2.unitTask = ut2

map1 = Graph("SGOMS Test")
map1.addNode(pun1)
map1.addNode(utn1)
map1.addNode(utn2)

map1.addEdge(pun1,utn1)
map1.addEdge(utn1,utn2)

#map1.SGOMS = s
print map1


#for node in map1.nodes:
#    print node.recursed
'''


frame = GraphEditorFrame("Map1", map1)

#print frame.graph
#print frame.graph.SGOMS

#map1.SGOMS.printModelContentsAdvanced()


