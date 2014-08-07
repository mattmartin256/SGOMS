
                                      #################### SGOMS ###################

import sys

sys.path.insert(0, 'C:/CCMSuite/CCMSuite/')

import ccm      
log=ccm.log()
#log=ccm.log(html=True) 

from ccm.lib.actr import *



# --------------- Environment ------------------

class MyEnvironment(ccm.Model):
    
    ## I think these are chunks that represent knowledge about the environment
    ## Each chunk has a number of slots that are filled with various symbols
    ## The first slot specifies what the chunk is, the rest are other parameters
    chicken=ccm.Model(isa='chicken',location='grill',state='cooked',salience=0.2)
    pita=ccm.Model(isa='pita',location='bins2',status='in_bag',salience=0.2)
    
    cheese=ccm.Model(isa='cheese',location='in_bins1',salience=0.2)
    feta=ccm.Model(isa='feta',location='in_bins1',salience=0.2)
    cucumber=ccm.Model(isa='cucumber',location='in_bins1',salience=0.2)
    green_pepper=ccm.Model(isa='green_pepper',location='in_bins1',salience=0.2)
    mushroom=ccm.Model(isa='mushroom',location='in_bins1',salience=0.2)
    lettuce=ccm.Model(isa='lettuce',location='in_bins1',salience=0.2)
    tomato=ccm.Model(isa='tomato',location='in_bins1',salience=0.2)

    green_olives=ccm.Model(isa='green_olives',location='in_bins2',salience=0.2)
    black_olives=ccm.Model(isa='black_olives',location='in_bins2',salience=0.2)
    hot_peppers=ccm.Model(isa='hot_peppers',location='in_bins2',salience=0.2)
    onion=ccm.Model(isa='onion',location='in_bins2',salience=0.2)
    
    humus=ccm.Model(isa='humus',location='in_bins2',salience=0.2)
    tzatziki=ccm.Model(isa='tzatziki',location='in_bins2',salience=0.2)

    hot_sauce=ccm.Model(isa='hot_sauce',location='in_bins2',salience=0.2)
    
    worker=ccm.Model(isa='worker',location='at_counter',salience=0.2)
    spider=ccm.Model(isa='spider',location='on_counter',feature1='yellow_stripe',salience=0.99)

    motor_finst=ccm.Model(isa='motor_finst',state='re_set')     ## I'm not sure what a motor_finst is or what it does, but it seems important



# --------------- Motor Module ------------------

class MotorModule(ccm.Model):     ### defines actions on the environment
        
    def change_location(self, env_object, slot_value):
        yield 2                   
        x = eval('self.parent.parent.' + env_object)    #self.parent.parent is the environment
        print self.parent.parent, 'XXX'
        x.location= slot_value
        print env_object
        print slot_value
        self.parent.parent.motor_finst.state='finished'
        
    def motor_finst_reset(self):             
        self.parent.parent.motor_finst.state='re_set'
        

# --------------- Methods Module ------------------

class MethodModule(ccm.ProductionSystem):  # creates an extra production system for the motor system
    production_time=0.04


    # adding method

    ## If the method buffer contains the chunk 'method:add target:?target state:start'
    ## Then change the target chunk to have a new location
    ## And change the content of the method buffer to be a chunk with a 'running' state

    ## I believe this is the syntax for defining a 'pattern' to match with a chunk
    ## The target is a variable, as indicated by the '?', which means it could match to any target 
    ## The LHS of the ':' specifies the slot name, the RHS specifies the value of the slot
    ## Spaces separate the slots
    def do_add(b_method='method:add target:?target state:start'): # target is the chunk to be altered
        print "(do_add) Fires!"
        motor.change_location(target,"in_wrap")
        b_method.set('method:add target:?target state:running')
        print 'target=',target
        print "(do_add) Method finished"
     
    def done_add(b_method='method:add target:?target state:running',
                 motor_finst='state:finished'):
        print "(done_add) Fires!"
        b_method.set('method:add target:?target state:finished')
        motor.motor_finst_reset()
        print 'finished=',target
        print "(done_add) Method finished"
        

    # checking method


    def do_check(b_method='method:check target:?target state:start'): # target is the chunk to be checked
        print "(do_check) Fires!"
        b_method.set('method:check target:?target state:running')
        print 'target=',target
        print "(do_check) Method finished"
     
    def result1_check(b_method='method:check target:?target state:running',
                      chicken='state:cooked'):
        print "(result1_check) Fires!"
        b_method.set('method:check target:?target state:finished')
        print 'finished=',target
        print "(result1_check) Method finished"

    def result2_check(b_method='method:check target:?target state:running',
                      chicken='state:raw'):
        print "(result2_check) Fires!"
        b_method.set('method:check target:?target state:finished')
        print 'finished=',target
        print "(result2_check) Method finished"


