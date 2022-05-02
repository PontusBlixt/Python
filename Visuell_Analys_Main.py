import numpy as np
from inlämning_pontus_blixt_vg import clustering
from class2 import clusteringMeanShift

def main1():
    go1 = clusteringMeanShift('buddymove.csv','User Id')
    go1.plot()
    go1.pca(4)
    go1.tsne(2,15,200)
    go1.meanshift(n_samples=249,quantile=0.2,seeding=True)
def main():
    go = clustering('heart_failure.csv','DEATH_EVENT')
    go.pca(4)
    go.tsne(2,20,520)
    #go.meanshift(n_samples=249,quantile=0.5,seeding=True)
    go.kmeans(2)

if __name__ == '__main__':
    main()
