"""""
                ### Task planning Problem ###

Suppose you have three tasks A, B, and C with durations of 1, 2, 
and 3 time units respectively, and they must be completed in a 
total time window of 6 units. 
There must be no overlap between activities.


                        ### Formula ###

### 1 Every task has a beginning and an end.

### 2 Tasks must not overlap.

### 3 All tasks must be completed within 6 time units.

"""""

from z3 import *

# We define the beginning and end of each activity
start_A, end_A = Int("start_A"), Int("end_A")
start_B, end_B = Int("start_B"), Int("end_B")
start_C, end_C = Int("start_C"), Int("end_C")

# Durations
duration_A, duration_B, duration_C = 1, 2, 3

# Constraints (1): Tasks must end after they have started
durations = [
    end_A == start_A + duration_A,
    end_B == start_B + duration_B,
    end_C == start_C + duration_C,
]

# Constraints (2): Activities must not overlap
not_overlap = [
    Or(end_A <= start_B, end_B <= start_A),
    Or(end_A <= start_C, end_C <= start_A),
    Or(end_B <= start_C, end_C <= start_B),
]

# Time window constraint (3)
time_window = [
    And(start_A >= 0, end_A <= 6),
    And(start_B >= 0, end_B <= 6),
    And(start_C >= 0, end_C <= 6),
]

# Let's create the solver and add the constraints
s = Solver()
s.add(durations + not_overlap + time_window)

# Let's check the satisfiability
if s.check() == sat:
    m = s.model()
    result = {
        "A": (m.evaluate(start_A), m.evaluate(end_A)),
        "B": (m.evaluate(start_B), m.evaluate(end_B)),
        "C": (m.evaluate(start_C), m.evaluate(end_C)),
    }
    print("Planning of activities:", result) #Planning of activities: {'A': (0, 1), 'B': (1, 3), 'C': (3, 6)}
else:
    print("No solution found!")