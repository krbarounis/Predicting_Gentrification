import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE

# Pipline for implementing K-means clustering.
def scale_df(df):
    """
    scale_df(df):
    This function uses sklearn's min-max scaler to return a scaled dataframe.

    Params:
        df: unscaled dataframe
    Returns:
        A scaled dataframe.
    """
     # scale the data
    scaler=MinMaxScaler()
    # fit the data
    scaled_data = scaler.fit_transform(df.values)
    # put scaled data into a df
    df_scaled = pd.DataFrame(scaled_data,index=df.index,columns=df.columns)
    return df_scaled

def check_k_means(df_scaled):
    """
    check_k_means(df_scaled):
    This function
    
    Params:
    Returns:
    
    """
    # check elbow
    # Calculate the Within-Cluster-Sum of Squared Errors (WSS) for different values of k, 
    # and choose the k for which WSS first starts to diminish. In the plot of WSS-versus-k, 
    # this is visible as an elbow.
    # Specifying the dataset and initializing variables

    X = df_scaled
    distorsions = []

    # Calculate SSE for different K

    for k in range(2, 10):
        kmeans = KMeans(n_clusters=k, random_state = 301)
        kmeans.fit(X)
        distorsions.append(kmeans.inertia_)

    # Plot values of SSE
    plt.figure(figsize=(15,8))
    plt.subplot(121, title='Elbow curve')
    plt.xlabel('k')
    plt.ylabel('WSS')
    plt.plot(range(2, 10), distorsions)
    plt.grid(True)

    # check sillhouette

    silhouette_plot = []
    for k in range(2, 10):
        clusters = KMeans(n_clusters=k, random_state=10)
        cluster_labels = clusters.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette_plot.append(silhouette_avg)
    # Plot Silhouette coefficient
    plt.figure(figsize=(15,8))
    plt.subplot(121, title='Silhouette coefficients over k')
    plt.xlabel('k')
    plt.ylabel('silhouette coefficient')
    plt.plot(range(2, 10), silhouette_plot)
    plt.axhline(y=np.mean(silhouette_plot), color="red", linestyle="--")
    plt.grid(True)
    
def fit_k_means(n_clusters,scaled_df):
    """
    fit_k_means(n_clusters,scaled_df):
    Params:
        n_clusters:
        scaled_df:
    Returns:
    
    """
    model = KMeans(n_clusters=n_clusters).fit(scaled_df)
    return model

def create_cluster_df(model,scaled_df):
    cluster_map = pd.DataFrame()
    cluster_map['tractid']=scaled_df.index.values
    cluster_map['cluster']=model.labels_
    return cluster_map

def plot_clusters_tsne(df_scaled,df_cluster):
    
    tsne_results=TSNE(n_components=2,verbose=1,perplexity=40, n_iter=300).fit_transform(df_scaled.values)
    
    df_subset=pd.DataFrame()
    df_subset['tsne-2d-one']=tsne_results[:,0]
    df_subset['tsne-2d-two']=tsne_results[:,1]
    df_toplot = df_subset.merge(df_cluster,how='outer',left_index=True,right_index=True)
    
    plt.figure(figsize=(15,8))
    plt.scatter(x='tsne-2d-one',y='tsne-2d-two',hue='cluster',data=df_toplot)
    