#SyncPilot

#Notes: 
#March 15 - zero movement means zero salience. Need to try error:True
#
import pickle

import socket
import time
import re

import ccm
log=ccm.log(html=True)


from ccm.lib.actr import *

differencesList = []

class MyEnvironment(ccm.Model):
    speed=ccm.Model(isa='dial',which='speed',value=0,salience=0.8)
    altitude_indicator=ccm.Model(isa='dial',value=0)
    pitch=ccm.Model(isa='dial',value=0)
    yow=ccm.Model(isa='state',value=0)
    turn_rate=ccm.Model(isa='dial',value=0)
    heading=ccm.Model(isa='dial',which='heading',salience=0,value=0)
    engine_sound=ccm.Model(isa='sound',which='engine',value='none',salience=1)

    runway_heading=ccm.Model(isa='visuaal',value=0,salience=1)
    
    speed_change=ccm.Model(isa='noticable',change='speed',salience=0)
    heading_change=ccm.Model(isa='noticable',change='heading',direction='none',salience=0,rate='0.0',
                             x_value='0.0',timePeriod='0.0')
    pitch_change=ccm.Model(isa='noticable',which_change='pitch',direction='none',salience=0)
    
    
    
    def start(self):
        #ENVSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #ENVSock.bind(('127.0.0.1', 5557))
        Elapsed=0.0
        Heading=0.0
        Altitude=0.0
        Speed=0.0
        Pitch=0.0
        RPM=0.0
        Elevator=0.0
        ElevatorTrim=0.0
        Aileron=0.0
        AileronTrim=0.0
        #EVars = ENVSock.recvfrom(1024)
        #EVars = EVars[0]
        #Elapsed,Heading,Altitude,Speed,Pitch,RPM,Elevator,ElevatorTrim,
        #Aileron,AileronTrim = re.split(';',EVars,10)
        #EVars = re.split(';',EVars)
        #EVars = [float(x.strip()) for x in EVars]
        #print EVars
        while 1:
            yield 0.05
            ENVSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ENVSock.bind(('127.0.0.1',5557))
            EVars = ENVSock.recvfrom(1024)
            EVars = EVars[0]
            EVars = re.split(';',EVars)
            EVars = [float(x.strip()) for x in EVars]
            print EVars, "EVARS"

            if Heading == 0.0:
                Heading = EVars[3]
                
            if not Heading == 0.0:
                self.runway_heading.value = EVars[3] - self.heading.value
                
            self.heading.value = EVars[1]
            self.speed.value = EVars[3]


            global VisualReturn
            [x_value, y_value, timePeriod] = VisualReturn.differences

            self.heading_change.x_value=x_value
            self.heading_change.timePeriod=timePeriod
            if abs(x_value/timePeriod) > 300: #avoids anamolous large readings
                x_value = 0.0
            #x_value / timePeriod should give you pixels/second
            self.heading_change.rate=x_value/timePeriod
            self.heading_change.salience = abs(x_value/timePeriod/100) * 2.5
            #(x,y,z) = VisualReturn.differences
            
            
            #self.differencesList
            #self.differencesList.append((x,y,z))

            ####
            ####Eye output test
            #global differencesList
            #differencesList.append(x_value/timePeriod)
            
            #output = open('visual.pkl','wb')
            #pickle.dump(differencesList,output)
            #output.close()
            #print VisualReturn.difference, "Differencesssssssssssssssssssssssssssssssssssssssssssssss"
        
            
