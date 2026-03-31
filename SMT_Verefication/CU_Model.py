from z3 import *

assigned_before = Bool('assigned_before')
duration_before = Int('duration_before')

assigned_after = Bool('assigned_after')
duration_after = Int('duration_after')

transition_assign = And(
    assigned_before == False,
    assigned_after == True,
    duration_after > 0
)

transition_tick = If(
    assigned_before == True,
    If(duration_before > 0,
       And(assigned_after == True, duration_after == duration_before - 1),
       And(assigned_after == False, duration_after == 0)
    ),
    And(assigned_after == False, duration_after == 0)
)

s = Solver()
s.add(transition_assign)
s.add(Not(assigned_after == True)) 
print("assignCalculations:", s.check())

s = Solver()
s.add(transition_tick)
s.add(assigned_before == True, duration_before == 1) 
s.add(Not(assigned_after == False)) 
print("tick (duration = 1):", s.check()) 
print(s.model)

s = Solver()
s.add(transition_tick)
s.add(assigned_before == True, duration_before > 1)
s.add(Not(assigned_after == True))
print("tick (duration > 1):", s.check()) 

s = Solver()
s.add(transition_tick)
s.add(assigned_before == False)
s.add(Not(assigned_after == False))