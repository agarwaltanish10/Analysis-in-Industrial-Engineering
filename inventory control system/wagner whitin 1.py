import pandas as pd

def wagner_whitin_alg():    
    z1_star = setup_cost
    z_star = [z1_star]
    final_cost = z1_star
    j_star = [0]
    
    table = [[0 for i in range(N)] for j in range(N)]
    table[0][0] = z1_star
    
    for t in range(1, N):
        new_term = z_star[t-1] + setup_cost
        table[t][t] = new_term
        final_cost = table[t][t]
        pos = t
        
        for x in range(j_star[t - 1], t):
            table[x][t] = table[x][t-1] + (t - x) * carrying_cost * demand[t]
            if final_cost > table[x][t]:
                final_cost = table[x][t]
                pos = x
        
        z_star.append(final_cost)
        j_star.append(pos)
    
    
    # production schedule
    
    prod_schedule = [0 for i in range(N)]
    ub = N-1
    while ub >= 0:
        total_demand = 0
        for l in range(ub,j_star[ub]-1,-1):
            total_demand += demand[l]
        prod_schedule[j_star[ub]] = total_demand
        ub = l-1
    
    # display output
    
    table.append(z_star)
    for i in range(len(j_star)):
        j_star[i] += 1
    table.append(j_star)

    row_labels = [(i+1) for i in range(N)]
    row_labels.append('z*')
    row_labels.append('j*')
    
    for i in range(N):
        for j in range(N):
            if table[i][j] == 0:
                table[i][j] = ""
    
    df = pd.DataFrame(table, columns = [(i+1) for i in range(N)], index = row_labels)
    display(df)
    
    df1 = pd.DataFrame(prod_schedule, columns = ['number of units'], index = [(i+1) for i in range(N)])
    print("Production Schedule (row number represents t):")
    display(df1)
    print("Optimal cost: ", z_star[-1])
    
    
    
N = int(input("Time horizon (number of weeks/months):"))
setup_cost = float(input("Enter constant setup cost:"))
carrying_cost = float(input("Enter constant carrying cost:"))
print("Enter demand values:")
for i in range(N):
    demand.append(int(input()))

# demand = [20,50,10,50,50,10,20,40,20,30]
# setup_cost = 100
# carrying_cost = 1
# N=10
    
wagner_whitin_alg()