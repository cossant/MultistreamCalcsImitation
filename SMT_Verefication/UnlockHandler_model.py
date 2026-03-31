from z3 import *

Addr = IntSort()
Owner = IntSort()

owner = Int('owner')
start = Int('start')
end = Int('end')

a = Int('a')

locks_before = Array('locks_before', Addr, Owner)

pre = ForAll([a], Implies(And(a >= start, a <= end), locks_before[a] == owner))

locks_after = Array('locks_after', Addr, Owner)
transition = ForAll([a], locks_after[a] == If(And(a >= start, a <= end), -1, locks_before[a]))

post = ForAll([a], Implies(And(a >= start, a <= end), locks_after[a] == -1))

s = Solver()
s.add(pre, transition, Not(post))

res = s.check()
print("Unlock verification result:", res)

if res == sat:
    print("Counterexample found!")
    print(s.model())
else:
    print("Property proved: unlock correctly releases locks.")