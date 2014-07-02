'''
Created on Jun 13, 2014

@author: Matthew Martin

This is an Extension of SimpleGraph1, where I include multiple JPanels into my Frame
'''

from java.awt import *
from java.awt.event import *
from java.util import *
from javax.swing import *

import os

########
# The SGOMS-Related model stuff from ACT-R_GUI-2 (As of 2014.06.17
########

class PlanningUnit:
    '''An SGOMS Planning Unit that contains a list of Unit Tasks'''

    def __init__(self, theID="Planning Unit", theUnitTaskList=None):
        '''Creates a PlanningUnit

        theID should be a string that identifies the Planning Unit
        theUnitTaskList should be a list of UnitTasks'''

        self.ID = theID
        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == None:
            self.unitTaskList = []

        print "(PlanningUnit.__init__) Planning Unit Created: ", self.ID
        self.printPlanningUnitContents()
        
    def _str_(self):
        '''Returns a string representation of the Planning Unit'''
        
        return "PU: " + self.ID + " # of Unit Tasks: " + len(self.unitTaskList)

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
    
    def __init__(self, theID="Unit Task", theParentPlanningUnits=None):
        '''Creates a Unit Task

        ID is a string that names the Unit Task
        theParentPlanningUnits should be a list of PlanningUnits'''

        self.ID = theID
        self.parentPlanningUnits = theParentPlanningUnits
        if theParentPlanningUnits == None:
            self.parentPlanningUnits = []       

        print "(UnitTask.__init__) Unit Task Created: ", self.ID,
        self.printParentPlanningUnits()
        
    def _str_(self):
        '''Returns a string representation of the Unit Task'''
        
        return "UT: " + self.ID + ", # of Parent PUs: " + len(self.parentPlanningUnits)

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

    def __init__(self, theID="PUxUTRelation", thePlanningUnit=None, theUnitTask=None):
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


##### The Model #####
        
