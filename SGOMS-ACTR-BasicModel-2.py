import sys

sys.path.insert(0, 'C:/CCMSuite/CCMSuite/')

import ccm
log=ccm.log()

from ccm.lib.actr import *

'''2014.07.07
This is going to be a simple two planning-unit model based on Gears of War.
Each planning unit will have two unit tasks that fire.

I am changing SGOMS-ACTR-BasicModel-1 to make it more generic, and less hard-coded

The planning units will be:
Take Area
    UT: Advance
    UT: Kill Enemies
Hold Area
    UT: Find Cover

The behaviour should be:
Context is set

PU fires
Request Next UT (Sets new PU chunk in DM)
Retrieve Next UT (Retrieves new PU chunk in DM)
Ut
Request Next UT
Retrive Next UT
UT
Request Next UT
Retrieve Next UT
Last UT

PU Fires
'''

# --------------- Environment ------------------

class MyEnvironment(ccm.Model):
    ## Add relevant details to the environment here
    ## We'll have big and little monters, and cover in our environment
    ## Right now the agent does not interact with the environment - 2014.05.30

    littleMonster = ccm.Model(isa='monster', size='little', state='alive', salience=0.2)
    bigMonster = ccm.Model(isa='monster', size='big', state='alive', salience=0.4)

    cover = ccm.Model(isa='cover', location='accessible', salience=0.2)
    area = ccm.Model(isa='area', status='not_clear', salience=0.2)

    motor_finst = ccm.Model(isa='motor_finst',
                            state='re_set')  ## I'm not sure what a motor_finst is or what it does, but it seems important


# --------------- Motor Module ------------------

class MotorModule(ccm.Model):  ### defines actions on the environment
    ## Define what actions do what
    ## These are just copied from the Roosters model, I don't actually know what they do here.

    def change_location(self, env_object, slot_value):
        yield 2
        x = eval('self.parent.parent.' + env_object)  #self.parent.parent is the environment
        print self.parent.parent, 'XXX'
        x.location = slot_value
        print env_object
        print slot_value
        self.parent.parent.motor_finst.state = 'finished'

    def kill_enemy(self, env_object, slot_value):  ## This is my attempt at creating my own motor method
        yield 2
        x = eval('self.parent.parent.' + env_object)  #self.parent.parent is the environment
        print self.parent.parent, 'XXX'
        x.state = slot_value
        print env_object
        print slot_value
        self.parent.parent.motor_finst.state = 'finished'

    def motor_finst_reset(self):
        self.parent.parent.motor_finst.state = 're_set'


# --------------- Methods Module ------------------

class MethodModule(ccm.ProductionSystem):  # creates an extra production system for the motor system
    production_time = 0.04


## This will probably contain methods in the future, I'm just going to use unit tasks for the job now


# --------------- Vision Module ------------------

class VisionModule(ccm.ProductionSystem):  ## This is basically just a place holder right now
    production_time = 0.045


# --------------- Emotion Module ------------------

class EmotionalModule(ccm.ProductionSystem):  ## This is basically just a place holder right now
    production_time = 0.043


# --------------- Agent ------------------

