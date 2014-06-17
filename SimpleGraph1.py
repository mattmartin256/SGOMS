'''
Created on Jun 10, 2014

@author: Matthew Martin

This is just meant to be a learning exercise where I figure out how 
to use Jython
'''

from java.awt import *
from java.awt.event import *
from java.util import *
from javax.swing import *

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
        self.selected = False  ## Indicates whether the node is selected or not
    
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
        
        # Draw a label at the top right corner of the node
        aPen.setColor(Color.black)
        aPen.drawString(self.label, self.location.x + self.RADIUS, self.location.y - self.RADIUS)
        
    
    def printNode(self):
        '''Prints the node as: label(x,y)'''
        
        print self.label, "(", self.location.x, ",", self.location.y, ")" 

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
        
class Graph:
    '''Defines a collection of Nodes, Edges, and their behaviour'''
    
    def __init__(self, theLabel = "Graph", theNodes = None):
        '''Initializes the Graph, with a set of nodes and edges
        
        theLabel should be a string
        theNodes should be a list of Nodes
        '''
        
        self.label = theLabel 
        
        if theNodes == None:
            self.nodes = []
        else:
            self.nodes = theNodes
            
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
    
    def addEdge(self, startNode, endNode):
        '''Adds an edge to the Nodes' incident edges
        
        startNode should be a Node
        endNode should be a Node'''
        
        anEdge = Edge(startNode, endNode)
        
        startNode.addIncidentEdge(anEdge)
        endNode.addIncidentEdge(anEdge)
        
    def deleteEdge(self, theEdge):
        '''Deletes the parameter edge from self.edges
        
        theEdge should be an Edge'''
        
        theEdge.startNode.incidentEdges.remove(theEdge)
        theEdge.endNode.incidentEdges.remove(theEdge)
        
    def deleteNode(self, theNode):
        '''Deletes the parameter node, and all of its incident edges'''
        
        for edge in theNode.incidentEdges:
            edge.otherEndFrom(theNode).incidentEdges.remove(edge)
        self.nodes.remove(theNode)
        
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
        
        if (event.getClickCount() == 2):
            
            print "(mouseClicked) at (", event.getX(), ",", event.getY(), ")"
            aNode = self.graph.nodeAt(event.getPoint()) ##Find the node where the click happened
            
            if aNode == None:   ##If there was no node, check to see if it was an edge
                anEdge = self.graph.edgeAt(event.getPoint())
                if anEdge == None:
                    self.graph.addNode(Node("x",event.getPoint()))  ##If no edge and no node clicked, create a new node
                else:
                    anEdge.toggleSelected() ##If there was an edge, toggle select
            else:   ## If there was a node that was clicked, toggle select it
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
        ##If the click was in an edge (i.e. not in a node, store the dragEdge variables
        else:
            self.dragEdge = self.graph.edgeAt(event.getPoint())
        
        ## Keep track of the eventPoint (for dragging edges, and multiple nodes)
        self.dragPoint = event.getPoint()
            
    def mouseDragged(self, event):
        '''Defines what happens when the mouse is dragged'''
        
        print "(mouseDragged)"
        ## Behaviour for dragging nodes
        if self.dragNode != None:
            if self.dragNode.selected == True:
                ## Drag each selected node
                for n in self.graph.returnSelectedNodes():
                    n.location.translate(event.getPoint().x - self.dragPoint.x,
                                         event.getPoint().y - self.dragPoint.y)
                self.dragPoint = event.getPoint()
                print "(mouseDragged) location of node = ", self.dragNode.location.x, ",", self.dragNode.location.y
            else:
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
            
        self.editor = GraphEditor(theGraph)
        
        self.add(self.editor)
        
        self.setTitle(theTitle)
        self.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE)
        self.setSize(600, 400)
        self.setVisible(True)
       
        

point1 = Point(1,2)
point2 = Point(3,4)        
node1 = Node("node1", point1)
node2 = Node("node2", point2)
edge1 = Edge(node1, node2, "edge1")
print node1
print edge1

map1 = Graph("Ontario and Quebec")
ottawa = Node("Ottawa", Point(250,100))
toronto = Node("Toronto", Point(100,170))
kingston = Node("Kingston", Point(200, 150))
montreal = Node("Montreal", Point(300,90))
map1.addNode(ottawa)
map1.addNode(toronto)
map1.addNode(kingston)
map1.addNode(montreal)

map1.addEdge(ottawa, toronto);
map1.addEdge(ottawa, montreal);
map1.addEdge(ottawa, kingston);
map1.addEdge(kingston, toronto);

print map1

for node in map1.nodes:
    print node.label

frame = GraphEditorFrame("title", map1)