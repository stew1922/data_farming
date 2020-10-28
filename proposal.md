# Data Farming
## **Project Proposal**

![Basic Project Outline](/images/project_idea.png)

## **Team Members**
* Carolina
* Jonathan
* Jordan
* Travis

## **Outline**

* Use correlations between weather, USDA crop data, and ETF/futures pricing to predict the outcome of the next crop report and make a trading recommendation for either an ETF or a futures contract.
* Use the PyPI Backtesting library to test our strategy.
* Look at the correlation between ETFs and futures contracts to see if one instrument or the other is more sensitive.

## **Research Questions**
* Is there a correlation between reported crop volumes vs. expected crop volumes and futures/ETF pricing?
* Is there a strong correlation between futures market and the respective ETFs?
* Is there a correlation between weather trends (precipitation, temperature, cloud cover(?), etc.) and the reported crop volumes?
* If there is a strong correlation between weather and crop volumes, is Monte Carlo simulation a valid method for predicting the next reported volumes?



## **Datasets to be Used**
* Alpaca API for ETF pricing
* PyPI Backtesting library
* Tradestation / CME / QUANDL API for futures
* USDA crop data
* NOAA weather data

## **_Rough_ Breakdown of Tasks**
* [x] Create Outline
* [ ] Find datasources
* [ ] Clean datasources
* [ ] Decide which crops to run the analysis on (corn, soybean, wheat?)
* [ ] Find correlations between reported crop data vs. expected crop data and ETFs/futures
    * i.e.- if report data is higher than expected, do ETF/futures prices drop?
* [ ] Find correlations between ETFs and futures
* [ ] Find correlations between weather data and crop volumes
    - [ ] Find correlation between temp and volumes
    - [ ] Find correlation between precipitation and volumes
    - [ ] Find correlation between cloud cover and volumes
* [ ] Run Monte Carlo simulation
