import pandas as pd

def mrp_calculation(n, demand, inventory_0, sr):    
    proj_inventory = [0 for e in range(n)]   # projected available on hand inventory 
    net_req = [0 for e in range(n)]
    x = 0
    
    for t in range(0, n):
        if t == 0:
            proj_inventory[t] = inventory_0 - demand[t]
        else:
            proj_inventory[t] = proj_inventory[t-1] - demand[t]
        
        # accomodating scheduled receipts in case of no projected available on hand inventory
        while proj_inventory[t] < 0 and x < len(sr):
            proj_inventory[t] += sr[x]
            x += 1
            
        net_req[t] = min(max(0, -proj_inventory[t]), demand[t])
        
    return net_req

def wagner_whitin_alg(N, demand, setup_cost, carrying_cost):
    j_star = list()
    z_star = list()
    table = [[0 for i in range(N)] for j in range(N)]
    
    counter = 0
    for counter in range(N):
        j_star.append(0)
        z_star.append(0)            
        if demand[counter]!=0:
            break
           
    z1_star = setup_cost
    z_star[counter] = z1_star
    final_cost = z1_star
    table[counter][counter] = z1_star
    j_star[counter] = counter
    
    for t in range(counter+1, N):
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
            if table[i][j] == 0 and not(i>=j and i<=counter-1 and j<=counter-1):
                table[i][j] = ""

    df = pd.DataFrame(table, columns = [(i+1) for i in range(N)], index = row_labels)
    print("Planning horizon:\n", df)
    df1 = pd.DataFrame(prod_schedule, columns = ['number of units'], index = [(i+1) for i in range(N)])
    print("\nProduction Schedule (row number represents t):\n", df1)
    print("\nOptimal cost (INR): ", z_star[-1])

    
# input
n = 8
demand = [15, 20, 30, 10, 30, 30, 30, 30]
inventory_0 = 30
sr = [20, 10, 5]

net_req = mrp_calculation(n, demand, inventory_0, sr)
print("The net requirements for each time period of the planning horizon are:", net_req, "\n")

setup_cost = 100
carrying_cost = 1
wagner_whitin_alg(n, net_req, setup_cost, carrying_cost)