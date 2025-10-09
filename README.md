# Data Analysis - DAX

## Data Retrieval
- List of companies in the DAX as of 22 September 2025 web scraped from [Wikipedia](https://de.wikipedia.org/wiki/DAX).
- Prices retrieved from Yahoo! Finance's API using the [yfinance Python library](https://pypi.org/project/yfinance/).
- Macroeconomic indicators:
  - Exchange rates (EUR/USD and EUR/GBP) and interest rates from [Deutsche Bundesbank](https://www.bundesbank.de/en/statistics/time-series-databases).
  - Unemployment rates from [Bundesagentur für Arbeit](https://statistik.arbeitsagentur.de/DE/Navigation/Statistiken/Interaktive-Statistiken/Zeitreihen/Lange-Zeitreihen-Nav.html?Fachstatistik%3Dalo%26DR_Gebietsstruktur%3Dd%26Gebiete_Region%3DDeutschland%26DR_Region%3Dd%26DR_Region_d%3Dd%26DR_RK%3Dinsg%26mapHadSelection%3Dfalse%26toggleswitch_saison%3D0).

## Other Sources
- [European Central Bank Data Portal](https://data.ecb.europa.eu/).

## Roadblocks
- Limits in free-tier plans of different news APIs ([NewsAPI](https://newsapi.org/), [mediastack](https://mediastack.com/), [FMP](https://site.financialmodelingprep.com/)), impeding the extraction of sentiment-related data.