# --------------- Vision Module ------------------

class VisionModule(ccm.ProductionSystem):  
    production_time=0.045

# --------------- Emotion Module ------------------

class EmotionalModule(ccm.ProductionSystem):  
    production_time=0.043


# --------------- Agent ------------------

class MyAgent(ACTR):

    # module buffers
    b_system=Buffer()                            # create system buffers
    b_DM=Buffer()            
    b_motor=Buffer
    b_visual=Buffer()
    b_image=Buffer()

    # goal buffers
    b_context=Buffer()                          # create buffers to represent the goal module
    b_plan_unit=Buffer()                        ## There is a planning unit buffer which keeps track of the relevant planning unit                       
    b_unit_task=Buffer()                        ## And a Unit Task buffer
    b_method=Buffer()                           ## As well as a Method buffer which is utilized
    b_operator=Buffer()                         ## I think the operator buffer is defined here but not implemented in any way
    b_emotion=Buffer()                          ## ^Same goes for the emotion buffer

    # associative memory
    DM=Memory(b_DM)                              # create the DM memory module

    # perceptual motor module
    vision_module=SOSVision(b_visual,delay=0)    # create the vision module
    motor=MotorModule(b_motor)                   # put motor production module into the agent

    # auxillary production modules
    Methods=MethodModule(b_method)               # put methods production module into the agent    
    Eproduction=EmotionalModule(b_emotion)       # put the Emotion production module into the agent
    p_vision=VisionModule(b_visual)    
    
    
    
    def init():                                             

    ##LHS of colon = slot, RHS of colon = value of the slot, the whole thing is a chunk(?) - terminology is ambiguous

    ## Add each of the planning units to the DM memory module
    ## Each item in memory seems to correspond to one relationship between the planning unit and unit task
        
    ## The syntax for representing planning units in DM seems to be as follows:
    ##          Which planning unit         previous trigger     trigger to fire    associated next unit task       
        DM.add ('planning_unit:prep_wrap    cue:start          unit_task:veggies')     ##I'm not sure why both cuelag and cue are necessary                  
        DM.add ('planning_unit:prep_wrap    cue:veggies        unit_task:cheese')      ## If it's just to differentiate the PUs in DM, they can
        DM.add ('planning_unit:prep_wrap    cue:cheese         unit_task:pickles')     ## be differentiated by their associated unit tasks alone
        DM.add ('planning_unit:prep_wrap    cue:pickles        unit_task:spreads')
        DM.add ('planning_unit:prep_wrap    cue:spreads        unit_task:sauce')
        DM.add ('planning_unit:prep_wrap    cue:sauce          unit_task:finished')

        DM.add ('planning_unit:meat    cue:start          unit_task:check_meat')                     
        DM.add ('planning_unit:meat    cue:check_meat     unit_task:add_meat')
        DM.add ('planning_unit:meat    cue:add_meat       unit_task:finished')       


        b_context.set('customer:new order:wrap status:not_started completed:no')        ## Here the initial context is set

        ## These need to be added to memory because the buffers need to be set by them (?)

## These are productions starting here and below
########### choose a planning unit  ## These are the planning units

## If the context buffer matches one of these two patterns, start firing the appropriate planning unit
                        
    def prep_wrap(b_context='customer:new order:wrap status:not_started'):
         print "(prep_wrap) Fires! context buffer matched to:  customer:new order:wrap status:not_started"
         print "(prep_wrap) About to set the planning unit buffer..."
         b_plan_unit.set('planning_unit:prep_wrap cue:start unit_task:veggies state:running') # which planning unit and where to start
         print "(prep_wrap) Finished setting planning unit buffer to:  planning_unit:prep_wrap cuelag:none cue:start unit_task:veggies state:running"
         print "(prep_wrap) About to set the unit task buffer..."
         b_unit_task.set('unit_task:veggies state:finished') # there is always a unit task that has finished before another can start
         print "(prep_wrap) Finished setting unit task buffer to:  unit_task:veggies state:finished"
         print "(prep_wrap) About to set the context buffer..."
         b_context.set('customer:new order:wrap status:started') # update context
         print "(prep_wrap) Finished setting context buffer to:  customer:new order:wrap status:started"
         print '(prep_wrap) method finished'

    def get_meat(b_context='customer:new order:wrap status:prepped done:!meat'):
         b_plan_unit.set('planning_unit:meat cue:start unit_task:check_meat state:running') ##Setting the buffer is what pushes the program along
         b_unit_task.set('unit_task:check_meat state:finished')
         b_context.set('customer:new order:wrap status:started')
         print 'get the meat'
  

