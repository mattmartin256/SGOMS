import sys
sys.path.insert(0, 'C:/CCMSuite/CCMSuite/')
import ccm
log=ccm.log()
from ccm.lib.actr import *

class MyEnvironment(ccm.Model):
   pass

class MyAgent(ACTR):
    b_context=Buffer()
    b_plan_unit=Buffer()
    b_unit_task=Buffer()
    b_DM=Buffer()
    DM=Memory(b_DM)

    def init():
        DM.add('planning_unit:PU1 cuelag:none cue:start unit_task:UT1')
        DM.add('planning_unit:PU1 cuelag:start cue:UT1 unit_task:UT2')
        DM.add('planning_unit:PU1 cuelag:UT1 cue:UT2 unit_task:finished')
        pass    ## Required for Python syntax reasons when there are no Unit Tasks in the Model
##Initial Model Behaviours
        pass    ## Required for Python syntax reasons when there are no Unit Tasks in the Model    
## Planning Units

    def PU1():
        pass
        pass    ## Required for Python syntax reasons when there are no Planning Units in the Model    
## Unit Tasks

    def UT1():
        pass

    def UT2():
        pass

    def finished():
        pass

## Global productions for retrieving Unit Tasks from DM

    def request_next_unit_task(b_plan_unit='planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running', b_unit_task='unit_task:?unit_task state:finished'):
        DM.request('planning_unit:?planning_unit cue:?unit_task unit_task:? cuelag:?cue')
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:retrieve')

    def retrieve_next_unit_task(b_plan_unit='state:retrieve', b_DM='planning_unit:?planning_unit cuelag:?cuelag cue:?cue!finished unit_task:?unit_task'):
        b_plan_unit.set('planning_unit:?planning_unit cuelag:?cuelag cue:?cue unit_task:?unit_task state:running')
        b_unit_task.set('unit_task:?unit_task state:start')

    def last_unit_task(b_unit_task='unit_task:finished state:start', b_plan_unit='planning_unit:?planning_unit'):
        b_unit_task.set('stop')

## Code to run the model
tim = MyAgent()
env = MyEnvironment()
env.agent = tim
ccm.log_everything(env)

env.run()
ccm.finished()
