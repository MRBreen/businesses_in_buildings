## Objective
To find find businesses in a local area which may not be readily known.  Finding these businesses in buildings would facilitate opportunities for networking, sales, and community building.

## Data Understanding
Data was sourced from the Washington Business License Service one scrape at a time by street name and city of Seattle.  Business licenses designate the entity type, and some of the ones of interest in this project include  corporations, llc, and joint ventures.  The company name, registered business address and Seattle were put into a bing search.  Subsequent data scraping placed data into three main categories: ten links, ten text summaries paired with each link and the number of search results.

## Data
Queried public records with Selenium - saved Webpage (.html) in AWS S3.
Extracted name and address with Beautiful Soup - saved data in MongoDB.
Queried search engine with Selenium - saved webpage (.html) in AWS S3.
Extracted data with Beautiful Soup - saved data in MongoDB.

## Modeling
TF-IDF was performed with follow on nmf clustering.  For text search, setting a minimum word size (token size) of four screened out abbreviations such as "ave" and produced more relevant groupings.  Cluster sizes from two to twenty were evaluated, and seven was selected as it held information without overloading the users.

## Evaluation:
This exercise was successful in identifying business that are likely to be in the local area that are not necessarily on yelp or google places.

## Deployment:
The results of the model are available on google maps layer.
