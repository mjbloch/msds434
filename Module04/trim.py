f=open("201502.bck").readlines()

fout=open("201502.csv", "w")

for i in range(101):
    fout.write(f[i])

fout.close()