class SGOMS_Model:
    '''The underlying model that the GUI runs on'''

    def __init__(self, thePlanningUnitList=None, theUnitTaskList=None, thePUxUTRelationList=None):
        '''The initializing method for the model

        planningUnitList should be a list of Planning Units
        unitTaskList should be a list of Unit Tasks'''

        print "SGOMS_Model initiated"

        self.planningUnitList = thePlanningUnitList
        if thePlanningUnitList == None:
            self.planningUnitList = []
        self.planningUnitCounter = len(self.planningUnitList)

        self.unitTaskList = theUnitTaskList
        if theUnitTaskList == None:
            self.unitTaskList = []
        self.unitTaskCounter = len(self.unitTaskList)

        if thePUxUTRelationList == None:   
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
            theParentPlanningUnit.addUnitTask(theUnitTask)

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

    ########## Write to ACT-R ##########

    def outputToACTR(self):
        '''Takes what is in the model and outputs it into python ACT-R readable code'''

        directory = os.getcwd()
        print directory

        f = open("TestWriting.py", "w")  ## Open a new file for writing

        ## Write the basic import statements
        f.write("import ccm\n")
        f.write("log=ccm.log()\n")
        f.write("from ccm.lib.actr import *\n\n")

        ## Write the environment statements
        f.write("class MyEnvironment(ccm.Model):\n")
        f.write("   pass\n\n")

        ## Write the Agent
        f.write("class MyAgent(ACTR):\n")
        f.write("    focus=Buffer()\n")
        f.write("    DMbuffer=Buffer()\n")
        f.write("    DM=Memory(DMbuffer)\n\n")

        ## Write the init method
        f.write("    def init():\n")
        f.write("        pass\n\n")
                      
        ## Write the Planning Units/productions
        for planningUnit in self.planningUnitList:
            f.write("    def " + planningUnit.ID + "():\n")
            f.write("        pass\n\n")

        ## Write the code to run the model

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
            
        #self.RADIUS = 15    ##The default radius of the Node
        self.rootNode = False  ## By default, a node is not the root
        self.selected = False  ## Indicates whether the node is selected or not
        self.recursed = False  ## A flag for using the function getRootNode
        
        ## Specifies the default order within the planning unit (distance from the root)
        orderVar = self.getHopsToRootNode() 
        if orderVar == None:    ## If can't find a root node, treat itself as a root node
            self.order = 0
        else:
            self.order = orderVar   
        #self.everyConnectedNode = []  ## A list for keeping track of nodes recursed over during getRootNode()
    
    def __str__(self):
        '''Returns a string representing the Node as label (x,y)'''
        
        return self.label + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
    
    def toggleSelected(self):
        '''Changes the selected boolean to True/False depending on previous state'''
        
        if self.selected == False: 
            self.selected = True
        else:
            self.selected = False
            
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
        Used in getRootNodeHelper'''
        
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
        Calls getHopsToRootNodeHelper'''
               
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
        
        returnVar = self.getHopsToRootNodeHelper(nodeList, everyConnectedNode)
        
        print "(Node.getHopsToRootNode) hops to root node from", self.label, "=", returnVar
        self.recursed = False   ## Reset the recursed flag to False at the end
        return returnVar
        
        
        
    def getHopsToRootNodeHelper(self, theNodeList, everyConnectedNode, times=0):
        '''Helper method for getHopsToRootNode
        Returns the number of hops away from the root node the current node is'''

        for item in theNodeList:
            item.recursed = True
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                    
        ## Print the recursive level 
        print "---------- Level", times+1, "----------"
       
        ## This is the check for end state, if it has gone 20 times, the function ends and returns None
        ## This is basically throwing an exception
        if times > 19:
            print ("(Node.getRootNodeHelper) Recursed 20 times, returning None")
            return None
        
        ## Another check for the end state, if it has found the root node, return the # of hops
        ## (each item in theNodeList is one hop away from the previous node, so hops = times +1
        for item in theNodeList:
            if item.rootNode == True:
                ## Reset each recursed flag back to False before returning
                for thing in everyConnectedNode:
                    thing.recursed = False
                return times+1
                
        passList = []  ## A variable for storing the list to be passed on to the next function call
        
        for item in theNodeList:
            ## For every item in theNodeList keep a list of related nodes
            ## tempList is a list of Nodes related to the item in question, each item will have a tempList
            tempList = []   ## This is not going to contain anything that has already been activated, 
                            ## as they are excluded in the returnUnvisitedNeighbourNodes method
            tempList += item.returnUnvisitedNeighbourNodes()
            
            print "Length of tempList on times", times, len(tempList)
            
            ## Check the end condition, if didn't find anything, return empty list
            #if len(tempList) < 1:
            #    print "Length of templist was 0, returning empty list"
            #    return tempList
            
            for thing in tempList:
                print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## and it has not found a root node, return None (throw an exception)
        if len(passList) < 1:
            #returnList = []
            print "(Node.getHopsToRootNodeHelper) passList is empty, returning None"
            for item in everyConnectedNode:
                #print item.label
                item.recursed = False
                #if item not in returnList:
                #    returnList.append(item)
                #    print "appending happened ok"
            #print "helper returnlist", str(returnList)
            return None
        
        #print "hi"        
        return self.getHopsToRootNodeHelper(passList, everyConnectedNode, times+1)     
        
    def getEveryConnectedNode(self):
        '''Returns a list of all nodes that the current node is (indirectly) connected to
        Returns an empty list if there are no connected nodes'''
       
        self.recursed = True  ## Prevent the function from finding itself
        
        everyConnectedNode = [] ## The list to keep track of each connected node
        
        nodeList = self.returnUnvisitedNeighbourNodes()  ## The initial list of related nodes to send to helper
        
        ## Return empty list if there are no neighbour nodes 
        if len(nodeList) < 1:
            print self.label, " is not connected to anything"
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
        self.recursed = False
        
        return returnList

    def getEveryConnectedNodeHelper(self, theNodeList, everyConnectedNode, times=0):
        '''A helper method for the recursive getEveryConnectedNode() method'''
        
        for item in theNodeList:
            item.recursed = True
            if item not in everyConnectedNode:
                everyConnectedNode.append(item)
                
        ## Print the recursive level 
        print "---------- Level", times+1, "----------"
       
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
            
            print "Length of tempList on times", times, len(tempList)
            
            ## Check the end condition, if didn't find anything, return empty list
            #if len(tempList) < 1:
            #    print "Length of templist was 0, returning empty list"
            #    return tempList
            
            for thing in tempList:
                print item.label, " is connected to ", thing.label
                thing.recursed = True   ## Keep track of which nodes have been found already
                passList.append(thing)  ## Everything that returnUnvisited has found gets put into passList
                
        ## This is the check for the end state, if there are no unvisited nodes left,
        ## return the list of every connected node
        if len(passList) < 1:
            returnList = []
            print "passList is empty, returning everyConnectedNode:"
            for item in everyConnectedNode:
                print item.label
                item.recursed = False
                if item not in returnList:
                    returnList.append(item)
                    #print "appending happened ok"
            print "helper returnlist", str(returnList)
            return returnList
        
        print "hi"        
        #return (theNodeList + self.getEveryConnectedNodeHelper(passList, everyConnectedNode, times+1))
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
    
    PUNode inherits from Node'''
    
    HEIGHT = 40
    WIDTH = 50
    
    def __init__(self, aLabel = None, aLocation = None, theIncidentEdges = None, thePU = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string, by default it is the Label of thePU 
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        thePU should be a PlanningUnit'''
        
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
            
        if thePU == None:
            self.planningUnit = PlanningUnit()
        else:
            self.planningUnit = thePU
        
        self.label = aLabel 
        if aLabel == None:
            self.label = self.planningUnit.ID

        self.selected = False  ## Indicates whether the node is selected or not
        self.rootNode = True  ## Specifies whether the node is the root node (PUs are by default the root)
        self.recursed = False
        
        print "(PUNode) initiated, ", self 
        
    def _str_(self):
        '''Returns a string representation of the PUNode'''
        
        return "PUNode: " + self.label + " PU: " + self.planningUnit.ID \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
        
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
        aPen.drawString(self.label, self.location.x + PUNode.WIDTH, self.location.y - PUNode.HEIGHT)
        
