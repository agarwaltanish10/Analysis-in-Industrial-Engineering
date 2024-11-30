class bomItem:
    def __init__(self, n, demand, inventory_0, sr, children, itemNum):  # object initialization
        self.n = n
        self.demand = demand
        self.inventory_0 = inventory_0
        self.sr = sr
        self.children = children
        self.itemNum = itemNum
        
    def mrpCalculation(self):  
        proj_inventory = [0 for e in range(self.n)]   # projected available on hand inventory 
        net_req = [0 for e in range(self.n)]
        x = 0

        for t in range(0, self.n):
            if t == 0:
                proj_inventory[t] = self.inventory_0 - self.demand[t]
            else:
                proj_inventory[t] = proj_inventory[t-1] - self.demand[t]
                
            # accomodating scheduled receipts in case of no projected available on hand inventory
            while proj_inventory[t] < 0 and x < len(self.sr):
                proj_inventory[t] += self.sr[x]
                x += 1

            net_req[t] = min(max(0, -proj_inventory[t]), self.demand[t])

        return net_req

    def childNodesMRP(self, net_req):  # calculating MRP and demands of children nodes
        for c in self.children:
            # c is a pair (object, frequency required)
            child = c[0]
            frequency = c[1]
            
            childNodeDemand = [(frequency * net_req[e]) for e in range(len(net_req))]
            for i in range(planning_horizon):
                child.demand[i] += childNodeDemand[i]

            temp_req = child.mrpCalculation()
            child.childNodesMRP(temp_req)
            
        return    

# inputs
planning_horizon = 8
num_items = 3
items = [None for e in range(num_items)]

# instantiating class objects

# we create an array of 0's for the demands of B and C, to be updated later
# itemNum to be updated starting from 0 (root node)
A = items[0] = bomItem(n = planning_horizon, demand = [15, 20, 30, 10, 30, 30, 30, 30], inventory_0 = 30, sr = [20, 10], children = [], itemNum = 0)
B = items[1] = bomItem(n = planning_horizon, demand = [0 for e in range(planning_horizon)], inventory_0 = 60, sr = [10], children = [], itemNum = 1)
C = items[2] = bomItem(n = planning_horizon, demand = [0 for e in range(planning_horizon)], inventory_0 = 60, sr = [20, 10], children = [], itemNum = 2)

# defining children relationships of items
A.children = [(B,1), (C,2)]
B.children = [(C,1)]

# creating 2D array to store the net requirements for each item
net_requirements = [[] for e in range(num_items)]
net_requirements[0] = A.mrpCalculation()

# calculate net requirements of child nodes of A (root)
A.childNodesMRP(net_requirements[0])

for i in range(1, num_items):
    net_requirements[i] = items[i].mrpCalculation()

for i in range(num_items):
    print(f"Net requirements for {chr(i+65)}: {net_requirements[i]}")
