# Predicting_Gentrification

This project aims to explore trends in the Boston area using 2000 and 2010 census data and ultimately predict which census tracts will be considered gentrifying by the 2020 census.

I've created a dashboard that reflects trends discovered during the EDA process as well as the gentrified neighborhoods in Boston discovered through use of a clustering algorithm. Take a look! https://kristinab-dash-app.herokuapp.com/ (please be patient, loading the site takes a few moments)

## Tech Stack
- Python
  - Pandas
  - Sklearn
  - Plotly
  - Dash
- Heroku

## Intro

I'm originally from the Boston area, so I was naturally interested in exploring this data and testing my knowledge of the city. I also was inspired to undertake this project in order to build a model that could hypothetically be used by:
- *policy makers and politicians*, who can help minority groups that are displaced as a result of gentrification
- *mom-and-pop real estate investors*, who can take advantage of buying opportunities to generate passive income

## EDA


## Clustering

Rather than strictly defining thresholds for what constitutes gentrification, I relied on unsupervised algorithms (k-means and agglomerative heirarchical clustering) to group census tracts based on 6 traditional indicators of gentrification (in terms of percent change between the 2000 and 2010 census):
- Median rent
- Median home value
- Median income
- Population with 4 year college degree or more
- Non-White population
- Owner-occupied housing

## Classifying



## Next Steps



## Sources
http://www.s4.brown.edu/us2010/Researcher/Bridging.htm
Logan, John R., Zengwang Xu, and Brian Stults. 2014. "Interpolating US Decennial Census Tract Data from as Early as 1970 to 2010: A Longitudinal Tract Database" The Professional Geographer 66(3): 412–420.