class UTNode(Node):
    '''Specifies the behaviour/appearance of a UnitTaskNode (PUNode)
    
    UTNode inherits from Node'''
    
    RADIUS = 20
    
    def __init__(self, aLabel = None, aLocation = None, theIncidentEdges = None, 
                 theUT = None, thePUxUTRelation = None):
        '''Initializes the Node with an empty point and label, if none provided
        
        aLabel should be a string, by default it is the Label of theUT  
        aLocation should be a Point
        theIncidentEdges should be a list of Edges
        theUT should be a PlanningUnit
        thePUxUTRelation should be a PUxUTRelation'''
        
        self.selected = False  ## Indicates whether the node is selected or not
        self.rootNode = False  ## Indicates whether the node is the root node (false by default for UTs)
        self.recursed = False        
        
        
  
        if aLocation == None:
            self.location = Point(0,0)
        else:
            self.location = aLocation
            
        if theIncidentEdges == None:
            self.incidentEdges = []
        else:
            self.incidentEdges = theIncidentEdges
        
        ## Create an empty UnitTask
        if theUT == None:
            self.unitTask = UnitTask()
        else:
            self.unitTask = theUT
        
        self.label = aLabel
        if self.label == None:
            self.label = self.unitTask.ID
            
        ## Specifies the default order within the planning unit (distance from the root)
        orderVar = self.getHopsToRootNode() 
        if orderVar == None:    ## If can't find a root node, order = 0
            self.order = 0
        else:
            self.order = orderVar
        
        ## The adding of a PUxUT relation comes when connecting to a root-connected node
        self.pUxUTRelation = thePUxUTRelation   ## None by default
        
        ## We are assuming that the root is a PUNode
        #if thePUxUTRelation == None:    ## If there is no Relation specified
        #    root = self.getRootNode()
        #    if root != None or self:  ## And there is a rootNode (i.e. a PU)
        #        self.pUxUTRelation = PUxUTRelation("R",root.planningUnit,self.unitTask)
        
        print "(UTNode) initiated, ", self 
    
    def _str_(self):
        '''Returns a string representation of the UTNode'''
        
        return "UTNode: " + self.label + " UT: " + self.unitTask.ID \
                + " (" + str(self.location.x) + "," + str(self.location.y) + ")"
    
    def returnRelation(self):
        '''Returns the PUxUTRelation of the node, if it exists, returns None if none is specified'''
        
        return self.pUxUTRelation
    
    def returnUnitTask(self):
        '''Returns the UnitTask'''
        
        return self.unitTask
    
    def update(self):
        '''Updates the Node
        
        calls self.updateOrder()'''
        
        print "(Node.update)"
        self.updateOrder()
        #self.updateRelation()
    
    def updateOrder(self):
        '''Updates self.order based on the distance to root node'''
        
        print "(Node.updateOrder)"
        orderVar = self.getHopsToRootNode() ## Will return None if can't find root node
        if orderVar == None:    ## If can't find a root node, distance is zero
            self.order = 0
        else:
            self.order = orderVar
            
    def updateRelation(self):
        '''(Obsolete: function happens in Graph now)
        Updates self.pUxUTRelation based on the node's distance to the PU root'''
        
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
        
    def draw(self, aPen):
        '''Draws the UTNode
        
        aPen should be a Graphics object'''
        
        '''
        ## Node syntax
        aPen.fillOval(self.location.x - Node.RADIUS, self.location.y - Node.RADIUS, Node.RADIUS * 2,
                      Node.RADIUS * 2)
        '''
                 
        #Draw a black border around the rectangle
        aPen.setColor(Color.black)
        aPen.fillOval(self.location.x - UTNode.RADIUS, self.location.y - UTNode.RADIUS, UTNode.RADIUS * 2,
                      UTNode.RADIUS * 2)
        
        #Draw a blue-filled rectangle around the center of the node (if not selected)
        if self.selected == True:
            aPen.setColor(Color.red)
        else:
            aPen.setColor(Color.green)
        
        aPen.fillOval(self.location.x - UTNode.RADIUS, self.location.y - UTNode.RADIUS, UTNode.RADIUS * 2,
                      UTNode.RADIUS * 2)
        
        # Draw a label at the top right corner of the node
        # Label looks like: UT.label, order within PU
        aPen.setColor(Color.black)
        stringVar = self.label + "," + str(self.order)
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
        
        if self.selected == False: 
            self.selected = True
        else:
            self.selected = False
            
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

