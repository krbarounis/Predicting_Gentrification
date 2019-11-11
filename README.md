# Predicting_Gentrification

This project explores demographic, socioeconomic, and racial trends in the Boston area using 2000 and 2010 census data and ultimately predicts which census tracts will be considered gentrifying by the 2020 census using a classification model.

I'm originally from the Boston area, so I was naturally interested in exploring this data and testing my knowledge of the city! I was also inspired to undertake this project in order to build a model that could hypothetically be used by policy makers and politicians so that they could help minority groups that would be likely be displaced as a result of gentrification.

I've created a dashboard that highlights some of the major trends I discovered during the EDA process as well as a depitction of the gentrified neighborhoods (as of 2010) discovered through the use of a clustering algorithm. Take a look! https://kristinab-dash-app.herokuapp.com/ (please be patient, loading the site takes a few moments).

Once the 2020 census is released, I'll be able to compare my predictions to the data and determine the accuracy of my model!

- [Tech Stack](#tech-stack)

- [Data](#data)
  - [EDA](#eda)

- [Clustering](#clustering)

- [Modeling](#modeling) 

- [Sources](#sources)

## Tech Stack
- Python
  - Pandas
  - Sklearn
  - Scipy
  - Plotly
  - Dash
- Heroku

## Data

Census tracts are not fixed over time. Boundaries are very often redrawn by politicians, which complicates looking at census data over time. As a result, I got my data from the Longitudinal Tract Data Base (http://www.s4.brown.edu/us2010/Researcher/Bridging.htm), a resource which provides census data estimates within 2010 tract boundaries for prior censuses (going back to 1970). To read about the interpolation method used by the team, click here: https://s4.ad.brown.edu/Projects/Diversity/Researcher/Logan%20etal_2014_PG.pdf.

After getting access to the database, I filtered for Suffolk County, MA and removed census tracts that had populations of less than 500 people, since a lot of the fields were empty for those tracts. My final dataset had 191 census tracts and over 50 features, including racial, ethnic, income, housing, employment, and education information.

## Clustering

Rather than strictly defining thresholds for what constitutes gentrification, I relied on unsupervised algorithms (k-means and agglomerative heirarchical clustering) to group census tracts based on 6 traditional indicators of gentrification (in terms of percent change between the 2000 and 2010 census):
- Median rent
- Median home value
- Median income
- Population with 4 year college degree or more
- Non-White population
- Owner-occupied housing

Based on my domain knowledge of Boston, in conjunction with the results of the below two graphs, I decided to apply k=4 to the k-means clustering algorithm. 

![](/Images/Elbow_curve.png)
The elbow curve shows the total within-cluster sum of squares (WSS) for every value of k. The WSS represents the intra-cluster variation, which is a value that should be minimized when clustering. Ideally, the elbow, or the point where adding another cluster doesn't materially decrease the WSS, would be obvious, but in this case you could argue k=4, k=6, or even k=7 make sense.

One downfall of k-means clustering is that the clusters are very sensitive to the starting point of the centroids. In order to address this, I used an iterative approach to finding an optimal starting point for the centroids. After applying this to my data, the algorithm sorted 190 tracts into clusters 1-3, and only 1 tract into cluster 4. As a result, at this point in my analysis, I focused on clusters 1-3 to generalize my data, deciding that group 4 was an anomaly.

In order to interpret the clusters, I looked at the summary statistics of the features across the different groups, and relative to the county as a whole. More specifically, I compared the county average for each variable to the cluster average for each variable and then created my own labels for those clusters based on how those values differed:
- **Gentrifying**: these are census tracts which saw larger increases in 5/6 variables when compared to the baseline (county average), with the one exception being percent change in Non-White population, for which a decline is typically associated with gentrification.  
- **Lagging behind**: these are census tracts which saw either smaller increases, or overall declines, in measures of income, housing values, and education levels when compared to the baseline. Neighborhoods in this cluster also experienced larger than average increases in the Non-White population.
- **Representing the average**: these are census tracts which saw changes that were generally in line with those of the baseline across all variables. 

![](/Images/Cluster_radar_plot.png)

## Classifying
After assigning labels to the clusters, I built a classification model to see if it would be possible to predict which areas would gentrify based on point in time values. In this model, the target variable is the cluster/label (one of the three groups discussed above) and the feature space is the data from the 2000 census, i.e. the "starting point" of a census tract. This step in the project helped answer the question: how necessary is it to know exactly how variables are changing over time to identify gentrification? Can we foresee gentrification simply based on point in time data?

The classification models I created included a larger set of features than those using in clustering. These features cover the following: population across racial groups, age groups, immigration backgrounds, educational backgrounds, employment status, poverty data, housing units, marriage status, and more.

### Implementing SMOTE
Given the class imbalance in my dataset, my model naturally performs worse when predicting the least frequenct class, which in this case is the gentrifying group. To address this, I implemented SMOTE (synthetic minority over-sampling technique) on the training set. At this point, the classes were evenly balanced, with each group making up 1/3 of the observations. 

### Modeling
I started by running a Dummy Classifier on my data as a baseline. This model defaults to predicting the most frequent class for every observation, which in this case is the cluster titled "Representing the average." The model acheieved accuracy scores of 43% and 42% for the training and testing sets, respectively. 

After parameter tuning with grid search, the following are the training and testing accuracy scores for all the models that were tested. Random Forest achieved the highest accuracy scores amongst the models, but is relatively overfit to the training data, especially compared to KNN. Given a long-term goal of using this model for other major metropolitan areas, I wanted to ensure my model would generalize well to unseen data. KNN may be a better model for this purpose, but ultimately if I want an accurate model for the Boston area, I'd choose Random Forest.

| Accuracy  | Dummy  | KNN | Decision Tree | Random Forest | XGBoost |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Training | 33% | 69% | 91% | 92% | 94% |
| Testing | 16% | 46% | 52% | 57% | 47% |

## Sources
http://www.s4.brown.edu/us2010/Researcher/Bridging.htm <br>
Logan, John R., Zengwang Xu, and Brian Stults. 2014. "Interpolating US Decennial Census Tract Data from as Early as 1970 to 2010: A Longitudinal Tract Database" The Professional Geographer 66(3): 412–420.

## Next steps

- Dig into which census tracts were misclassified
- Expand dataset to include other towns typically associated with the Boston area (Cambridge, Brookline, etc.)
