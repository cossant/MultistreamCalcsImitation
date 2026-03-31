from z3 import *

Worker = DeclareSort('Worker')
id_of = Function('id_of', Worker, IntSort())

w1, w2 = Consts('w1 w2', Worker)

s = Solver()

s.add(ForAll([w1, w2], Implies(w1 != w2, id_of(w1) != id_of(w2))))
s.add(Exists([w1, w2], And(w1 != w2, id_of(w1) == id_of(w2))))
# s = Solver()

# s.add(w1 != w2)
# s.add(id_of(w1) != id_of(w2)) 

res = s.check()

print("Result:", res)

if res == sat:
    print("Counterexample:")
    print(s.model())
else:
    print("Property holds")