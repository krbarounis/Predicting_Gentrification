# Predicting_Gentrification

This project explores demographic, socioeconomic, and racial trends in the Boston area using 2000 and 2010 census data and ultimately predicts which census tracts will be considered gentrifying by the 2020 census using a classification model.

I'm originally from the Boston area, so I was naturally interested in exploring this data and testing my knowledge of the city! I also was inspired to undertake this project in order to build a model that could hypothetically be used by policy makers and politicians so that they could help minority groups that would be likely be displaced as a result of gentrification.

I've created a dashboard that highlights some of the major trends I discovered during the EDA process as well as the gentrified neighborhoods (as of 2010) discovered through the use of a clustering algorithm. Take a look! https://kristinab-dash-app.herokuapp.com/ (please be patient, loading the site takes a few moments).

Once the 2020 census is released, I'll be able to compare my predictions to the data and determine the accuracy of my model!

- [Tech Stack](#tech-stack)

- [Data](#data)
  - [EDA](#eda)

- [Clustering](#clustering)

- [Classifying](#classifying) 
  - [Implementing SMOTE](#implementing-smote)

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

After getting access to the database, I filtered for Suffolk County, MA and cleaned out some of the census tracts that had populations of less than 500 people, as a lot of the fields were empty for those tracts. My final dataset had 190 census tracts and over 50 features, including racial, ethnic, income, housing, employment, and education information.

### EDA

## Clustering

Rather than strictly defining thresholds for what constitutes gentrification, I relied on unsupervised algorithms (k-means and agglomerative heirarchical clustering) to group census tracts based on 6 traditional indicators of gentrification (in terms of percent change between the 2000 and 2010 census):
- Median rent
- Median home value
- Median income
- Population with 4 year college degree or more
- Non-White population
- Owner-occupied housing

Based on my domain knowledge of Boston, as well as the results from the below two graphs, I decided to use the outputs from k-means clustering with k=4. 

![](/Images/Elbow_curve.png)
The elbow curve shows the total within-cluster sum of squares (WSS) for every value of k. The WSS represents the intra-cluster variation, which is a value that should be minimized when clustering.

![](/Images/Silhouette.png)

In order to provide meaning/context for the groups, I compared the mean value for the county as a whole to the mean value for each cluster across the 6 variables mentioned above. I then created my own labels for those clusters based on this comparison:
- Gentrifying (n=31): these are census tracts which saw larger increases in 5/6 variables when compared to the baseline (county average)
- Becoming more affordable(n=77): these are census tracts which saw either smaller increases, or declines in 5/6 variables when compared to the baseline
- Remaining costly (n=82): these are census tracts which saw changes that were in line with those of the baseline for all variables

![](/Images/Cluster_radar_plot.png)

## Classifying

After assigning labels to the clusters, I built a classification model, where the target variable is the cluster/label and the feature space is the data from the 2000 census, i.e. the "starting point" of a census tract. This step in the project helped answer the question of, how necessary is it to know exactly how variables are changing over time to predict gentrification? Can we foresee gentrification simply based on point in time data?

### Baseline model: Dummy Classifier
I started by running a Dummy Classifier on my data to create a baseline accuracy score. Using the most frequent class (

### Final model: Random Forest

### Implementing SMOTE:
Given the class imbalance in my dataset, my model naturally performs worse when predicting the smallest class, which in this case is the gentrifying group. To address this, I implemented SMOTE (synthetic minority over-sampling technique).

## Sources
http://www.s4.brown.edu/us2010/Researcher/Bridging.htm <br>
Logan, John R., Zengwang Xu, and Brian Stults. 2014. "Interpolating US Decennial Census Tract Data from as Early as 1970 to 2010: A Longitudinal Tract Database" The Professional Geographer 66(3): 412–420.