########## request a unit task  ## These are kind of global methods for setting planning units in motion

    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cue:?cue unit_task:?unit_task state:running',                   
                               b_unit_task='unit_task:?unit_task state:finished'):
        print "(request_next_unit_task) Fires!, b_plan_unit matches: planning_unit... state:running, b_unit_task matches: unit_task... state:finished" 
        print "(request_next_unit_task) About to request DM for next planning unit by feeding it variable planning units, cues etc."
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:?')
        print "(request_next_unit_task) Finished requesting DM for next planning unit"
        print "(request_next_u_t) About to set planning unit buffer to: planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve"
        b_plan_unit.set('planning_unit:?planning_unit cue:?cue unit_task:?unit_task state:retrieve') # next unit task
        print "(request_next_u_t) Finished setting planning unit buffer to: planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve"
        print '(request_next_unit_task) Production Finished. unit task = ',unit_task

    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cue:?cue!finished unit_task:?unit_task'):
        print "(retrieve_next_u_t) Fires! b_plan_unit matches: state:retrieve, " \
        "b_DM matches: planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task"
        print "(retrieve_u_t) About to set b_plan_unit"
        b_plan_unit.set('planning_unit:?planning_unit cue:?cue unit_task:?unit_task state:running')
        print "(retrieve_u_t) Finished setting b_plan_unit to: planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running"
        print "(retrieve_u_t) About to set unit task buffer..."
        b_unit_task.set('unit_task:?unit_task state:start')
        print "(retrieve_u_t) Finished setting unit task buffer to:  'unit_task:?unit_task state:start'"
        print '(retrieve_u_t) Production Finished. unit_task = ',unit_task


    def last_unit_task(b_unit_task='unit_task:finished state:start',
                       b_plan_unit='planning_unit:?planning_unit'):
        print "(last_unit_task) Fires! b_unit_task matches:  unit_task:finished state:start. b_plan_unit matches: 'planning_unit:?planning_unit'" 
        print '(last_unit_task) finished planning unit=',planning_unit
        print "(last_unit_task) About to set the unit task buffer to 'stop'"
        b_unit_task.set('stop')
        print "(last_unit_task) Finished setting the unit task buffer to 'stop'"
        print "(last_unit_task) About to set the context buffer..."
        b_context.set('customer:new order:wrap status:prepped done:?planning_unit')
        print "(last_unit_task) Finished setting context buffer to: 'customer:new order:wrap status:prepped done:?planning_unit'"
        print "(last_unit_task) Production Finished."




################# unit tasks ###################



## veggies

## I think 'veggies' is a single unit task with multiple steps,
## Each function definition is one step/method to be completed serially
        
    def vegg_unit_task(b_unit_task='unit_task:veggies state:start'):    ## Veggies doesn't actually fire in this model...
        print '### (vegg_unit_task) start the veggies unit task'
        print "(vegg_unit_task) About to set the unit task buffer..."
        b_unit_task.set('unit_task:veggies state:running')
        print "(vegg_unit_task) Finished setting the unit task buffer"
        print "(vegg_unit_task) About to set the method buffer"
        b_method.set('method:add target:lettuce state:start')
        print "(vegg_unit_task) Finished setting the method buffer"
        print "(vegg_unit_task) Production finished"

    def lettuce(b_unit_task='unit_task:veggies state:running',          ## A method within the veggies unit task, as are all below
                b_method='method:add target:lettuce state:finished'):
        print 'lettuce method finished'
        b_method.set('method:add target:tomato state:start')   
        
    def tomato(b_unit_task='unit_task:veggies state:running',
               b_method='method:add target:tomato state:finished'):
        print 'tomato method finished'
        b_method.set('method:add target:cucumber state:start')

    def cucumber(b_unit_task='unit_task:veggies state:running',
                 b_method='method:add target:cucumber state:finished'):
        print 'cucumber method finished'
        b_method.set('method:add target:green_pepper state:start')

    def green_pepper(b_unit_task='unit_task:veggies state:running',
                     b_method='method:add target:green_pepper state:finished'):
        print 'green_pepper method finished'
        b_method.set('method:add target:mushroom state:start')

    def mushroom(b_unit_task='unit_task:veggies state:running',
                 b_method='method:add target:mushroom state:finished'):
        print 'mushroom method finished'
        b_unit_task.set('unit_task:veggies state:finished')
        
        


