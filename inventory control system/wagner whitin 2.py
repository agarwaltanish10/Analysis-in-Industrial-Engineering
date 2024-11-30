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
    
    
    
demand = [100, 90, 115, 120, 95, 100, 90, 105, 105, 100, 110, 105]
N = 12

setup_time = 75
tool_wear = 0.005
tool_cost = 2500

oil_amt = 0.4
oil_cost = 100

salary = 50
warehouse_size = 500
warehouse_rent = 2
elec_charge = 100
maint_charge = 100
num_units = 500

setup_cost = oil_amt*oil_cost + salary*(setup_time/60) + tool_cost*(setup_time/60)*(tool_wear/1)
carrying_cost = (warehouse_rent*warehouse_size + elec_charge + maint_charge)/num_units          # divide by 500 since carrying cost is per unit

wagner_whitin_alg()