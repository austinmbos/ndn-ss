# sum the numbers from to_total.txt
import statistics
import sys


def tally(filename,mach,data_size,num_of_data,is_docker):

    total = []
    docker_total = []
    count=0
    docker_count=0
    """
    if is_docker == True:
        file = "_data/"+filename+"-"+data_size+"-"+num_of_data+"."+mach+".docker.log"
    else:
        file = "_data/"+filename+"-"+data_size+"-"+num_of_data+"."+mach+".log"
    """

    docker_file = file = "_data/"+filename+"-"+data_size+"-"+num_of_data+"."+mach+".docker.log"

    file = "_data/"+filename+"-"+data_size+"-"+num_of_data+"."+mach+".log"

    

    with open(file,"r") as f:
        for line in f.readlines():
            total.append(float(line))
            count += 1

    with open(docker_file,"r") as f:
        for line in f.readlines():
            docker_total.append(float(line))
            docker_count += 1


    mean_val = statistics.mean(total)
    mean_val = mean_val / 10**3
    coeff = 1 / (mean_val / 10**6) 
    thru_put = float(data_size) * coeff
    thru_put = thru_put / 10**6

    # docker results
    d_mean_val = statistics.mean(docker_total)
    d_mean_val = d_mean_val / 10**3
    d_coeff = 1 / (d_mean_val / 10**6) 
    d_thru_put = float(data_size) * d_coeff
    d_thru_put = d_thru_put / 10**6

    print("test("+mach+"): " + filename)
    print("mean(normal): %.2f" % mean_val + " microseconds")
    print("mean(docker): %.2f" % d_mean_val + " microseconds")
    print("throughput(normal): %.2f" % thru_put + " MB/s")
    print("throughput(docker): %.2f" % d_thru_put + " MB/s")
    print("")


    """
    if is_docker:
        print("test: " + filename + "  RUN IN DOCKER ")
    else:
        print("test:        " + filename)
    #print("data size:   " + data_size)
    #print("num of data: " + str(num_of_data))
    print("Mean:        %.2f" % mean_val)
    print("through put: %.2f" % thru_put)
    #print("Std Dev:     %.2f" % statistics.stdev(total))
    #print("Variance: "+str(statistics.variance(total,mean_val)))
    print("")
    """




if __name__ == "__main__":

    print("== timing in is microseconds ==")
    print("== all tests run 1000 times  ==")
    print("== data size ignored, but    ==")
    print("== was used to calc thruput  ==")

    tally("sign","laptop","1000","1000",is_docker=False)
    #tally("sign","laptop","1000","1000",is_docker=True)
    #tally("sign","laptop","75000","1000",is_docker=False)
    #tally("sign","laptop","75000","1000",is_docker=True)
    #tally("sign","laptop","2000000","1000",is_docker=False)
    #tally("sign","laptop","2000000","1000",is_docker=True)

    tally("sig-ver","laptop","1000","1000",is_docker=False)
    #tally("sig-ver","laptop","1000","1000",is_docker=True)
    #tally("sig-ver","laptop","75000","1000",is_docker=False)
    #tally("sig-ver","laptop","75000","1000",is_docker=True)
    #tally("sig-ver","laptop","2000000","1000",is_docker=False)
    #tally("sig-ver","laptop","2000000","1000",is_docker=True)

    tally("rsa-enc","laptop","100","1000",is_docker=False)
    #tally("rsa-enc","laptop","100","1000",is_docker=True)
    #tally("rsa-enc","laptop","10","1000",is_docker=False)
    #tally("rsa-enc","laptop","10","1000",is_docker=True)

    tally("rsa-dec","laptop","100","1000",is_docker=False)
    #tally("rsa-dec","laptop","100","1000",is_docker=True)
    #tally("rsa-dec","laptop","10","1000",is_docker=False)
    #tally("rsa-dec","laptop","10","1000",is_docker=True)

    tally("sym-enc","laptop","1000","1000",is_docker=False)
    #tally("sym-enc","laptop","1000","1000",is_docker=True)
    #tally("sym-enc","laptop","75000","1000",is_docker=False)
    #tally("sym-enc","laptop","75000","1000",is_docker=True)
    #tally("sym-enc","laptop","2000000","1000",is_docker=False)
    #tally("sym-enc","laptop","2000000","1000",is_docker=True)

    tally("sym-dec","laptop","1000","1000",is_docker=False)
    #tally("sym-dec","laptop","1000","1000",is_docker=True)






