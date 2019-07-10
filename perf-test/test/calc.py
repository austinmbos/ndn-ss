# sum the numbers from to_total.txt
import statistics

total=[]
count=0

with open("results/sym-enc-10000-1000.log","r") as f:
    for line in f.readlines():
        total.append(float(line))
        count += 1

mean_val = statistics.mean(total)

print("Mean:     "+str(mean_val))
print("Std Dev:  "+str(statistics.stdev(total)))
print("Variance: "+str(statistics.variance(total,mean_val)))


