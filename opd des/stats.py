import pandas as pd
from scipy import stats

df = pd.read_excel('Assg_6_data.xlsx')
cols = list(df.columns)
data = [list() for i in range(3)]
for i in range(3):
    data[i] = df[cols[i]].tolist()

best_dist = list()

for i in range(3):
    arg_norm = stats.norm.fit(data[i])
    res_norm = stats.kstest(data[i], stats.norm.cdf, args = arg_norm)
    arg_expon = stats.expon.fit(data[i])
    res_expon = stats.kstest(data[i], stats.expon.cdf, args = arg_expon)

    if res_norm[1] > res_expon[1]:
        best_dist.append("Gaussian")
    else:
        best_dist.append("Exponential")
        
    print(f"Best fit distribution (out of Gaussian and exponential) for {cols[i]}: {best_dist[i]}")
    
    if res_norm[1] > res_expon[1]:
        print("Mean and standard deviation of the distribution are: ", arg_norm[0], arg_norm[1])
    else:
        print("Mean of the distribution is:", arg_expon[1])
    print("\n")
