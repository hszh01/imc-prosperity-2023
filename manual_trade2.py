import numpy as np
import matplotlib.pyplot as plt 

perc50_sum = 0
perc25_sum = 0
perc45_sum = 0
perc55_sum = 0
simulations = 10000
for i in range (1, simulations):
    randomNums = np.random.seed(i)
    randomInts = np.random.normal(size = 10000, loc = 10625)

    perc50 = np.percentile(randomInts, 50)
    perc25 = np.percentile(randomInts, 25)
    perc50_sum += perc50
    perc25_sum += perc25

    perc45 = np.percentile(randomInts, 45)
    perc55 = np.percentile(randomInts, 55)
    perc45_sum += perc45
    perc55_sum += perc55

    # # Plot:
    # axis = np.arange(start=min(randomInts), stop = max(randomInts) + 1)
    # plt.hist(randomInts, bins = axis)
    # plt.show()
    
print("avg 50th perc:", (perc50_sum / simulations))
print("avg 25th perc:", (perc25_sum / simulations))
print("avg 45th perc:", (perc45_sum / simulations))
print("avg 55th perc:", (perc55_sum / simulations))



