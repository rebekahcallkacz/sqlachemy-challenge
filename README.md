# sqlachemy-challenge
Version: 1.0.0

## Description
This project analyzes rainfall and temperature trends in  Hawaii.

## Data
A SQLite database of climate data in Hawaii with two tables (station and measurement) was used to conduct this analysis. SQLalchemy was used to access the data in the database. The last date in this dataset is 08-23-2017.

## Analysis
As can be seen from the figure below, average rainfall varies throughout the year, and there does not seem to be a clear rainy or dry season. 
![alt text](https://github.com/rebekahcallkacz/sqlachemy-challenge/blob/main/Images/avgrainfall.png "Avg Rainfall for Last Year")

The most active station in the dataset is in Waihee, HI. As can be seen from the histogram, it seems to rain the most when the temperature is around 75F and the least when the temperature is 60F or 80F.
![alt text](https://github.com/rebekahcallkacz/sqlachemy-challenge/blob/main/Images/tempsmostactivestation.png "Most Active Station Rainfall")

The potential trip dates chosen were 05-10 to 05-25. The daily normals for this date range in the last year of the dataset can be seen in the figure below.
![alt text](https://github.com/rebekahcallkacz/sqlachemy-challenge/blob/main/Images/tripdailynormals.png "Daily Normals for Trip Dates")

## Instructions
The trip dates can be changed based on the user's interest.

## Contributors
Rebekah Callari-Kaczmarczyk

## License and Copyright
&copy; Rebekah Callari-Kaczmarczyk