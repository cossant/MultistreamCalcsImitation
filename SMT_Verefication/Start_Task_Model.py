from z3 import *

Worker = DeclareSort('Worker')

isTPC = Function('isTPC', Worker, BoolSort())
isFree = Function('isFree', Worker, BoolSort())
hasTask = Function('hasTask', Worker, BoolSort())

w = Const('w', Worker)
x = Const('x', Worker)

pre = And(isTPC(w), isFree(w))

isFree_prime = Function('isFree_prime', Worker, BoolSort())
hasTask_prime = Function('hasTask_prime', Worker, BoolSort())

transition = And(
    hasTask_prime(w) == True,
    isFree_prime(w) == False,
    ForAll([x], 
        Implies(x != w, 
            And(isFree_prime(x) == isFree(x),
                hasTask_prime(x) == hasTask(x))
        )
    )
)

post = hasTask_prime(w)

s = Solver()
s.add(pre, transition, Not(post))

res = s.check()
print("Verification result:", res)
if res == sat:
    print("Counterexample found:", s.model())
else:
    print("Property proved: enact correctly assigns task.")