import statistics as stat

nums = []


def calc(filename):
    with open(filename,"r") as f:
        for line in f.readlines():
            n = line[-6:-2]
            nums.append(float(n))

    mean_val = round(stat.mean(nums),3)
    return mean_val



print("Symmetric")
print(calc("sym-good.txt"))
print(calc("sym-bad.txt"))

print("Sig")
print(calc("sig-good.txt"))
print(calc("sig-bad.txt"))
