def mrp_calculation(n, demand, inventory_0, sr):    
    proj_inventory = [0 for e in range(n)]   # projected available on hand inventory 
    net_req = [0 for e in range(n)]
    x = 0
    
    for t in range(0, n):
        if t == 0:
            proj_inventory[t] = inventory_0 - demand[t]
        else:
            proj_inventory[t] = proj_inventory[t-1] - demand[t]
        
        # adjusting scheduled receipts in case of no projected available on hand inventory
        while proj_inventory[t] < 0 and x < len(sr):
            proj_inventory[t] += sr[x]
            x += 1
            
        net_req[t] = min(max(0, -proj_inventory[t]), demand[t])
        
    return net_req

    
# take input

n = int(input("Enter number of time periods in planning horizon: "))

demand = input("Enter demand values separated by commas: ")
demand = [int(demand_ele) for demand_ele in demand.split(',')]

inventory_0 = int(input("Enter available on hand inventory: "))

sr = input("Enter scheduled receipts separated by commas: ")
sr = [int(sr_element) for sr_element in sr.split(',')]

net_req = mrp_calculation(n, demand, inventory_0, sr)
print("The net requirements for each time period of the planning horizon are:", net_req)


# n = 8
# demand = [15, 20, 30, 10, 30, 30, 30, 30]
# inventory_0 = 30
# sr = [20, 10, 5]