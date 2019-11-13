import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import silhouette_score
from sklearn.manifold import TSNE

# These 4 functions serve as a pipline for implementing K-means clustering.

def scale_df(df):
    """
    scale_df(df):
    This function uses sklearn's min-max scaler to return a scaled dataframe where each feature is individually scaled to have a
    range of values between 0 and 1.
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
    This function returns 2 plots which assist in determing the optimal number of clusters to use in k-means clustering 
    for a specific dataset:
        1. Elbow Plot
        2. Silhouette Curve
    Params:
        df_scaled: dataframe of scaled data
    Returns:
    The first plot returned is the Elbow Plot, which shows the WSS (within-cluster sum of square errors) for different values of
    k. The idea is to select the k for which the WSS first starts to diminish. In the plot of WSS-versus-k, this is visible as an
    elbow.," i.e. the pointwhere increasing the number of clusters no longer materially decreases the WSS.
    
    The second plot returned is the Silhouette Curve, which shows the average silhouette score (a measure of how close each point 
    in one cluster is to points in the neighboring clusters) for different values of k. The idea is to select the k for there is 
    a global maxima in the curve. 
    """
    # Specify the dataset and initialize variables
    X = df_scaled
    distorsions = []

    # Calculate SSE for different K
    for k in range(2, 10):
        kmeans = KMeans(n_clusters=k, random_state = 301)
        kmeans.fit(X)
        distorsions.append(kmeans.inertia_)

    # Plot values of SSE
    plt.figure(figsize=(15,8),dpi=100)
    plt.subplot(121, title='Elbow curve')
    plt.xlabel('k')
    plt.ylabel('WSS')
    plt.plot(range(2, 10), distorsions)
    plt.grid(True)

    # check silhouette
    silhouette_plot = []
    # Calculate silhouette coefficient for different K
    for k in range(2, 10):
        clusters = KMeans(n_clusters=k, random_state=10)
        cluster_labels = clusters.fit_predict(X)
        silhouette_avg = silhouette_score(X, cluster_labels)
        silhouette_plot.append(silhouette_avg)
    # Plot Silhouette coefficient
    plt.figure(figsize=(15,8), dpi=100)
    plt.subplot(121, title='Silhouette coefficients over k')
    plt.xlabel('k')
    plt.ylabel('silhouette coefficient')
    plt.plot(range(2, 10), silhouette_plot)
    plt.axhline(y=np.mean(silhouette_plot), color="red", linestyle="--")
    plt.grid(True)
    
def fit_k_means(n_clusters,scaled_df):
    """
    fit_k_means(n_clusters,scaled_df):
    This function fits data to Sklearn's k-means algorithm and returns the model.
    Params:
        n_clusters: number of clusters to divide the data into
        scaled_df: the scaled data that is to be fit to the algorithm
    Returns:
        A fitted k-means model.
    """
    model = KMeans(n_clusters=n_clusters).fit(scaled_df)
    return model

def best_centroids(sample_size, random_state, n_clusters, n_iterations, n_attempts):
    """
    best_centroids()
    Params:
        sample_size:
        random_state:
        n_clusters:
        n_iterations:
        n_attempts:
    Returns:
    
    """
    # create sample of dataframe
    data_sample = df_subset_scaled.sample(frac=sample_size, random_state=random_state, replace=False)
    
    final_cents = []
    final_inert = []

# each iteration randomly initializes k centroids and performs n interations of k-means
    for sample in range(n_attempts):
        print('\nCentroid attempt: ', sample)
        km = KMeans(n_clusters=n_clusters, init='random', max_iter=1, n_init=1)
        km.fit(data_sample)
        inertia_start = km.inertia_
        intertia_end = 0
        cents = km.cluster_centers_

        for iter in range(NUM_ITER):
            km = KMeans(n_clusters=NUM_CLUSTERS, init=cents, max_iter=1, n_init=1)
            km.fit(data_sample)
            print('Iteration: ', iter)
            print('Inertia:', km.inertia_)
            print('Centroids:', km.cluster_centers_)
            inertia_end = km.inertia_
            cents = km.cluster_centers_

        final_cents.append(cents)
        final_inert.append(inertia_end)
        print('Difference between initial and final inertia: ', inertia_start-inertia_end)
        
def create_cluster_df(model,scaled_df):
    """create_cluster_df(model,scaled_df)
    This function takes in a fitted k-means model and a scaled dataframe and returns a dataframe of clusters and tract IDs to 
    visualize which tracts were grouped into each cluster.
    Params:
        model: fitted k-means model
        scaled_df: scaled data that was fit to the algorithm
    Returns:
        A dataframe of clusters and IDs.
    """
    cluster_df = pd.DataFrame()
    cluster_df['tractid']=scaled_df.index.values
    cluster_df['cluster']=model.labels_
    return cluster_df

    