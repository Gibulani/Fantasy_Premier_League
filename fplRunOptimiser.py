# Helper variables
POS = slim_elements_df.element_type.unique()
CLUBS = slim_elements_df.team.unique()
BUDGET = 100
pos_available = {
    1: 5,
    2: 3,
    3: 5,
    4: 2,
}

# Initialize Variables
names = [slim_elements_df.full_name[i] for i in slim_elements_df.index]
teams = [slim_elements_df.team[i] for i in slim_elements_df.index]
positions = [slim_elements_df.element_type[i] for i in slim_elements_df.index]
prices = [slim_elements_df.cost[i] for i in slim_elements_df.index]
points = [slim_elements_df.total_points[i] for i in slim_elements_df.index]
xPoints = [slim_elements_df.xPoints[i] for i in slim_elements_df.index]
players = [LpVariable("player_" + str(i), cat="Binary") for i in slim_elements_df.index]

# Initialize the problem
lpModel = LpProblem("FPL_Optimal_Team", LpMaximize)

# Define the objective
lpModel += lpSum(players[i] * xPoints[i] for i in range(len(slim_elements_df))) # Objective

# Build the constraints
lpModel += lpSum(players[i] * slim_elements_df.cost[slim_elements_df.index[i]] for i in range(len(slim_elements_df))) <= BUDGET # Budget Limit

for pos in POS:
  lpModel += lpSum(players[i] for i in range(len(slim_elements_df)) if positions[i] == pos) <= pos_available[pos] # Position Limit

for club in CLUBS:
  lpModel += lpSum(players[i] for i in range(len(slim_elements_df)) if teams[i] == club) <= 3 # Club Limit

  # Solve the problem
lpModel.solve()

for v in lpModel.variables():
  if v.varValue != 0:
    name = slim_elements_df.full_name[int(v.name.split("_")[1])]
    club = slim_elements_df.team[int(v.name.split("_")[1])]
    position = slim_elements_df.element_type[int(v.name.split("_")[1])]
    total_points = slim_elements_df.total_points[int(v.name.split("_")[1])]
    xPoints = slim_elements_df.xPoints[int(v.name.split("_")[1])]
    cost = slim_elements_df.cost[int(v.name.split("_")[1])]
    print(name, position, club, total_points, xPoints, cost, sep=" | ")