class RelationEdge(Edge):
    '''Specifies the behaviour of an edge containing a PUxUTRelation
    
    Inherits from Edge'''
    
    def __init__(self, theStartNode, theEndNode, theLabel="Edge", thePUxUTRelation = None):
        '''Initializes the Edge with a startnode and end node
        
        theStartNode should be a Node
        theEndNode should be a Node
        thePuxUTRelation should be a PUxUTRelation'''
        
        self.startNode = theStartNode
        self.endNode = theEndNode
        if theLabel == None:
            self.label = theStartNode.label + " --> " + theEndNode.label 
        else:
            self.label = theLabel
            
        self.pUxUTRelation = thePUxUTRelation   ##Not sure if I'm going to use this or not
        
        self.selected = False
       
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
        
        aNode should be a Node'''
        
        self.nodes.append(aNode)
        
        if isinstance(aNode, PUNode):
            self.SGOMS.addPlanningUnit(aNode.planningUnit)
            
        if isinstance(aNode, UTNode):
            self.SGOMS.addUnitTask(aNode.unitTask)
        
        self.update()
    
    def addEdge(self, startNode, endNode):
        '''Adds an edge to the Nodes' incident edges
        
        startNode should be a Node
        endNode should be a Node'''
        
        anEdge = Edge(startNode, endNode)
        
        startNode.addIncidentEdge(anEdge)
        endNode.addIncidentEdge(anEdge)
        
        ## The start node is the one where the dragging comes from (see GraphEditor.mouseReleased)
        ## but need to check both nodes if they are UT nodes (connection can come from either direction)
        
        if isinstance(startNode, UTNode):
            self.addEdgeHelper(startNode)
            
        if isinstance(endNode, UTNode):
            self.addEdgeHelper(endNode)
        
        self.update()
    
    def addEdgeHelper(self, aNode):
        '''Specifies behaviour for connecting UTNodes together
        
        aNode should be a UTNode'''
        
        print "(Graph.addEdgeHelper),", aNode.label
        
        root = aNode.getRootNode()
        
        aNode.updateOrder() ## Make sure the order is correct
        
        ## If the root is a PUNode:
        if isinstance(root, PUNode):
            ## Insert the UT in the correct location of the PU's list (at index 0 if first UT)
            root.planningUnit.unitTaskList.insert(aNode.order-1, aNode.unitTask)  ##PUNode's order = 0
            ## Set the UT's parent Planning Unit
            aNode.unitTask.setParentPlanningUnit(root.planningUnit)
            ## Add a new relation to the UTNode, the location is specified by order of UT in PU's list
            aNode.pUxUTRelation = PUxUTRelation(aNode.label, root.planningUnit, aNode.unitTask)
            ## Add the relation to the SGOMS list
            self.SGOMS.pUxUTRelationList.append(aNode.pUxUTRelation)
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
        '''Deletes the parameter node, and all of its incident edges'''
        
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
        
            d = (((p.x - c.x) * (p.x - c.x)) + ((p.y - c.y) * (p.y - c.y)))
            #FDO print "(Graph.nodeAt) d = ", d
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
                if anEdge == None:
                    self.graph.addNode(Node("x",event.getPoint()))  ##If no edge and no node clicked, create a new node
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
        
        print "(update) Begin Update"
        self.requestFocus()
        self.removeEventHandlers()
        self.repaint()
        self.addEventHandlers()
        
class ButtonPanel(JPanel):
    '''A panel that contains a few buttons for creating PUs, UTs, etc.'''
    
    def __init__(self, aGraph = None):
        '''Initializes the ButtonPanel
        
        aGraph should be a Graph'''
        
        super(ButtonPanel, self).__init__()
        
        ##Store the Graph
        if aGraph == None:
            self.graph = Graph()
        else:
            self.graph = aGraph
            self.setBackground(Color.white)
        
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
        
        uTButton = JButton("Create New \nUnitTask")
        #uTButton.setLocation(220,120)
        uTButton.setSize(60,40)
        self.add(uTButton)
        
class GraphEditorFrame(JFrame):
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
        self.buttonPannel = ButtonPanel(theGraph)
        
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
        
        
        self.setTitle(theTitle)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setSize(1000, 600)
        self.setVisible(True)
       
     
'''
## Default Test Code
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
'''

#toronto.getHopsToRootNode()
#montreal.getHopsToRootNode()
#quebec.getHopsToRootNode()
#halifax.getHopsToRootNode()

        
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

## SGOMS Test Code
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

frame = GraphEditorFrame("Map1", map1)

map1.SGOMS.printModelContentsAdvanced()


