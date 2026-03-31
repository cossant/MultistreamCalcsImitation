from z3 import *

Addr = IntSort()
Owner = IntSort()

locks = Array('locks', Addr, Owner)

owner = Int('owner')
start = Int('start')
end = Int('end')  

a = Int('a')

pre = ForAll([a], Implies(And(a >= start, a <= end), locks[a] == -1))

new_locks = Array('new_locks', Addr, Owner)
transition = ForAll([a], new_locks[a] == If(And(a >= start, a <= end), owner, locks[a]))

post = ForAll([a], Implies(And(a >= start, a <= end), new_locks[a] == owner))

s = Solver()
s.add(pre, transition, Not(post))
res = s.check()
print("Lock verification result:", res)
if res == sat:
    print("Counterexample:", s.model())
else:
    print("Property proved: lock correctly sets locks.")