class MyAgent(ACTR):
    # module buffers
    b_system = Buffer()  # create system buffers
    b_DM = Buffer()
    b_motor = Buffer
    b_visual = Buffer()
    b_image = Buffer()

    # goal buffers
    b_context = Buffer()
    b_plan_unit = Buffer()  # create buffers to represent the goal module
    b_unit_task = Buffer()
    b_method = Buffer()
    b_operator = Buffer()
    b_emotion = Buffer()

    # associative memory
    DM = Memory(b_DM)  # create the DM memory module

    # perceptual motor module
    vision_module = SOSVision(b_visual, delay=0)  # create the vision module
    motor = MotorModule(b_motor)  # put motor production module into the agent

    # auxillary production modules
    Methods = MethodModule(b_method)  # put methods production module into the agent
    Eproduction = EmotionalModule(b_emotion)  # put the Emotion production module into the agent
    p_vision = VisionModule(b_visual)


    def init():
        ##LHS of colon = slot, RHS of colon = value of the slot, the whole thing is a chunk
        ##(or made up of chunks?) - terminology is ambiguous

        ## Add each of the planning units to the DM memory module
        ## Each item in memory seems to correspond to one relationship between the planning unit and unit task

        ## The syntax for representing planning units in DM seems to be as follows:
        ##      Which planning unit         trigger to fire      set next trigger   associated next unit task (one ahead of 'cue')
        DM.add('planning_unit:take_area    cuelag:none          cue:start          unit_task:advance')
        DM.add('planning_unit:take_area    cuelag:start         cue:advance        unit_task:kill_enemies')
        DM.add('planning_unit:take_area    cuelag:advance       cue:kill_enemies   unit_task:finished')

        DM.add('planning_unit:hold_area    cuelag:none          cue:start          unit_task:find_cover')
        DM.add('planning_unit:hold_area    cuelag:start         cue:find_cover     unit_task:finished')
        #DM.add ('planning_unit:hold_area    cuelag:find_cover    cue:kill_enemies   unit_task:finished')       

        b_context.set('area:not_clear cover:not_taken status:not_started completed:no')  ## Here the initial context is set


    ########### These are the planning units

    ## If the context buffer matches the pattern, start firing the planning unit

    def take_area(b_context='area:not_clear status:not_started'):
        print "(take_area) Fires!"
        b_plan_unit.set(
            'planning_unit:take_area cuelag:none cue:start unit_task:advance state:running')  # which planning unit and where to start
        b_unit_task.set('unit_task:advance state:running')
        b_context.set('area:not_clear status:started')  # update context

    def hold_area(b_context='area:clear cover:not_taken status:not_started'):
        print "(hold_area) Fires!"
        b_plan_unit.set('planning_unit:hold_area cuelag:none cue:start unit_task:find_cover state:running')
        b_unit_task.set('unit_task:find_cover state:start')
        b_context.set('area:clear status:started')  # update context


    ######### These are the unit tasks

    def advance_unit_task(b_unit_task='unit_task:advance state:running'):
        print "(advance_unit_task) Fires!"
        b_unit_task.set('unit_task:advance state:finished')  ## This should trigger request_next_unit_task to fire

    def kill_enemies_unit_task(b_unit_task='unit_task:kill_enemies state:start'):
        print "(kill_enemies_unit_task) Fires!"
        b_unit_task.set('unit_task:kill_enemies state:finished')  ## This should trigger the last_unit_task to fire
        ## It should request DM for the next UT, find the 'finished' flag in the PU buffer, and change the context
        b_context.set('area:clear cover:not_taken status:not_started')

    def find_cover(b_unit_task='unit_task:find_cover state:start'): ##This is the unit task for Hold Area
        print "(find_cover_unit_task) Fires!"
        b_unit_task.set('unit_task:find_cover state:finished')  ## This should trigger the last_unit_task to fire
        b_context.set('area:clear cover:taken status:completed')


    ########## request a unit task  ## These are kind of global methods for setting planning units in motion

    def request_next_unit_task(
            b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running',
            b_unit_task='unit_task:?unit_task state:finished'):
        print "(request_next_unit_task) Fires!, b_plan_unit matches: planning_unit... state:running, b_unit_task matches: unit_task... state:finished"
        print "(request_next_unit_task) About to request DM for next planning unit by feeding it variable planning units, cues etc."
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')
        print "(request_next_unit_task) Finished requesting DM for next planning unit"
        print "(request_next_u_t) About to set planning unit buffer to: planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve"
        b_plan_unit.set(
            'planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve')  # next unit task
        print "(request_next_u_t) Finished setting planning unit buffer to: planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve"
        print '(request_next_unit_task) Production Finished. unit task = ', unit_task

    def retrieve_next_unit_task(b_plan_unit='state:retrieve',
                                b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):
        print "(retrieve_next_u_t) Fires! b_plan_unit matches: state:retrieve, " \
              "b_DM matches: planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task"
        print "(retrieve_u_t) About to set b_plan_unit"
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        print "(retrieve_u_t) Finished setting b_plan_unit to: planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running"
        print "(retrieve_u_t) About to set unit task buffer..."
        b_unit_task.set('unit_task:?unit_task state:start')
        print "(retrieve_u_t) Finished setting unit task buffer to:  'unit_task:?unit_task state:start'"
        print '(retrieve_u_t) Production Finished. unit_task = ', unit_task

    def last_unit_task(b_unit_task='unit_task:finished state:start', ## Where is unit_task set to 'finished'?
                       b_plan_unit='planning_unit:?planning_unit'):
        print "(last_unit_task) Fires! b_unit_task matches:  unit_task:finished state:start. b_plan_unit matches: 'planning_unit:?planning_unit'"
        print '(last_unit_task) finished planning unit=', planning_unit
        print "(last_unit_task) About to set the unit task buffer to 'stop'"
        b_unit_task.set('stop')
        print "(last_unit_task) Finished setting the unit task buffer to 'stop'"
        print "(last_unit_task) About to set the context buffer..."
        #b_context.set('area:clear status:completed')
        print "(last_unit_task) Finished setting context buffer to: 'area:clear status:completed'"
        print "(last_unit_task) Production Finished."


tim = MyAgent()  # name the agent
subway = MyEnvironment()  # name the environment
subway.agent = tim  # put the agent in the environment
ccm.log_everything(subway)  # print out what happens in the environment

subway.run()  # run the environment
ccm.finished()  # stop the environment