class VisionModule(ccm.ProductionSystem):
    production_time=0.05

    def find(b_plan_unit='planning_unit:get_to_speed', vision_module='busy:False error:False', b_cue='cue:!looking', b_unit_task='unit_task:!manage_heading'):
        #print "FINDING...."
        vision_module.request('isa:noticable change:?which')

    def find_fail(vision_module='error:True busy:False', b_unit_task='unit_task:!manage_heading!correct_steering'):
        vision_module.error = False
        

    def heading_change(b_vision='change:heading', b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:!manage_heading!correct_steering'): #vision had rate:?RATE
        #print RATE, "RATE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        b_unit_task.set('unit_task:manage_heading')
        

class AuditoryModule(ccm.ProductionSystem):
    production_time=0.05
    counter=0

    def listen(auditory_module='busy:False'):
        auditory_module.request('isa:sound which:?which value:?value')


class MotorMethods(ccm.ProductionSystem):
    production_time=0.05


    def right_rudder_increase(b_motor='right_leg:moving_rudder'):
        pass
    

    def right_rudder_slow_increase(b_motor='right_leg:moving_rudder'):
        current = float(self.parent.toDo[3].strip(';'))
        current = current + 0.0025
        if current >= 1.00:
            current = 1.00
            self.parent.b_motor.chunk['right_leg'] = 'max_rudder'

        self.parent.toDo[3] = repr(current) + ';'
        
    def to_full_throttle(b_motor='right_arm:moving_throttle'):
        current = float(self.parent.toDo[2].strip(';'))
        current = current + 0.005
        if current >= 1.00:
            current = 1.00
            self.parent.b_motor.chunk['right_arm'] = 'stopped_throttle'
            
        self.parent.toDo[2] = repr(current) + ';'
        
            
   # def throttle_stop_feedback(b_motor='right_arm:stopped_throttle'):
   #     self.b_cue['right_arm'] = 'stopped_throttle'
        
        

class MotorModule(ccm.Model):

    def do_wait(self, amount):
        #this is a waiting cheat.  See other comments
        amount = float(amount)
        yield amount
        self.parent.b_cue.set('cue:look_speed')

        
    def steady_throttle_increase(self):
        self.parent.b_motor.chunk['right_arm'] = 'moving_throttle'

    def get_speed(self):
        yield 0.0
        print "nope nope nope"

    def set_aileron_trim(self, value):
        yield 0.0
        self.parent.toDo[7] = repr(value) + ';' #TEMPORARY


    def hold_rudder(self):
        print "rudder"
        self.stop()
        
    def apply_rudder_for_zero(self, rate): #has direct access to the vision buffer NO IT DOESN"T
        yield 0.500
        rate = float(rate)
        if rate > 10.0:
            self.parent.b_motor.chunk['right_leg'] = 'moving_rudder'
        elif rate < 10 and rate > 0.00:
            self.parent.b_motor.chunk['right_leg'] = 'slowing_rudder_movement'
        elif round(rate,2) == 0.00:
            self.parent.b_motor.chunk['right_leg'] = 'holding_rudder_steady'
            
                              
        
        #self.stop()

            
        #print self.parent
        #print self.parent.b_vision
        #print self.parent.b_vision.chunk
        #print self.parent.b_vision.__dict__
        #print self.parent.b_vision.rate
        #rate = self.parent.b_vision.chunk['rate']
        
        #self.parent.toDo[2] = '0.3;'
    

    def release_brakes(self):
        yield 0.700
        self.parent.toDo[8] = '0;'
        self.parent.toDo[9] = '0;'
        self.parent.b_motor.chunk['left_leg']='none'
        self.parent.b_motor.chunk['right_leg']='none' #this probably doesn't work!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #print "pre-chunk"
        #print self.parent.b_motor.chunk, "chunky"
        #self.parent.b_operator.set('operator:abort')
        
        
    def apply_full_ground_brakes(self):
        #print "brakes!!!!"
        yield 1.0
        self.parent.toDo[8] = '1;' #temporary no brakes
        self.parent.toDo[9] = '1;'

        chk = str(self.parent.b_motor.chunk)
        lst = chk.split()
        target1 = False
        target2 = False
        for i in range(len(lst)):
            if 'right_leg' in lst[i]:
                target1 = i
            if 'left_leg' in lst[i]:
                target2 = i
        if target1:
            lst.remove(lst[target1])
        if target2:
            lst.remove(lst[target2])
        lst.append('right_leg:brake')
        lst.append('left_leg:brake')
        chk = ''
        for x in lst:
            chk = chk + ' ' + x
        
        self.parent.b_motor.set(chk)

    def start_engine(self):
        #print "WTF ENGINE?????????????????????????????????????????", FC
        #FC.work_queue.put('set /controls/switches/starter 1')#cmds = ['set /controls/switches/starter 1']
        self.parent.toDo[8]='0;'
        self.parent.toDo[9]='0;'
        self.parent.toDo[1]='1;'
        self.parent.toDo[2]='0;'
        self.parent.b_motor.chunk['right_arm']='hold_start'
        print "Engine starting."
        self.start_engine_followup()

    def start_engine_followup(self):
        yield 3.5 #HOW long the engine takes?
        #self.parent.b_auditory.set('engine:steady')
        self.parent.parent.engine_sound.which='engine'
        self.parent.parent.engine_sound.value='steady-low'
        self.parent.b_motor.chunk['right_arm']='none'
        
        


    
class MyAgent(ACTR):
    b_plan_unit=Buffer()
    b_unit_task=Buffer()
    b_cue=Buffer()
    b_method=Buffer()
    b_operator=Buffer()
    
    DMbuffer=Buffer()                           # create a buffer for the declarative memory (henceforth DM)
    DM=Memory(DMbuffer,latency=0.0,threshold=None)                         # create DM and connect it to its buffer    
    #motor=MotorModule()

    b_vision = Buffer()
    vision_module = SOSVision(b_vision,delay=0)
    p_vision=VisionModule(b_vision)

    b_motor = Buffer()
    motor=MotorModule()
    p_motor = MotorMethods(b_motor)

    b_auditory = Buffer()
    auditory_module = SOSVision(b_auditory,delay=0)
    p_auditory=AuditoryModule(b_auditory)    
    def init():
        DM.add('planning_unit:prepare_for_take_off unit_task:get_started cue:getting_started')
        DM.add('planning_unit:prepare_for_take_off unit_task:starter cue:break_on')
        DM.add('planning_unit:get_to_speed desired_speed:60 desired_heading:283.87 unit_task:get_to_speed cue:none')
        DM.add('planning_unit:get_to_speed desired_speed:60 desired_heading:283.87 unit_task:get_to_speed cue:throttled')
        
        b_motor.set('right_leg:none left_leg:none right_arm:none left_arm:none')
        b_plan_unit.set('planning_unit:prepare_for_take_off')
        b_unit_task.set('unit_task:none')
        b_operator.set('operator:none')
        b_cue.set('cue:none')


    def start1(b_plan_unit='planning_unit:prepare_for_take_off',b_unit_task='unit_task:none',b_cue='cue:none'):
        b_cue.set('cue:getting_started')
        DM.request('planning_unit:prepare_for_take_off unit_task:? cue:getting_started')
            
    def recall_start(b_plan_unit='planning_unit:prepare_for_take_off', b_unit_task='unit_task:none',DMbuffer='unit_task:?UT', b_cue='cue:getting_started'):
        b_unit_task.set('unit_task:' + UT)
        b_cue.set('cue:none')
        #print UT, "UT"
        #self.stop()

    def get_started(b_unit_task='unit_task:get_started', b_operator='operator:none', b_motor='right_leg:none left_leg:none'):
        print b_auditory.chunk, "ASDFAASDFASDFASF"
        b_operator.set('operator:both_ground_brakes')
        #self.stop()
        #b_cue.set('cue:get_started_two')
        chk = str(b_cue.chunk)
        chk = chk + ' trim:none'
        b_cue.set(chk)
        #self.stop()

    def press_both_brakes(b_operator='operator:both_ground_brakes'):
        motor.apply_full_ground_brakes()
        b_operator.set('operator:none')
        #self.stop()

    #def start_engine(b_operator='operato

    def get_started_trim(b_unit_task='unit_task:get_started', b_operator='operator:none', b_cue='trim:!set'): #motor doesn't matter
        print "work on this..."
        
        motor.set_aileron_trim(0.09)
        chk = str(b_cue.chunk)
        lst = chk.split()
        lst.remove('trim:none')
        lst.append('trim:set')
        chk = ''
        for item in lst:
           chk = chk + ' ' + item
        b_cue.set(chk)
        #self.stop()

    def get_started_two(  b_unit_task='unit_task:get_started', b_operator='operator:none', b_motor='right_leg:brake left_leg:brake', b_cue='trim:set', b_auditory='which:engine value:none'):
        b_operator.set('operator:start_engine')
        #self.stop()
        #b_cue.set('cue:get_started_three')

    def start_engine(b_operator='operator:start_engine'):
        motor.start_engine()
        b_operator.set('operator:wait_for_engine')
        
        
        

    def wait_for_engine(b_operator='operator:wait_for_engine', b_auditory='which:engine value:steady-low'):
        b_operator.set('operator:none')
        b_plan_unit.set('planning_unit:get_to_speed')
        b_unit_task.set('unit_task:none')
        b_cue.set('cue:none')
        

    def get_to_speed_1(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:none'):
        DM.request('planning_unit:get_to_speed unit_task:? cue:none')
        b_cue.set('cue:recall')

    def get_to_speed_2(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:none',DMbuffer='unit_task:?UT', b_cue='cue:recall'):
        b_unit_task.set('unit_task:' + UT)
        b_cue.set('cue:none')
        b_operator.set('operator:release_brakes')

    def get_to_speed_release_brakes(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:get_to_speed',
                                    b_operator='operator:release_brakes', b_cue='cue:none'):
        motor.release_brakes()
        b_operator.set('operator:throttle_up')

    def get_to_speed_throttle_up(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:get_to_speed',
                                    b_operator='operator:throttle_up', b_cue='cue:none'):
        motor.steady_throttle_increase()
        b_unit_task.set('unit_task:monitor_takeoff')
        b_operator.set('operator:none')
        

    def get_to_speed_monitor_takeoff(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:monitor_takeoff',
                                    b_operator='operator:none', b_cue='cue:none'):
        b_cue.set('cue:window')


    def get_to_speed_window(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:monitor_takeoff', b_operator='operator:none',
                            b_cue='cue:window'):
        motor.do_wait(3.00)
        b_cue.set('cue:wait_cue_not_matchable')
        
    def get_to_speed_monitor_look_speed(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:monitor_takeoff', b_operator='operator:none',
                            b_cue='cue:look_speed'):
        b_operator.set('operator:look_speed')
        b_cue.set('cue:none')

    def get_to_speed_monitor_look_at_speedometer(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:monitor_takeoff',
                                                 b_operator='operator:look_speed', b_cue='cue:none'):
        pass        
        #vision_module.request('isa:dial which:speed value:?')
        
        
   # def get_to_speed_steer1(b_plan_unit='planning_unit:get_to_speed', b_unit_task='unit_task:none',
   #                         b_opertator='operator:none', b_cue='cue:movement'):
   #     pass

    def manage_heading(b_unit_task='unit_task:manage_heading', b_operator='operator:!apply_rudder!look_for_movement!see_the_movement'): #temporarily use to find correction formula
        #The !(s) are because the operator is left over whenever it was interupted. So, as long as it's not any of the ones used for correction, that's fine.
        b_operator.set('operator:none')
        


    def manage_heading2(b_unit_task='unit_task:manage_heading', b_operator='operator:none'):
        b_operator.set('operator:look_for_movement')

    #if take the b_unit_task='unit_task:manage_heading' out, then these operators can be recycled in a countersteering unit_task
        #SyncPilot11.py
        
    def manage_heading_look_movement(b_operator='operator:look_for_movement'):
        vision_module.request('isa:noticable change:?which rate:?RATE')#this is possible because it's already been alerted that there's a change
        b_operator.set('operator:see_the_movement')
        
    def manage_heading_look_movement2(b_operator='operator:see_the_movement', b_vision='rate:?RATE', b_motor='right_leg:!holing_rudder_steady'):
        motor.apply_rudder_for_zero(RATE)
        #self.stop()
        b_operator.set('operator:look_for_movement') #reason to think there should be another unit task
                                                    #the pilot will respond, but the motor system will take time,
                                                    #and a failure to see the could happen, which ends up a strange
                                                    #situation where it's correcting, but doing something else.
        b_unit_task.set('unit_task:correct_steering')

#To note, is the system can't actually see 0 (zero) movement. It will have a salience of zero. A failure to see, means there was no movement!

    def correct_steering_steady(b_motor='right_leg:holding_rudder_steady'):
        print "holding steady"
        self.stop()
        

    def correct_steering_no_movement(b_unit_task='unit_task:correct_steering', vision_module='error:True', b_vision=None):
        motor.hold_rudder()
        
                                     
    #if you take the unit_task out of this one too, it will also be recycled.    
    def manage_heading_look_failed(b_operator='operator:see_the_movement',
                                   vision_module='error:True', b_vision=None): #should fire ~%50 of the time with _so_return
        
        b_operator.set('operator:look_for_movement')
        
        
    def manage_heading_look_failed_so_return(b_unit_task='unit_task:manage_heading', b_operator='operator:see_the_movement',
                                   vision_module='error:True', b_vision=None):
        b_operator.set('operator:none')
        b_unit_task.set('unit_task:none') #should reset and find a new unit task

        
        
VisualReturn = ccm.scheduler.TC        
pilot=MyAgent()
Cockpit=MyEnvironment()
Cockpit.differencesList = []
Cockpit.agent=pilot
pilot.toDo = ccm.scheduler.aTodo
pilot.toDo[3] = '0;' #rudder initialization
Cockpit.VisualReturn = ccm.scheduler.TC
pilot.VisualReturn = ccm.scheduler.TC
ccm.log_everything(Cockpit)

Cockpit.run(25)
ccm.finished()



