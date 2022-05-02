
from ast import expr_context
import pandas as pd
import numpy as np
from pyrsistent import optional 
import seaborn as sns 
import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from sklearn import metrics 
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans,MeanShift,estimate_bandwidth
from sklearn.metrics import silhouette_score

class clustering():
    def __init__(self,csv:str,label:str):
        """Detta är min konstruktor och den tar emot csv filen och skapar label.
        Har ditt dataset ingen label sätt istället din inedex column som label 
        Skalar också om datan med en standard scaler
        
        ARGS: 
        csv : csv fil
        label : den kolumn du vill kalla label i denna klassen är detta DEATH_EVENT
        """
        try:
            self.data = pd.read_csv(csv)
            self.label = self.data[label]
            self.data.drop(label,axis=1,inplace=True)
            
        except:
            self.data = pd.read_csv(csv,index_col=label)
            

        self.process_data = StandardScaler().fit_transform(self.data)
    
    def pca(self,n_components : int):
        """Denna funktion gör en dimensionreducering i form av PCA.
        Du får även en snygg plot och en liten text som förklarar variansen av data i dina valda komponents.
        Sist men inte minst gör den en transform på ditt dataset så du lämnar denna funktion med en dataframe som endast innehåller
        dina 1st och 2nd PC och om du har en label inkluderas denna också 
        
        ARGS: 
        n_components : Antal komponents du vill använda till din pca"""

        try:
            pca = PCA(n_components=n_components)
            xt = pca.fit_transform(self.process_data)

            sns.scatterplot(x=xt[: ,0], y= xt[: ,1],hue=self.label)
            plt.xlabel('1st Principal component')
            plt.ylabel('2nd Principal component')
            plt.legend()
            plt.show()
        except:
            pca = PCA(n_components=n_components)
            xt = pca.fit_transform(self.process_data)

            sns.scatterplot(x=xt[: ,0], y= xt[: ,1])
            plt.xlabel('1st Principal component')
            plt.ylabel('2nd Principal component')
            plt.legend()
            plt.show()
        
        percentage_var_expl = pca.explained_variance_ / np.sum(pca.explained_variance_)
        cum_var_expl = np.cumsum(percentage_var_expl)
        
        plt.figure(figsize=(6,6))
        plt.plot(cum_var_expl)
        plt.xlabel('Features/components')
        plt.ylabel('cumulative_explined_variance')
        plt.title('PCA plot')
        plt.show()
        try: 
            df_base =columns={'PC0': xt[:,0] , 'PC1':xt[:,1],'Target':self.label}
            pca_df = pd.DataFrame(data=df_base)
            self.process_data = pca_df
        except:
            df_base =columns={'PC0': xt[:,0] , 'PC1':xt[:,1]}
            pca_df = pd.DataFrame(data=df_base)
            self.process_data = pca_df
        return  print(f'Variance of data in princpial components {cum_var_expl}! Dataframe updated with 1st and 2nd principal components and label/target')



    def tsne(self,n_components:int, perplexity:int,learning_rate:int):
        """TSNE här omvandlas återigen ditt dataframe för att sära på punkterna och hitta kluster.
        Du får också en fin plot som visar dina nya kluster.
        
        ARGS :
        n_components : Väljer hur många dimensioner som ska användas för denna funktion är min 2 och max 3
        perplexity : Denna parameter väljer hur många neighbors varje punkt ska ha i dina kluster
        Learning_rate : Denna parameter särar på eller drar ihop dina cluster för att forma bättre kluster
        """
        try:
            tsne = TSNE(n_components =n_components, perplexity =perplexity,learning_rate=learning_rate,random_state=213)
            self.process_data = tsne.fit_transform(self.process_data)
            sns.scatterplot(x = self.process_data[:,0], y = self.process_data[:,1],hue = self.label, legend = 'full')
            plt.xlabel('1st TSNE component')
            plt.ylabel('2nd TSNE component')
            plt.title('T-SNE plot')
            plt.show()
        
        except:
            tsne = TSNE(n_components =n_components, perplexity =perplexity,learning_rate=learning_rate,random_state=213)
            self.process_data = tsne.fit_transform(self.process_data)
            sns.scatterplot(x = self.process_data[:,0], y = self.process_data[:,1])
            plt.xlabel('1st TSNE component')
            plt.ylabel('2nd TSNE component')
            plt.title('T-SNE plot')
            plt.show()
        


    
    def kmeans(self,n_clusters:int):
        """Denna klass gör en KMean alghoritm på din data, plottar den och använder sedan elbow metoden för att avgöra om du kunde valt bättre antal kluster.
        Funktionen börjar med att initiera Kmean, sedan predikterar den på din data för att ta fram sina egna kluster och labels.
        Sedan kommer ploten med färger som matchar dina predikterade labels.
        Funktionen avslutar sedan med en for loop som kör mellan 2-10 för att ta fram ditt optimala antal kluster och plottar detta.

        ARGS :
        n_clusters : Välj antal kluster du vill att din KMean ska använda
        """
        km = KMeans(n_clusters=n_clusters)

        pred_lab = km.fit_predict(self.process_data)

        
        sns.scatterplot(x = self.process_data[:,0], y = self.process_data[:,1], hue = pred_lab, legend = 'full')
        plt.title('Kmeans Plot')
        plt.show()

        elbow = []
        silhouette = []
        min_clusters = 2
        max_cluster = 10

        for k in range(min_clusters,max_cluster):
            kmeans = KMeans(n_clusters=k).fit(self.process_data)
            elbow.append(kmeans.inertia_) 
            silhouette.append(silhouette_score(self.process_data,kmeans.labels_)) 


        plt.plot(np.arange(min_clusters,max_cluster),elbow)
        plt.xlabel('Amount of Clusters')
        plt.ylabel('Elbow')
        plt.title('The elbow method')
        plt.show()


    def meanshift(self,n_samples:int,quantile:float,seeding:bool):
        """MeanShift börjar med att skapa bandwidth vilket är en väldigt unik hyperparameter med tanke på att den 
        kan ta in flera variabel i form av en tidigare sparad variabel med hjälp av library estimate bandwidth
        Efter detta är det ganska straight forward den väljer själv hur många kluster som ska användas och plottar ut sin slutsats 
        Efter detta används error metric fowlkes_mallows_score vilket ger en väldigt orättvis bild i detta dataset då jag har för lite punkter för att dela upp min data
        
        ARGS: 
        n_samples : antal samples som ska användas 
        quantile : median av distans mellan varje granne
        seeding : ökar prestandan på din meanshift och tiden den tar att köra"""
        bandwidth = estimate_bandwidth(self.process_data,quantile=quantile,n_samples=n_samples)

        ms = MeanShift(bandwidth=bandwidth,bin_seeding=seeding)
        ms.fit(self.process_data)

        labels = ms.labels_
        labels_unique = np.unique(labels)
        n_clusters_=len(labels_unique)

        print("number of estimated clusters : %d" % n_clusters_)

        y_pred = ms.predict(self.process_data)

        plt.scatter(self.process_data[:, 0], self.process_data[:, 1], c=y_pred, cmap="viridis")
        plt.xlabel("Feature 1")
        plt.ylabel("Feature 2")
        plt.show()
        fms = metrics.fowlkes_mallows_score(labels_pred=y_pred,labels_true=labels)
        print(f'Fowlkes mallows score, perfect = 1 worst = 0, mine is {fms} ' )
    
