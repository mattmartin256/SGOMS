'''
2014.07.03

@author: Matt Martin

This is a workspace to figure out how to represent the output from the GUI in a workable ACT-R model


For every planning unit:

Need a chunk in DM that represents each unit task, including:
Which PU the UT belongs to (planning_unit:name)
The preceding Unit Task (cuelag)
The cue to fire (cue)
The Unit Task (unit_task:name)  
*** Need an *extra* UT in DM at the end called 'finished'
A single-UT model would look like:

DM.add ('planning_unit:prep_wrap    cuelag:none          cue:start          unit_task:veggies')
DM.add ('planning_unit:prep_wrap    cuelag:start         cue:veggies        unit_task:finished')

^ PUxUTRelations will do this job

Need a production which:
Fires based on some context (ie. buffer contents)
Sets the unit tasks in motion (changes UT and PU buffer contents)
Changes the context (changes context buffer contents) 

For each unit task: 

Need a production that fires based on the unit task buffer
The production must change the contents of some buffer (either the context or other UT buffers)

the cuelag is the previous  cue ('none' if no previous cue)
the cue is the previous unit_task ('start' if no previous unit_task)
^ This is only true for the Rooster's model, the cue can be something else entirely (as in the pilot model) 


The cuelag was meant to represent the previous unit task that fired
in order to keep track of where the agent was in the planning unit
'''