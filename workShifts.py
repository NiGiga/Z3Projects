"""""
      ### Scheduling Problem for Optimize work shift tabel ###

Imagine having to manage a small shop and having to work shifts 
every week. you have 4 employees N, V, G, D. 
The store has a 12-hour shift from 8:00 am and 8:00 pm over 7 days. 

N and V have a contract of 24 hours per week, while G,D of 40.
N,V can work 4 hours a day for 6 days 
or 5 hours a day for 4 days plus a day of 4.

G,D can work 6 hours a day for 4 days and 8 hours a day 
with 1 hour off for the remaining 2.

All 4 cannot work more than 8 consecutive days and each 
of them must have one free every 3 Sundays worked.

N is a working student so he prefers to work in the evening and more on weekends

V prefers to work in the morning to spend the afternoon with his children

D is a Napoli fan and therefore wants to see all his games 
(Otherwise he watches them while he works)

We want to create hours that comply with the laws imposed by the CCNL of Commerce 
but that are the best possible for employees

In this example, we will have a month of work with the following requests:

### 1 12-hour shift from 8:00 am and 8:00 pm over 7 days always covered

### 2 N,V can work 4h day for 6 days or 5h day for 5 days + 4h for 1 day 

### 3 G,D can work 6h day for 4 days + 8h day with 1 hour off for 2 days.

### 4 N,V,G,D max 8 consecutive days 

### 5 N,V,G,D each have 1 Saturday/Sunday free on 4

### 6 N must work after 4:00 pm at least for 3 days from monday to friday

### 7 V must end the shift before 2:00 pm at least for 3 days

### 8 Let's supose that Napoli plays on Wednesday 8:45 pm and 
      on Sunday 8:45 pm the first and third week an for 
      the second and fourth week only on Saturdays at 6 pm
      so D must finish at least 2h before in  order to be 
      adequately prepared for the event
      

"""""

from z3 import *

# Constants
days = 28  # 4 weeks of 7 days
shifts = 12  # 12-hour shifts
employees = ["N", "V", "G", "D"]
hours_per_week = {"N": 24, "V": 24, "G": 40, "D": 40}

# Solver
solver = Solver()

# Variables
schedule = {e: [Int(f"{e}_{d}") for d in range(days)] for e in employees}

# Constraints
for e in employees:
    for d in range(days):
        # Each shift is between 0 and 12 hours
        solver.add(schedule[e][d] >= 0, schedule[e][d] <= shifts)

# 1. Weekly hours for each employee
for e, weekly_hours in hours_per_week.items():
    for week in range(4):  # 4 weeks
        solver.add(Sum(schedule[e][week * 7: (week + 1) * 7]) == weekly_hours)

# 2. Daily work limits for N and V (24 hours per week, shifts of max 4 hours/day)
for e in ["N", "V"]:
    for week in range(4):
        week_schedule = schedule[e][week * 7: (week + 1) * 7]
        solver.add(
            Or(
                And([Sum(week_schedule) == 24] + [w <= 4 for w in week_schedule]),
                And(Sum(week_schedule[:6]) == 24, week_schedule[6] == 4)
            )
        )

# For G and D (work 40 hours a week with specific shift constraints)
for e in ["G", "D"]:
    for week in range(4):
        week_schedule = schedule[e][week * 7: (week + 1) * 7]
        solver.add(
            And(
                Sum(week_schedule) == 40,  # Total sum for the week
                Sum([If(w == 6, 1, 0) for w in week_schedule]) == 4,  # 4 days of 6-hour shifts
                Sum([If(w == 8, 1, 0) for w in week_schedule]) == 2   # 2 days of 8-hour shifts
            )
        )

# 3. Max 8 consecutive days of work
for e in employees:
    for start in range(days - 8):
        solver.add(Sum(schedule[e][start:start + 8]) <= 8 * shifts)  # Ensure no more than 8 consecutive days of work

# 4. Constraint for Saturday/Sunday off over 4 weeks but not at the same time
for week in range(4):
    # Check that each employee has either Saturday or Sunday off, but not both in the same week
    for e in employees:
        solver.add(
            Or(
                schedule[e][week * 7 + 5] == 0,  # Saturday off
                schedule[e][week * 7 + 6] == 0   # Sunday off
            )
        )

# 5. Specific constraints for N and V
for week in range(4):
    # N: Work after 4 pm for 3 days (Monday-Friday)
    solver.add(Sum([If(schedule["N"][week * 7 + d] >= 4, 1, 0) for d in range(5)]) >= 3)
    # V: End shift before 2 pm at least 4 days
    solver.add(Sum([If(schedule["V"][week * 7 + d] <= 6, 1, 0) for d in range(7)]) >= 3)

# 6. D's Napoli game constraints
napoli_games = {
    "week_1": [2, 6],
    "week_2": [5],
    "week_3": [2, 6],
    "week_4": [5]
}
game_times = [20, 20, 18, 18]  # In hours

for week, (game_days, game_time) in enumerate(zip(napoli_games.values(), game_times)):
    for day in game_days:
        solver.add(schedule["D"][week * 7 + day] <= game_time - 2)

# 7. Constraint that the 12 hours of opening must always be covered
for d in range(days):
    solver.add(Sum([schedule[e][d] for e in employees]) >= 12)  # 12 ore di apertura coperte ogni giorno

# Solve
if solver.check() == sat:
    model = solver.model()
    for e in employees:
        print(f"Schedule for {e}:")
        print([model[schedule[e][d]] for d in range(days)])
else:
    print("No solution found.")














































