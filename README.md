# Predicting vinyl record prices on Discogs
Scraper to retrieve Discogs data. Notebooks with linear and mixed-effect models to predict prices. 

## What's in this repository?
- A scraper that retrieves Discogs user collections, artists discographies and release information
- A notebook containing analysis on Discogs record prices: uni- and bi-variate distributions, fitting linear and mixed-effect models to the data.

## Prerequisites
Install the packages in the `requirements.txt` file using the following command in your terminal:
```buildoutcfg
$ pip install -r requirements.txt
```

Create a `credentials.yaml` file in the `config` folder. This file should contain your Discogs API token. It should be structured like this:
```buildoutcfg
discogs-api:
  token: [YOUR TOKEN HERE]
```
## How does the scraper works?
The scraper uses the [Discogs API] (https://www.discogs.com/developers) to retrieve data.
I built a set of generic functions within the `DiscogsAPIFetcher` class in `vinyl_record_scraper/discogs/api_fetcher`.
Scraper functions are in `vinyl_record_scraper/scrape`.