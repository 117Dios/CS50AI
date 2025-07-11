# ruff: noqa: F403, F405

from logic import *  

rain = Symbol("rain")
hagrid = Symbol("hagrid")
dumbledore = Symbol("dumbledore")

knowledge = And(
    Implication(Not(rain),hagrid), 
    Or(hagrid,dumbledore),
    Not(And(hagrid,dumbledore)),
    dumbledore
)

model_check(knowledge,rain)

print(knowledge.formula())

print(model_check(knowledge,rain))