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

After getting access to the database, I filtered for Suffolk County, MA and removed census tracts that had populations of less than 500 people, since a lot of the fields were empty for those tracts. My final dataset had 190 census tracts and over 50 features, including racial, ethnic, income, housing, employment, and education information.

### EDA

![](/Images/Population_change_dist.png)
The total population in my data set increased 4.5%, from approximately 690k to 722k. Census tracts were relatively evenly split between population growth and declines, with 58% of census tracts having experienced population growth and the remaining 42% seeing declines.

![](/Images/Race_pop_2000.png)
![](/Images/Race_pop_changes.png)
The first figure shows the distribution of population by race across census tracts in 2000 while the second figure shows the distribution of population *changes from 2000-2010* by race across census tracts. What this shows is that on average, census tracts in 2000 were mostly made up of Non-Hispanic White people, followed by Hispanic, Black, and Asian. However, between 2000 and 2010, growth in the population of these groups was led by Hispanics, followed by Asians and Blacks, while the White population actually declined on average. Boston became more racially diverse over those 10 years.

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
The elbow curve shows the total within-cluster sum of squares (WSS) for every value of k. The WSS represents the intra-cluster variation, which is a value that should be minimized when clustering. Ideally, the elbow, or the point where adding another cluster doesn't materially decrease the WSS, would be obvious, but in this case you could argue k=4, k=6, or even k=7 make sense.

In order to provide meaning/context for the clusters, I compared the mean value for the county to the mean value for each cluster across the 6 variables mentioned above. I then created my own labels for those clusters based on this comparison:
- **Gentrifying**: these are census tracts which saw larger increases in 5/6 variables when compared to the baseline (county average), with the one exception being percent change in non-White population, for which a decline is typically associated with gentrification.  
- **Becoming more affordable**: these are census tracts which saw either smaller increases, or overall declines in 5/6 variables when compared to the baseline paired with a higher than average increase in the non-White population
- **Becoming more costly**: these are census tracts which saw changes that were in line with those of the baseline for all variables. I thought "Becoming more costly" was fitting given that, on average, Boston experienced large increases in housing prices, with smaller increases in income, resulting in increasingly unaffordable neighborhoods. This census tract matched the average well.

![](/Images/Cluster_radar_plot.png)

## Classifying
After assigning labels to the clusters, I built a classification model, where the target variable is the cluster/label and the feature space is the data from the 2000 census, i.e. the "starting point" of a census tract. This step in the project helped answer the question: how necessary is it to know exactly how variables are changing over time to identify gentrification? Can we foresee gentrification simply based on point in time data?

### Modeling
I started by running a Dummy Classifier on my data to create a baseline accuracy score. This model defaults to predictnig the most frequent class for every observation, and therefore acheieved an accuracy score of 43% on the training set and 42% on the testing set.

The Random Forest model resulted in an accuracy score 75% and 59% on the training and testing set, respectively, using the following parameters.

### Implementing SMOTE:
Given the class imbalance in my dataset, my model naturally performs worse when predicting the smallest class, which in this case is the gentrifying group. To address this, I implemented SMOTE (synthetic minority over-sampling technique).

## Sources
http://www.s4.brown.edu/us2010/Researcher/Bridging.htm <br>
Logan, John R., Zengwang Xu, and Brian Stults. 2014. "Interpolating US Decennial Census Tract Data from as Early as 1970 to 2010: A Longitudinal Tract Database" The Professional Geographer 66(3): 412–420.