## cheese

    def cheese_unit_task(b_unit_task='unit_task:cheese state:start'):   ## Unit Task
        print '### start the cheese unit task'
        b_unit_task.set('unit_task:cheese state:running')
        b_method.set('method:add target:feta state:start')  
        
    def cheese(b_unit_task='unit_task:cheese state:running',            ## Method
               b_method='method:add target:feta state:finished'):
        print 'cheese method finished'
        b_unit_task.set('unit_task:cheese state:finished')

## pickles


    def pickles_unit_task(b_unit_task='unit_task:pickles state:start'):
        print 'start the pickles unit task'
        b_unit_task.set('unit_task:pickles state:running')
        b_method.set('method:add target:green_olives state:start')  

    def green_olives(b_unit_task='unit_task:pickles state:running',
                     b_method='method:add target:green_olives state:finished'):
        print 'green_olives method finished'
        b_method.set('method:add target:black_olives state:start')   
        
    def black_olives(b_unit_task='unit_task:pickles state:running',
               b_method='method:add target:black_olives state:finished'):
        print 'black_olives method finished'
        b_method.set('method:add target:onion state:start')

    def onion(b_unit_task='unit_task:pickles state:running',
                 b_method='method:add target:onion state:finished'):
        print 'onion method finished'
        b_unit_task.set('unit_task:pickles state:finished')


## spreads

    def humus_unit_task(b_unit_task='unit_task:spreads state:start'):
        print 'start the spreads unit task'
        b_unit_task.set('unit_task:spreads state:running')
        b_method.set('method:add target:humus state:start')  

    def humus_end(b_unit_task='unit_task:spreads state:running',
                    b_method='method:add target:humus state:finished'):
        print "spreads finished"
        b_unit_task.set('unit_task:spreads state:finished')


## sauce

    def sauce_unit_task(b_unit_task='unit_task:sauce state:start'):
        print 'start the sauce unit task'
        b_unit_task.set('unit_task:sauce state:running')
        b_method.set('method:add target:hot_sauce state:start')  

    def sauce_end(b_unit_task='unit_task:sauce state:running',
                    b_method='method:add target:hot_sauce state:finished'):
        print "sauce finished"
        b_unit_task.set('unit_task:sauce state:finished')
        
## check_meat

    def check_meat_unit_task(b_unit_task='unit_task:check_meat state:start'):
        print 'start the check_meat unit task'
        b_unit_task.set('unit_task:check_meat state:running')
        b_method.set('method:check target:chicken state:start')  
        
    def check_meat(b_unit_task='unit_task:check_meat state:running',
                   b_method='method:check target:chicken state:finished'):
        print 'chicken is checked'
        b_unit_task.set('unit_task:check_meat state:finished')

## add_meat

    def add_meat_unit_task(b_unit_task='unit_task:add_meat state:start'):
        print 'start the add_meat unit task'
        b_unit_task.set('unit_task:add_meat state:running')
        b_method.set('method:add target:chicken state:start')  
        
    def add_meat(b_unit_task='unit_task:add_meat state:running',
                 b_method='method:add target:chicken state:finished'):
        print 'chicken is added'
        b_unit_task.set('unit_task:add_meat state:finished')
        

############# last unit task in a planning unit

##    def last_unit_task(b_unit_task='unit_task:finished state:start'):
##        print 'finished planning unit'
##        b_unit_task.set('stop')
##        b_context.set('customer:new order:wrap status:prepped')





          
tim=MyAgent()                              # name the agent
subway=MyEnvironment()                     # name the environment
subway.agent=tim                           # put the agent in the environment
ccm.log_everything(subway)                 # print out what happens in the environment

subway.run()                               # run the environment
ccm.finished()                             # stop the environment
