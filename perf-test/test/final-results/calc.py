# sum the numbers from to_total.txt
import statistics
import sys


def tally(filename,mach,data_size,num_of_data,is_docker):

    total=[]
    count=0

    if is_docker == True:
        file = "_data/"+filename+"-"+data_size+"-"+num_of_data+"."+mach+".docker.log"
    else:
        file = "_data/"+filename+"-"+data_size+"-"+num_of_data+"."+mach+".log"

    with open(file,"r") as f:
        for line in f.readlines():
            total.append(float(line))
            count += 1

    mean_val = statistics.mean(total)


    print("test:        " + filename)
    print("data size:   " + data_size)
    print("num of data: " + num_of_data)
    print("Mean:     "+str(mean_val))
    print("Std Dev:  "+str(statistics.stdev(total)))
    #print("Variance: "+str(statistics.variance(total,mean_val)))
    print("")




if __name__ == "__main__":

    tally("sign","top","1000","1000",is_docker=False)
    tally("sign","laptop","1000","1000",is_docker=True)
    tally("sign","top","75000","1000",is_docker=False)
    tally("sign","laptop","75000","1000",is_docker=True)
    tally("sign","top","2000000","1000",is_docker=False)
    tally("sign","laptop","2000000","1000",is_docker=True)
